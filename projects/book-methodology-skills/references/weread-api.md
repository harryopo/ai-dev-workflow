# 微信读书 API 参考

## 统一入口

```
POST https://i.weread.qq.com/api/agent/gateway
```

## 鉴权

- Header: `Authorization: Bearer $WEREAD_API_KEY`
- 若未设置: `export WEREAD_API_KEY=<你的apikey>`

## 请求格式

- Method: POST, Content-Type: application/json
- Body: JSON, `api_name` 指定接口，**每次必须带 `skill_version`**
- 业务参数和 `api_name`、`skill_version` 放同一层，不要包在 `params` 内

## 支持的能力

| 能力 | api_name | 说明 |
|------|----------|------|
| 搜索书籍 | `/store/search` | 书城搜索 |
| 书籍信息 | `/book/info` | 详情、章节、进度 |
| 书架管理 | `/shelf/sync` | 查看书架 |
| 阅读统计 | `/readdata/summary` | 时长、天数、偏好 |
| 笔记划线 | `/review/list/mine` | 个人笔记和想法 |
| 书签列表 | `/book/bookmarklist` | 用户划线 |
| 热门划线 | `/book/bestbookmarks` | 章节热门划线 |
| 书籍点评 | `/book/readreviews` | 公开点评 |

## 请求 few-shot

**正确：业务参数平铺在 body 顶层。**

```json
{"api_name":"/user/notebooks","count":100,"skill_version":"1.0.5"}
```

**错误：不要把业务参数包在 `params` 内。**

```json
{"api_name":"/user/notebooks","params":{"count":100},"skill_version":"1.0.5"}
```

错误写法会导致参数未被转发，后端按默认值返回第一页。

## 响应格式

- JSON，回包经过字段裁剪，只返回核心字段
- `errcode` 非 0 时表示错误，给出中文提示
- 发送 `{"api_name": "/_list"}` 可查看所有可用接口及参数定义

## 通用规则（10 条）

1. **版本上报**：每次请求必须带 `"skill_version": "1.0.3"`，若回包有 `upgrade_info` 必须立即暂停操作并升级
2. **参数平铺**：业务参数与 `api_name`、`skill_version` 同层，不要包在 `params` 内
3. **能力文档预检**：调用接口前先阅读对应说明文件，确认参数含义，禁止凭经验猜测
4. **字段解释优先级**：以说明文件为准，字段名与直觉冲突时服从文档
5. **bookId 解析**：用户输入书名时先调 `/store/search` 获取 bookId
6. **书架数量**：按 `books.length + albums.length + (mp 非空 ? 1 : 0)` 计算
7. **结果展示**：列表用编号，搜索展示书名/作者/评分，字段禁止直接翻译
8. **上下文衔接**：记住已查询的 bookId，后续操作无需重复提供
9. **深度链接**：展示划线/想法/章节时拼接跳转链接
10. **数据规范**：时间戳转 YYYY-MM-DD，时长秒转"X小时Y分钟"

## 深度链接（URL Schema）

### 打开书籍（跳转到上次阅读进度）

```
weread://reading?bId={bookId}
```

### 跳转到指定章节

```
weread://reading?bId={bookId}&chapterUid={chapterUid}
```

### 跳转到划线/想法所在位置

```
weread://bestbookmark?bookId={bookId}&chapterUid={chapterUid}&rangeStart={rangeStart}&rangeEnd={rangeEnd}&userVid={userVid}
```

**range 解析**：`range` 格式为 `"起始-结束"`（如 `"900-2004"`），拆分后分别填入 `rangeStart` 和 `rangeEnd`。

**使用场景**：
- 展示划线列表时，每条附上跳转链接
- 展示热门划线时，每条附上跳转链接
- 展示想法时，只有包含 `chapterUid` 和 `range` 时才附上跳转链接

## 流水线步骤

**Step 1: 搜索书籍获取 bookId**
```json
{"api_name": "/store/search", "keyword": "书名", "count": 5, "skill_version": "1.0.3"}
```

**Step 2: 获取用户笔记**
```json
{"api_name": "/review/list/mine", "bookid": "{bookId}", "count": 100, "skill_version": "1.0.3"}
```

**Step 3: 获取用户划线**
```json
{"api_name": "/book/bookmarklist", "bookId": "{bookId}", "skill_version": "1.0.3"}
```

**Step 4: 获取热门划线（补充）**
```json
{"api_name": "/book/bestbookmarks", "bookId": "{bookId}", "skill_version": "1.0.3"}
```

**Step 5: 合并整理为结构化文本**

```markdown
# 《书名》阅读笔记

## 用户划线
1. "划线内容1" —— 第X章

## 用户笔记
1. 笔记内容1

## 热门划线（补充）
1. "热门划线1" —— N人划线
```
