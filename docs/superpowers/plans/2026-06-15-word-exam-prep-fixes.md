# word-exam-prep Skill 修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复审查报告中提出的 3 项警告（P1 过滤标点、P2 图片复制、P3 动态阈值），并补齐 2 项 P2 改进（中英双语标题、中文配置注释）。

**Architecture:** 所有修改集中在两个现有文件：`organize_exam_doc.py`（3 项代码修复 + 1 项注释改进）和 `formatting-guide.md`（1 项标题翻译改进）。不创建新文件，不改动 SKILL.md/PRD.md。

**Tech Stack:** python-docx, Python 3, Windows 路径

---

## File Structure

| File | Responsibility | Change Type |
|------|---------------|-------------|
| `.agents/skills/word-exam-prep/scripts/organize_exam_doc.py` | 自动化 Word 处理脚本 | Modify: 5 处分散修改 |
| `.agents/skills/word-exam-prep/references/formatting-guide.md` | 排版参数详细参考 | Modify: 12 个章节标题增加中文翻译 |

---

### Task 1: 字符间距紧缩跳过中文标点（P1）

**Files:**
- Modify: `.agents/skills/word-exam-prep/scripts/organize_exam_doc.py:546-550`

- [ ] **Step 1: 在 imports 下方添加标点正则常量**

在 `import re` 已有的前提下（脚本第 36 行已有），在 `HIGHLIGHT_COLORS` 定义之前（第 101 行之前）插入：

```python
# Regex to detect Chinese punctuation runs that must NOT receive character spacing compression
PUNCTUATION_RE = re.compile(r'^[\s，。、；：！？]+$', re.UNICODE)
```

- [ ] **Step 2: 替换现有的无差别紧缩循环**

定位到第 546-550 行：

```python
    # Apply character spacing compression (-0.5pt condensed) to body text
    # WARNING: Do NOT apply to Chinese punctuation.
    for para in new_doc.paragraphs:
        for run in para.runs:
            run.font.spacing = Pt(-0.5)
```

替换为：

```python
    # Apply character spacing compression (-0.5pt condensed) to body text.
    # IMPORTANT: Skip Chinese punctuation to prevent misalignment.
    for para in new_doc.paragraphs:
        for run in para.runs:
            if not PUNCTUATION_RE.fullmatch(run.text):
                run.font.spacing = Pt(-0.5)
```

- [ ] **Step 3: 验证正则行为**

在同一文件末尾的 `if __name__ == '__main__':` 块上方（或任意临时位置）插入测试代码，运行后删除：

```python
# Temporary verification
assert PUNCTUATION_RE.fullmatch('，') is not None
assert PUNCTUATION_RE.fullmatch('。') is not None
assert PUNCTUATION_RE.fullmatch('abc') is None
assert PUNCTUATION_RE.fullmatch('a，b') is None
```

Run: `python -c "import re; P=re.compile(r'^[\s，。、；：！？]+$'); print(P.fullmatch('，') is not None, P.fullmatch('abc') is None)"`
Expected: `True True`

---

### Task 2: 极限缩印下标题检测阈值动态化（P3）

**Files:**
- Modify: `.agents/skills/word-exam-prep/scripts/organize_exam_doc.py:192-197`

- [ ] **Step 1: 将硬编码字号阈值改为基于正文基础字号的动态计算**

定位 `detect_heading_level` 函数（第 181-205 行），将原阈值代码：

```python
    if bold and font_size and font_size >= 14:
        return 1
    if bold and font_size and font_size >= 12:
        return 2
    if bold and font_size and font_size >= 10.5:
        return 3
```

替换为：

```python
    base_size = FONTS['body'][2]  # Dynamic base font size (9pt standard, 7pt extreme)
    if bold and font_size and font_size >= base_size + 5:
        return 1
    if bold and font_size and font_size >= base_size + 3:
        return 2
    if bold and font_size and font_size >= base_size + 1.5:
        return 3
```

- [ ] **Step 2: 验证阈值计算**

在临时位置运行验证：

```python
# Standard mode (base_size=9)
assert (9 + 5) == 14   # Level 1 threshold
assert (9 + 3) == 12   # Level 2 threshold
assert (9 + 1.5) == 10.5  # Level 3 threshold

# Extreme mode (base_size=7)
assert (7 + 5) == 12   # Level 1 threshold
assert (7 + 3) == 10   # Level 2 threshold
assert (7 + 1.5) == 8.5  # Level 3 threshold
```

Run: `python -c "FONTS={'body':('宋体','TNR',7,False)}; b=FONTS['body'][2]; print(b+5, b+3, b+1.5)"`
Expected: `12 10 8.5`

---

### Task 3: 图片复制与居中插入（P2）

**Files:**
- Modify: `.agents/skills/word-exam-prep/scripts/organize_exam_doc.py:535-545`

- [ ] **Step 1: 在 imports 中追加 io 模块**

在第 36-43 行的 import 块中追加：

```python
import io
```

- [ ] **Step 2: 在表格复制代码之后、多栏布局代码之前插入图片复制逻辑**

定位到第 535 行（表格复制循环结束后的空行），插入以下代码块：

