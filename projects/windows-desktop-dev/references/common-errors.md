# 常见错误及解决方案

## 1. ModuleNotFoundError: No module named 'xxx'

**原因**：缺少依赖包

**解决**：
```bash
pip install xxx
```

**预防**：确保 requirements.txt 包含所有依赖

---

## 2. 打包后找不到资源文件

**原因**：打包后路径变化，相对路径失效

**解决**：使用以下函数获取资源路径
```python
import sys
import os

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境
    return os.path.join(os.path.abspath('.'), relative_path)

# 使用示例
icon_path = get_resource_path("resources/icon.png")
```

---

## 3. 中文路径乱码

**原因**：Windows 路径编码问题

**解决**：使用 `os.path` 处理路径
```python
import os

# 错误做法
path = "C:\用户\文档\文件.txt"

# 正确做法
path = os.path.join("C:", "用户", "文档", "文件.txt")
# 或
path = os.path.normpath("C:/用户/文档/文件.txt")
```

---

## 4. 打包体积过大（超过 200MB）

**原因**：包含了不必要的大型库（如 numpy、pandas）

**解决**：
```bash
# 排除不需要的模块
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy --exclude-module pandas main.py
```

**优化**：
1. 只导入需要的模块
2. 使用 `--exclude-module` 排除大型库
3. 考虑使用虚拟环境减少依赖

---

## 5. 界面卡死/无响应

**原因**：耗时操作阻塞了主线程

**解决**：使用多线程
```python
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    finished = Signal(str)
    error = Signal(str)
    
    def run(self):
        try:
            # 耗时操作
            result = do_something()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# 在主线程中使用
self.worker = Worker()
self.worker.finished.connect(self.on_finished)
self.worker.error.connect(self.on_error)
self.worker.start()
```

---

## 6. 窗口显示异常（控件重叠、布局混乱）

**原因**：布局使用不当

**解决**：使用布局管理器
```python
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

# 创建布局
layout = QVBoxLayout()

# 添加控件
layout.addWidget(widget1)
layout.addWidget(widget2)

# 设置间距
layout.setSpacing(10)
layout.setContentsMargins(10, 10, 10, 10)

# 应用布局
container = QWidget()
container.setLayout(layout)
self.setCentralWidget(container)
```

---

## 7. 中文显示乱码

**原因**：文件编码问题

**解决**：
1. 确保 Python 文件使用 UTF-8 编码
2. 在文件开头添加：
```python
# -*- coding: utf-8 -*-
```
3. 字符串使用 Unicode：
```python
text = "中文内容"
```

---

## 8. 程序启动闪退

**原因**：未捕获的异常

**解决**：添加全局异常处理
```python
import sys
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox

def excepthook(exc_type, exc_value, exc_tb):
    """全局异常处理"""
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    QMessageBox.critical(None, "错误", f"程序发生错误：\n{tb}")

sys.excepthook = excepthook
```

---

## 9. 数据库锁定

**原因**：多个连接同时访问数据库

**解决**：
```python
import sqlite3

# 使用 with 语句自动关闭连接
with sqlite3.connect("data.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
```

---

## 10. 打包后运行报错 "Failed to execute script"

**原因**：缺少依赖或路径问题

**解决**：
1. 检查是否有隐藏的导入
2. 使用 `--hidden-import` 添加缺失的模块
3. 使用 `--add-data` 添加资源文件
```bash
pyinstaller --onefile --windowed --hidden-import=模块名 --add-data="资源文件;目标目录" main.py
```

---

## 11. 窗口图标不显示

**原因**：图标路径错误或格式不支持

**解决**：
```python
from PySide6.QtGui import QIcon

# 使用资源路径函数
icon_path = get_resource_path("resources/icon.ico")
window.setWindowIcon(QIcon(icon_path))
```

**注意**：Windows 图标需要 .ico 格式

---

## 12. 中文输入法问题

**原因**：某些控件不支持中文输入

**解决**：使用 QLineEdit 或 QTextEdit 接收中文输入
```python
from PySide6.QtWidgets import QLineEdit

input_field = QLineEdit()
input_field.setPlaceholderText("请输入中文")
```

---

## 调试技巧

### 1. 打印调试
```python
print(f"变量值: {variable}")
```

### 2. 使用日志
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("调试信息")
logging.error("错误信息")
```

### 3. 使用断点
```python
# 在代码中添加断点
import pdb; pdb.set_trace()
```

### 4. 查看错误堆栈
```python
import traceback

try:
    # 可能出错的代码
    pass
except Exception as e:
    traceback.print_exc()
```
