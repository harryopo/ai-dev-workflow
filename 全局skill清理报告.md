# 全局 Skill 清理报告（2026-09-06）

> 只分析，未删除任何文件。

## 一、总体状况

| 位置 | 数量 | 磁盘 | 说明 |
|---|---|---|---|
| `C:\Users\Administrator\.zcode\skills` | 390 | 349 MB | 主目录 |
| `C:\Users\Administrator\.agents\skills` | 390 | 349 MB | 与主目录**逐目录完全相同** |
| `D:\ai\claude code\skill开发\.agents\skills` | 294 | 30 MB | 上面两者的**纯子集**，无任何独有 skill |

- 三处都是真实目录（非软链接），每个 skill 实际存了 2~3 份。
- 每次会话，390 个 skill 的「名称+描述」会以 3 份副本进入上下文（约 1170 条目），这是最大的上下文负担。
- 全部 SKILL.md 正文合计约 **4.8 MB**。单文件最大：`last30days` 190 KB、`claude-api` 73 KB、`ai-dev-workflow` 64 KB、`harryopo-office` 48 KB、`ui-ux-pro-max` 44 KB。

## 二、第 0 层：结构性重复（收益最大，无争议）

- 删除 `C:\Users\Administrator\.agents\skills` 整个目录 → 省 349 MB，上下文 skill 列表降为 1/3。
- 删除项目内 `D:\ai\claude code\skill开发\.agents\skills` → 再省 30 MB。
  ⚠️ 唯一注意点：这个项目本身就是 skill 开发工作区，若你的流程是"项目级 skill 用于本地测试"，可以保留项目级、只删 `~\.agents`。

## 三、第 1 层：确定的垃圾（18 个，建议直接删）

**备份/草稿/同名冲突：**
- `harryopo-office.bak-20260902`（9月2日备份残留，且被当作独立 skill 加载）
- `待优化skill`（idea-to-dev 的旧草稿，同名注册冲突）
- `mineru-document-extractor`（与 `mineru` 注册名完全相同 "MinerU Document Extractor"，二选一，留 `mineru`）
- `composition-patterns`（注册名 vercel-composition-patterns，与 `vercel-composition-patterns` 目录撞名）
- `react-native-skills`（注册名 vercel-react-native-skills，同样撞名）
- `template-skill`（0.1 KB 模板残根）

**空壳存根（<2 KB，无实质内容）：**
`zoom-out`、`grill-me`、`edit-article`、`superpowers-lab`、`defuddle`、`internal-comms`、`obsidian-vault`、`sciverse`、`web-design-guidelines`、`writing-guidelines`

**与已装插件重复：**
- `github`、`gh-cli`（已装官方 github 插件，含 commit/pr/issue/release/repo/gist/codespace/secret/workflow-run/setup 全套）

## 四、第 2 层：按工作范围整类删（大头在这里，约 120 个 / 1.6 MB）

### A. 区块链/加密审计（13 个，168 KB）
`algorand-vulnerability-scanner`、`cairo-vulnerability-scanner`、`cosmos-vulnerability-scanner`、`solana-vulnerability-scanner`、`substrate-vulnerability-scanner`、`ton-vulnerability-scanner`、`defi-protocol-templates`、`nft-standards`、`solidity-security`、`token-integration-analyzer`、`risk-metrics-calculation`、`vector-forge`、`mermaid-to-proverif`

### B. 二进制安全 / Fuzzing（21 个，280 KB）
`aflpp`、`libafl`、`libfuzzer`、`cargo-fuzz`、`ossfuzz`、`atheris`、`ruzzy`、`fuzzing-dictionary`、`fuzzing-obstacles`、`dwarf-expert`、`memory-forensics`、`yara-rule-authoring`、`anti-reversing-techniques`、`binary-analysis-patterns`、`address-sanitizer`、`protocol-reverse-engineering`、`burpsuite-project-parser`、`firebase-apk-scanner`、`sarif-parsing`、`variant-analysis`、`entry-point-analyzer`

