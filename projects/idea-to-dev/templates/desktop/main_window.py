import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget,
    QListWidgetItem, QMessageBox, QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from todo_adapter import TodoAdapter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("待办事项")
        self.setMinimumSize(600, 500)
        self.todo_adapter = TodoAdapter()
        self.init_ui()
        self.refresh_items()

    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("待办事项")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Input area
        input_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("输入新的待办事项...")
        self.task_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1296db;
            }
        """)
        self.task_input.returnPressed.connect(self.on_add)
        input_layout.addWidget(self.task_input)

        add_button = QPushButton("添加")
        add_button.setStyleSheet(self._button_style("#4CAF50"))
        add_button.clicked.connect(self.on_add)
        input_layout.addWidget(add_button)

        main_layout.addLayout(input_layout)

        # Todo list
        self.todo_list = QListWidget()
        self.todo_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #000;
            }
        """)
        main_layout.addWidget(self.todo_list)

        # Action buttons
        button_layout = QHBoxLayout()

        toggle_button = QPushButton("标记完成/撤销")
        toggle_button.setStyleSheet(self._button_style("#2196F3"))
        toggle_button.clicked.connect(self.on_toggle)
        button_layout.addWidget(toggle_button)

        delete_button = QPushButton("删除")
        delete_button.setStyleSheet(self._button_style("#f44336"))
        delete_button.clicked.connect(self.on_delete)
        button_layout.addWidget(delete_button)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("font-size: 12px; color: #666; margin: 5px;")
        main_layout.addWidget(self.stats_label)

        # Status bar
        self.statusBar().showMessage("就绪")

    def _button_style(self, color: str) -> str:
        """Generate a styled button stylesheet."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 0, 0, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """

    def refresh_items(self):
        """Reload items from the business adapter and update the UI."""
        self.todo_list.clear()
        items = self.todo_adapter.get_items()

        for item in items:
            list_item = QListWidgetItem()
            if item.completed:
                list_item.setText(f"✓ {item.name}")
                list_item.setForeground(Qt.GlobalColor.gray)
            else:
                list_item.setText(f"○ {item.name}")
            list_item.setData(Qt.ItemDataRole.UserRole, item.id)
            self.todo_list.addItem(list_item)

        self._update_stats(items)

    def _update_stats(self, items=None):
        stats = self.todo_adapter.get_stats(items)
        self.stats_label.setText(
            f"总计: {stats.total} 项 | 已完成: {stats.completed} 项 | 待完成: {stats.pending} 项"
        )

    def _get_selected_id(self) -> str | None:
        current_item = self.todo_list.currentItem()
        if current_item is None:
            return None
        return current_item.data(Qt.ItemDataRole.UserRole)

    def on_add(self):
        """Add a new todo item."""
        task = self.task_input.text().strip()
        if not task:
            QMessageBox.warning(self, "警告", "请输入待办事项内容")
            return

        try:
            self.todo_adapter.add_item(task)
            self.task_input.clear()
            self.refresh_items()
            self.statusBar().showMessage("添加成功", 2000)
        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))

    def on_toggle(self):
        """Toggle the completed state of the selected item."""
        item_id = self._get_selected_id()
        if item_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        self.todo_adapter.toggle_item(item_id)
        self.refresh_items()
        self.statusBar().showMessage("状态已更新", 2000)

    def on_delete(self):
        """Delete the selected item after confirmation."""
        item_id = self._get_selected_id()
        if item_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这个任务吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.todo_adapter.delete_item(item_id)
            self.refresh_items()
            self.statusBar().showMessage("删除成功", 2000)


def main():
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
