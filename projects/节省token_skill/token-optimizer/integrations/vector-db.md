# 向量数据库集成

## 概述
向量检索(RAG)是当前工业界最主流的长期记忆方案。

## 支持的向量数据库

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| Chroma | 轻量级，易部署 | 小型项目 |
| Milvus | 高性能，分布式 | 大型项目 |
| Pinecone | 云服务，免运维 | 快速启动 |
| Weaviate | GraphQL 接口 | 复杂查询 |

## 集成步骤

### Step 1: 安装依赖
```bash
pip install chromadb  # 或其他向量数据库
```

### Step 2: 初始化客户端
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("memory")
```

### Step 3: 存储记忆
```python
def store_memory(content, metadata):
    # 生成向量
    embedding = embed(content)

    # 存储
    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[generate_id()]
    )
```

### Step 4: 检索记忆
```python
def retrieve_memory(query, top_k=5):
    # 查询向量
    query_embedding = embed(query)

    # 检索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
```

## 最佳实践

1. **分块存储**：将长文档分成小块存储，提高检索精度
2. **元数据过滤**：使用元数据过滤无关结果
3. **定期清理**：删除过期或无用的记忆
4. **监控质量**：定期评估检索质量，调整参数
