"""
待办事项应用示例 - PySide6 + SQLite
这是一个简单的待办事项应用，展示如何使用 SQLite 存储数据。
"""

import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("待办事项")
        self.setMinimumSize(500, 400)
        self.db_path = "todos.db"
        self.init_db()
        self.init_ui()
        self.load_todos()
    
    def init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed INTEGER DEFAULT 0
                )
            """)
            conn.commit()
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title = QLabel("待办事项")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 输入区域
        input_layout = QHBoxLayout()
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("输入新的待办事项...")
        self.task_input.setStyleSheet("padding: 10px; font-size: 14px;")
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        
        add_button = QPushButton("添加")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_button.clicked.connect(self.add_task)
        input_layout.addWidget(add_button)
        
        layout.addLayout(input_layout)
        
        # 待办列表
        self.todo_list = QListWidget()
        self.todo_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QListWidgetItem {
                padding: 10px;
            }
        """)
        layout.addWidget(self.todo_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        complete_button = QPushButton("标记完成")
        complete_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        complete_button.clicked.connect(self.complete_task)
        button_layout.addWidget(complete_button)
        
        delete_button = QPushButton("删除")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        # 状态栏
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12px; color: #666; margin: 5px;")
        layout.addWidget(self.status_label)
    
    def load_todos(self):
        """加载待办事项"""
        self.todo_list.clear()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, task, completed FROM todos ORDER BY id DESC")
            for row in cursor.fetchall():
                task_id, task, completed = row
                item = QListWidgetItem()
                if completed:
                    item.setText(f"✓ {task}")
                    item.setForeground(Qt.GlobalColor.gray)
                else:
                    item.setText(f"○ {task}")
                item.setData(Qt.ItemDataRole.UserRole, task_id)
                self.todo_list.addItem(item)
        
        self.update_status()
    
    def add_task(self):
        """添加任务"""
        task = self.task_input.text().strip()
        if not task:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
        
        self.task_input.clear()
        self.load_todos()
    
    def complete_task(self):
        """标记任务完成"""
        current_item = self.todo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return
        
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE todos SET completed = 1 - completed WHERE id = ?", (task_id,))
            conn.commit()
        
        self.load_todos()
    
    def delete_task(self):
        """删除任务"""
        current_item = self.todo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return
        
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "确认", "确定要删除这个任务吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
                conn.commit()
            
            self.load_todos()
    
    def update_status(self):
        """更新状态栏"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM todos")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
            completed = cursor.fetchone()[0]
        
        self.status_label.setText(f"总计: {total} 项 | 已完成: {completed} 项 | 未完成: {total - completed} 项")


def main():
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
