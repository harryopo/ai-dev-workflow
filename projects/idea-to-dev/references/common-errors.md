# 各平台常见错误及解决方案

## 通用问题

### 问题：依赖安装失败
**解决**：
```bash
# 清除缓存重试
npm cache clean --force && npm install
# 或使用国内镜像
npm config set registry https://registry.npmmirror.com
```

### 问题：端口被占用
**解决**：
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :3000
kill -9 <PID>
```

## 小程序 (Taro)

### 问题：编译报错 "Cannot find module"
**解决**：检查是否安装了所有依赖
```bash
npm install
```

### 问题：页面白屏
**解决**：检查 `app.config.ts` 中的 pages 路径是否正确

### 问题：样式不生效
**解决**：检查是否在页面组件中导入了样式文件

## 桌面应用 (PySide6)

### 问题：ModuleNotFoundError
**解决**：`pip install PySide6`

### 问题：打包后找不到资源文件
**解决**：使用 `get_resource_path()` 函数
```python
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)
```

### 问题：界面卡死
**解决**：耗时操作使用 QThread 多线程

### 问题：打包体积过大
**解决**：排除不需要的模块
```bash
pyinstaller --onefile --windowed --exclude-module matplotlib main.py
```

### 问题：中文路径乱码
**解决**：使用 `os.path` 处理路径，避免硬编码

## 网页应用 (Next.js)

### 问题：Hydration Error
**解决**：确保服务端和客户端渲染结果一致
```tsx
'use client'
// 客户端组件需要声明
```

### 问题：样式不生效
**解决**：检查 Tailwind CSS 配置，确保扫描路径正确

### 问题：API 路由 404
**解决**：检查文件结构 `app/api/xxx/route.ts`

## 手机App (React Native)

### 问题：Metro bundler 启动失败
**解决**：
```bash
npx expo start --clear
```

### 问题：模拟器连接失败
**解决**：检查模拟器是否正常运行，或使用 Expo Go App 真机调试

### 问题：iOS 构建失败
**解决**：需要在 macOS 上进行，检查 Xcode 版本

## Skill

### 问题：Skill 不触发
**解决**：检查 `description` 中的触发词是否准确

### 问题：权限不足
**解决**：检查 `allowed-tools` 是否包含需要的工具
