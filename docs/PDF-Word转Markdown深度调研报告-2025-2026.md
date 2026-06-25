# PDF/Word 转 Markdown 深度调研报告（2025-2026）

*生成日期: 2026-06-20 | 来源: 25+ | 可信度: 高*

---

## 执行摘要

2025-2026年，文档转Markdown领域经历了从"规则提取"到"VLM端到端理解"的范式转移。**MinerU 3.3.x**（上智实验室）以高精度中文解析和109语言OCR成为综合最强开源方案；**Marker**（EndlessAI）以25页/秒的H100吞吐量成为速度之王；**Docling**（IBM/Linux Foundation）以MIT许可和40M+下载量成为企业RAG首选；**MarkItDown**（微软）以126K+ Star和20+格式覆盖成为轻量级通用转换器。VLM架构（如Granite Docling、DeepSeek-OCR 2、HunyuanOCR）正在取代传统OCR管线，实现端到端文档理解。RAG场景下，结构感知的自适应切分（Adaptive Chunking）成为新趋势，而非一刀切的固定窗口。

---

## 一、PDF 转 Markdown 工具深度对比

### 1.1 MinerU（magic-pdf）— 高精度中文文档解析专家

| 维度 | 详情 |
|------|------|
| **开发者** | 上海人工智能实验室 OpenDataLab |
| **最新版本** | 3.3.1（2026年6月） |
| **GitHub Star** | 62,000+ |
| **许可证** | MinerU Open Source License（代码友好，模型含AGPL） |
| **Python** | 3.10-3.13 |
| **核心架构** | VLM+OCR 双引擎，版面检测+OCR+表格+公式多模型管线 |
| **输入格式** | PDF、DOCX、PPTX、XLSX、图片、网页 |
| **输出格式** | Markdown、JSON、HTML、LaTeX |
| **OCR语言** | 109种语言 |
| **部署方式** | CLI、Python SDK、Web UI、桌面客户端、Docker、API |

**核心优势**：
- 公式识别准确率92.5%，支持复杂长数学公式，行内/行间公式含序号识别
- 表格解析业界领先：旋转表格、无边框/半边框表格、跨页表格、表格内图片/公式
- 印章文字识别（中国文档圆形印章）、竖排文本支持
- 2.0版本彻底移除PyMuPDF依赖，自动模型管理，开箱即用
- 3.x版本新增DOCX/PPTX/XLSX原生支持、MCP Server、LangChain/Dify/FastGPT集成
- 单卡4090 + sglang加速，峰值吞吐超10,000 tokens/s

**不足**：
- GPU推荐（8GB+显存），纯CPU模式较慢
- 模块化程度不如Docling开放，替换特定OCR引擎不够灵活
- 安装包较大（含多个模型权重）

### 1.2 Marker（marker-pdf）— 轻量快速PDF转Markdown

| 维度 | 详情 |
|------|------|
| **开发者** | Vik Paruchuri → EndlessAI |
| **最新版本** | 持续更新中 |
| **核心架构** | PyMuPDF + Surya OCR + 深度学习布局分析 |
| **输出格式** | Markdown、JSON、HTML、Chunks |
| **许可证** | GPL代码 + Open RAIL-M模型权重（商用需授权） |

**核心优势**：
- H100批处理25页/秒，单页约0.6秒，速度4-10x于Nougat
- 安装简单，VRAM占用低（8GB推荐）
- 公式自动转LaTeX，图片内嵌保存
- 支持LLM增强模式优化复杂表格

**不足**：
- 中文等复杂字符集原生支持弱（早期版本明确不支持CJK）
- 复杂布局解析能力弱于MinerU/Docling
- GPL许可证商业使用需额外授权
- 表格处理相对较弱

### 1.3 Docling（IBM）— 企业级多格式文档流水线

| 维度 | 详情 |
|------|------|
| **开发者** | IBM苏黎世研究院 → Linux Foundation AI & Data |
| **最新版本** | v2+（持续更新） |
| **GitHub Star** | 10K+（上线一个月即达） |
| **PyPI下载** | 40M+，日下载50万+ |
| **许可证** | MIT（最宽松） |
| **核心架构** | DocLayNet布局分析 + TableFormer表格识别 + 多OCR引擎 |
| **输入格式** | PDF、DOCX、PPTX、XLSX、HTML、Markdown、LaTeX、JATS、USPTO专利、XBRL、图片、音频、视频 |
| **输出格式** | Markdown、JSON、HTML |
| **企业服务** | Docling for IBM watsonx（$4/1000页，托管服务） |

