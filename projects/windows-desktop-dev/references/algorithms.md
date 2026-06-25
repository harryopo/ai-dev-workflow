# 算法参考指南

## 概述

本文档介绍桌面应用中常用的算法。只在需要时才引入，不要过度设计。

## 搜索算法

### 线性搜索
适用场景：小数据量（< 1000 条）

```python
def linear_search(items, target):
    """线性搜索"""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
```

### 二分搜索
适用场景：已排序的大数据量

```python
def binary_search(sorted_items, target):
    """二分搜索（需要已排序）"""
    left, right = 0, len(sorted_items) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 全文搜索
适用场景：搜索文本内容

```python
import re

def full_text_search(text, keyword):
    """全文搜索（不区分大小写）"""
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.findall(text)
```

---

## 排序算法

### 内置排序（推荐）
Python 内置排序已经足够高效，大多数情况直接使用。

```python
# 升序排序
sorted_items = sorted(items)

# 降序排序
sorted_items = sorted(items, reverse=True)

# 按key排序
sorted_items = sorted(items, key=lambda x: x['name'])
```

### 快速排序
适用场景：需要自己实现排序时

```python
def quicksort(arr):
    """快速排序"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

---

## 数据验证

### 正则表达式

```python
import re

# 验证邮箱
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# 验证手机号
def is_valid_phone(phone):
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

# 验证身份证号
def is_valid_id_card(id_card):
    pattern = r'^\d{17}[\dXx]$'
    return re.match(pattern, id_card) is not None
```

---

## 加密算法

### 哈希加密
适用场景：密码存储、数据校验

```python
import hashlib

def hash_password(password):
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """验证密码"""
    return hash_password(password) == hash_value
```

### 对称加密
适用场景：数据加密存储

```python
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(b"敏感数据")

# 解密
decrypted = cipher.decrypt(encrypted)
```

---

## 压缩算法

### ZIP 压缩

```python
import zipfile

# 压缩文件
def compress_file(input_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(input_path)

# 解压文件
def extract_file(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(output_dir)
```

### GZIP 压缩

```python
import gzip

# 压缩
def compress_gzip(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)

# 解压
def extract_gzip(input_path, output_path):
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)
```

---

## 图像处理

### Pillow 库

```python
from PIL import Image

# 打开图片
img = Image.open("image.jpg")

# 调整大小
img_resized = img.resize((800, 600))

# 裁剪
img_cropped = img.crop((100, 100, 400, 400))

# 旋转
img_rotated = img.rotate(90)

# 保存
img.save("output.jpg")
```

---

## 数据统计

### 基本统计

```python
import statistics

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 平均值
mean = statistics.mean(data)

# 中位数
median = statistics.median(data)

# 标准差
stdev = statistics.stdev(data)
```

### 频率统计

```python
from collections import Counter

data = ['a', 'b', 'a', 'c', 'b', 'a']
counter = Counter(data)

# 获取频率最高的元素
most_common = counter.most_common(2)  # [('a', 3), ('b', 2)]
```

---

## 日期时间处理

### 日期格式化

```python
from datetime import datetime

# 当前时间
now = datetime.now()

# 格式化
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# 解析
dt = datetime.strptime("2024-01-01", "%Y-%m-%d")
```

### 日期计算

```python
from datetime import datetime, timedelta

now = datetime.now()

# 7天后
future = now + timedelta(days=7)

# 30天前
past = now - timedelta(days=30)

# 日期差
diff = future - past
days = diff.days
```

---

## 文件操作

### 遍历目录

```python
import os

def list_files(directory):
    """遍历目录"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)
```

### 读写 JSON

```python
import json

# 读取
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 写入
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 读写 CSV

```python
import csv

# 读取
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# 写入
with open('data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerow({'name': '张三', 'age': 25})
```

---

## 何时使用算法

| 场景 | 是否需要算法 | 推荐方案 |
|------|-------------|----------|
| 搜索 100 条数据 | 否 | 直接遍历 |
| 搜索 10000 条数据 | 是 | 二分搜索或索引 |
| 排序数据 | 否 | 使用 sorted() |
| 验证输入格式 | 是 | 正则表达式 |
| 存储密码 | 是 | hashlib |
| 压缩文件 | 是 | zipfile |
| 处理图像 | 是 | Pillow |

**原则：能用内置库就用内置库，能用简单方案就用简单方案。**