### C. 安全合规 / 密码学（21 个，355 KB）
`constant-time-analysis`、`constant-time-testing`、`wycheproof`、`zeroize-audit`、`stride-analysis-patterns`、`pci-compliance`、`gdpr-data-handling`、`threat-mitigation-mapping`、`attack-tree-construction`、`security-requirement-extraction`、`crypto-protocol-diagram`、`memory-safety-patterns`、`seatbelt-sandboxer`、`secrets-management`、`supply-chain-risk-auditor`、`fp-check`、`genotoxic`、`codeql`、`semgrep`、`semgrep-rule-creator`、`semgrep-rule-variant-creator`
（`security-best-practices`、`insecure-defaults`、`secure-workflow-guide` 偏通用开发安全，可留可删）

### D. 公司/产品定制（19 个，204 KB）—— 非对应公司/产品就用不到
- 非腾讯系：`byted-bp-cdn-pagesdeploy`、`byted-seedream-image-generate`、`mtunion-product-ai-guide`、`meituan-travel`、`dashi-ppt`、`luma-vision-mcp`、`tikhub-api-helper`、`modlens`、`weread-skills`、`wechatide-skill`、`wecom-weisheng-scrm`、`bdpan-storage`、`cloud-upload-backup`、`miniprogram-report-screenshots`
- 腾讯系（你装了 CloudBase 插件，可能真在用，自行取舍）：`tencent-docs`、`tencent-esign-contract`、`tencent-meeting-mcp`、`tencent-survey`、`kdocs`
- 飞书系（同理）：`lark-doc`、`lark-shared`、`lark-whiteboard`、`feishu-business-diagram`、`feishu-cli-whiteboard-draw`、`project-arch-to-feishu`

### E. 冷门技术栈/基础设施（45 个，551 KB）
- 框架/中间件：`airflow-dag-patterns`、`dbt-transformation-patterns`、`bazel-build-optimization`、`istio-traffic-management`、`linkerd-patterns`、`helm-chart-scaffolding`、`godot-gdscript-patterns`、`unity-ecs-patterns`、`spark-optimization`、`temporal-python-testing`、`remotion-best-practices`、`electron`、`dotnet-backend-patterns`、`backtesting-frameworks`
- K8s/云/可观测：`k8s-manifest-generator`、`k8s-security-policies`、`terraform-module-library`、`hybrid-cloud-networking`、`multi-cloud-architecture`、`grafana-dashboards`、`prometheus-configuration`、`distributed-tracing`、`service-mesh-observability`、`slo-implementation`、`mtls-configuration`、`incident-runbook-templates`、`on-call-handoff-patterns`、`gitops-workflow`、`gitlab-ci-patterns`
- 前端工程化（若不碰 monorepo 可删）：`nx-workspace-patterns`、`monorepo-management`、`turborepo-caching`
- AI/数据类（若不做 RAG/ML 可删）：`rag-implementation`、`embedding-strategies`、`hybrid-search-implementation`、`similarity-search-patterns`、`vector-index-tuning`、`langchain-architecture`、`llm-evaluation`、`ml-pipeline-workflow`、`data-quality-frameworks`

### F. 书籍方法论/心理自助/商业咨询（22 个，237 KB）
- 书籍类：`cognitive-awakening`、`courage-to-be-disliked`、`power-of-now`、`another_them`、`let-fate-decide`、`persona-switch`、`book-methodology-skills`、`fbs_bookwriter`、`caveman`、`interpreting-culture-index`
- 商业/咨询：`market-sizing-analysis`、`competitive-landscape`、`startup-financial-modeling`、`startup-metrics-framework`、`kpi-dashboard-design`、`cost-optimization`、`billing-automation`、`employment-contract-templates`、`data-storytelling`、`audit-prep-assistant`、`audit-augmentation`、`audit-context-building`

### G. 其他长尾（按需）
- 笔记工具：`obsidian-bases`、`obsidian-cli`、`obsidian-markdown`（不用 Obsidian 就删）
- 支付：`paypal-integration`、`stripe-integration`
- 生活：`travel-photo-planner`、`meituan-travel`
- 杂项评估：`db-homework-agent`、`scaffold-exercises`、`debug-buttercup`、`dogfood`、`sharp-edges`、`hyperframes`、`bilingual-diagram`、`slack-gif-creator`

