#!/usr/bin/env python3
"""
微云通用上传脚本 — 一键上传本地文件到微云网盘。

整合了以下三个步骤：
  1. 计算上传参数（block_sha_list、file_sha、check_sha、check_data、file_md5）
  2. MCP 预上传（检查秒传或获取上传通道）
  3. MCP 分片上传（循环「预上传获取通道 → 上传一片」直到完成）

使用方法：
  python3 upload_to_weiyun.py <文件路径> [--pdir_key <目录key>]

环境变量（可选，也可通过命令行参数传入）：
  WEIYUN_MCP_URL    — MCP 服务地址，默认 https://www.weiyun.com/api/v3/mcpserver
  WEIYUN_MCP_TOKEN  — MCP token，必须提供（命令行 --token 或环境变量）
  WEIYUN_ENV_ID     — 环境标识（如 sit-0cd15bb3），可选

示例：
  # 使用命令行参数
  python3 upload_to_weiyun.py /tmp/Test666.json --token 1fc54abae52bb44d4b8a421cc2734c04

  # 使用环境变量
  export WEIYUN_MCP_TOKEN=1fc54abae52bb44d4b8a421cc2734c04
  python3 upload_to_weiyun.py /tmp/Test666.json

  # 指定上传目录
  python3 upload_to_weiyun.py /tmp/Test666.json --token xxx --pdir_key abc123

依赖：
  pip install requests（如未安装）

重要说明：
  本脚本包含纯 Python SHA1 实现，支持提取未经 finalization 的内部寄存器状态。
  这是 Python 标准库 hashlib.sha1 无法做到的，也是微云上传协议的核心需求。
"""

import _encoding_fix  # noqa: F401  Windows UTF-8 fix, must be first import

import argparse
import base64
import hashlib
import json
import os
import struct
import sys
import time
import ctypes
import ctypes.util

try:
    import requests
except ImportError:
    print("错误：需要 requests 库，请执行 pip install requests")
    sys.exit(1)


# ========== 优化的 SHA1 实现（C 加速 + 纯 Python 回退）==========

_sha1_lib = None
_SHA1_CTX = None
_c_sha1_init = None
_c_sha1_update = None

def _init_ctypes_sha1():
    global _sha1_lib, _SHA1_CTX, _c_sha1_init, _c_sha1_update
    if _c_sha1_init is not None:
        return True
    lib_names = []
    if sys.platform == "darwin":
        lib_names = ["libSystem.B", "libcrypto"]
    elif sys.platform.startswith("linux"):
        lib_names = ["libc.so.6", "libcrypto.so.3", "libcrypto.so.1.1"]
    for name in lib_names:
        path = ctypes.util.find_library(name)
        if path:
            try:
                _sha1_lib = ctypes.CDLL(path)
                if hasattr(_sha1_lib, 'SHA1_Init'):
                    _c_sha1_init = _sha1_lib.SHA1_Init
                    _c_sha1_update = _sha1_lib.SHA1_Update
                    class _SHA1_CTX_Struct(ctypes.Structure):
                        _fields_ = [
                            ("h0", ctypes.c_uint32), ("h1", ctypes.c_uint32),
                            ("h2", ctypes.c_uint32), ("h3", ctypes.c_uint32),
                            ("h4", ctypes.c_uint32),
                            ("Nl", ctypes.c_uint32), ("Nh", ctypes.c_uint32),
                            ("data", ctypes.c_ubyte * 64), ("num", ctypes.c_uint32),
                        ]
                    _SHA1_CTX = _SHA1_CTX_Struct
                    _c_sha1_init.argtypes = [ctypes.POINTER(_SHA1_CTX)]
                    _c_sha1_init.restype = ctypes.c_int
                    _c_sha1_update.argtypes = [ctypes.POINTER(_SHA1_CTX), ctypes.c_char_p, ctypes.c_size_t]
                    _c_sha1_update.restype = ctypes.c_int
                    return True
            except Exception:
                continue
    return False

def _get_state_le(ctx):
    return struct.pack("<IIIII", ctx.h0, ctx.h1, ctx.h2, ctx.h3, ctx.h4).hex()

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

