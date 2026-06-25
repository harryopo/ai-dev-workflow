# 打包指南

## PyInstaller 打包（推荐）

### 安装

```bash
pip install pyinstaller
```

### 基本打包

```bash
# 打包成单个 exe 文件
pyinstaller --onefile --windowed --name MyApp main.py

# 参数说明：
# --onefile: 打包成单个文件
# --windowed: 不显示控制台窗口
# --name: 指定输出文件名
```

### 打包结果

打包完成后，在 `dist/` 目录下会生成 `MyApp.exe` 文件。

### 常用参数

```bash
# 添加图标
pyinstaller --onefile --windowed --icon=app.ico main.py

# 添加资源文件
pyinstaller --onefile --windowed --add-data="resources;resources" main.py

# 排除不需要的模块
pyinstaller --onefile --windowed --exclude-module matplotlib main.py

# 添加隐藏导入
pyinstaller --onefile --windowed --hidden-import=module_name main.py
```

### 完整示例

```bash
pyinstaller --onefile --windowed --name MyApp --icon=app.ico --add-data="resources;resources" --exclude-module matplotlib --exclude-module numpy main.py
```

### spec 文件

如果需要更复杂的配置，可以使用 spec 文件：

```bash
# 生成 spec 文件
pyinstaller --name MyApp main.py

# 编辑 MyApp.spec 文件
# 然后使用 spec 文件打包
pyinstaller MyApp.spec
```

### spec 文件示例

```python
# MyApp.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)
```

---

## 常见打包问题

### 1. 打包后运行报错

**问题**：打包后运行时报错 "Failed to execute script"

**解决**：
1. 检查是否有隐藏的导入
2. 使用 `--hidden-import` 添加缺失的模块
3. 检查资源文件是否正确打包

### 2. 打包体积过大

**问题**：打包后的 exe 文件超过 200MB

**解决**：
1. 使用虚拟环境，只安装必要的包
2. 使用 `--exclude-module` 排除大型库
3. 使用 UPX 压缩（默认启用）

### 3. 资源文件找不到

**问题**：打包后运行时找不到资源文件

**解决**：
1. 使用 `--add-data` 添加资源文件
2. 在代码中使用 `get_resource_path()` 函数
3. 检查资源文件路径是否正确

### 4. 中文路径问题

**问题**：打包后中文路径显示乱码

**解决**：
1. 使用 `os.path` 处理路径
2. 避免硬编码路径
3. 使用相对路径

### 5. 图标不显示

**问题**：打包后 exe 文件没有图标

**解决**：
1. 使用 `.ico` 格式的图标
2. 使用 `--icon` 参数指定图标
3. 检查图标文件是否存在

---

## 打包优化

### 1. 使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 打包
pyinstaller --onefile --windowed main.py
```

### 2. 使用 UPX 压缩

```bash
# 下载 UPX: https://github.com/upx/upx/releases
# 解压到目录，如 C:\upx

# 使用 UPX 打包
pyinstaller --onefile --windowed --upx-dir=C:\upx main.py
```

### 3. 减少依赖

```bash
# 查看依赖
pip freeze > requirements.txt

# 只保留必要的依赖
# 编辑 requirements.txt，删除不需要的包
```

---

## 测试打包结果

### 1. 基本测试

```bash
# 运行打包后的程序
dist\MyApp.exe
```

### 2. 功能测试

- 启动程序
- 测试所有功能
- 检查资源文件
- 测试中文路径

### 3. 兼容性测试

- 在不同 Windows 版本上测试
- 在没有 Python 环境的电脑上测试
- 检查是否有杀毒软件误报

---

## 发布

### 1. 创建安装包（可选）

使用 NSIS 或 Inno Setup 创建安装包：

```nsis
; NSIS 示例脚本
OutFile "MyApp_Setup.exe"
InstallDir "$PROGRAMFILES\MyApp"

Section "Install"
    SetOutPath $INSTDIR
    File "dist\MyApp.exe"
    CreateShortCut "$DESKTOP\MyApp.lnk" "$INSTDIR\MyApp.exe"
SectionEnd
```

### 2. 数字签名（可选）

使用 signtool 对 exe 进行数字签名，避免杀毒软件误报。

---

## 其他打包工具

### cx_Freeze

```bash
pip install cx_Freeze

# 创建 setup.py
# 运行
python setup.py build
```

### Nuitka

```bash
pip install nuitka

# 打包
nuitka --standalone --onefile --windows-disable-console main.py
```

### py2exe

```bash
pip install py2exe

# 创建 setup.py
# 运行
python setup.py py2exe
```

---

## 总结

推荐使用 PyInstaller 打包，命令简单，社区支持好：

```bash
pyinstaller --onefile --windowed --name MyApp main.py
```

如有特殊需求，可以使用 spec 文件进行更详细的配置。
