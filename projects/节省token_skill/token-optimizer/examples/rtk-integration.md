# RTK 集成示例

## 场景：Python 项目测试

### 无 RTK
```bash
$ pytest tests/
============================= test session starts ==============================
platform linux -- Python 3.10.0, pytest-7.4.0
rootdir: /home/user/project
collected 100 items

tests/test_main.py::test_add PASSED                                      [  1%]
tests/test_main.py::test_subtract PASSED                                 [  2%]
tests/test_main.py::test_multiply PASSED                                 [  3%]
... (97 more lines)

============================== 100 passed in 2.34s ==============================
```

Token 消耗：~500 tokens

### 有 RTK
```bash
$ rtk pytest tests/
100 tests passed (2.34s)
```

Token 消耗：~20 tokens
节省：96%

## 场景：Git 操作

### 无 RTK
```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)

        modified:   src/main.py
        modified:   src/utils.py
        modified:   tests/test_main.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        docs/new-feature.md

no changes added to commit (use "git add" and/or "git commit -a")
```

Token 消耗：~150 tokens

### 有 RTK
```bash
$ rtk git status
Branch: main (up to date)
Modified: src/main.py, src/utils.py, tests/test_main.py
Untracked: docs/new-feature.md
```

Token 消耗：~30 tokens
节省：80%

## 场景：Maven 测试

### 无 RTK
```bash
$ mvn test
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------< com.example:my-project >-------------------
[INFO] Building my-project 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
...
[INFO]  T E S T S   R U N
[INFO] -------------------------------------------------------
[INFO]  Total: 100  |  Passed: 100  |  Failed: 0  |  Skipped: 0
[INFO] -------------------------------------------------------
[INFO] BUILD SUCCESS
```

Token 消耗：~800 tokens

### 有 RTK
```bash
$ rtk mvn test
100 tests passed (12.345s)
BUILD SUCCESS
```

Token 消耗：~30 tokens
节省：96%