class PySHA1:
    """纯 Python SHA1（回退）"""
    def __init__(self):
        self.h0 = 0x67452301; self.h1 = 0xEFCDAB89; self.h2 = 0x98BADCFE
        self.h3 = 0x10325476; self.h4 = 0xC3D2E1F0
        self._message_byte_length = 0; self._unprocessed = b""
    def update(self, data):
        self._unprocessed += data; self._message_byte_length += len(data)
        while len(self._unprocessed) >= 64:
            self._process_chunk(self._unprocessed[:64]); self._unprocessed = self._unprocessed[64:]
    def _process_chunk(self, chunk):
        w = [struct.unpack(">I", chunk[i*4:(i+1)*4])[0] for i in range(16)]
        for i in range(16, 80): w.append(_left_rotate(w[i-3]^w[i-8]^w[i-14]^w[i-16], 1))
        a,b,c,d,e = self.h0,self.h1,self.h2,self.h3,self.h4
        for i in range(80):
            if i<=19: f=(b&c)|((~b)&d); k=0x5A827999
            elif i<=39: f=b^c^d; k=0x6ED9EBA1
            elif i<=59: f=(b&c)|(b&d)|(c&d); k=0x8F1BBCDC
            else: f=b^c^d; k=0xCA62C1D6
            temp=(_left_rotate(a,5)+f+e+k+w[i])&0xFFFFFFFF
            e=d;d=c;c=_left_rotate(b,30);b=a;a=temp
        self.h0=(self.h0+a)&0xFFFFFFFF;self.h1=(self.h1+b)&0xFFFFFFFF
        self.h2=(self.h2+c)&0xFFFFFFFF;self.h3=(self.h3+d)&0xFFFFFFFF
        self.h4=(self.h4+e)&0xFFFFFFFF
    def get_state(self):
        assert len(self._unprocessed)==0
        return struct.pack("<IIIII",self.h0,self.h1,self.h2,self.h3,self.h4).hex()
    def hexdigest(self):
        mbl=self._message_byte_length; up=self._unprocessed
        h0,h1,h2,h3,h4=self.h0,self.h1,self.h2,self.h3,self.h4
        up+=b"\x80"; up+=b"\x00"*((56-len(up)%64)%64); up+=struct.pack(">Q", mbl*8)
        tmp=PySHA1.__new__(PySHA1); tmp.h0,tmp.h1,tmp.h2,tmp.h3,tmp.h4=h0,h1,h2,h3,h4
        tmp._unprocessed=b""; tmp._message_byte_length=mbl
        while len(up)>=64: tmp._process_chunk(up[:64]); up=up[64:]
        return "{:08x}{:08x}{:08x}{:08x}{:08x}".format(tmp.h0,tmp.h1,tmp.h2,tmp.h3,tmp.h4)

class FastSHA1:
    def __init__(self):
        self.use_c = _init_ctypes_sha1()
        if self.use_c: self.ctx = _SHA1_CTX(); _c_sha1_init(ctypes.byref(self.ctx))
        else: self.inner = PySHA1()
    def update(self, data):
        if self.use_c: _c_sha1_update(ctypes.byref(self.ctx), data, len(data))
        else: self.inner.update(data)
    def get_state(self):
        if self.use_c: return _get_state_le(self.ctx)
        else: return self.inner.get_state()
    def hexdigest(self):
        if self.use_c:
            py=PySHA1(); py.h0=self.ctx.h0; py.h1=self.ctx.h1; py.h2=self.ctx.h2
            py.h3=self.ctx.h3; py.h4=self.ctx.h4
            py._message_byte_length=self.ctx.Nl|(self.ctx.Nh<<32)
            py._unprocessed=bytes(self.ctx.data[:self.ctx.num])
            return py.hexdigest()
        return self.inner.hexdigest()


# ========== 文件参数计算 ==========

BLOCK_SIZE = 524288  # 512KB


def calc_upload_params(file_path):
    """
    计算微云上传所需的全部参数：
    - block_sha_list：分块 SHA1 列表
    - file_sha：整个文件的标准 SHA1
    - file_md5：整个文件的 MD5
    - check_sha：SHA1 校验中间状态
    - check_data：文件末尾校验字节的 Base64 编码

    返回 dict，可直接用于 MCP 预上传请求。
    """
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    # 计算 lastBlockSize 和 checkBlockSize
    last_block_size = file_size % BLOCK_SIZE
    if last_block_size == 0:
        last_block_size = BLOCK_SIZE
    check_block_size = last_block_size % 128
    if check_block_size == 0:
        check_block_size = 128
    before_block_size = file_size - last_block_size
    block_sha_list = []
    sha1 = FastSHA1()
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # 处理除最后一块之外的所有 block
        for offset in range(0, before_block_size, BLOCK_SIZE):
            data = f.read(BLOCK_SIZE)
            sha1.update(data)
            md5.update(data)
            block_sha_list.append(sha1.get_state())
        # 读取最后一块中去掉 checkBlockSize 之后的部分
        between_data = f.read(last_block_size - check_block_size)
        sha1.update(between_data)
        md5.update(between_data)
        check_sha = sha1.get_state()
        # 读取 checkData 部分
        check_data_bytes = f.read(check_block_size)
        sha1.update(check_data_bytes)
        md5.update(check_data_bytes)
        file_sha = sha1.hexdigest()
        check_data = base64.b64encode(check_data_bytes).decode("utf-8")
        # 最后一个 block 的 sha 为 file_sha
        block_sha_list.append(file_sha)
    file_md5 = md5.hexdigest()
    return {
        "filename": filename,
        "file_size": file_size,
        "file_sha": file_sha,
        "file_md5": file_md5,
        "block_sha_list": block_sha_list,
        "check_sha": check_sha,
        "check_data": check_data,
    }


