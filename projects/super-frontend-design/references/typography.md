# Typography 硬规则

> 基于 Open Design `craft/typography.md`（MIT 许可）精炼
> 这些规则覆盖 DESIGN.md 的排版 section，是 design 和 review 阶段的硬约束

---

## 1. 字号阶（乘法比例 1.2 或 1.25）

| 角色 | 字号范围 | 用途 |
|------|:---:|------|
| Display | 48–72 px | 品牌展示、超级标题 |
| H1 | 32–48 px | 页面标题 |
| H2 | 24–32 px | Section 标题 |
| H3 | 20–24 px | 子标题 |
| Body | 15–18 px | 正文 |
| Small | 13–14 px | UI 标签、辅助文字 |
| Caption | 11–12 px | 脚注、时间戳 |

每页面可见字号 ≤ 6–8 种。

---

## 2. 行高 (Line Height)

| 文字大小 | 行高 | 说明 |
|----------|:---:|------|
| Display / H1 (≥32 px) | `1.0 – 1.2` | 紧凑 |
| Body (15–18 px) | `1.5 – 1.6` | 标准可读 |
| Small (≤14 px) | `1.5` | 最小 |

---

## 3. 字间距 (Letter Spacing) — AI 最大盲区

| 上下文 | 字间距 | 强制性 |
|--------|:---:|:---:|
| Body text (14–18 px) | `0` (默认) | 必须 |
| Small text (11–13 px) | `0.01em – 0.02em` (正值) | 必须 |
| UI 标签和按钮文字 | `0.02em` | 必须 |
| **ALL CAPS** | **`0.06em – 0.1em`** | **绝对必须** |
| Headings 32 px+ | `-0.01em – -0.02em` | 必须 |
| Display 48 px+ | `-0.02em – -0.03em` | 必须 |

**为什么 ALL CAPS 需要 0.06em tracking：**
不带此规则的 ALL CAPS 文字看起来拥挤且业余。这是 AI 生成设计中最可靠的"AI 指纹"之一。
0.06em 下限来自印刷和网页排版实践的收敛值（参考 Bringhurst《The Elements of Typographic Style》§3.2.7）。

---

## 4. 字体配对

- 每个页面最多 **2 个 typeface**（display + body，或一个可变字体多 weight）
- 始终声明系统回退链
- **禁止** `font-family: system-ui` 单独用于标题 — 这是教科书级 AI 默认

```css
/* ✅ 正确 */
h1 { font-family: var(--font-display); }
body { font-family: var(--font-body); }

/* ❌ 错误 — AI 默认 */
h1 { font-family: Inter, system-ui, sans-serif; }
```

---

## 5. 正文最大宽度

```
max-width: 65ch
```

65 字符/行是 web 正文的可读性安全宽度（约 50–75 字符范围）。

---

## 6. 三 Weight 系统

大多数精心设计的 UI 恰好使用 3 个 weight：

| Weight | 数值 | 用途 |
|--------|:---:|------|
| **Read** | 400 / 450 | body copy |
| **Emphasize** | 500 / 550 | UI text, labels, navigation |
| **Announce** | 600 | headlines, buttons |

Weight 700+ 极少需要。如果你的设计用了 Bold on Bold，说明其他地方缺少 weight 纪律。

---

## 7. review 阶段 Typography 检查清单

| # | 检查项 | 检测方式 | 严重度 |
|:---:|------|---------|:---:|
| T1 | ALL CAPS 缺少 letter-spacing ≥ 0.06em | Grep `text-transform:\s*upper` 并检查 letter-spacing | 🔴 High |
| T2 | Display text ≥32px 缺少负 tracking | 检查 ≥32px 的文本元素是否有 letter-spacing 负值 | 🟡 Medium |
| T3 | Body text 行高 < 1.5 | 检查 15–18px 文本的 line-height | 🟡 Medium |
| T4 | Body copy 行宽超 75 字符 | 计算 `max-width` 字符数 | 🟡 Medium |
| T5 | >2 个 typeface 在同一页面 | 统计 `font-family` 声明中的第一字体 | 🟡 Medium |
| T6 | `font-family: system-ui` 在标题元素 | Grep `h[1-6].*font-family.*system-ui` | 🔴 High |
| T7 | Weight 超过 3 个 | 统计 `font-weight` 值种类 | 🟢 Low |
| T8 | `text-align: justify` 在 body copy | Grep `text-align:\s*justify` | 🔴 High |