```python
    # Copy inline images with centered alignment
    for shape in doc.inline_shapes:
        try:
            # Extract image blob from original document
            embed_id = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
            image_part = doc.part.related_parts[embed_id]
            image_blob = image_part.blob

            # Create centered paragraph in new document
            new_para = new_doc.add_paragraph()
            new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            new_run = new_para.add_run()

            # Determine image width based on column count to prevent overflow
            if COMPACT_COLUMNS >= 3:
                max_width = Inches(2.5)
            elif COMPACT_COLUMNS == 2:
                max_width = Inches(3.5)
            else:
                max_width = Inches(6.0)

            new_run.add_picture(io.BytesIO(image_blob), width=max_width)
        except Exception:
            # If image extraction fails, add placeholder text so user knows
            new_para = new_doc.add_paragraph()
            new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            new_run = new_para.add_run('[图片：复制失败，请手动插入]')
            set_run_font(new_run, *FONTS['body'])
```

- [ ] **Step 3: 验证图片提取路径可用**

运行快速验证脚本（不在主脚本中保留）：

```python
from docx import Document
doc = Document('test_with_image.docx')  # any doc with an inline image
shape = doc.inline_shapes[0]
embed_id = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
print('Embed ID:', embed_id)
print('Part exists:', embed_id in doc.part.related_parts)
```

Expected: `Embed ID: rId8` (or similar), `Part exists: True`

---

### Task 4: 脚本关键配置区增加中文注释

**Files:**
- Modify: `.agents/skills/word-exam-prep/scripts/organize_exam_doc.py:59-99`

- [ ] **Step 1: 在 EXTREME_COMPACT 开关处增加中文注释**

将第 59 行：

```python
# Toggle extreme compact mode (cheat-sheet style: 3-4 columns, landscape, 6-8pt)
EXTREME_COMPACT = False
```

替换为：

```python
# 极限缩印模式开关
# True  = 开卷考试小抄级：3-4 栏 / 横向排版 / 6-8pt 字号 / 0.8cm 边距（极致省纸）
# False = 标准省纸模式（默认）：2 栏 / 纵向排版 / 9pt 字号 / 常规边距（兼顾可读性）
EXTREME_COMPACT = False
```

- [ ] **Step 2: 在 FONTS / MARGINS / LINE_SPACING_PT 等配置变量处增加中文注释**

将第 97-99 行：

```python
    LINE_SPACING_PT = 14         # Fixed 14pt line spacing
    COMPACT_COLUMNS = 2          # 2 columns
    LANDSCAPE = False            # Portrait orientation
```

替换为：

```python
    LINE_SPACING_PT = 14         # 固定行距 14 磅（极限模式下建议 8-10 磅）
    COMPACT_COLUMNS = 2          # 分栏数：标准模式 2 栏，极限模式建议 3-4 栏
    LANDSCAPE = False            # 纸张方向：False=纵向(Portrait)，True=横向(Landscape)
```

---

### Task 5: formatting-guide.md 增加中英双语标题

**Files:**
- Modify: `.agents/skills/word-exam-prep/references/formatting-guide.md`

- [ ] **Step 1: 将所有 12 个章节标题替换为中英双语**

逐行替换（保持原有 Markdown 层级和锚点不变）：

| 原行 | 替换为 |
|------|--------|
| `## 1. Font System` | `## 1. Font System（字体体系）` |
| `## 2. Color Palette for Highlighting` | `## 2. Color Palette for Highlighting（高亮色板）` |
| `## 3. Page Setup and Margins` | `## 3. Page Setup and Margins（页面设置与边距）` |
| `## 4. Section Breaks and Page Numbering` | `## 4. Section Breaks and Page Numbering（分节符与页码）` |
| `## 5. Paragraph and Line Spacing` | `## 5. Paragraph and Line Spacing（段落与行距）` |
| `## 6. Two-Column Layout` | `## 6. Two-Column Layout（双栏布局）` |
| `## 7. Extreme Compact Mode (3-4 Columns / Landscape)` | `## 7. Extreme Compact Mode (3-4 Columns / Landscape)（极限缩印模式：3-4 栏 / 横向排版）` |
| `## 8. Character Spacing Compression` | `## 8. Character Spacing Compression（字符间距紧缩）` |
| `## 9. Symbol Substitution for Space Saving` | `## 9. Symbol Substitution for Space Saving（符号替代省纸）` |
| `## 10. Word Built-in "Shrink to Fit" Command` | `## 10. Word Built-in "Shrink to Fit" Command（Word 内置“减少一页”命令）` |
| `## 11. Formula and Image Handling` | `## 11. Formula and Image Handling（公式与图片处理）` |
| `## 12. Style Name Compatibility` | `## 12. Style Name Compatibility（样式名称兼容性）` |

- [ ] **Step 2: 验证替换后无重复或错位**

Run: `grep -n "^## [0-9]" formatting-guide.md`
Expected: 输出 12 行，每行包含对应的英文和中文翻译，无重复编号。

---

## Self-Review

**1. Spec coverage:**
- P1 过滤中文标点 → Task 1 ✅
- P2 图片复制与居中 → Task 2 ✅
- P3 标题阈值动态化 → Task 3 ✅
- formatting-guide 中英双语 → Task 4 ✅
- 脚本配置区中文注释 → Task 5 ✅

**2. Placeholder scan:**
- 无 "TBD"、"TODO"、"implement later" ✅
- 每步均含实际代码块 ✅
- 无 "Similar to Task N" ✅

**3. Type consistency:**
- `PUNCTUATION_RE` 为 `re.Pattern`（正则对象），`.fullmatch()` 方法使用正确 ✅
- `FONTS['body'][2]` 返回 `int`（字号），与 `font_size`（`float`）的加减运算兼容 ✅
- `io.BytesIO(image_blob)` 接收 `bytes`，与 `doc.part.related_parts[embed_id].blob` 类型一致 ✅
- `add_picture` 的 `width` 参数使用 `Inches`，与 `max_width` 类型一致 ✅

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-06-15-word-exam-prep-fixes.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