# ========== MCP 调用 ==========

_request_id = 0


def mcp_call(mcp_url, headers, tool_name, arguments):
    """调用微云 MCP Tool，返回解析后的响应 dict"""
    global _request_id
    _request_id += 1
    payload = {
        "jsonrpc": "2.0",
        "id": _request_id,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    resp = requests.post(mcp_url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    result = resp.json()
    content = result.get("result", {}).get("content", [])
    for item in content:
        if item.get("type") == "text":
            return json.loads(item["text"])
    # 如果没有 text 类型的 content，返回原始 result
    return result


# ========== 上传核心逻辑 ==========

def upload_file(file_path, mcp_url, headers, pdir_key=None, max_rounds=50):
    """
    上传文件到微云的完整流程：
    1. 计算分块参数
    2. 预上传（检查秒传）
    3. 循环分片上传

    参数：
      file_path   — 本地文件路径
      mcp_url     — MCP 服务地址
      headers     — HTTP 请求头（含 Cookie 和 WyHeader）
      pdir_key    — 上传目标目录 key（可选，不填使用 token 绑定的目录）
      max_rounds  — 最大上传轮数，防止死循环

    返回：
      成功时返回 dict: {"file_id": "...", "filename": "..."}
      失败时抛出异常
    """
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    # 第一步：计算上传参数
    print(f"[1/3] 计算上传参数: {filename} ({file_size} 字节)...")
    params = calc_upload_params(file_path)
    print(f"  block_count={len(params['block_sha_list'])}, "
          f"file_sha={params['file_sha'][:16]}..., "
          f"file_md5={params['file_md5'][:16]}...")
    # 构建预上传请求参数
    pre_upload_args = {
        "filename": params["filename"],
        "file_size": params["file_size"],
        "file_sha": params["file_sha"],
        "file_md5": params["file_md5"],
        "block_sha_list": params["block_sha_list"],
        "check_sha": params["check_sha"],
        "check_data": params["check_data"],
    }
    if pdir_key:
        pre_upload_args["pdir_key"] = pdir_key
    # 读取文件数据到内存（用于分片上传）
    with open(file_path, "rb") as f:
        file_data = f.read()
    # 第二步 & 第三步：循环「预上传 → 上传一片」
    print(f"[2/3] 开始上传...")
    round_num = 0
    while round_num < max_rounds:
        round_num += 1
        # 预上传，获取当前需要上传的通道
        pre_rsp = mcp_call(mcp_url, headers, "weiyun.upload", pre_upload_args)
        # 检查错误
        if pre_rsp.get("error"):
            raise RuntimeError(f"预上传失败: {pre_rsp['error']}")
        # 检查秒传
        if pre_rsp.get("file_exist", False):
            file_id = pre_rsp.get("file_id", "")
            fname = pre_rsp.get("filename", filename)
            print(f"  ✅ 秒传成功！file_id={file_id}")
            return {"file_id": file_id, "filename": fname}
        # 获取通道列表
        ch_list = pre_rsp.get("channel_list", [])
        uk = pre_rsp.get("upload_key", "")
        ex = pre_rsp.get("ex", "")
        # 找第一个 len > 0 的通道
        ch = None
        for c in ch_list:
            if int(c.get("len", 0)) > 0:
                ch = c
                break
        if ch is None:
            state = int(pre_rsp.get("upload_state", 0))
            if state == 2:
                file_id = pre_rsp.get("file_id", "")
                fname = pre_rsp.get("filename", filename)
                print(f"  ✅ 上传完成！file_id={file_id}")
                return {"file_id": file_id, "filename": fname}
            raise RuntimeError(f"无可上传通道，upload_state={state}")
        offset = int(ch["offset"])
        length = int(ch["len"])
        channel_id = int(ch["id"])
        actual_len = min(length, len(file_data) - offset)
        progress_pct = min(100, int(offset / file_size * 100))
        print(f"  [{round_num}] 上传分片: offset={offset}, len={actual_len}, "
              f"ch={channel_id}, progress≈{progress_pct}%")
        # 准备分片数据
        chunk = file_data[offset:offset + actual_len]
        chunk_b64 = base64.b64encode(chunk).decode("utf-8")
        cl = [{"id": int(c["id"]), "offset": int(c["offset"]), "len": int(c["len"])}
              for c in ch_list]
        # 上传分片
        up_rsp = mcp_call(mcp_url, headers, "weiyun.upload", {
            "filename": filename,
            "file_size": file_size,
            "file_sha": params["file_sha"],
            "block_sha_list": [],
            "check_sha": params["check_sha"],
            "upload_key": uk,
            "channel_list": cl,
            "channel_id": channel_id,
            "ex": ex,
            "file_data": chunk_b64,
        })
        # 检查上传结果
        if up_rsp.get("error"):
            raise RuntimeError(f"分片上传失败: {up_rsp['error']}")
        state = int(up_rsp.get("upload_state", 0))
        if state == 2:
            file_id = up_rsp.get("file_id", "")
            fname = up_rsp.get("filename", filename)
            print(f"[3/3] ✅ 上传完成！file_id={file_id}, filename={fname}")
            return {"file_id": file_id, "filename": fname}
    raise RuntimeError(f"超过最大上传轮数 ({max_rounds})，上传未完成")


# ========== 命令行入口 ==========

def main():
    parser = argparse.ArgumentParser(
        description="微云通用上传脚本 — 一键上传本地文件到微云网盘",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /tmp/Test666.json --token 1fc54abae52bb44d4b8a421cc2734c04
  %(prog)s /tmp/Test666.json --token xxx --pdir_key abc123
  %(prog)s /tmp/Test666.json --token xxx --env_id sit-0cd15bb3

环境变量：
  WEIYUN_MCP_URL    MCP 服务地址（默认 https://www.weiyun.com/api/v3/mcpserver）
  WEIYUN_MCP_TOKEN  MCP token
  WEIYUN_ENV_ID     环境标识
""",
    )
    parser.add_argument("file_path", help="要上传的本地文件路径")
    parser.add_argument("--token", default=None,
                        help="MCP token（也可通过 WEIYUN_MCP_TOKEN 环境变量设置）")
    parser.add_argument("--pdir_key", default=None,
                        help="上传目标目录 key（不填则使用 token 绑定的目录）")
    parser.add_argument("--mcp_url", default=None,
                        help="MCP 服务地址（默认 https://www.weiyun.com/api/v3/mcpserver）")
    parser.add_argument("--env_id", default=None,
                        help="环境标识（如 sit-0cd15bb3，也可通过 WEIYUN_ENV_ID 环境变量设置）")
    parser.add_argument("--max_rounds", type=int, default=50,
                        help="最大上传轮数（默认 50）")
    args = parser.parse_args()
    # 校验文件存在
    if not os.path.isfile(args.file_path):
        print(f"错误：文件不存在: {args.file_path}")
        sys.exit(1)
    # 解析参数（命令行 > 环境变量 > 默认值）
    mcp_url = args.mcp_url or os.environ.get("WEIYUN_MCP_URL", "https://www.weiyun.com/api/v3/mcpserver")
    mcp_token = args.token or os.environ.get("WEIYUN_MCP_TOKEN")
    env_id = args.env_id or os.environ.get("WEIYUN_ENV_ID")
    if not mcp_token:
        print("错误：必须提供 MCP token（--token 参数或 WEIYUN_MCP_TOKEN 环境变量）")
        sys.exit(1)
    # 构建 HTTP 请求头
    headers = {
        "Content-Type": "application/json",
        "WyHeader": f"mcp_token={mcp_token}",
    }
    if env_id:
        headers["Cookie"] = f"env_id={env_id}"
    # 执行上传
    print(f"=" * 60)
    print(f"微云上传: {args.file_path}")
    print(f"MCP URL:  {mcp_url}")
    print(f"Token:    {mcp_token[:8]}...{mcp_token[-4:]}")
    if args.pdir_key:
        print(f"目标目录: {args.pdir_key}")
    if env_id:
        print(f"环境标识: {env_id}")
    print(f"=" * 60)
    start_time = time.time()
    try:
        result = upload_file(
            file_path=args.file_path,
            mcp_url=mcp_url,
            headers=headers,
            pdir_key=args.pdir_key,
            max_rounds=args.max_rounds,
        )
        elapsed = time.time() - start_time
        file_size = os.path.getsize(args.file_path)
        speed = file_size / elapsed / 1024 if elapsed > 0 else 0
        print(f"\n{'=' * 60}")
        print(f"上传成功！")
        print(f"  文件名:  {result['filename']}")
        print(f"  文件ID:  {result['file_id']}")
        print(f"  文件大小: {file_size} 字节")
        print(f"  耗时:    {elapsed:.1f} 秒")
        print(f"  平均速度: {speed:.1f} KB/s")
        print(f"{'=' * 60}")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n上传失败（耗时 {elapsed:.1f} 秒）: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
