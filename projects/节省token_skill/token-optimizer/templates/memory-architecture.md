# 记忆架构模板

## 初始化

```bash
mkdir -p refs canvas
touch refs/summary.jsonl refs/metadata.json canvas/task-state.mmd
```

## Level 0: 保存原文

```bash
# 保存工具调用结果
echo "$(date): Tool call result" >> refs/tool-calls-$(date +%Y%m%d).md
```

## Level 1: 生成摘要

每次工具调用后，追加 JSONL 摘要到 refs/summary.jsonl：
```json
{"timestamp":"...","tool":"...","input":"...","output_summary":"...","key_facts":[...],"token_saved":N}
```

## Level 2: 更新 Mermaid 画布

每完成一个步骤，更新 canvas/task-state.mmd 添加新节点和连接。

## Level 3: 更新元数据

任务完成时，写入 refs/metadata.json 记录任务级统计。
