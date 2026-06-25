# PySide6 开发指南

## 简介

PySide6 是 Qt 6 的 Python 官方绑定，用于开发跨平台桌面应用程序。

## 安装

```bash
pip install PySide6
```

## 基本结构

### 最小示例

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication(sys.argv)
window = QMainWindow()
window.setCentralWidget(QLabel("Hello, PySide6!"))
window.setWindowTitle("我的应用")
window.resize(400, 300)
window.show()
sys.exit(app.exec())
```

### 推荐结构

```python
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## 常用控件

### 按钮
```python
from PySide6.QtWidgets import QPushButton

button = QPushButton("点击我")
button.clicked.connect(lambda: print("被点击了"))
```

### 文本框
```python
from PySide6.QtWidgets import QLineEdit

text_input = QLineEdit()
text_input.setPlaceholderText("请输入内容")
text = text_input.text()  # 获取文本
```

### 标签
```python
from PySide6.QtWidgets import QLabel

label = QLabel("这是标签")
label.setText("新文本")
```

### 布局
```python
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

# 垂直布局
layout = QVBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)

# 水平布局
layout = QHBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)

# 应用布局
container = QWidget()
container.setLayout(layout)
```

### 对话框
```python
from PySide6.QtWidgets import QMessageBox, QFileDialog

# 消息框
QMessageBox.information(window, "标题", "消息内容")
QMessageBox.warning(window, "警告", "警告内容")
QMessageBox.question(window, "确认", "确定吗？")

# 文件对话框
file_path, _ = QFileDialog.getOpenFileName(window, "选择文件")
```

### 表格
```python
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

table = QTableWidget()
table.setRowCount(3)
table.setColumnCount(2)
table.setItem(0, 0, QTableWidgetItem("数据1"))
table.setItem(0, 1, QTableWidgetItem("数据2"))
```

### 列表
```python
from PySide6.QtWidgets import QListWidget

list_widget = QListWidget()
list_widget.addItem("项目1")
list_widget.addItem("项目2")
```

### 下拉框
```python
from PySide6.QtWidgets import QComboBox

combo = QComboBox()
combo.addItems(["选项1", "选项2", "选项3"])
current_text = combo.currentText()
```

### 复选框
```python
from PySide6.QtWidgets import QCheckBox

checkbox = QCheckBox("同意条款")
is_checked = checkbox.isChecked()
```

## 信号与槽

```python
# 按钮点击
button.clicked.connect(self.on_button_click)

def on_button_click(self):
    # 处理点击事件
    pass

# 文本变化
text_input.textChanged.connect(self.on_text_change)

def on_text_change(self, text):
    # 处理文本变化
    pass
```

## 样式设置

```python
# 使用 CSS 样式
button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
```

## 多线程

```python
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    finished = Signal(str)
    progress = Signal(int)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        # 耗时操作
        for i in range(100):
            self.progress.emit(i)
            import time
            time.sleep(0.1)
        self.finished.emit("完成")

# 使用
worker = Worker()
worker.finished.connect(self.on_finished)
worker.progress.connect(self.on_progress)
worker.start()
```

## 数据库（SQLite）

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# 创建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
""")

# 插入数据
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("张三", 25))

# 查询数据
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# 提交并关闭
conn.commit()
conn.close()
```

## 文件操作

```python
# 读取文件
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 写入文件
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("内容")
```

## 更多资源

- 官方文档：https://doc.qt.io/qtforpython-6/
- 示例：https://doc.qt.io/qtforpython-6/examples/
