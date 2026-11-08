#!/usr/bin/env bash
# Sync this skill into the shared repo https://github.com/smthelp/smthelp-skill (main), add/refresh its README row,
# commit and tag smt-3d-product-media-v<VERSION>, push. Needs push rights (gh auth / git credential) on the machine.
# usage: tools/publish_to_repo.sh [repo_dir]   (clones to /tmp/smthelp-skill when no repo_dir is given)
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"; NAME="$(basename "$SK")"; VER="$(cat "$SK/VERSION")"
REPO="${1:-/tmp/smthelp-skill}"
[ -d "$REPO/.git" ] || git clone --depth 50 https://github.com/smthelp/smthelp-skill.git "$REPO"
git -C "$REPO" pull --ff-only
rsync -a --delete --exclude '__pycache__' --exclude 'out*' --exclude '*.pyc' "$SK/" "$REPO/$NAME/"
ROW="| \`$NAME\` | Hark agent | 产品 3D 图（STEP）→ ① 工作原理动画视频（CPU 渲染、品牌字幕条、步骤字幕、披露说明、实机片段插入、机身 logo、中英 AI 配音，EN/ZH MP4）② 产品介绍 PPT（SM 16:9 模板，内嵌视频与封面，经 smt-product-ppt-rebrand 构建）；单一 job.json（schema job@1）、统一 CLI \`smt3dmedia.py\`（13 个可续跑阶段、--set 覆盖、JSON 结果 + 退出码 0/2/3）、manifest 追溯、smoke 测试、S7040P 示例、升级/兼容规则（v$VER） |"
python3 - "$REPO/README.md" "$NAME" "$ROW" <<'P'
import sys, re
p, name, row = sys.argv[1:]; s = open(p, encoding="utf-8").read()
lines = s.split("\n"); hit = [i for i, l in enumerate(lines) if l.startswith(f"| `{name}`")]
if hit: lines[hit[0]] = row
else:
    # insert after the last row of the first table under "自建技能"
    start = next(i for i, l in enumerate(lines) if "自建技能" in l)
    i = start + 1
    while i < len(lines) and not lines[i].startswith("|"): i += 1
    while i < len(lines) and lines[i].startswith("|"): i += 1
    lines.insert(i, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
P
cd "$REPO"; git add "$NAME" README.md
git commit -m "$NAME v$VER" || echo "nothing to commit"
git tag -f -a "$NAME-v$VER" -m "$NAME v$VER"
git push origin HEAD && git push -f origin "$NAME-v$VER"
echo "published $NAME v$VER"
