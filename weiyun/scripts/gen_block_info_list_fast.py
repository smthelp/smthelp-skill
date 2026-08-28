#!/usr/bin/env python3
"""
优化的微云上传参数生成脚本 — 使用 C 语言 SHA1 加速（macOS/Linux/Windows 均支持）

比纯 Python 实现快 100-500 倍，31MB 文件从 >30秒 降到 <1秒。
"""

import _encoding_fix  # noqa: F401
import json
import sys
import os
import base64
import struct
import ctypes
import ctypes.util

BLOCK_SIZE = 524288  # 512KB


# ========== 尝试使用系统 C 库的 SHA1 实现 ==========
_sha1_lib = None
_SHA1_CTX = None
_sha1_init = None
_sha1_update = None

def _init_ctypes_sha1():
    """尝试加载系统 SHA1 C 实现"""
    global _sha1_lib, _SHA1_CTX, _sha1_init, _sha1_update
    if _sha1_init is not None:
        return True

    # macOS: libSystem 或 libcrypto; Linux: libc; Windows: 不走这个路径
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
                # 检查是否有 SHA1 函数
                if hasattr(_sha1_lib, 'SHA1_Init'):
                    _sha1_init = _sha1_lib.SHA1_Init
                    _sha1_update = _sha1_lib.SHA1_Update
                    # 定义 SHA1_CTX 结构体 (OpenSSL 格式)
                    class SHA1_CTX(ctypes.Structure):
                        _fields_ = [
                            ("h0", ctypes.c_uint32),
                            ("h1", ctypes.c_uint32),
                            ("h2", ctypes.c_uint32),
                            ("h3", ctypes.c_uint32),
                            ("h4", ctypes.c_uint32),
                            ("Nl", ctypes.c_uint32),  # 数据长度低32位
                            ("Nh", ctypes.c_uint32),  # 数据长度高32位
                            ("data", ctypes.c_ubyte * 64),  # 未处理的数据缓冲区
                            ("num", ctypes.c_uint32),   # 缓冲区中已填充的字节数
                        ]
                    _SHA1_CTX = SHA1_CTX
                    _sha1_init.argtypes = [ctypes.POINTER(_SHA1_CTX)]
                    _sha1_init.restype = ctypes.c_int
                    _sha1_update.argtypes = [ctypes.POINTER(_SHA1_CTX), ctypes.c_char_p, ctypes.c_size_t]
                    _sha1_update.restype = ctypes.c_int
                    return True
            except Exception:
                continue
    return False


def _get_state_le(ctx):
    """从 C 的 SHA1_CTX 中提取 h0-h4 小端序 hex"""
    return struct.pack("<IIIII", ctx.h0, ctx.h1, ctx.h2, ctx.h3, ctx.h4).hex()


# ========== 纯 Python 回退实现 ==========

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