**核心优势**：
- MIT许可证，企业集成无法律风险
- 统一DoclingDocument中间格式，支持格式互转
- TableFormer表格识别TEDS评分93.6%，复杂表格单元格准确率97.9%
- DocLayNet识别11类文档元素
- LangChain、LlamaIndex、spaCy原生集成
- Granite Docling VLM模型（258M参数，Apache 2.0）实现端到端文档理解
- 完全本地运行，适配涉密场景

**不足**：
- 中文支持标注为"实验性"，多语言未企业级验证
- 处理速度较慢（约0.25页/秒）
- 在特定高难度任务（复杂公式、扫描件OCR）上不及专门优化工具
- 最低32GB内存推荐

### 1.4 Pandoc — 通用文档转换瑞士军刀

| 维度 | 详情 |
|------|------|
| **开发者** | John MacFarlane（2006年至今） |
| **许可证** | GPL |
| **PDF转MD能力** | 有限，需配合pdftotext |

**PDF场景评价**：
- PDF转MD不是Pandoc强项，需先pdftotext提取再转换
- 代码块语言标注丢失，表格转为空格对齐纯文本
- 30页文档约10秒，速度快但质量差
- 适合纯文本简单文档，复杂PDF不推荐

### 1.5 pdfplumber + 自定义提取 — 灵活度最高

| 维度 | 详情 |
|------|------|
| **核心能力** | 表格提取TEDS 93.4%（PDFBench最高） |
| **适用场景** | 需要精细控制提取逻辑的开发者 |

**评价**：
- 表格提取精度在所有工具中最高
- 但整体编辑相似度仅70.4%（PDFBench数据）
- 需要大量自定义代码，不适合通用场景
- 适合特定文档类型的批量处理

### 1.6 LlamaParse — 云端方案

| 维度 | 详情 |
|------|------|
| **开发者** | LlamaIndex |
| **模式** | Fast(1积分/页)、Balanced(10积分)、Premium(45积分)、Agentic Plus(90积分) |
| **编辑相似度** | 约78%（与开源领先者持平） |
| **成本** | $0.003/页 |

**评价**：
- 与开源领先者精度持平，但需付费
- 被批评为"LLM的中间件包装"，现代VLM可直接处理文档
- 存在Bug（如v0.6.1原始OCR问题）
- 适合已使用LlamaIndex生态的团队

### 1.7 Mathpix — 学术论文场景王者

| 维度 | 详情 |
|------|------|
| **核心能力** | 公式识别精度业界最高 |
| **成本** | $0.01-0.05/页 |
| **最新动态** | 2026年持续更新，SuperNet-109p7模型 |

**评价**：
- 数学公式识别无出其右，支持多行显示公式
- 输出Mathpix Markdown（MMD）格式，支持LaTeX/DOCX/HTML多格式导出
- 2026年新增：页内断点标记、使用量告警、MathML输出等
- 纯云端服务，成本较高
- 学术论文、数学教材首选

### 1.8 Nougat（Meta）— 学术论文专用

| 维度 | 详情 |
|------|------|
| **开发者** | Meta AI |
| **架构** | Vision Transformer |
| **速度** | ~30秒/页（需6GB+ GPU VRAM） |

**评价**：
- 专为arXiv论文设计，LaTeX文档表现优秀
- 速度慢（Marker的4-10倍差距）
- 长文档容易产生幻觉
- 泛化能力弱于Marker/MinerU
- 适合纯学术场景，不推荐通用

### 1.9 新兴VLM方案

| 工具 | 开发者 | 参数量 | 特点 |
|------|--------|--------|------|
| **Granite Docling** | IBM | 258M | 端到端VLM，DocTags标记语言，Apache 2.0 |
| **DeepSeek-OCR 2** | DeepSeek | - | 因果流查询机制，OCR 2.0代表 |
| **HunyuanOCR** | 腾讯 | 1B | ICDAR 2025 DIMT冠军，强化学习优化 |
| **PaddleOCR-VL-1.5** | 百度 | - | 开源SOTA，异形框定位领先 |
| **Nemotron Parse 1.1** | NVIDIA | - | VLM架构，保留布局+阅读顺序 |

---

## 二、Word 转 Markdown 工具深度对比

### 2.1 Pandoc — DOCX转MD的最佳实践

