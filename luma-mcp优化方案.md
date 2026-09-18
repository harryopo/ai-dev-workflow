# luma-mcp 优化方案

> 基于深度源码分析 + 20+竞品对比
> 日期：2026-08-08

---

## 一、luma-mcp 现状分析

### 已有优势（做得好的地方）

| 特性 | 实现质量 |
|---|---|
| 多Provider支持 | ✅ 6个（智谱/硅基/阿里/火山/腾讯/自定义） |
| 多裁剪大图 | ✅ 自适应裁剪、文本密集保真 |
| 安全防护 | ✅ SSRF防护、路径遍历防护、像素限制 |
| LRU缓存 | ✅ 进程级缓存、SHA-256 key摘要 |
| HTTP/Docker | ✅ Streamable HTTP、Bearer鉴权 |
| 重试机制 | ✅ 指数退避+随机jitter |
| 错误脱敏 | ✅ Bearer token/secret脱敏 |
| 单工具设计 | ✅ `image_understand` 简洁入口 |

### 架构总结

```
用户调 image_understand
  ↓
config.ts 加载配置（单Provider）
  ↓
image-processor.ts 预处理（读取/验证/压缩/裁剪）
  ↓
vision-client.ts → 某 Provider 客户端 → 视觉模型 API
  ↓
返回文字描述
```

---

## 二、优化空间（按优先级排序）

### P0 — 核心竞争力差距（必须做）

#### 1. 多Provider Fallback链

**现状：** 只能配置一个Provider，主Provider挂了就报错
**优化：** 支持配置多个Provider形成降级链

```
主Provider（智谱GLM-4.6V）→ 备用1（硅基DeepSeek-OCR）→ 备用2（阿里Qwen-VL）→ local（Ollama）
```

**实现思路：**
```typescript
// config.ts 新增
interface FallbackConfig {
  primary: ProviderConfig;
  fallbacks: ProviderConfig[];
  strategy: "sequential" | "race";  // 顺序降级 or 竞速
}

// 环境变量
FALLBACK_CHAIN=zhipu,siliconflow,qwen
FALLBACK_STRATEGY=sequential  // 或 race
```

**参考：** ds-vision-skill 的 Race Pool（竞速池），vision-bridge-mcp 的多模型 fallback

---

#### 2. Focus Hint 机制（上下文感知描述）

**现状：** 所有图片用同一个 `DEFAULT_BASE_VISION_PROMPT`，不考虑用户意图
**优化：** 从用户的 prompt 提取关注点，让视觉模型只描述相关细节

**对比：**
- 现在：固定prompt → "描述这张图的布局、元素、颜色..."
- 优化后：用户问"这个按钮什么颜色" → focus hint="关注颜色信息" → 只描述颜色

**实现思路：**
```typescript
// 新增 focus-hint.ts
function extractFocusHint(userPrompt: string, taskType: TaskType): string {
  // 从用户prompt提取关键词，生成针对性的focus hint
  // 例：用户问"报错信息是什么" → focus="提取所有错误文本和堆栈信息"
  // 例：用户问"页面布局" → focus="描述DOM层级关系和空间排列"
}
```

**参考：** agent-vision-toolkit (348⭐) 的核心创新——"Focus Hint"

---

#### 3. 增加专用工具（OCR + 对比）

**现状：** 只有 `image_understand` 一个工具
**优化：** 增加 `image_ocr`（专用OCR）和 `image_compare`（图片对比）

**新增工具定义：**
```typescript
// image_ocr — 专用文字提取（走OCR通道更快更准）
server.tool("image_ocr", {
  image_source: z.string(),
  language_hint: z.enum(["zh", "en", "ja", "auto"]).optional(),
  output_format: z.enum(["plain", "markdown", "json"]).optional(),
});

// image_compare — 前后对比（设计稿vs实现）
server.tool("image_compare", {
  image_source_before: z.string(),
  image_source_after: z.string(),
  prompt: z.string(),  // "找出差异"
});
```

**参考：** Visual-Enhancement-mcp 的 `vision_ocr`、visionbridge 的 `compare_images`

---

### P1 — 体验提升（应该做）

#### 4. 批量图片处理

**现状：** 一次只处理一张图
**优化：** 支持传入多个图片路径，并行处理

```typescript
// image_understand 支持多图
server.tool("image_understand", {
  image_source: z.string().or(z.array(z.string())),  // 支持单张或多张
  prompt: z.string(),
});
```

**参考：** llm-vision-mcp 的 `describe_images`（批量100张）

