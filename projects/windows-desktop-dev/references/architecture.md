# 架构设计指南

## 概述

选择合适的架构是开发成功的关键。本文档介绍常见的桌面应用架构。

## MVC 架构

### 适用场景
- 简单应用（1-3 个功能）
- 快速原型开发
- 学习阶段

### 结构
```
Model（数据） ← Controller（逻辑） → View（界面）
```

### 优点
- 结构清晰，易于理解
- 开发速度快
- 代码量少

### 缺点
- 复杂应用会变得臃肿
- Controller 容易变成"上帝类"
- 测试困难

### 示例代码
```python
# models/user.py
class UserModel:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_users(self):
        # 从数据库获取用户
        pass

# controllers/app_controller.py
class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def load_users(self):
        users = self.model.get_users()
        self.view.display_users(users)

# views/main_window.py
class MainWindow:
    def display_users(self, users):
        # 显示用户列表
        pass
```

---

## MVVM 架构

### 适用场景
- 数据绑定多的应用
- 界面复杂的应用
- 需要频繁更新界面的应用

### 结构
```
View（界面） ↔ ViewModel（绑定） ↔ Model（数据）
```

### 优点
- 界面和逻辑完全分离
- 数据绑定减少代码量
- 易于测试 ViewModel

### 缺点
- 学习成本高
- 数据绑定可能有性能问题
- 调试困难

### 示例代码
```python
# models/user.py
class UserModel:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)

# viewmodels/main_viewmodel.py
from PySide6.QtCore import QObject, Signal

class MainViewModel(QObject):
    users_changed = Signal(list)
    
    def __init__(self, model):
        super().__init__()
        self.model = model
    
    def load_users(self):
        users = self.model.get_users()
        self.users_changed.emit(users)

# views/main_window.py
class MainWindow(QMainWindow):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.viewmodel.users_changed.connect(self.display_users)
    
    def display_users(self, users):
        # 显示用户列表
        pass
```

---

## MVP 架构

### 适用场景
- 需要单元测试的应用
- 界面和逻辑需要完全分离
- 团队协作开发

### 结构
```
View（界面） ↔ Presenter（表现器） ↔ Model（数据）
```

### 优点
- 易于单元测试
- 界面和逻辑完全分离
- 职责清晰

### 缺点
- 代码量较大
- 接口定义繁琐
- 开发速度较慢

### 示例代码
```python
# models/user.py
class UserModel:
    def get_users(self):
        # 从数据库获取用户
        pass

# presenters/main_presenter.py
class MainPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def load_users(self):
        users = self.model.get_users()
        self.view.display_users(users)

# views/main_window.py
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.presenter = None
    
    def set_presenter(self, presenter):
        self.presenter = presenter
    
    def display_users(self, users):
        # 显示用户列表
        pass
```

---

## 分层架构

### 适用场景
- 复杂业务逻辑
- 大型应用
- 需要长期维护

### 结构
```
表示层（UI）
    ↓
业务逻辑层（Services）
    ↓
数据访问层（Repositories）
    ↓
数据源（Database）
```

### 优点
- 职责清晰
- 易于扩展
- 可维护性高

### 缺点
- 初期开发慢
- 代码量大
- 需要更多设计

### 示例代码
```python
# repositories/user_repository.py
class UserRepository:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_all(self):
        # 从数据库获取所有用户
        pass
    
    def save(self, user):
        # 保存用户到数据库
        pass

# services/user_service.py
class UserService:
    def __init__(self, repository):
        self.repository = repository
    
    def get_users(self):
        return self.repository.get_all()
    
    def create_user(self, data):
        # 业务逻辑验证
        user = User(data)
        self.repository.save(user)
        return user

# views/main_window.py
class MainWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()
        self.service = service
    
    def load_users(self):
        users = self.service.get_users()
        self.display_users(users)
```

---

## 架构选择决策树

```
你的应用复杂度？
│
├── 简单（1-3个功能）
│   └── 推荐：MVC
│
├── 中等（4-10个功能）
│   ├── 需要数据绑定？
│   │   ├── 是 → MVVM
│   │   └── 否 → MVP
│   └── 需要单元测试？
│       ├── 是 → MVP
│       └── 否 → MVC
│
└── 复杂（10+功能）
    └── 推荐：分层架构
```

---

## 最佳实践

### 1. 单一职责
每个类只负责一件事。

### 2. 依赖注入
通过构造函数传入依赖，而不是在类内部创建。

### 3. 接口隔离
定义小而专一的接口。

### 4. 关注点分离
UI、业务逻辑、数据访问分开。

### 5. 可测试性
设计时考虑如何测试。
