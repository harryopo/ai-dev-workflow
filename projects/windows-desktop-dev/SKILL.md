---
name: windows-desktop-dev
description: |
  Windows 桌面应用开发助手。当用户提到"开发桌面应用"、"做桌面软件"、
  "Windows应用"、"桌面程序"、"做个exe"、"桌面工具"时触发。
  分析用户需求，结合知识库给出最优架构和算法方案，AI 全程负责代码编写。
argument-hint: "[应用功能描述]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Bash
---

# Windows 桌面应用开发助手

帮助用户开发 Windows 桌面应用。AI 会分析用户需求，结合知识库给出最优架构和算法方案。

## 核心原则

> **先分析需求，再选择架构，最后写代码。** 不要一上来就写代码，先搞清楚用户要什么。

## 触发条件

> 触发词已在 description 中定义，此处不重复。

### 模糊匹配
- 用户想做一个在 Windows 上运行的软件
- 用户提到"本地运行"、"不需要联网"的应用
- 用户想把 Python 脚本做成有界面的程序

### 不触发条件
- 用户想做网页应用（应使用前端 Skill）
- 用户想做手机应用（应使用移动端 Skill）
- 用户只是问技术问题，不是要做应用

## 工作流程

### 第一步：需求分析（必须先做）

**不要跳过这一步！** 先问用户以下问题：

1. **功能需求**
   - 这个软件用来做什么？
   - 需要哪些核心功能？
   - 有没有优先级？

2. **数据需求**
   - 需要保存数据吗？
   - 数据量大概多大？
   - 需要搜索/排序/过滤吗？

3. **界面需求**
   - 界面有什么特殊要求？
   - 需要哪些交互方式？
   - 有没有参考的软件？

4. **性能需求**
   - 需要处理大量数据吗？
   - 需要多线程处理吗？
   - 对响应速度有要求吗？

**输出**：一份需求清单，让用户确认。

### 第二步：架构选择（用户决定）

根据需求分析，向用户推荐合适的架构：

#### 架构选项

| 架构 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **MVC** | 简单应用 | 结构清晰，易于理解 | 复杂应用会臃肿 |
| **MVVM** | 数据绑定多的应用 | 界面和逻辑分离好 | 学习成本高 |
| **MVP** | 需要测试的应用 | 易于单元测试 | 代码量较大 |
| **分层架构** | 复杂业务逻辑 | 职责清晰，可扩展 | 初期开发慢 |

**向用户解释每种架构，让用户选择。**

#### 架构选择决策树

```
用户需求复杂度？
├── 简单（1-3个功能）→ MVC
├── 中等（4-10个功能）→ MVP 或 MVVM
└── 复杂（10+功能）→ 分层架构

需要数据绑定？
├── 是 → MVVM
└── 否 → MVC 或 MVP

需要单元测试？
├── 是 → MVP
└── 否 → MVC
```

### 第三步：算法选择（按需）

根据功能需求，选择合适的算法：

#### 常见算法场景

| 场景 | 推荐算法 | 参考资料 |
|------|----------|----------|
| 搜索 | 二分查找、全文搜索 | ${CLAUDE_SKILL_DIR}/references/algorithms.md |
| 排序 | 快速排序、归并排序 | ${CLAUDE_SKILL_DIR}/references/algorithms.md |
| 数据验证 | 正则表达式 | ${CLAUDE_SKILL_DIR}/references/algorithms.md |
| 加密 | hashlib、cryptography | ${CLAUDE_SKILL_DIR}/references/algorithms.md |
| 压缩 | zlib、zipfile | ${CLAUDE_SKILL_DIR}/references/algorithms.md |
| 图像处理 | Pillow | ${CLAUDE_SKILL_DIR}/references/algorithms.md |

**只在需要时才引入算法，不要过度设计。**

### 第四步：创建项目结构

根据选择的架构，创建对应的项目结构：

#### MVC 架构结构
```
my-app/
├── main.py              # 入口文件
├── models/              # 数据模型
│   └── user.py
├── views/               # 界面
│   └── main_window.py
├── controllers/         # 控制器
│   └── app_controller.py
├── services/            # 业务逻辑
├── utils/               # 工具函数
├── data/                # 数据存储
├── CLAUDE.md            # 项目说明
└── requirements.txt     # 依赖清单
```

#### MVVM 架构结构
```
my-app/
├── main.py              # 入口文件
├── models/              # 数据模型
│   └── user.py
├── views/               # 界面（XAML 或 Python）
│   └── main_window.py
├── viewmodels/          # 视图模型
│   └── main_viewmodel.py
├── services/            # 业务逻辑
├── utils/               # 工具函数
├── data/                # 数据存储
├── CLAUDE.md            # 项目说明
└── requirements.txt     # 依赖清单
```

### 第五步：编写代码

按照选择的架构，逐层编写代码：

1. **Models 层** — 数据结构和数据库操作
2. **Services 层** — 业务逻辑
3. **Views 层** — 界面设计
4. **Controllers/ViewModels 层** — 连接界面和业务逻辑
5. **main.py** — 入口文件