---

#### 5. 持久化缓存

**现状：** 进程级 LRU 内存缓存，重启即失效
**优化：** 增加磁盘缓存层

```typescript
// 新增 disk-cache.ts
interface DiskCacheConfig {
  enabled: boolean;
  dir: string;          // 缓存目录
  maxAge: number;       // 最大缓存时间（ms）
  maxSize: number;      // 最大缓存大小（MB）
}
```

**好处：** 跨会话复用结果，同一张截图不需要重复调API

---

#### 6. 自动调用规则注入

**现状：** 需要用户手动提示模型调用 `image_understand`
**优化：** 提供 `vision_rules` 工具，自动生成注入规则

```typescript
// 新增工具：生成自动调用规则
server.tool("vision_rules", {}, async () => {
  return {
    content: `当用户上传图片或提到截图/界面/报错时，自动调用 image_understand 工具。
    不要说"我看不到图片"，直接调工具。`
  };
});
```

**参考：** vision-bridge-mcp 的 `vision_rules` + 自动CLAUDE.md注入

---

#### 7. 配置文件支持

**现状：** 全部通过环境变量（15+个env var）
**优化：** 支持 `luma.config.json` 配置文件

```json
{
  "providers": {
    "primary": { "provider": "zhipu", "apiKey": "${ZHIPU_API_KEY}" },
    "fallback": [
      { "provider": "siliconflow", "apiKey": "${SILICONFLOW_API_KEY}" }
    ]
  },
  "image": {
    "multiCrop": true,
    "maxTiles": 5,
    "cache": { "type": "disk", "dir": ".luma-cache" }
  },
  "tools": {
    "ocr": true,
    "compare": true,
    "batch": true
  }
}
```

---

### P2 — 锦上添花（可以做）

#### 8. PDF/文档解析

**现状：** 只处理图片格式
**优化：** 集成 MinerU 或 PDF 解析能力

**参考：** ds-vision-skill 的 MinerU 集成

---

#### 9. 音频/视频理解

**现状：** 不支持
**优化：** 利用 GLM-4.6V 的视频理解能力扩展

---

#### 10. Web 监控仪表盘

**现状：** 日志记录到文件
**优化：** HTTP模式下增加 `/dashboard` 页面

**展示内容：**
- 调用次数/成功率/平均延迟
- 各Provider使用占比
- 缓存命中率
- 费用估算
- 历史调用记录

---

## 三、优化优先级总表

| 优先级 | 优化项 | 工作量 | 影响 | 参考项目 |
|---|---|---|---|---|
| **P0** | 多Provider Fallback链 | 大 | 🔴 可靠性大幅提升 | ds-vision-skill |
| **P0** | Focus Hint机制 | 中 | 🔴 描述质量提升 | agent-vision-toolkit |
| **P0** | 增加OCR+对比工具 | 中 | 🔴 功能完整性 | Visual-Enhancement-mcp |
| **P1** | 批量图片处理 | 小 | 🟡 效率提升 | llm-vision-mcp |
| **P1** | 持久化缓存 | 中 | 🟡 成本降低 | - |
| **P1** | 自动调用规则注入 | 小 | 🟡 用户体验 | vision-bridge-mcp |
| **P1** | 配置文件支持 | 小 | 🟡 易用性 | - |
| **P2** | PDF/文档解析 | 大 | 🟢 场景扩展 | ds-vision-skill |
| **P2** | 音频/视频理解 | 大 | 🟢 场景扩展 | - |
| **P2** | Web监控仪表盘 | 中 | 🟢 可观测性 | - |

---

## 四、建议的开发路线

### 第一阶段（核心增强）
1. 多Provider Fallback链 — 提升可靠性
2. Focus Hint机制 — 提升描述质量
3. 增加 `image_ocr` 工具 — 补齐OCR专用场景

### 第二阶段（体验优化）
4. 批量图片处理
5. 持久化磁盘缓存
6. 自动调用规则注入

### 第三阶段（生态扩展）
7. PDF/文档解析
8. 配置文件支持
9. Web监控仪表盘

---

## 五、Fork策略建议

**方案A：直接Fork luma-mcp，在此基础上开发**
- 优点：完整代码基础，省大量时间
- 缺点：需要跟进上游更新

**方案B：基于luma-mcp的思想，重新构建精简版**
- 优点：代码更干净，可以只保留需要的功能
- 缺点：工作量更大

**推荐方案A** — Fork luma-mcp，按上述优先级逐步增强，同时保持与上游的兼容性。