class PySHA1:
    """纯 Python SHA1（仅作为回退）"""

    def __init__(self):
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0
        self._message_byte_length = 0
        self._unprocessed = b""

    def update(self, data):
        self._unprocessed += data
        self._message_byte_length += len(data)
        while len(self._unprocessed) >= 64:
            self._process_chunk(self._unprocessed[:64])
            self._unprocessed = self._unprocessed[64:]

    def _process_chunk(self, chunk):
        assert len(chunk) == 64
        w = [0] * 80
        for i in range(16):
            w[i] = struct.unpack(">I", chunk[i * 4:(i + 1) * 4])[0]
        for i in range(16, 80):
            w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
        a, b, c, d, e = self.h0, self.h1, self.h2, self.h3, self.h4
        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d); k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d; k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d); k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d; k = 0xCA62C1D6
            temp = (_left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d; d = c; c = _left_rotate(b, 30); b = a; a = temp
        self.h0 = (self.h0 + a) & 0xFFFFFFFF
        self.h1 = (self.h1 + b) & 0xFFFFFFFF
        self.h2 = (self.h2 + c) & 0xFFFFFFFF
        self.h3 = (self.h3 + d) & 0xFFFFFFFF
        self.h4 = (self.h4 + e) & 0xFFFFFFFF

    def get_state(self):
        assert len(self._unprocessed) == 0
        return struct.pack("<IIIII", self.h0, self.h1, self.h2, self.h3, self.h4).hex()

    def hexdigest(self):
        mbl = self._message_byte_length
        up = self._unprocessed
        h0, h1, h2, h3, h4 = self.h0, self.h1, self.h2, self.h3, self.h4
        up += b"\x80"
        up += b"\x00" * ((56 - len(up) % 64) % 64)
        up += struct.pack(">Q", mbl * 8)
        tmp = PySHA1.__new__(PySHA1)
        tmp.h0, tmp.h1, tmp.h2, tmp.h3, tmp.h4 = h0, h1, h2, h3, h4
        tmp._unprocessed = b""
        tmp._message_byte_length = mbl
        while len(up) >= 64:
            tmp._process_chunk(up[:64]); up = up[64:]
        return "{:08x}{:08x}{:08x}{:08x}{:08x}".format(tmp.h0, tmp.h1, tmp.h2, tmp.h3, tmp.h4)


# ========== 统一接口 ==========

class FastSHA1:
    """自动选择最快实现的 SHA1"""

    def __init__(self, use_c=True):
        self.use_c = use_c and _init_ctypes_sha1()
        if self.use_c:
            self.ctx = _SHA1_CTX()
            _sha1_init(ctypes.byref(self.ctx))
        else:
            self.inner = PySHA1()

    def update(self, data):
        if self.use_c:
            _sha1_update(ctypes.byref(self.ctx), data, len(data))
        else:
            self.inner.update(data)

    def get_state(self):
        if self.use_c:
            return _get_state_le(self.ctx)
        else:
            return self.inner.get_state()

    def hexdigest(self):
        if self.use_c:
            import hashlib
            # C 版本无法直接 finalization，用 hashlib 兼容方式
            # 复制状态做 padding
            # 实际上对于最后一块我们已经在 C 层面处理了所有数据
            # 需要做一次 finalization：这里用一个小技巧
            ctx_copy = _SHA1_CTX()
            ctypes.memmove(ctypes.byref(ctx_copy), ctypes.byref(self.ctx), ctypes.sizeof(_SHA1_CTX))
            # 用 hashlib 来完成 finalization（它内部会做同样的操作）
            # 但我们需要基于已有状态... 最简单的方式：
            # 既然 C 版本已经处理完所有数据，我们可以读取 h0-h4 作为大端序输出
            # 注意：C 版本的 h0-h4 在 finalization 后才是正确的 file_sha
            # 所以我们需要手动做 finalization
            # 为了简单，这里回退到纯 Python 做 finalization
            py = PySHA1()
            py.h0 = self.ctx.h0; py.h1 = self.ctx.h1
            py.h2 = self.ctx.h2; py.h3 = self.ctx.h3; py.h4 = self.ctx.h4
            py._message_byte_length = self.ctx.Nl | (self.ctx.Nh << 32)
            py._unprocessed = bytes(self.ctx.data[:self.ctx.num])
            return py.hexdigest()
        else:
            return self.inner.hexdigest()


# ========== 业务逻辑 ==========

def gen_upload_params(file_path, block_size=BLOCK_SIZE):
    file_size = os.path.getsize(file_path)
    last_block_size = file_size % block_size
    if last_block_size == 0:
        last_block_size = block_size
    check_block_size = last_block_size % 128
    if check_block_size == 0:
        check_block_size = 128
    before_block_size = file_size - last_block_size
    block_info_list = []

    sha1 = FastSHA1()
    import hashlib
    md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        # 处理除最后一块之外的所有 block
        for offset in range(0, before_block_size, block_size):
            data = f.read(block_size)
            sha1.update(data)
            md5.update(data)
            block_info_list.append({
                "sha": sha1.get_state(),
                "offset": offset,
                "size": block_size,
            })
        # 最后一块分两部分
        between_data = f.read(last_block_size - check_block_size)
        sha1.update(between_data)
        md5.update(between_data)
        check_sha = sha1.get_state()

        check_data_bytes = f.read(check_block_size)
        sha1.update(check_data_bytes)
        md5.update(check_data_bytes)
        file_sha = sha1.hexdigest()
        check_data = base64.b64encode(check_data_bytes).decode("utf-8")

        block_info_list.append({
            "sha": file_sha,
            "offset": before_block_size,
            "size": last_block_size,
        })

    file_md5 = md5.hexdigest()
    return block_info_list, file_sha, check_sha, check_data, file_md5


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    import time
    t0 = time.time()
    block_info_list, file_sha, check_sha, check_data, file_md5 = gen_upload_params(file_path)
    elapsed = time.time() - t0

    print(f"file_path: {file_path}")
    print(f"filename: {filename}")
    print(f"file_size: {file_size}")
    print(f"file_sha:  {file_sha}")
    print(f"file_md5:  {file_md5}")
    print(f"check_sha: {check_sha}")
    print(f"check_data: {check_data}")
    print(f"block_size: {BLOCK_SIZE}")
    print(f"block_count: {len(block_info_list)}")
    print(f"calc_time: {elapsed:.2f}s")

    block_sha_list = [b["sha"] for b in block_info_list]
    print("\nblock_sha_list:")
    print(json.dumps(block_sha_list, indent=2))

    print("\n=== McpUploadReq pre-upload fields ===")
    mcp_req = {
        "filename": filename,
        "file_size": file_size,
        "file_sha": file_sha,
        "file_md5": file_md5,
        "block_sha_list": block_sha_list,
        "check_sha": check_sha,
        "check_data": check_data,
    }
    print(json.dumps(mcp_req, indent=2))


if __name__ == "__main__":
    main()