| 维度 | 详情 |
|------|------|
| **地位** | Word转Markdown的金标准 |
| **推荐命令** | `pandoc input.docx -t gfm --wrap=none --extract-media=./media -o output.md` |

**核心优势**：
- 20年持续开发，最成熟的文档转换工具
- 支持格式最多（Word/HTML/LaTeX/Markdown/RST/AsciiDoc/ODT/ePub/JATS等）
- 标题、列表、链接、表格、代码块、脚注、图片均可保留
- `--extract-media`提取图片到本地目录
- `--reference-doc`支持自定义模板
- 批量转换脚本10行即可实现

**不足**：
- 复杂表格（合并单元格）转换不佳
- 自定义字体/颜色/文本框/形状丢失
- 需安装Haskell运行时
- 输出有时冗余

### 2.2 mammoth — JS语义方案

| 维度 | 详情 |
|------|------|
| **语言** | JavaScript（有Python移植） |
| **核心哲学** | 语义样式映射，忽略视觉格式 |
| **输出** | HTML优先，Markdown需二次转换 |

**核心优势**：
- 纯Python/JS实现，无需外部依赖
- 可配置样式映射（style map），对模板化文档精度最高
- 输出干净的语义HTML

**不足**：
- HTML-first设计，Markdown是下游转换
- 复杂表格/样式转换不完美
- 图片以Base64嵌入Markdown
- 不如Pandoc全面

### 2.3 MarkItDown（Microsoft）— 轻量级万能转换器

| 维度 | 详情 |
|------|------|
| **开发者** | 微软 AutoGen 团队 |
| **GitHub Star** | 126,884+（2026年5月） |
| **最新版本** | v0.1.6（2026年5月27日） |
| **许可证** | MIT |
| **PyPI周下载** | 150万+ |
| **支持格式** | 20+种（PDF/DOCX/PPTX/XLSX/图片/音频/HTML/CSV/JSON/XML/ZIP/YouTube/EPub等） |

**核心优势**：
- 格式覆盖面最广，"万物皆可Markdown"
- MIT许可证，免费可商用
- 极简安装：`pip install markitdown[all]`
- CLI/Python API/Docker/VS Code插件/MCP Server多种使用方式
- 设计理念：保留对LLM有用的结构信息，Token效率高
- 插件架构，可扩展自定义格式处理器

**不足**：
- PDF解析基于PDFMiner，精度不如MinerU/Marker/Docling
- 表格识别一般（简单表格或纯文本，样式丢失）
- 公式处理弱
- 不导出图片（仅占位符）
- 发布节奏慢（v0.1.5到v0.1.6间隔3个月+）
- MCP Server仍为alpha版本

### 2.4 python-docx + 自定义提取

**评价**：
- 完全控制提取逻辑，灵活度最高
- 需要大量自定义代码处理样式、表格、图片
- 适合特定模板的批量处理
- 不适合通用场景

### 2.5 docx2python

**评价**：
- 提取DOCX中所有文本内容，包括页眉页脚
- 输出为纯文本，丢失格式信息
- 适合只需要文本内容的场景

---

## 三、关键能力对比维度

### 3.1 综合对比表

