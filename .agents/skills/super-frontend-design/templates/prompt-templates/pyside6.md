# PySide6 / Qt 桌面应用 Prompt 模板

> 适用场景：PySide6 / PyQt6 + Python 桌面应用 UI 设计
> 合并来源：desktop-patterns + professional-software + pyside6-patterns

## 技术栈

- **框架**：PySide6（Qt6 for Python）
- **语言**：Python 3.11+
- **样式**：QSS（Qt Style Sheets，类似 CSS）
- **图标**：Qt Awesome / Custom SVG
- **动效**：QPropertyAnimation / QGraphicsEffect

## 目录结构

```
project/
├── main.py                 # 入口
├── app/
│   ├── __init__.py
│   ├── window.py           # 主窗口
│   ├── components/         # 自定义组件
│   │   ├── sidebar.py
│   │   ├── command_palette.py
│   │   └── property_panel.py
│   ├── styles/
│   │   └── qss/
│   │       ├── light.qss
│   │       └── dark.qss
│   └── resources/
│       └── icons/
└── requirements.txt
```

## 核心设计决策

### 1. 主窗口布局

```python
# app/window.py
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QLabel, QSplitter, QStackedWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Name")
        self.resize(1400, 900)
        self.setMinimumSize(1024, 768)

        # 中心 widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 自定义标题栏
        self.titlebar = TitleBar()
        layout.addWidget(self.titlebar)

        # 主体布局
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # 侧边栏
        self.sidebar = Sidebar()
        body.addWidget(self.sidebar)

        # 主内容区
        self.content = QStackedWidget()
        body.addWidget(self.content)

        layout.addLayout(body)

        # 状态栏
        self.statusbar = QLabel("✓ 就绪")
        self.statusbar.setFixedHeight(24)
        self.statusbar.setStyleSheet("background: #1e293b; color: #94a3b8; font-size: 11px;")
        layout.addWidget(self.statusbar)

        self.apply_theme("dark")
```

### 2. 自定义标题栏

```python
# app/components/titlebar.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

class TitleBar(QWidget):
    close_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedHeight(32)
        self.setStyleSheet("""
            TitleBar { background: #0f172a; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        # 左侧：菜单按钮 + 标题
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setFixedSize(24, 24)
        self.btn_menu.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover { background: #334155; color: #f8fafc; }
        """)
        layout.addWidget(self.btn_menu)

        self.label_title = QLabel("App Name")
        self.label_title.setStyleSheet("color: #f8fafc; font-size: 13px; font-weight: 500;")
        layout.addWidget(self.label_title)

        layout.addStretch()

        # 右侧：窗口控制按钮（macOS 风格）
        self.btn_minimize = self._create_window_btn("─", "#f59e0b")
        self.btn_maximize = self._create_window_btn("□", "#22c55e")
        self.btn_close = self._create_window_btn("✕", "#ef4444", True)

        layout.addWidget(self.btn_minimize)
        layout.addWidget(self.btn_maximize)
        layout.addWidget(self.btn_close)

    def _create_window_btn(self, text, color, is_close=False):
        btn = QPushButton(text)
        btn.setFixedSize(32, 24)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {color};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{ background: {color}22; }}
        """)
        if is_close:
            btn.clicked.connect(self.close_requested)
        return btn
```

### 3. 侧边栏

```python
# app/components/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

class SidebarItem(QWidget):
    def __init__(self, icon, label, active=False):
        super().__init__()
        self.setFixedHeight(36)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(12)

        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("color: #94a3b8; font-size: 16px;")
        self.label = QLabel(label)
        self.label.setStyleSheet("color: #94a3b8; font-size: 13px;")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)
        layout.addStretch()

        if active:
            self.setStyleSheet("background: #1e293b;")
            self.label.setStyleSheet("color: #f8fafc; font-weight: 500;")

    def set_active(self, active):
        if active:
            self.setStyleSheet("background: #1e293b;")
            self.label.setStyleSheet("color: #f8fafc; font-weight: 500;")
        else:
            self.setStyleSheet("")
            self.label.setStyleSheet("color: #94a3b8;")

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("""
            Sidebar { background: #0f172a; border-right: 1px solid #1e293b; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(2)

        items = [
            ("🏠", "首页"),
            ("📁", "文件"),
            ("🔍", "搜索"),
            ("✅", "任务"),
            ("⚙️", "设置"),
        ]

        for icon, label in items:
            btn = QPushButton(f"  {icon}  {label}")
            btn.setFixedHeight(36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #94a3b8;
                    text-align: left;
                    padding-left: 16px;
                    border: none;
                    border-radius: 4px;
                    font-size: 13px;
                }
                QPushButton:hover { background: #1e293b; color: #f8fafc; }
            """)
            layout.addWidget(btn)

        layout.addStretch()
```

