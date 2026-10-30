---
name: nas-smb-dedup-quarantine
description: 在 SMB/NAS 挂载卷上批量识别与安全清理重复文件（递归拷贝、手机同步副本）。
  当 NAS 抛 BlockingIOError [Errno 35] EAGAIN、读取成功率极低、无法做全量哈希校验，
  或需要安全清理大量重复图片/文件时使用。核心是「元数据判据 + 同卷移动到隔离区」，
  绝不依赖 os.remove，绝不依赖 os.walk。
agent_created: true
---

# NAS / SMB 卷重复文件清理

适用于 SMB 挂载的 NAS（群晖 DSM、Btrfs 等）上批量清理重复副本。
典型场景：`Photo/photo/` 是 `Photo/` 的递归拷贝、`HuaweiPhotos/` 是手机同步副本。

## 三条硬规则

1. **不要用 `os.remove` 删 SMB 上的文件**
   环境有 safe-delete 拦截：`os.remove` 会转 `FSMoveObjectToTrashSync`，
   在 SMB 卷上失败（status -120）后 fail-closed，删除被阻断。
   → 改用**同卷 `os.rename` 移动到隔离区**，完全可逆。

2. **不要用 `os.walk`**
   `os.walk` 在 `scandir` 抛错时**静默跳过整棵子树**，扫描结果会静默失真
   （实测：同一棵树从 125,480 个文件掉到 2,815 个，无任何报错）。
   → 用带重试的自定义遍历（见下）。

3. **不要指望读文件内容**
   EAGAIN 期间：元数据操作（listdir / lstat / mkdir）100% 正常；
   读文件内容成功率可能只有 0.5%~18%；rename 成功率 40%~70%。
   → 优先用**元数据判据**，内容只做抽样验证。

## 判定方法（按可靠性排序）

| 级别 | 判据 | 适用 |
|---|---|---|
| A | 同相对路径 + 同 size + 同 mtime（秒级） | 递归拷贝目录，mtime 保留是 FastCopy/robocopy/rsync -a 的特征 |
| C | 同 size + 同 mtime | 手机同步目录，无对应路径 |
| B | 仅同 size | 弱证据，不要据此删除 |

同卷内判定流程：
1. 遍历全卷，收集 `(path, size, mtime)`，按顶层目录区分「副本区」与「权威区」
2. 副本区文件先在权威区按 (size, mtime) 建索引匹配
3. 递归拷贝目录额外用「去掉拷贝前缀后的相对路径」直接定位原件

## 执行流程

```bash
# 1. 建索引 + 元数据匹配
python dedupe_meta2.py        # 输出 dup_meta.json（by_path / by_meta / unmatched）

# 2. 抽样内容验证（NAS 读取能力允许时）
python fp_bulk.py copy        # 采副本侧 8KB 指纹
python fp_bulk.py origin      # 采原件侧指纹并比对，输出准确率

# 3. 移动到隔离区（幂等，多轮跑直到待重试归零）
python quarantine_move.py

# 4. 导出还原映射清单
python export_report.py
```

### 移动前必须复核

每个文件移动前重新 `lstat` 副本与原件，确认：
副本 size/mtime 与扫描时一致、原件仍存在、两者 size 一致。任一不符则跳过并记录。
这一步是廉价的（元数据操作永远可用），也是最后一道防线。

### 分批与续跑

- 每 1000 个落盘一次 `done` / `skip` 记录，可随时中断
- 失败的下一轮自动重试（EAGAIN 是瞬时错误，多轮可收敛）
- 实测收敛曲线：23,851 → 5,318 → 1,583 → 2,414（波动但总体下降）

## 释放空间的真相

同卷移动**不释放空间**，只是把文件移出原目录。要真正回收：
1. 确认隔离区内容无误
2. 在 DSM File Station 删除隔离区目录
3. 清空共享文件夹回收站 `#recycle`

## 排查 rename 失败的常见原因

- NAS 侧 **Syncthing / Cloud Sync / 索引服务**正在占用文件
  （目录下有 `.stfolder` 即为 Syncthing 标记）→ 暂停同步服务后成功率显著上升
- Btrfs 卷使用率 ≥ 80% 时性能与稳定性急剧下降
- inode 使用率 ≥ 79% 同样会触发异常

## 卷整体挂起时的应对

SMB 卷挂起会导致 shell 工具因工作目录不可访问而**完全无法执行**，
任何 `cd /tmp && ...` 前缀都绕不过。此时：
- 立即停止重试
- 用 Write 工具把进度报告落到**本地盘**（不要试图写 NAS）
- 报告里写明「已处理 / 待重试」的准确数字和续跑命令