| 能力维度 | MinerU 3.x | Marker | Docling | MarkItDown | Pandoc | Mathpix | LlamaParse |
|----------|-----------|--------|---------|------------|--------|---------|------------|
| **表格识别** | ⭐⭐⭐⭐⭐ HTML嵌入 | ⭐⭐⭐ MD表格 | ⭐⭐⭐⭐⭐ TEDS 93.6% | ⭐⭐ 简单表格 | ⭐⭐⭐ 基本表格 | ⭐⭐⭐⭐ 优秀 | ⭐⭐⭐ 良好 |
| **数学公式** | ⭐⭐⭐⭐⭐ 92.5% | ⭐⭐⭐⭐ 优秀 | ⭐⭐⭐ 良好 | ⭐⭐ 一般 | ⭐⭐ 基础 | ⭐⭐⭐⭐⭐ 业界最佳 | ⭐⭐⭐ 良好 |
| **图片提取** | ⭐⭐⭐⭐⭐ 导出+描述 | ⭐⭐⭐⭐ 高清保存 | ⭐⭐⭐⭐ 提取+关联 | ⭐ 仅占位符 | ⭐⭐⭐ 提取到目录 | ⭐⭐⭐⭐ 完整 | ⭐⭐⭐ 良好 |
| **中文支持** | ⭐⭐⭐⭐⭐ 专为中文优化 | ⭐⭐ CJK弱 | ⭐⭐ 实验性 | ⭐⭐⭐ 基本支持 | ⭐⭐⭐ 基本支持 | ⭐⭐⭐ 良好 | ⭐⭐⭐ 良好 |
| **批量处理** | ⭐⭐⭐⭐ CLI/API | ⭐⭐⭐⭐⭐ 25页/秒 | ⭐⭐⭐ 批量API | ⭐⭐⭐ CLI/API | ⭐⭐⭐⭐⭐ 脚本化 | ⭐⭐⭐ API | ⭐⭐⭐ API |
| **本地运行** | ✅ 完全本地 | ✅ 完全本地 | ✅ 完全本地 | ✅ 完全本地 | ✅ 完全本地 | ❌ 云端 | ❌ 云端 |
| **安装复杂度** | 中等（模型下载） | 简单 | 中等 | 极简 | 简单 | 无需安装 | 无需安装 |
| **输出纯度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **许可证** | 开源友好 | GPL/RAIL-M | MIT | MIT | GPL | 商业 | 商业 |
| **成本** | 免费 | 免费/商用付费 | 免费 | 免费 | 免费 | $0.01-0.05/页 | $0.003/页 |

### 3.2 Word转Markdown专项对比

| 能力维度 | Pandoc | mammoth | MarkItDown | python-docx |
|----------|--------|---------|------------|-------------|
| **标题层级** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ 需自定义 |
| **表格** | ⭐⭐⭐ 基本表格 | ⭐⭐ 简单表格 | ⭐⭐⭐ 基本表格 | ⭐⭐⭐ 需自定义 |
| **图片** | ⭐⭐⭐⭐ 提取到目录 | ⭐⭐ Base64嵌入 | ⭐⭐⭐ 提取 | ⭐⭐⭐ 需自定义 |
| **列表** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ 需自定义 |
| **链接** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ 需自定义 |
| **脚注** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| **安装** | 需安装Pandoc | 纯Python | pip一键 | 纯Python |
| **格式覆盖** | 数十种 | 仅DOCX→HTML | 20+种 | 仅DOCX |

---

## 四、行业趋势

### 4.1 VLM（视觉语言模型）在文档解析中的应用

2025-2026年，文档解析正经历从**OCR 1.0（模块化管线）** 到**OCR 2.0（VLM端到端）** 的范式转移：

**传统管线的局限**：
- 检测→识别→后处理的串联架构，错误逐级传播
- 复杂布局（多栏、公式、表格）结构信息丢失
- Unicode连字问题（U+FB01 "fi"）静默破坏关键词搜索

**VLM的优势**：
- 端到端架构：图像直接输入，结构化Markdown/LaTeX输出
- 原生布局理解：ViT视觉编码器捕获空间上下文
- 消除中间OCR层：避免"垃圾进、垃圾出"瓶颈
- 统一多任务：文本识别+布局分析+结构输出一步完成

**代表性VLM模型**：

| 模型 | 参数量 | 特点 | 许可证 |
|------|--------|------|--------|
| Granite Docling | 258M | DocTags标记，轻量端到端 | Apache 2.0 |
| DeepSeek-OCR 2 | - | 因果流查询，OCR 2.0代表 | 开源 |
| HunyuanOCR | 1B | ICDAR 2025冠军，RL优化 | 开源 |
| PaddleOCR-VL-1.5 | - | 异形框定位全球领先 | 开源 |
| Nemotron Parse 1.1 | - | NVIDIA VLM，语义分割 | 商业 |

**2026年核心技术趋势**：
1. 端到端VLM解析取代模块化流程
2. 强化学习用于布局建模（阅读顺序预测）
3. 小型化趋势（<1B参数的OCR专用VLM涌现）
4. "OCR-Free"端到端识别成为新标准

### 4.2 端到端文档理解方案

**从管线到一体化**：
- 传统：PDF→OCR→布局分析→结构提取→Markdown
- 新范式：PDF→VLM→Markdown（一步到位）

**Granite Docling的DocTags创新**：
- 专用标记语言DocTags，分离内容与布局
- 忠实保留表格、代码块、行内/块级数学公式、文档层级
- 258M参数即可达到生产级精度
- 支持transformers/vLLM/ONNX/MLX多种推理后端

