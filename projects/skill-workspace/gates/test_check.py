"""门一自身的回归测试：每类跳过规则都要有"该跳过的确实跳过 + 不该跳过的仍然报"两侧断言。

只有一条抑制通道的门才会被行内注释关掉（ESLint 的教训），所以这里锁的是
"规则不许被绕过"，同时锁住 S5 的成果：包内 .md 不许再出现花括号路径变量。

用法：python gates/test_check.py  （无第三方依赖，失败退出码 1）
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import check  # 必须先插 path 再导入：check.py 用自身位置推导包根

fails = []


def case(name, cond):
    if not cond:
        fails.append(name)
    print(f"  {'✓' if cond else '✗'} {name}")


def skip_reason(line, raw=None):
    m = check.CODE_PATH_RE.search(line)
    assert m, f"样例没被正则命中：{line}"
    return check._ref_skippable(line, m, raw or m.group(0))


print("— shell 变量前缀（$SCRIPTS/x.sh 不是路径）")
case("含 $ 前缀被跳过", skip_reason('bash "$SCRIPTS/source-cleanup.sh" list'))
case("真实路径不被跳过", not skip_reason("跑 scripts/source-cleanup.sh 看看"))

print("— 花括号占位前缀（{技能目录}/x 待替换，不是字面路径）")
case("} 前缀被跳过", skip_reason('bash "{技能目录}/scripts/source-cleanup.sh" auto'))
case("无占位前缀仍判存在", not skip_reason("详见 `references/deploy.md`"))

print("— URL 尾巴（https://host/a/b.md 不是本地路径）")
case("URL 被跳过", skip_reason("见 https://example.com/docs/guide.md"))

print("— 内容级跳过")
case("外链跳过", check._skip_by_content("https://a.md"))
case("裸文件名按运行时产物跳过", check._skip_by_content("state.json") == "运行时产物")
case("模板占位跳过", check._skip_by_content("{全局skills目录}/x.md") == "模板占位")
case("带花括号的裸文件名也跳过", bool(check._skip_by_content("report-{date}.md")))
case("包内相对路径不跳过", check._skip_by_content("references/deploy.md") is None)

print("— 花括号路径变量识别（S5 废除的对象）")
for token in ("${SKILL_DIR}", "${CLAUDE_SKILL_DIR}", "${_CLAUDE_SKILL_DIR}"):
    case(f"认出 {token}", bool(check.PLACEHOLDER_RE.search(token)))
for benign in ("SKILL_DIR", "CLAUDE_SKILL_DIR", "{技能目录}", "{新技能}/references/x.md"):
    case(f"不误伤 {benign}", not check.PLACEHOLDER_RE.search(benign))

print("— S5 收口：包内 .md 与 evals.json 不许再出现花括号路径变量")
bad = []
for p in ROOT.rglob("*.md"):
    top = p.relative_to(ROOT).parts[0]
    if top in check.SKIP_DIRS or top == "artifacts":
        continue
    for m in check.PLACEHOLDER_RE.finditer(p.read_text(encoding="utf-8")):
        bad.append(f"{p.relative_to(ROOT).as_posix()} {m.group(0)}")
for p in list(ROOT.rglob("evals.json")):
    for m in check.PLACEHOLDER_RE.finditer(p.read_text(encoding="utf-8")):
        bad.append(f"{p.relative_to(ROOT).as_posix()} {m.group(0)}")
case(f"变量残留为 0（实测 {len(bad)} 处）", not bad)
for x in bad[:8]:
    print("     ", x)

print()
if fails:
    print(f"FAIL {len(fails)} 条：{fails}")
    sys.exit(1)
print("全部通过")
