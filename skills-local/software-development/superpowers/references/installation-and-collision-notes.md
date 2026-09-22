# Superpowers Installation Notes

## Skill Collision (Critical)

4 Superpowers sub-skills share **identical bare names** with existing Hermes built-in skills in `software-development/`:

| Superpowers sub-skill | Collides with built-in |
|---|---|
| `superpowers/subagent-driven-development` | `software-development/subagent-driven-development` |
| `superpowers/systematic-debugging` | `software-development/systematic-debugging` |
| `superpowers/test-driven-development` | `software-development/test-driven-development` |
| `superpowers/writing-plans` | `software-development/writing-plans` |

**Symptom**: `skill_view(name='subagent-driven-development')` fails with:
```
Ambiguous skill name 'X': 2 skills match across your local skills dir and external_dirs
```

**Fix**: Always use the full category/path prefix:
```
skill_view(name='superpowers/subagent-driven-development')
skill_view(name='superpowers/writing-plans')
skill_view(name='superpowers/systematic-debugging')
skill_view(name='superpowers/test-driven-development')
```

The Superpowers versions are more comprehensive (they are the canonical ones from obra/superpowers). The built-in Hermes versions predate Superpowers and are less full-featured.

## Installation Verification

```bash
ls ~/.hermes/skills/superpowers/
# Should show: brainstorming, dispatching-parallel-agents, executing-plans,
#              finishing-a-development-branch, receiving-code-review,
#              requesting-code-review, subagent-driven-development,
#              systematic-debugging, test-driven-development,
#              using-git-worktrees, using-superpowers,
#              verification-before-completion, writing-plans, writing-skills

hermes skills list | grep superpowers
# Should show 14 skills under the superpowers category
```

## Cloning for Future Updates

To pull latest Superpowers changes:
```bash
cd /tmp/superpowers-update
git clone --depth=1 https://github.com/obra/superpowers.git .
cp -r skills/* ~/.hermes/skills/superpowers/
rm -rf /tmp/superpowers-update
```