**前沿LLM直接处理**：
- GPT-5.1：92%编辑相似度（视觉输入），但$0.05/页
- Gemini 3 Pro：88%编辑相似度
- Claude 4：原生PDF/图像输入，结构理解能力强
- 趋势：LLM本身正在成为文档解析器，但成本仍是瓶颈

### 4.3 RAG场景下的文档切分最佳实践

**核心发现**：同一解析器在不同文档类型上准确率差距可达49个百分点（PDFBench数据），切分策略同样如此。

**2025-2026年切分策略演进**：

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| **递归切分** | 按分隔符层级切分，工业界最通用 | 通用场景，LangChain默认 |
| **语义切分** | 基于embedding相似度在语义边界切分 | 高精度场景 |
| **结构感知切分** | 按Markdown标题/代码块/表格等原子单元切分 | 结构化文档 |
| **LGMGC** | 大粒度+小粒度双索引，检索小块返回大块 | 企业级RAG |
| **自适应切分** | 根据文档特征自动选择最优策略 | 2026年新趋势 |
| **MDKeyChunker** | 结构切分+单次LLM元数据增强+语义键重组 | 高精度RAG |

**关键最佳实践**：
1. **Markdown先于切分**：先用高质量工具转为Markdown，再基于结构切分
2. **原子单元不可拆**：标题、代码块、表格、列表作为原子单元保留
3. **元数据增强**：每个chunk附加章节标题、文档来源等上下文
4. **父子块策略**：检索细粒度小块，返回粗粒度父块
5. **动态overlap**：语义密度高的段落overlap 25-30%，低的5-10%
6. **Hybrid Search**：BM25 + 向量检索混合，Recall@5可达1.000

**Docling的RAG集成优势**：
- 原生支持HybridChunker，基于文档结构的智能切分
- 输出DoclingDocument可直接对接LlamaIndex/LangChain
- 保留表格、图片、公式的完整性，避免跨chunk断裂

---

## 五、推荐方案

### 5.1 按场景推荐

| 场景 | 推荐工具 | 理由 |
|------|----------|------|
| **中文学术论文/财务报表** | MinerU 3.x | 中文优化最强，表格/公式精度最高 |
| **英文科研文献批量处理** | Marker | 速度最快，公式/表格平衡好 |
| **企业RAG知识库** | Docling | MIT许可，结构保留最佳，生态集成 |
| **日常办公文档快速转换** | MarkItDown | 20+格式，极简安装，MIT免费 |
| **数学教材/公式密集文档** | Mathpix | 公式识别无出其右 |
| **Word文档转Markdown** | Pandoc | 金标准，最成熟可靠 |
| **涉密文档本地处理** | MinerU/Docling | 完全本地运行，数据不出本机 |
| **多格式一站式处理** | Docling/MarkItDown | 格式覆盖最广 |
| **预算有限的学术场景** | Marker/MinerU | 开源免费，精度够用 |

### 5.2 组合方案推荐

**高精度RAG管线**：
```
PDF/DOCX → MinerU/Docling → Markdown → 结构感知切分 → 向量数据库 → RAG
```

**快速批量处理管线**：
```
PDF → Marker → Markdown → 递归切分 → 向量数据库 → RAG
```

**企业级全格式管线**：
```
任意文档 → Docling → DoclingDocument → HybridChunker → LangChain/LlamaIndex → RAG
```

**Word专用管线**：
```
DOCX → Pandoc -t gfm → Markdown → 结构切分 → 知识库
```

---

## 六、关键要点

1. **VLM正在取代传统OCR管线**：端到端视觉理解消除了中间文本提取的精度损失，Granite Docling（258M参数）证明了轻量VLM也能达到生产级精度
2. **没有万能工具**：同一解析器在不同文档类型上准确率差距可达49个百分点，需根据文档类型选择
3. **MinerU是中文场景综合最优**：专为中文优化，表格/公式/印章/竖排文字全面领先
4. **Docling是企业RAG首选**：MIT许可+40M下载+LangChain/LlamaIndex集成+结构保留最佳
5. **MarkItDown是轻量级万能入口**：126K Star+20+格式+极简安装，适合快速原型和日常使用
6. **Pandoc仍是Word转MD金标准**：20年持续开发，`pandoc -t gfm`是最可靠的转换命令
7. **RAG切分比解析更重要**：结构感知切分+元数据增强可将RAG正确率从62%提升到72%
8. **成本与精度权衡**：GPT-5.1视觉输入92%精度但$0.05/页，LlamaParse 78%精度仅$0.003/页，开源方案免费但需GPU