## 五、第 3 层：同类近义重复 —— 每组只留一个

| 组 | 成员 | 建议 |
|---|---|---|
| 代码审查 | `code-review` / `code-review-excellence` / `differential-review` | 留 `code-review` |
| TDD | `tdd` / `test-driven-development` | 留一个 |
| 图表生成 | `diagram-design`(40K) / `diagram-skill` / `diagramming-code` / `super-diagram` / `flowchart-generator` | 留 `diagram-design`，其余删 |
| 前端设计 | `frontend-design` / `frontend-skill` / `super-frontend-design`(36K) / `ui-ux-pro-max`(44K) / `impeccable` | 留 1 个主用的 |
| TypeScript | `typescript` / `typescript-advanced-types` | 视情况合并 |
| Supabase | `supabase` / `supabase-postgres-best-practices` | 用 CloudBase 则都可删 |
| Office 文档 | `docx`/`pdf`/`pptx`/`xlsx` 手动版 vs 官方 document-skills 插件版 vs `office-document-suite` | ⚠️ 先确认 `harryopo-office` 是否依赖本地版再删 |
| 文档提取 | `mineru` / `mineru-document-extractor` | 已在第 1 层处理 |

## 六、第 4 层：大块头单点评估（上下文大户）

| Skill | 大小 | 说明 |
|---|---|---|
| `last30days` | **190 KB** | 单个最大，若不常用，删它一个顶删几十个小 skill |
| `claude-api` | 73 KB | 做 LLM/skill 开发有用，但注意它有强触发词（凡提到 Claude/LLM 就加载） |
| `ai-dev-workflow` | 64 KB | 评估实际使用频率 |
| `ui-ux-pro-max` | 44 KB | 与其他前端设计 skill 重复，二选一 |
| `harryopo-office` | 48 KB | 自用核心，保留 |

## 七、保留白名单（建议不动）

- **Skill 开发工具链**：`skill-creator`、`skill-dev`、`skill-workspace`、`skill-improver`、`skill-review`、`write-a-skill`、`designing-workflow-skills`、`harness-writing`、`mcp-builder`、`find-skills`
- **研究/文档**：`deep-research-ultra`、`oss-finder`、`doc-coauthoring`、`latex-writer`、`paper-style-polish`、`thesis-figure-skill`、`doc-html-pdf`、`mineru`、`harryopo-office`、`office-document-suite`
- **Agent/浏览器**：`agent-browser`、`local-computer-use`、`screenshot`、`chrome-mcp-troubleshooting`、`context7`
- **工作流**：`brainstorming`、`writing-plans`、`executing-plans`、`systematic-debugging`、`verification-before-completion`、`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`
- **Git/GitHub 流程**：`git-commit`、`git-cleanup`、`git-advanced-workflows`、`github-actions-templates`、`github-deploy`、`github-triage`、`finishing-a-development-branch`、`to-issues`、`to-prd`、`triage-issue`、`changelog-automation`、`dependency-upgrade`
- **Python 全家桶（15 个，191 KB）**：你在用 Python（deep-research-ultra），建议整体保留
- **按你实际技术栈保留的前端族**：Next/React 系（`nextjs-app-router-patterns`、`react-state-management`、`tailwind-design-system` 等按项目需要留 3~5 个）

## 八、预期效果

| 指标 | 现状 | 清理后（保守估计） |
|---|---|---|
| Skill 数量 | 390 × 3 副本 | ~120 × 1 副本 |
| 上下文 skill 列表 | ~1170 条目 | ~120 条目（降 ~90%） |
| 磁盘 | 728 MB | ~40-60 MB |

执行顺序建议：第 0 层 → 第 1 层 → 第 2 层中你确认不做的整类 → 第 3 层合并 → 第 4 层逐个判断。删除前可将整批移入一个 `_trash` 目录观察两周再真删。
