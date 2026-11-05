"""agent-memory core — 编码 agent 的记忆模块核心库（M1）。

六模块：store（四套格式读写+校验）/ retrieval（排序检索）/ consolidate（四操作）/
snapshot（§0 快照）/ doctor（体检）/ addressing（宿主无关寻址）。

铁律：Markdown 文件是唯一权威，本库只是"带保证的读写器"。
纯标准库；Python ≥3.9；fail-closed——schema 不通过就报错，绝不静默降级。
"""

__version__ = "0.1.0"