### 4. Command Palette

```python
# app/components/command_palette.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeySequence

class CommandPalette(QDialog):
    command_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setFixedSize(480, 360)
        self.setStyleSheet("""
            QDialog { background: #1e293b; border: 1px solid #334155; border-radius: 8px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 搜索框
        self.search = QLineEdit()
        self.search.setPlaceholderText("搜索命令...")
        self.search.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #f8fafc;
                border: none;
                border-bottom: 1px solid #334155;
                padding: 12px 16px;
                font-size: 14px;
            }
            QLineEdit::placeholder { color: #64748b; }
        """)
        layout.addWidget(self.search)

        # 结果列表
        self.list = QListWidget()
        self.list.setStyleSheet("""
            QListWidget {
                background: #1e293b;
                border: none;
                font-size: 13px;
                color: #94a3b8;
            }
            QListWidget::item {
                padding: 10px 16px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #334155;
                color: #f8fafc;
            }
        """)
        layout.addWidget(self.list)

        # 绑定搜索
        self.search.textChanged.connect(self.filter_commands)

        # 快捷键
        self.search.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
                return True
            elif event.key() == Qt.Key_Return:
                current = self.list.currentItem()
                if current:
                    self.command_selected.emit(current.text())
                    self.close()
                    return True
        return super().eventFilter(obj, event)

    def filter_commands(self, query):
        self.list.clear()
        for cmd in self.commands:
            if query.lower() in cmd['label'].lower():
                item = QListWidgetItem(f"{cmd['icon']}  {cmd['label']}")
                item.setData(Qt.UserRole, cmd)
                self.list.addItem(item)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    @property
    def commands(self):
        return [
            {"label": "新建项目", "icon": "📁", "shortcut": "⌘N"},
            {"label": "打开文件...", "icon": "📂", "shortcut": "⌘O"},
            {"label": "切换主题", "icon": "🎨", "shortcut": "⌘T"},
            {"label": "设置", "icon": "⚙️", "shortcut": "⌘,"},
        ]
```

### 5. QSS 主题系统

```css
/* app/styles/qss/dark.qss */
/* 基于 Design Token 的 QSS 主题 */

/* 颜色 Token */
* {
  color: #f8fafc;
}

QMainWindow {
  background: #0f172a;
}

QFrame#surface {
  background: #1e293b;
  border: 1px solid #334155;
}

QPushButton {
  background: transparent;
  color: #94a3b8;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 13px;
}

QPushButton:hover {
  background: #334155;
  color: #f8fafc;
}

QPushButton:pressed {
  background: #475569;
}

QLineEdit, QTextEdit, QPlainTextEdit {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 4px;
  padding: 6px 10px;
  color: #f8fafc;
  selection-background-color: #3b82f6;
}

QListWidget {
  background: #1e293b;
  border: none;
}

QListWidget::item:selected {
  background: #334155;
}

QScrollBar:vertical {
  background: transparent;
  width: 8px;
}

QScrollBar::handle:vertical {
  background: #334155;
  border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
  background: #475569;
}

QScrollBar::add-line, QScrollBar::sub-line {
  height: 0;
}
```

### 6. 应用入口

```python
# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 跨平台统一样式

    # 设置应用信息
    app.setApplicationName("App Name")
    app.setOrganizationName("Org")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## Prompt 使用指南

1. 调用 `super-frontend-design` Skill，路由到 `design` 子命令
2. 在 research 阶段，明确告知技术栈为 **PySide6 + Python**
3. PySide6 优势：原生 Qt 性能、跨平台一致性、丰富的组件库
4. 设计时参考 `references/desktop-patterns.md`
5. 输出时包含完整的 QSS 样式文件 + Python 代码

## 关键注意事项

- **Fusion 样式**：跨平台统一的基线样式
- **QSS 替代 CSS**：PySide6 使用 QSS，语法类似 CSS 但有差异
- **事件系统**：使用 Signal/Slot 替代 DOM 事件
- **动画**：使用 QPropertyAnimation + QEasingCurve
- **主题切换**：动态加载不同 QSS 文件
- **图标**：使用 Qt Awesome 或自定义 SVG
