"""
计算器示例 - PySide6 桌面应用
这是一个简单的计算器应用，展示 PySide6 的基本用法。
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
from PySide6.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算器")
        self.setFixedSize(300, 400)
        self.current_value = ""
        self.previous_value = ""
        self.operator = ""
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 显示框
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
        """)
        layout.addWidget(self.display)
        
        # 按钮布局
        buttons_layout = QGridLayout()
        
        # 按钮定义
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3),
        ]
        
        for btn_info in buttons:
            if len(btn_info) == 4:
                text, row, col, colspan = btn_info
                button = QPushButton(text)
                buttons_layout.addWidget(button, row, col, 1, colspan)
            else:
                text, row, col = btn_info
                button = QPushButton(text)
                buttons_layout.addWidget(button, row, col)
            
            button.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
                QPushButton:hover {
                    background-color: #e9e9e9;
                }
                QPushButton:pressed {
                    background-color: #d9d9d9;
                }
            """)
            
            # 连接信号
            if text in '0123456789.':
                button.clicked.connect(lambda checked, t=text: self.on_number_click(t))
            elif text in '+-×÷':
                button.clicked.connect(lambda checked, t=text: self.on_operator_click(t))
            elif text == '=':
                button.clicked.connect(self.on_equals_click)
            elif text == 'C':
                button.clicked.connect(self.on_clear_click)
            elif text == '±':
                button.clicked.connect(self.on_negate_click)
            elif text == '%':
                button.clicked.connect(self.on_percent_click)
        
        layout.addLayout(buttons_layout)
    
    def on_number_click(self, number):
        """数字按钮点击"""
        if number == '.' and '.' in self.current_value:
            return
        self.current_value += number
        self.display.setText(self.current_value)
    
    def on_operator_click(self, operator):
        """运算符按钮点击"""
        if self.current_value:
            if self.previous_value and self.operator:
                self.calculate()
            self.previous_value = self.current_value
            self.current_value = ""
            self.operator = operator
    
    def on_equals_click(self):
        """等号按钮点击"""
        if self.previous_value and self.current_value and self.operator:
            self.calculate()
            self.operator = ""
    
    def on_clear_click(self):
        """清除按钮点击"""
        self.current_value = ""
        self.previous_value = ""
        self.operator = ""
        self.display.setText("")
    
    def on_negate_click(self):
        """正负号按钮点击"""
        if self.current_value:
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value
            self.display.setText(self.current_value)
    
    def on_percent_click(self):
        """百分号按钮点击"""
        if self.current_value:
            value = float(self.current_value) / 100
            self.current_value = str(value)
            self.display.setText(self.current_value)
    
    def calculate(self):
        """执行计算"""
        try:
            prev = float(self.previous_value)
            curr = float(self.current_value)
            
            if self.operator == '+':
                result = prev + curr
            elif self.operator == '-':
                result = prev - curr
            elif self.operator == '×':
                result = prev * curr
            elif self.operator == '÷':
                if curr == 0:
                    self.display.setText("错误")
                    return
                result = prev / curr
            else:
                return
            
            # 显示结果
            if result == int(result):
                self.current_value = str(int(result))
            else:
                self.current_value = str(result)
            
            self.display.setText(self.current_value)
            self.previous_value = ""
            
        except Exception as e:
            self.display.setText("错误")


def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
