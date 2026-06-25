# 纯 HTML/CSS Prompt 模板

> 零依赖、单文件输出。
> 所有 CSS 变量定义在 `:root {}`，暗色模式用 `[data-theme="dark"]`。

---

## Block: {Block 类型}

```
生成一个纯 HTML/CSS 的 {Block 类型名称}（单文件，零依赖）。

**文件结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{页面标题}</title>
  <style>
    :root { /* DESIGN.md 的所有变量 */ }
    [data-theme="dark"] { /* 暗色覆盖 */ }
    /* 组件样式 — 禁止裸 hex 值 */
  </style>
</head>
<body>
  <!-- 语义化 HTML -->
</body>
</html>
```

**HTML 语义要求**：
- 使用 `<main>` / `<nav>` / `<section>` / `<article>` / `<footer>`
- 每个 section 有 `data-section-id`
- 图片使用 `loading="lazy"` + `alt`
- 表单使用 `<label>` + `<input>` 正确关联

**CSS 要求**：
- 所有颜色使用 CSS 变量
- 响应式：@media (max-width: 768px) 移动端适配
- prefers-reduced-motion: reduce 必须禁用动效
- :focus-visible 必须为所有交互元素定义

**全局约束**：见 react-tailwind.md（反 AI 规则 + Typography 硬规则全相同）

**纯 HTML 特有禁止**：
- ❌ 外部 CSS 文件（全部内联在 `<style>`）
- ❌ 外部字体 CDN（使用系统字体回退）
- ❌ JavaScript 框架引用（纯原生）
- ❌ 不完整的 HTML 结构（必须有 doctype + head + body）
```

---

## 核心组件模板

### 按钮 (纯 HTML)

```html
<button class="btn-primary" type="button">
  按钮文字
</button>

<style>
.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: var(--space-sm) var(--space-lg);
  font-family: var(--font-body);
  font-weight: 600;
  font-size: var(--text-body);
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: transform 100ms ease-in;
}
.btn-primary:hover { background: var(--color-primary-hover); transform: translateY(-1px); }
.btn-primary:active { transform: translateY(1px); }
.btn-primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 卡片 (纯 HTML)

```html
<article class="card">
  <h3 class="card-title">卡片标题</h3>
  <p class="card-body">卡片内容...</p>
</article>

<style>
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--space-lg);
}
.card:hover { border-color: var(--color-primary); }
</style>
```

### 表单 (纯 HTML)

```html
<form class="form">
  <label class="form-label" for="name">姓名</label>
  <input class="form-input" type="text" id="name" required>

  <label class="form-label" for="email">邮箱</label>
  <input class="form-input" type="email" id="email" required>

  <button class="btn-primary" type="submit">提交</button>
</form>

<style>
.form-label {
  display: block;
  font-size: var(--text-small);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xs);
}
.form-input {
  width: 100%;
  height: 40px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-body);
  font-size: var(--text-body);
  margin-bottom: var(--space-md);
  box-sizing: border-box;
}
.form-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 2px rgba({primary-r}, {primary-g}, {primary-b}, 0.2);
}
.form-input.error { border-color: var(--color-error); }
</style>
```