**参考资料**：
- PySide6 开发指南：${CLAUDE_SKILL_DIR}/references/pyside6-guide.md
- 架构设计指南：${CLAUDE_SKILL_DIR}/references/architecture.md
- 算法参考：${CLAUDE_SKILL_DIR}/references/algorithms.md

### 第六步：测试运行

1. 安装依赖：`pip install -r requirements.txt`
2. 运行程序：`python main.py`
3. 让用户测试并反馈问题

### 第七步：迭代优化

1. 根据用户反馈修改代码
2. 重复测试直到满意

### 第八步：打包发布

1. 安装打包工具：`pip install pyinstaller`
2. 打包命令：`pyinstaller --onefile --windowed --name AppName main.py`
3. 参考资料：${CLAUDE_SKILL_DIR}/references/packaging-guide.md

## 输入规范

### 必需输入
- 功能描述：用户想要什么功能的软件
- 项目目录：在哪里创建项目

### 可选输入
- 架构偏好：用户喜欢哪种架构（缺省时根据复杂度推荐）
- 算法需求：是否有特殊算法需求（缺省时不引入复杂算法）
- 界面要求：颜色、布局等（缺省时使用默认样式）

### 缺材料时
- 如果用户没说清楚功能，追问具体需求
- 如果用户没指定目录，问"在哪里创建项目？"
- 如果用户不确定架构，解释各架构优缺点让用户选择

## 输出规范

### 输出格式
- Python 代码文件（.py）
- 项目结构目录
- 可执行文件（.exe）

### 输出位置
- 所有文件保存在用户指定的项目目录中
- 不要保存到其他位置

### 输出模板
```
my-app/
├── main.py              # 入口文件
├── models/              # 数据模型
├── views/               # 界面
├── controllers/         # 控制器（MVC）或 viewmodels（MVVM）
├── services/            # 业务逻辑
├── utils/               # 工具函数
├── data/                # 数据存储
├── CLAUDE.md            # 项目说明
└── requirements.txt     # 依赖清单
```

## 参考资料

- PySide6 开发指南：${CLAUDE_SKILL_DIR}/references/pyside6-guide.md
- 架构设计指南：${CLAUDE_SKILL_DIR}/references/architecture.md
- 算法参考：${CLAUDE_SKILL_DIR}/references/algorithms.md
- 常见错误解决方案：${CLAUDE_SKILL_DIR}/references/common-errors.md
- 打包指南：${CLAUDE_SKILL_DIR}/references/packaging-guide.md
- 评测集：${CLAUDE_SKILL_DIR}/evals/evals.json（8 条：5 core + 1 boundary + 2 edge）

## 注意事项

### 必须遵守
- 先分析需求，再选择架构，最后写代码
- 所有文件保存在用户指定的项目目录中
- 使用 os.path 处理路径，不要硬编码绝对路径
- 每个文件不超过 300 行
- 使用中文注释
- 捕获可能的异常，给用户友好提示

### 禁止行为
- 不要跳过需求分析直接写代码
- 不要在不了解需求的情况下选择架构
- 不要引入不需要的复杂算法
- 不要在主线程执行耗时操作（会卡死界面）
- 不要硬编码资源文件路径（打包后会找不到）
- 不要忽略错误处理（会导致程序闪退）

## 示例

### 输入示例
用户："帮我开发一个记账软件，能记录每天的收入和支出"

### 期望输出
1. 需求分析：问清楚需要哪些功能（添加记录、查看统计、导出数据等）
2. 架构推荐：推荐 MVC 或 MVVM 架构
3. 创建项目结构
4. 编写代码
5. 测试运行
6. 打包发布

### 反例：不该触发的情况
- "Python 怎么做加法？" — 这是问技术问题，不是要做应用
- "帮我写个网页" — 这是网页开发，不是桌面应用
- "这个代码报错了" — 这是调试问题，不是开发新应用

## 失败处理

| 失败类型 | 表现 | 修复动作 |
|----------|------|----------|
| 需求不清 | 用户说"随便" | 追问具体功能 |
| 架构选择错误 | 代码臃肿难维护 | 重构为合适的架构 |
| 依赖缺失 | ModuleNotFoundError | 自动安装缺失依赖 |
| 路径错误 | 打包后找不到资源 | 使用 get_resource_path() 函数 |
| 界面卡死 | 点击按钮无响应 | 使用多线程处理耗时操作 |
| 打包失败 | PyInstaller 报错 | 参考 packaging-guide.md 解决 |

**连续失败 3 次应停下来问用户，不要无限重试。**

## Gotchas

### G1: 看起来像但不该触发
- 用户说"帮我看看这段代码"是调试，不是开发新应用
- 判断依据：是否明确说要做一个"新软件"或"新应用"

### G2: 容易误用的工具
- 不要用 Write 直接覆盖用户已有的文件，先用 Edit 做 diff
- 打包前先确认用户已经测试通过

### G3: 连续失败时停止
- 如果连续 3 次运行都报错，停下来问用户是否要换个方案

### G4: 需求分析不能跳过
- 不要因为用户说"随便"就跳过需求分析
- 至少问清楚：做什么、存什么数据、界面要求

### G5: 架构选择要用户决定
- 不要擅自选择架构，要向用户解释各架构优缺点
- 让用户做出选择，或者确认推荐的架构
