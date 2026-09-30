import re, glob, os, json

BS = chr(92)


def norm(p):
    return p.replace(BS, "/")


def body(p):
    raw = open(p, encoding="utf-8").read()
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n", raw, re.S)
    return raw[m.end():].encode() if m else raw.encode()


skill_files = ["SKILL.md"] + sorted(glob.glob("subskills/*/SKILL.md"))
ref_files = sorted(glob.glob("references/*.md"))

print("=== 体积：SKILL.md 正文 8000B 上限 ===")
over = []
for p in skill_files:
    n = len(body(p))
    if n > 8000:
        over.append(p)
    print("  %-34s %6dB %s" % (p, n, "ok" if n <= 8000 else "OVER"))
print("  超限:", over or "无")
for p in ref_files:
    print("  %-34s %6dB (reference,不受限)" % (p, os.path.getsize(p)))

print("=== 引用链接解析 ===")
bad = []
for p in skill_files:
    txt = open(p, encoding="utf-8").read()
    for ref in set(re.findall(r"(?:\.\./)*(?:references|subskills)/[\w.\-]+\.md", txt)):
        if ref.startswith(".."):
            t = os.path.normpath(os.path.join(os.path.dirname(p), ref))
        else:
            t = ref
        if not os.path.exists(t):
            bad.append((p, ref))
print("  断链:", bad or "无")

print("=== 残留违规 ===")
checks = {
    "宿主硬编码(非探测表)": r"\.claude/projects/\[project\]|\.claude/projects/<project>",
    "花括号路径变量": r"\$\{?SKILL_DIR|\$\{?CLAUDE_SKILL_DIR",
}
allf = skill_files + ref_files + ["CHANGELOG.md"]
for k, pat in checks.items():
    hits = [(p, i + 1) for p in allf for i, l in enumerate(open(p, encoding="utf-8")) if re.search(pat, l)]
    print("  %s: %d %s" % (k, len(hits), hits[:4]))

print("=== frontmatter ===")
raw = open("SKILL.md", encoding="utf-8").read()
m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", raw, re.S)
fm = m.group(1)
print("  字段:", re.findall(r"^(\w[\w-]*):", fm, re.M))
print("  frontmatter 字符数:", len(fm), "(上限 1024)")
print("  description 里含工作流箭头:", "->" in fm or "→" in fm)
print("  description 里含'合并来源':", "合并来源" in fm)

print("=== evals ===")
d = json.load(open("evals/evals.json", encoding="utf-8"))
kinds = {}
for c in d["cases"]:
    kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
print("  用例:", len(d["cases"]), kinds)
print("  全部标 not_executed:", all(c.get("status") == "not_executed" for c in d["cases"]))

print("=== 结构最小要求（项目 CLAUDE.md 第2节）==="
      )
for need in ["SKILL.md", "evals/evals.json"]:
    print("  %-20s %s" % (need, "存在" if os.path.exists(need) else "缺失"))

print("=== handoff 专项 ===")
codes = ["[V]", "[W]", "[Q]", "[R]", "[F]"]
hs = open("subskills/handoff/SKILL.md", encoding="utf-8").read()
print("  五个置信度码齐且互不重复:", all(c in hs for c in codes),
      "| 码数:", len(set(codes)), "| 无符号重叠:", len(set(c.split()[0] for c in codes)) == 5)

tpl = open("references/handoff-template.md", encoding="utf-8").read()
secs = re.findall(r"^## \*?\u2605?\*?(\d+)\.", tpl, re.M)
print("  模板节数:", len(secs), "期望 10 ->", "ok" if len(secs) == 10 else "MISMATCH", secs)
print("  必需节标记(★)出现次数:", tpl.count("★"), "(6 个必需节 + 1 处图例)")

tiers = open("references/knowledge-tiers.md", encoding="utf-8").read()
spots = [".learnings/", ".ai/HANDOFF.md", ".ai/knowledge/", "agent 记忆库", "规则文件"]
missing = [s for s in spots if s not in tiers]
print("  五处落点全覆盖:", "ok" if not missing else missing)

parent = open("SKILL.md", encoding="utf-8").read()
subs = sorted(glob.glob("subskills/*/SKILL.md"))
print("  子命令目录数:", len(subs), [os.path.basename(os.path.dirname(p)) for p in subs])
notrouted = [p for p in subs if norm(p) not in parent.replace(BS, "/")]
print("  未在主入口路由表中出现的子技能:", notrouted or "无")
for kw in ["handoff", "[V]", "knowledge-tiers"]:
    print("  主入口提到 %s: %s" % (kw, kw in parent))

print("=== evals 版本与 skill 版本一致 ===")
skill_ver = re.search(r"^version:\s*([\d.]+)", open("SKILL.md", encoding="utf-8").read(), re.M).group(1)
print("  SKILL.md:", skill_ver, "| evals:", d["version"], "| 一致:", skill_ver == d["version"])
print("  用例总数:", len(d["cases"]))
