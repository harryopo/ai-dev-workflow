from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的应用")
        self.setMinimumSize(600, 400)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加标题
        title = QLabel("欢迎使用我的应用")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # 添加输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("请输入内容...")
        self.input_field.setStyleSheet("padding: 10px; font-size: 16px;")
        layout.addWidget(self.input_field)
        
        # 添加按钮
        button = QPushButton("点击我")
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)
        
        # 添加状态标签
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(self.status_label)
        
        # 添加弹性空间
        layout.addStretch()
    
    def on_button_click(self):
        """按钮点击事件"""
        text = self.input_field.text()
        if text:
            self.status_label.setText(f"你输入了: {text}")
            QMessageBox.information(self, "提示", f"你输入了: {text}")
        else:
            QMessageBox.warning(self, "警告", "请输入内容")
