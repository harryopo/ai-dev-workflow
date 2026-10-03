# ⚠️ 这是过时镜像，不是开发主线

本目录是 deep-research-ultra 在工作区库里的**历史快照**（停在 v6.15.0，2026-09-30）。
不在这里开发、不要在这里修 bug——例如 `scripts/tests/test_mcp_client.py::test_no_orphan_after_timeout`
在本目录必挂，主线早已随 `mcp_client.py` 重写消失，不值得修。

- **开发主线**：`~/.zcode/skills/deep-research-ultra`（git 仓库，分支 `plan-a/plugin-shell`，远端 github.com/harryopo/deep-research-ultra）
- **第二安装位**：`~/.agents/skills/deep-research-ultra`（随主线同步）
- **全仓测试入口**：主线仓库根 `python run_all_tests.py`（内核 + 插件壳两套一起跑）

新增的设计/计划/方案文档仍放本目录 `references/`（如 `v6.51-修复方案书.md`），
**代码改动一律去开发主线做**。
