# GSAP Animation Guide — 前端动效最佳实践

> 基于 [greensock/gsap-skills](https://github.com/greensock/gsap-skills)（GSAP 官方 AI Skill）整理。
> GSAP 标准许可下可商用免费，含 SplitText、MorphSVG 等原 Club 插件（官方原文："Commercial usage is covered under the standard license"）。
> **唯一实质限制**：不得用 GSAP 构建与 Webflow 可视化动画编辑能力直接竞争的产品/工具；做这类产品需先取得 GSAP 方许可。
> 来源：https://gsap.com/community/standard-license/ （2026-10-04 核）

---

## 1. 何时选择 GSAP vs Motion

| 场景 | 推荐 | 原因 |
|------|------|------|
| 复杂时间轴编排 | **GSAP Timeline** | 精确的时序控制和嵌套 |
| 滚动驱动动画 | **GSAP ScrollTrigger** | 行业标准的滚动动画方案 |
| 文字逐字/逐词动画 | **GSAP SplitText** | 精细的文字拆解控制 |
| SVG 路径/形状动画 | **GSAP MorphSVG/DrawSVG** | SVG 动画最专业方案 |
| 布局过渡动画 | **GSAP Flip** | FLIP 技术实现无缝布局动画 |
| 简单入场/退出 | **CSS transitions + Motion** | 轻量、无需额外依赖 |
| React 快速原型 | **Motion (motion/react)** | 声明式 API、React 友好 |
| 高性能要求 | **GSAP + transforms** | 纯 compositor 层动画 |

**原则**：简单效果用 CSS/Motion，复杂/专业效果用 GSAP。

---

## 2. GSAP 核心 API

### 2.1 基础 Tween

```javascript
import { gsap } from "gsap";

// 入场动画
gsap.from(".hero-title", { y: 60, opacity: 0, duration: 0.8, ease: "power3.out" });

// 状态切换
gsap.to(".card", { scale: 1.05, duration: 0.3, ease: "back.out(1.7)" });

// 从指定状态到指定状态
gsap.fromTo(".box",
  { x: -100, opacity: 0 },
  { x: 0, opacity: 1, duration: 0.6, ease: "power2.inOut" }
);
```

### 2.2 时间轴（Timeline）

```javascript
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.6 } });

tl.from(".title", { y: 40, opacity: 0 })
  .from(".subtitle", { y: 30, opacity: 0 }, "-=0.3")
  .from(".cta", { scale: 0.8, opacity: 0 }, "-=0.2");

// 位置参数
tl.to(".panel", { x: 100 }, "start")   // 在 "start" 标签处开始
  .to(".dot", { rotation: 180 }, "+=0.2") // 在 start 后 0.2s
  .from(".footer", { y: 20 }, "-=0.1"); // 重叠 0.1s
```

### 2.3 缓动（Easing）

```javascript
// 推荐默认缓动
ease: "power2.out"   // 优雅的减速，最常用
ease: "power3.inOut" // 平滑的进出
ease: "back.out(1.7)" // 轻微回弹
ease: "expo.out"    // 快速开始，缓慢停止
ease: "none"        // 线性（用于 ScrollTrigger containerAnimation）
```

### 2.4 Stagger（交错）

```javascript
gsap.from(".card", {
  y: 40, opacity: 0,
  stagger: 0.08,           // 每项间隔 80ms
  duration: 0.5,
  ease: "power2.out"
});

// 从中心向两侧
gsap.from(".items", {
  y: 30, opacity: 0,
  stagger: { each: 0.05, from: "center" },
  duration: 0.4
});
```

---

## 3. ScrollTrigger — 滚动驱动动画

```javascript
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// 基础滚动触发动画
gsap.from(".feature-card", {
  scrollTrigger: {
    trigger: ".features-section",
    start: "top 80%",
    end: "bottom 20%",
    toggleActions: "play none none reverse"
  },
  y: 50, opacity: 0, duration: 0.6, ease: "power2.out"
});

// Scrub 模式（动画进度跟随滚动）
gsap.to(".progress-bar", {
  scaleX: 1,
  transformOrigin: "left",
  scrollTrigger: {
    trigger: "body",
    start: "top top",
    end: "bottom bottom",
    scrub: true
  }
});

// Pin + 内容动画
gsap.timeline({
  scrollTrigger: {
    trigger: ".pin-section",
    start: "top top",
    end: "+=1500",
    pin: true,
    scrub: 1
  }
})
.to(".panel-1", { x: 0, duration: 1 })
.to(".panel-2", { x: 0, duration: 1 }, "-=0.5");
```

### ScrollTrigger 最佳实践

| 规则 | 说明 |
|------|------|
| `refresh()` | DOM 变化后调用 `ScrollTrigger.refresh()` |
| `markers: true` | 开发时启用，生产环境关闭 |
| `once: true` | 只播放一次（避免重复触发） |
| `toggleActions` | 控制进入/离开/返回时的行为 |
| `scrub: true` | 直接跟随滚动，`scrub: 1` 带 1s 延迟平滑 |

---

## 4. React 集成（useGSAP）

```jsx
import { useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

function HeroSection() {
  const containerRef = useRef(null);

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    tl.from(".title", { y: 50, opacity: 0, duration: 0.8 })
      .from(".subtitle", { y: 30, opacity: 0, duration: 0.6 }, "-=0.4");
  }, { scope: containerRef }); // scope 确保选择器作用域

  return <div ref={containerRef} className="hero">...</div>;
}
```

### React 关键规则

- ✅ 始终使用 `scope` 限制选择器范围
- ✅ 使用 `useGSAP()` 替代 `useEffect` + `gsap.context()`
- ✅ GSAP 只在客户端运行（SSR 安全）
- ✅ 在事件回调中使用 `contextSafe()` 包装

```jsx
useGSAP((context, contextSafe) => {
  // 安全：在 useGSAP 执行时创建
  const btn = contextSafe(() => buttonRef.current);
  document.addEventListener("click", () => {
    gsap.to(btn(), { scale: 0.95, duration: 0.1 });
  });
}, { scope: containerRef });
```

---

## 5. SplitText — 文字动画

```javascript
import { gsap } from "gsap";
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words, chars" });

gsap.from(split.chars, {
  opacity: 0,
  y: 40,
  rotateX: -90,
  stagger: 0.02,
  duration: 0.6,
  ease: "back.out(1.7)"
});
```

**适用场景**：Hero 标题逐字入场、文字洗牌效果（ScrambleText）、数据可视化。

---

## 6. Flip — 布局动画

```javascript
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";
gsap.registerPlugin(Flip);

// 捕获状态 → 修改 DOM → 动画回原状态
function animateFilter() {
  const state = Flip.getState(".card");
  // 应用筛选（改变 DOM 布局）
  applyFilter(".card", ".filtered");
  Flip.from(state, { duration: 0.5, ease: "power2.inOut" });
}
```

**适用场景**：列表过滤、卡片展开/收起、网格重排。

---

## 7. 性能规范

| ✅ 推荐 | ❌ 避免 |
|---------|---------|
| `x`, `y`, `scale`, `rotation` | `width`, `height`, `top`, `left` |
| `autoAlpha`（opacity + visibility） | `opacity`（会保留 pointer-events） |
| `stagger` 批量动画 | 手动设置多个 `delay` |
| `gsap.quickTo()` 高频更新 | 每帧创建新 tween |
| `will-change: transform` | 给所有元素设 `will-change` |
| ScrollTrigger 批量注册 | 几百个独立 ScrollTrigger |

---

## 8. 无障碍（prefers-reduced-motion）

```javascript
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // 正常动画
  gsap.to(".hero", { y: -20, scrollTrigger: { /* ... */ } });
  return () => {}; // 清理
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // 减少模式：跳过动画
  return () => {};
});
```

---

## 9. 安装

```bash
# 单一包包含所有功能
npm install gsap
npm install @gsap/react  # React 专属 hook

# 导入
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { Flip } from "gsap/Flip";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, SplitText, Flip, useGSAP);
```

> **注意**：所有插件（SplitText、MorphSVG 等）现已无需 Club GSAP 会员；商用免费的前提是产品不属于"与 Webflow 竞争的动画构建工具"（见文首许可说明）。
