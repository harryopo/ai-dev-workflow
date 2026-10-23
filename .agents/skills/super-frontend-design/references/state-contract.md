# 状态契约（State Contract）— 把"页面在什么情况下会怎样"变成可校验的字段

> **为什么存在**：`references/admin-enterprise-patterns.md` §8 早就写了「空态 / 加载态 / 错误态」三态纪律和"列表页五状态齐全才允许交付"的自查清单。但这套纪律有两个问题：
>
> 1. **它只是参考文件里的一张人工清单**——`review` 的 13 项检查表不引用它，`design` 的 Step 6 交付清单也不引用它，没有任何一道门禁会读它。
> 2. **它只管 B 端**——C 端产品页、营销落地页同样有"数据还没来 / 数据是空的 / 请求失败了"的情况，但没有任何地方要求覆盖。
>
> 后果是可预见的：产出看起来"有内容"，但把接口关掉、把数据库清空、把网络断掉，页面就只剩一块空白——**所有门禁全绿，交付物仍然是个只能演示 happy path 的壳**。实测验证过：一个完全通过 slop_scan / token_lint / signature_check / composition_check 四道门禁的订单列表页，可以没有任何加载态、空态、错误态。
>
> 本文件把页面级状态转成**机器可判定的标记规范**，让"这个页面考虑了哪些情况"能被对账。

---

## 一、状态契约字段（State Contract）

页面存在异步数据或用户可触发操作时，必须在实现代码里落出状态声明。一个标记注释，逗号分隔：

```css
/* states: loading,empty,error */
```

```html
<!-- states: loading,empty,error -->
```

载体规则与构图契约一致：有独立 CSS 文件写 CSS 顶部，Tailwind / 单文件 HTML 写 HTML 注释，`state_check.py` 两种都认。

| 状态 | 含义 | 最低要求 |
|-----|------|---------|
| `loading` | 数据/操作进行中 | 骨架屏或进度指示，**且占位与真实内容对位**（不跳变布局） |
| `empty` | 数据为空（含筛选无结果） | 说清"这里将来是什么" + 给下一个动作 |
| `error` | 请求失败/操作失败 | 说清发生了什么 + 用户能做什么（重试/联系） |
| `success` | 操作成功反馈 | 与 `error` 成对出现，不单独存在 |
| `no-permission` | 无权限 | 说明原因 + 给申请入口（B 端常见） |
| `offline` | 离线/断网 | 网络依赖型应用 |

**状态与交互复杂度的派生关系**（不是所有项目都要全上）：

| `interaction-complexity`（research 第 3 轮） | 必须声明的状态 |
|---|---|
| `static`（纯静态展示） | **不需要声明**——静态页面没有异步数据，强制要求是噪音 |
| `basic`（表单/按钮/导航） | `error`、`success` |
| `moderate`（搜索/筛选/Tab/模态框） | `loading`、`empty`、`error` |
| `complex`（拖拽/实时数据/富文本） | `loading`、`empty`、`error`、`no-permission` |
| `app`（路由/状态管理/API） | 全量：`loading`、`empty`、`error`、`success`、`no-permission` |

> **`static` 是明确的豁免**——一条静态营销页没有 loading 态不是缺陷，要求它写 `/* states: */` 只会训练出"为了过门禁而堆标记"的反向作弊。这也是本契约必须由 `interaction-complexity` 驱动、不能一刀切的原因。

---

## 二、落地判据（状态 ≠ 声明就完事）

标记只是**对账锚点**。真正的落地是代码里看得见的证据：

| 状态 | 落地证据（`state_check.py` 找什么） |
|-----|-----------------------------------|
| `loading` | 类名 / 属性 / 文案三选一：`is-loading`、`aria-busy`、`data-state="loading"`、`加载中`、`骨架屏` |
| `empty` | `is-empty`、`data-state="empty"`、`空态`、`暂无`、`没有` |
| `error` | `is-error`、`aria-invalid`、`data-state="error"`、`失败`、`出错了`、`重试` |
| `success` | `is-success`、`data-state="success"`、`成功` |
| `no-permission` | `no-permission`、`无权限`、`没有权限` |
| `offline` | `offline`、`离线`、`网络` |

**判定规则**：

- 声明了 N 个状态，代码里必须有 N 个状态的证据 —— 少一个 FAIL（`state-declared-not-landed`）
- 代码里有状态证据但声明里没有 —— WARN（`state-landed-not-declared`），不阻塞：可能是实现先于声明
- `interaction-complexity` 派生集合里的状态，声明里缺 —— FAIL（`state-required-missing`）
- 零声明且复杂度非 `static` —— FAIL（`state-absent`）
- 零声明且复杂度 `static` 或未提供 —— PASS（豁免）

**证据判定刻意宽松**：`state_check.py` 只证明"这个状态在代码里出现过"，不判断状态设计得好不好（骨架屏对不对位、空态文案到不到位）。后者是 review #14 的人工职责。**脚本保证"做了"，review 保证"做对了"，两者不可互相替代。**

---

## 三、与既有机制的关系

| 机制 | 管什么 | 与状态契约的关系 |
|-----|-------|-----------------|
| `admin-enterprise-patterns.md` §8 | B 端三态纪律（设计质量） | 契约是它的**可校验投影**——从它取质量标准，然后按它落地 |
| slop-test `missing-interactive-states` | 控件态（`:hover` / `:focus-visible` / `:active`） | 那是**元素级**状态，契约管**页面级**状态，两者正交 |
| `ux-guidelines.md` IN1 | 表单输入 8 态 | 同理，元素级；契约不重复约束 |
| 构图契约（v2.12.0） | 页面形状 | 契约管**页面在什么情况下长什么样**，构图契约管**页面正常时长什么样** |

---

## 四、常见不落地情形（自查）

- [ ] 只做了有数据的列表页，没做空列表（用户第一次进来看到的就是这个）
- [ ] 加载态用了全屏 spinner，骨架屏位置和真实内容对不上，内容回来时布局跳变
- [ ] 错误态只有"出错了"三个字，没有重试入口
- [ ] 筛选无结果和有数据为空用了同一个空态（前者应该提示"换个筛选条件"）
- [ ] `success` 和 `error` 只做了一个（操作失败有提示、成功静默）
- [ ] 为了过门禁堆标记，代码里搜不到对应实现

---

## 五、机器校验

```bash
# 自动按页面里的状态证据推断复杂度，无派生要求
python scripts/state_check.py <实现目录>

# 指定 research 得出的交互复杂度，启用派生规则
python scripts/state_check.py . --complexity moderate
```

`--complexity` 接受 `static` / `basic` / `moderate` / `complex` / `app`；缺省时只检查"声明与实现一致"，不启用派生集合。
