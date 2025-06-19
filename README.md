# Profanity2 - 以太坊靓号地址生成器

![Screenshot](/img/screenshot.png?raw=true "以太坊靓号地址生成")

## 🚀 简介

Profanity2 是安全的以太坊靓号地址生成器，支持 GPU 加速，能快速生成自定义以太坊地址。

### ✨ 核心特性

- 🔒 **安全设计**：不直接生成私钥，使用种子公钥+偏移量方式确保安全
- ⚡ **GPU 加速**：支持 NVIDIA、AMD、Intel、Apple Silicon GPU
- 🎯 **多种模式**：前导字符、特定字符串、头尾匹配等
- 🔑 **自动计算**：新增自动计算最终私钥功能，无需手动计算

### 🍎 macOS 优化

- ✅ **Apple Silicon 原生支持**：M1/M2/M3/M4 系列芯片优化
- ✅ **Metal 性能库**：利用 Apple 原生图形性能
- ✅ **无需额外驱动**：开箱即用

## 🔧 安装和编译

### 系统要求

- **macOS**: Xcode 命令行工具
- **Ubuntu/Debian**: `sudo apt install build-essential opencl-headers`
- **Windows**: Visual Studio Build Tools 2019+

### 编译

```bash
# 克隆项目
git clone https://github.com/1inch/profanity2.git
cd profanity2

# 编译 (macOS/Linux)
make

# 验证编译
./profanity2 --help
```

## 🔑 使用方法

### 第一步：生成种子密钥

```bash
# 生成密钥对
python3 gen_eth_key.py
```

输出：

```
私钥已保存到 key.pem
公钥已保存到 pub.pem
公钥128字符hex: df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
```

### 第二步：提取种子私钥（新功能）

```bash
# 提取种子私钥用于自动计算
python3 extract_private_key.py
```

### 第三步：生成靓号地址

#### 方法 1：自动计算最终私钥（推荐）

```bash
# 使用 -k 参数，程序会自动计算最终私钥
./profanity2 --leading f -z [128字符公钥] -k [64字符种子私钥]
```

输出示例：

```
Time: 25s Score: 8 Private: 0x001234... Address: 0xfffffff7...
  🔑 最终私钥: 0x25af55d146c7fed0e449c4ac04e58e56d5a2887ba273963e796482acca373cc6
```

#### 方法 2：手动计算（传统方式）

```bash
# 不使用 -k 参数
./profanity2 --leading f -z [128字符公钥]

# 手动计算最终私钥
python3 calculate_final_key.py [种子私钥] [程序输出私钥]
```

## 🎯 常用模式

```bash
# 前导字符
./profanity2 --leading 8 -z [公钥] -k [种子私钥]      # 以8开头
./profanity2 --leading 0 -z [公钥] -k [种子私钥]      # 以0开头

# 特定字符串
./profanity2 --matching dead -z [公钥] -k [种子私钥]  # 包含dead
./profanity2 --matching 888888 -z [公钥] -k [种子私钥] # 包含888888

# 头尾匹配
./profanity2 --head-tail 888,fff -z [公钥] -k [种子私钥]  # 888开头fff结尾

# 最多零字符
./profanity2 --zeros -z [公钥] -k [种子私钥]          # 包含最多零

# 合约地址
./profanity2 --contract --leading 0 -z [公钥] -k [种子私钥]
```

## 📊 性能参考

| GPU 型号             | 速度      | 8 字符匹配时间 |
| -------------------- | --------- | -------------- |
| Apple M4 Max (40 核) | 350 MH/s  | ~12 秒         |
| Apple M1 Max (32 核) | 172 MH/s  | ~25 秒         |
| RTX 4090             | 1096 MH/s | ~3 秒          |
| GTX 1070             | 163 MH/s  | ~26 秒         |
| Apple M1 (8 核)      | 45 MH/s   | ~97 秒         |

## 🔧 高级设置

```bash
# 性能调优
./profanity2 --leading f -z [公钥] -k [种子私钥] \
  --work 128 \                    # 工作大小
  --inverse-multiple 16384        # 并行倍数

# 跳过设备
./profanity2 --skip 0 --leading f -z [公钥] -k [种子私钥]

# 禁用缓存
./profanity2 --no-cache --leading f -z [公钥] -k [种子私钥]
```

## ⚠️ 安全提醒

1. **最终私钥安全**：只有最终私钥才能导入钱包，不要使用程序直接输出的私钥
2. **种子私钥保护**：妥善保管 `key.pem` 文件，不要泄露
3. **离线计算**：私钥计算建议在离线环境进行
4. **小额测试**：使用前先导入小额资金测试地址正确性

## 📝 完整使用示例

```bash
# 1. 生成密钥对
python3 gen_eth_key.py

# 2. 提取种子私钥
python3 extract_private_key.py

# 3. 生成以888开头的地址并自动计算最终私钥
./profanity2 --leading 8 \
  -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde \
  -k 25af3e6788269b0a5b0bc6b232fbe32c4d53b9c8d269ead0c5b99754962b97e6

# 4. 将输出的最终私钥导入钱包
```

## 🛠️ 故障排除

**编译错误（macOS）**：

```bash
export SDKROOT=$(xcrun --show-sdk-path)
make clean && make
```

**Python 库错误**：

```bash
pip3 install --upgrade cryptography
```

**性能问题**：

```bash
# 降低参数
./profanity2 --leading f -z [公钥] -k [种子私钥] --inverse-multiple 8192
```

## 📚 参数说明

| 参数                            | 说明                          |
| ------------------------------- | ----------------------------- |
| `-z, --publicKey`               | 128 字符种子公钥（必需）      |
| `-k, --seed-private-key`        | 64 字符种子私钥（可选，推荐） |
| `--leading <字符>`              | 前导字符匹配                  |
| `--matching <字符串>`           | 特定字符串匹配                |
| `--head-tail <模式>`            | 头尾匹配，格式：head,tail     |
| `--zeros`                       | 最多零字符                    |
| `--contract`                    | 生成合约地址                  |
| `-w, --work <大小>`             | OpenCL 工作大小               |
| `-I, --inverse-multiple <倍数>` | 并行倍数                      |

## 🙏 致谢

- 原始项目：Johan Gustafsson
- 安全改进：1inch Network
- macOS 优化：社区贡献

---

**免责声明**：请始终验证生成的私钥对应正确的公钥。建议在测试环境中验证功能正确性。
