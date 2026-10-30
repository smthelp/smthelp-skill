---
name: npm-sandbox-install-fixes
description: 在 WorkBuddy 沙箱环境里跑 npm install / npm ci / next build 失败时的排查与解法。
  当出现 CODEBUDDY_BROKER_DENY、SAFE_DELETE_BULK_CONFIRM_REQUIRED、file-unlink 被拒、
  node_modules/.bin 为空、eslint 报 Cannot find module './Func.js'、
  Turbopack 报 "Operation not permitted (os error 1)"、
  或 Bash 工具整片 SIGTERM(137) 时使用。也覆盖「本机没有项目要求的 Node 版本」的安装路径。
  触发词：npm 装不上、npm install 失败、npm run check 失败、沙箱拦截、Node 版本不够。
agent_created: true
---

# 沙箱环境下的 Node 项目安装与构建

适用：macOS + WorkBuddy 沙箱。症状五花八门，但绝大多数是**权限拦截披着文件系统错误的外衣**。

## 症状 → 根因 → 解法速查

| 症状 | 真实根因 | 解法 |
|---|---|---|
| `npm error code CODEBUDDY_BROKER_DENY`<br>`ENOENT: rename .bin/acorn -> .acorn-xxxx` | 沙箱拒绝 `file-unlink`/rename，npm 建 bin 软链失败 | 用 **非沙箱模式**前台跑 npm（见下） |
| `[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] {"count":N,"threshold":50}` | 沙箱批量删除保护，单次删除 >50 个条目即 fail-closed | 别自己 `rm -rf node_modules`；交给 npm |
| `node_modules/.bin` 是空的 | 上一次被拒的安装留下的残局 | 重跑 npm（`.bin` 空时无需 unlink，能过） |
| `ESLint: Cannot find module './Func.js'`<br>（`prelude-ls/lib/` 缺 `Func.js`） | 被中断的安装留下半截解压包；大小写冲突文件（`Func.js` vs `func.js`）在 APFS 上丢失 | `npm ci` 从 lockfile 干净重装，一次修好 |
| React/Next 报某个包内部模块找不到 | 同上，半截解压 | 同上，`npm ci` |
| Turbopack: `failed to rename ... CURRENT.next to ... CURRENT: Operation not permitted (os error 1)` | `next build` 写 `.next/cache` 被沙箱拒 | 非沙箱模式重跑 `npm run build` / `npm run check` |
| Bash 工具每条命令都 `Exit Code 137 / SIGTERM`，连 `echo` 都不行 | **工作区 cwd 所在的卷挂死了**（外挂 USB/ExFAT/NAS 掉线）。`cd /tmp` 也绕不过 | 见文末「cwd 挂死」一节 |
| `install_binary` 找不到该工具 | 本会话未注册 | 手动下官方 tarball（见下） |

## 关键操作：非沙箱模式跑 npm

沙箱的 `safe-delete` / `file-unlink` 拦截**不会被前台普通命令绕过**，必须显式申请豁免：

```
Bash(command="cd <项目> && export PATH=<node_bin>:$PATH && npm ci --no-audit --no-fund",
     dangerouslyDisableSandbox=true, timeout=600000)
```

要点：
- **必须前台**。`run_in_background: true` 拿不到豁免，沙箱照拦（实测 stderr 仍出现 `[sandbox] 命令被沙箱拦截`）。
- 成功时结果里会带 `⚠️ Sandbox bypassed (escalation-approved)`。
- 输出容易被吞。稳妥做法：`> /tmp/xxx.log 2>&1; echo "EXIT=$?"; tail -50 /tmp/xxx.log`。
- **顺序**：先 `npm ci`（或 `npm install`）→ 再 `npm run check`，两条都走非沙箱。

## 推荐执行序列（干净一次过）

```zsh
PROJ=/path/to/project
export PATH=/Users/mac/.workbuddy/binaries/node/versions/<ver>/bin:$PATH

cd "$PROJ"
git log --oneline -1          # 确认版本
npm ci --no-audit --no-fund   # 干净重装，修半截包（无 lockfile 时用 npm install）
npm run check                 # lint + typecheck + build
```

`npm ci` 会自动清掉 `node_modules`，所以**不需要**先 `rm -rf node_modules`（那会撞 safe-delete 阈值）。

## 本机没有项目要求的 Node 版本

`install_binary` 工具不可用时，直接装官方二进制到受管目录：

```zsh
cd /tmp
curl -#L -o node.tar.xz https://nodejs.org/dist/v24.21.0/node-v24.21.0-darwin-x64.tar.xz
tar -xf node.tar.xz
mv node-v24.21.0-darwin-x64 /Users/mac/.workbuddy/binaries/node/versions/24.21.0
/Users/mac/.workbuddy/binaries/node/versions/24.21.0/bin/node -v
```

- 架构取 `uname -m`：Intel → `darwin-x64`，Apple Silicon → `darwin-arm64`。
- 新版本号查 `https://nodejs.org/dist/index.json`。
- 用绝对路径调 `bin/node` / `bin/npm`，或 `export PATH=<dir>/bin:$PATH`。
- **别动 `versions/current` 软链**，那会影响用户环境。

## cwd 挂死：Bash 工具整片 SIGTERM

工作区目录在外挂卷（ExFAT / USB / NAS）上时，该卷一挂，Bash 工具**全部命令**返回 137，
因为工具启动时要 `cd` 到工作区。`cd /tmp`、`/bin/echo` 都救不了。

能做的：
1. `Glob` / `Read` / `Write` 等文件工具仍然可用（不走 cwd）——用它们继续干活或落交接文件。
2. 让用户卸载并重新插拔该盘：`diskutil unmount force /Volumes/<name>`。
3. 恢复后立刻把工程**搬到内部盘**，别在原地重试。
4. 长远解法：新开一个工作区设在内部盘的会话。

## 工程选址硬规则

**不要在外挂 ExFAT 卷上放 Node 工程。** 实测代价：
- 克隆即生成大量 AppleDouble `._*` 伴生文件，`.git` 报 `non-monotonic index`。
- `node_modules` 分配体积虚高（ExFAT 簇大）：逻辑 ~600 M 的树占 ~6.6 G。
- 装依赖途中整卷挂死，连带把工作区锁死。
- 若该卷在百度网盘/iCloud 同步目录内，十万级文件还会被同步上去。

默认落位：`~/Projects/<name>`（内部 APFS）。