---

## 来源

1. [MinerU 深度评测：2026年最强开源PDF解析引擎](https://juejin.cn/post/7643722505254076458) — MinerU 3.x功能矩阵与实战
2. [MinerU vs Docling vs Marker：开源文档解析工具深度对比](https://juejin.cn/post/7636666943860572170) — 三大工具全面对比
3. [mineru 3.3.0 on PyPI](https://pypi.org/project/mineru/3.3.0/) — MinerU最新版本信息
4. [Docling for IBM watsonx](https://www.ibm.com/new/announcements/docling-for-ibm-watsonx-turn-complex-documents-into-ai-ready-data) — Docling企业服务发布
5. [Docling Technical Report (AAAI 2025)](https://arxiv.org/pdf/2501.17887v1) — Docling架构与基准测试
6. [Granite Docling Model](https://www.ibm.com/granite/docs/models/docling) — IBM端到端VLM模型
7. [微软 MarkItDown 深度解析](https://juejin.cn/post/7644776565671165992) — MarkItDown 126K Star详解
8. [MarkItDown MCP Server Review](https://chatforest.com/reviews/markitdown-mcp-server/) — MCP集成评估
9. [PDF转Markdown技术方案对比（2026）](https://cloud.tencent.com/developer/article/2689893) — 在线/API/开源实测
10. [PDF Parsing for LLM Input](https://nbrosse.github.io/posts/pdf-parsing/pdf-parsing.html) — Docling/Marker/MinerU技术对比
11. [We Tested 17 PDF Parsers on 800 Documents](https://liveinthefuture.org/stories/pdf-to-markdown-conversion-token-formatting-benchmark) — PDFBench大规模基准
12. [PDF转Markdown：6种常用开源工具深度对比](https://blog.csdn.net/xuebinding/article/details/151101364) — 6工具实战对比
13. [深度调研开源PDF转Markdown工具](https://blog.csdn.net/weixin_38754564/article/details/151841757) — Dolphin/MarkItDown/MinerU/Marker对比
14. [VLM Now Outperform OCR in Complex Document Parsing](https://www.thenextgentechinsider.com/pulse/vision-language-models-now-outperform-ocr-in-complex-document-parsing) — VLM范式转移分析
15. [NVIDIA Nemotron Parse 1.1](https://developer.nvidia.com/blog/turn-complex-documents-into-usable-data-with-vlm-nvidia-nemotron-parse-1-1/) — NVIDIA VLM文档理解
16. [HunyuanOCR Technical Report](https://arxiv.org/html/2511.19575v1) — 腾讯1B参数OCR VLM
17. [OCR工具深度调研报告](https://blog.csdn.net/qq_41581588/article/details/159160751) — 2026年OCR趋势
18. [Adaptive Chunking (arXiv 2026)](https://arxiv.org/pdf/2603.25333) — 自适应切分框架
19. [MDKeyChunker (arXiv 2026)](https://arxiv.org/html/2603.23533v1) — Markdown结构切分+LLM增强
20. [RAG文档切分最佳实践](https://blog.csdn.net/qq_38646027/article/details/159795650) — 企业级方案+策略决策树
21. [Mammoth vs Pandoc vs AI](https://mdisbetter.com/blog/mammoth-vs-pandoc-vs-ai-word-conversion) — Word转MD三种架构对比
22. [Converting Word Documents to Markdown](https://markdownftw.com/blog/word-to-markdown) — Word↔Markdown完整指南
23. [Mathpix Changelog](https://mathpix.com/docs/convert/changelog) — Mathpix 2026年持续更新
24. [PDF to Markdown: 5 Proven Methods (2026)](https://macmdviewer.com/blog/pdf-to-markdown-converter) — 5种方法实测
25. [PDF转Markdown完全指南（2026）](https://markdownconverter.pro/zh/blog/pdf-to-markdown-guide) — RAG就绪工作流

---

## 方法论

在 25+ 个查询中搜索了 web（百度、必应、Google、DuckDuckGo等）。分析了 25+ 个来源，包括学术论文（AAAI/arXiv）、技术博客（掘金/CSDN/IBM Blog）、基准测试（PDFBench）、官方文档（PyPI/GitHub）和行业报告。研究的子问题：PDF转MD工具对比、Word转MD工具对比、关键能力维度、VLM趋势、RAG切分实践。
