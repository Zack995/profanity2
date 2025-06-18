# Profanity2 - 以太坊靓号地址生成器

![Screenshot](/img/screenshot.png?raw=true "Wow! That's a lot of zeros!")

## 📖 项目简介

Profanity2 是一个高性能的以太坊靓号地址生成器，利用 GPU 的并行计算能力来快速生成自定义的以太坊地址。本项目是基于原始 profanity 项目的安全改进版本，采用"安全设计"理念，确保生成过程的安全性。

### 🍎 macOS 优化特性

本项目针对 macOS 系统进行了深度优化：

- ✅ **Apple Silicon 原生支持**：完美支持 M1/M2/M3/M4 系列芯片
- ✅ **Metal 性能库集成**：利用 Apple 的 Metal Performance Shaders 优化
- ✅ **统一内存架构优化**：充分利用 Apple Silicon 的统一内存设计
- ✅ **自适应编译**：自动检测芯片架构并选择最优编译参数
- ✅ **电源管理优化**：智能调节 GPU 使用强度，减少发热和功耗
- ✅ **macOS 框架集成**：使用原生 OpenCL 框架，无需额外驱动

### 🔒 安全性说明

⚠️ **重要提醒：** 原始 profanity 项目存在已知的安全漏洞，攻击者可以从公钥恢复私钥。

本项目 "profanity2" 解决了这个问题：

- ✅ 不直接生成私钥，而是调整用户提供的种子公钥
- ✅ 用户必须提供种子公钥（128 字符十六进制字符串）
- ✅ 最终私钥 = 种子私钥 + 程序输出私钥
- ✅ 可以安全地外包给不可信的第三方运行

## 🛠️ 环境要求

### 系统要求

- **操作系统**: Linux、macOS、Windows
- **GPU**: 支持 OpenCL 的 GPU（NVIDIA、AMD、Intel 或 Apple Silicon）
- **RAM**: 至少 4GB
- **存储**: 至少 1GB 可用空间

### 依赖软件

#### macOS（Apple Silicon 优化）

```bash
# 安装 Xcode 命令行工具（必需）
xcode-select --install

# 安装 Python 依赖（用于密钥生成）
pip3 install cryptography

# 验证 OpenCL 支持
system_profiler SPDisplaysDataType | grep -A5 "Metal Family"

# 可选：安装 Homebrew（推荐用于包管理）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**macOS 特别说明：**

- ✅ **无需额外 GPU 驱动**：Apple Silicon 内置完美的 OpenCL 支持
- ✅ **自动电源管理**：系统会根据温度自动调节 GPU 频率
- ✅ **统一内存优势**：CPU 和 GPU 共享内存，数据传输速度更快
- ⚠️ **散热建议**：长时间运行建议确保良好通风或使用散热支架

#### Ubuntu/Debian

```bash
# 安装编译工具和 OpenCL
sudo apt update
sudo apt install build-essential git python3 python3-pip
sudo apt install opencl-headers ocl-icd-opencl-dev

# 安装 GPU 驱动
# NVIDIA GPU:
sudo apt install nvidia-opencl-dev

# AMD GPU:
sudo apt install mesa-opencl-icd

# 安装 Python 依赖
pip3 install cryptography
```

#### CentOS/RHEL

```bash
# 安装编译工具
sudo yum groupinstall "Development Tools"
sudo yum install git python3 python3-pip

# 安装 OpenCL
sudo yum install opencl-headers

# 安装 Python 依赖
pip3 install cryptography
```

#### Windows

```bash
# 安装 Visual Studio Build Tools 2019 或更新版本
# 安装 Python 3.7+
pip install cryptography

# 下载并安装 GPU 驱动程序
# NVIDIA: https://www.nvidia.com/drivers/
# AMD: https://www.amd.com/support/
```

## 📥 获取和编译项目

### 1. 克隆项目

```bash
git clone https://github.com/1inch/profanity2.git
cd profanity2
```

### 2. 编译项目

#### macOS（推荐用于 Apple Silicon）

```bash
# 编译（自动优化 Apple Silicon）
make

# 多线程编译（推荐）
make -j$(sysctl -n hw.ncpu)

# 如果遇到编译问题，指定 SDK 路径
export SDKROOT=$(xcrun --show-sdk-path)
make clean && make

# 验证 Apple Silicon 优化
./profanity2 --benchmark -z [任意128字符公钥]
```

**macOS 性能提示：**

- 🔥 **M4 Max (40 核 GPU)**: 高达 350 MH/s，8 字符匹配仅需~12 秒
- 🚀 **M1 Max (32 核 GPU)**: 172 MH/s，8 字符匹配约 25 秒
- ⚡ **M3 Pro (18 核 GPU)**: 97 MH/s，8 字符匹配约 45 秒
- 💡 **M1 (8 核 GPU)**: 45 MH/s，8 字符匹配约 97 秒

#### Linux

```bash
# 编译
make

# 或者使用多线程编译（更快）
make -j$(nproc)
```

#### Windows (使用 CMake)

```bash
# 创建构建目录
mkdir build
cd build

# 生成项目文件
cmake ..

# 编译
cmake --build . --config Release
```

### 3. 验证编译成功

```bash
# macOS/Linux
./profanity2 --help

# Windows
./profanity2.exe --help
```

## 🔑 生成种子密钥

### 方法 1：使用提供的 Python 脚本（推荐）

```bash
# 生成密钥对
python3 gen_eth_key.py
```

脚本会输出：

```
私钥已保存到 key.pem
公钥已保存到 pub.pem
公钥128字符hex: df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
长度: 128 字符
```

### 方法 2：使用 OpenSSL

#### 生成新的密钥对

```bash
openssl ecparam -genkey -name secp256k1 -text -noout -outform DER | xxd -p -c 1000 | sed 's/41534e31204f49443a20736563703235366b310a30740201010420/Private Key: /' | sed 's/a00706052b8104000aa144034200/\'$'\nPublic Key: /'
```

#### 从现有私钥导出公钥

```bash
openssl ec -inform DER -text -noout -in <(cat <(echo -n "302e0201010420") <(echo -n "PRIVATE_KEY_HEX") <(echo -n "a00706052b8104000a") | xxd -r -p) 2>/dev/null | tail -6 | head -5 | sed 's/[ :]//g' | tr -d '\n' && echo
```

**注意：** 从公钥中移除开头的 "04" 前缀，确保是 128 字符的十六进制字符串。

## 🚀 基本使用方法

### 基本语法

```bash
./profanity2 [模式] [参数] -z [128字符公钥]
```

### 快速开始示例

```bash
# 生成以 'f' 开头的地址
./profanity2 --leading f -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde

# 生成包含 'dead' 的地址
./profanity2 --matching dead -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde

# 生成大量零的地址
./profanity2 --zeros -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
```

## 🎯 详细功能说明

### 1. 基础模式

#### 1.1 基准测试

```bash
# 运行性能基准测试
./profanity2 --benchmark -z [公钥]
```

#### 1.2 零字符匹配

```bash
# 生成包含最多零的地址
./profanity2 --zeros -z [公钥]

# 生成包含最多零字节的地址
./profanity2 --zero-bytes -z [公钥]
```

#### 1.3 字符类型匹配

```bash
# 生成包含最多字母的地址 (a-f)
./profanity2 --letters -z [公钥]

# 生成包含最多数字的地址 (0-9)
./profanity2 --numbers -z [公钥]
```

#### 1.4 镜像地址

```bash
# 生成从中心镜像的地址
./profanity2 --mirror -z [公钥]
```

#### 1.5 重复字符对

```bash
# 生成以重复字符对开头的地址 (如: 0x001122...)
./profanity2 --leading-doubles -z [公钥]
```

### 2. 指定字符模式

#### 2.1 前导字符

```bash
# 生成以指定字符开头的地址
./profanity2 --leading 8 -z [公钥]  # 以 8 开头
./profanity2 --leading 0 -z [公钥]  # 以 0 开头
./profanity2 --leading f -z [公钥]  # 以 f 开头
```

#### 2.2 匹配特定字符串

```bash
# 匹配特定字符串
./profanity2 --matching dead -z [公钥]
./profanity2 --matching 888888 -z [公钥]

# 匹配开头和结尾的特定模式 (X 表示任意字符)
./profanity2 --matching deadXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXbeef -z [公钥]
```

### 3. 范围匹配模式

#### 3.1 前导范围

```bash
# 生成前导字符在指定范围内的地址
./profanity2 --leading-range -m 0 -M 1 -z [公钥]    # 0-1
./profanity2 --leading-range -m 10 -M 12 -z [公钥]  # a-c
```

#### 3.2 全局范围

```bash
# 生成整个地址字符都在指定范围内的地址
./profanity2 --range -m 0 -M 1 -z [公钥]     # 只包含 0-1
./profanity2 --range -m 0 -M 9 -z [公钥]     # 只包含数字
./profanity2 --range -m 10 -M 15 -z [公钥]   # 只包含字母
```

**范围参数说明：**

- `-m, --min`: 最小值 (0-15)，0='0', 15='f'
- `-M, --max`: 最大值 (0-15)，0='0', 15='f'

### 4. 增强匹配模式

#### 4.1 最大相同字符数

```bash
# 生成包含最多指定字符的地址
./profanity2 --max-same 8 -z [公钥]  # 最多的 8
./profanity2 --max-same 0 -z [公钥]  # 最多的 0
./profanity2 --max-same f -z [公钥]  # 最多的 f
```

#### 4.2 最长连续字符序列

```bash
# 生成最长连续相同字符序列的地址
./profanity2 --continuous 8 -z [公钥]  # 最长连续 8
./profanity2 --continuous 0 -z [公钥]  # 最长连续 0
./profanity2 --continuous f -z [公钥]  # 最长连续 f
```

#### 4.3 头尾匹配模式

##### 字符串头尾匹配

```bash
# 生成指定开头和结尾的地址
./profanity2 --head-tail 888,fff -z [公钥]     # 888开头，fff结尾
./profanity2 --head-tail 000,999 -z [公钥]     # 000开头，999结尾
./profanity2 --head-tail abc,def -z [公钥]     # abc开头，def结尾
./profanity2 --head-tail dead-beef -z [公钥]   # 也可以用减号分隔
./profanity2 --head-tail 427317,f7fc8a -z [公钥] # 更复杂的模式
```

##### 相同字符头尾匹配

```bash
# 生成头尾相同字符的地址
./profanity2 --sandwich 8 -z [公钥]  # 如: 0x888...888
./profanity2 --sandwich 0 -z [公钥]  # 如: 0x000...000
./profanity2 --sandwich f -z [公钥]  # 如: 0xfff...fff
```

### 5. 合约地址模式

```bash
# 生成合约地址而不是账户地址
./profanity2 --contract --leading 0 -z [公钥]
./profanity2 --contract --zero-bytes -z [公钥]
./profanity2 --contract --matching dead -z [公钥]
```

## ⚙️ 高级设置

### 设备控制

```bash
# 跳过指定设备
./profanity2 --skip 0 --leading f -z [公钥]

# 不使用缓存的预编译内核
./profanity2 --no-cache --leading f -z [公钥]
```

### 性能调优

```bash
# 设置 OpenCL 本地工作大小 (默认: 64)
./profanity2 --work 128 --leading f -z [公钥]

# 设置最大工作大小
./profanity2 --work-max 32768 --leading f -z [公钥]

# 设置模逆运算大小 (默认: 255)
./profanity2 --inverse-size 511 --leading f -z [公钥]

# 设置并行倍数 (默认: 16384)
./profanity2 --inverse-multiple 8192 --leading f -z [公钥]
```

## 🔢 私钥计算

⚠️ **安全提醒：** 绝对不要使用在线计算器来计算私钥！

### 方法 1：使用终端（推荐）

```bash
# 使用 bc 计算器（私钥为64字符十六进制，不含0x前缀）
(echo 'ibase=16;obase=10' && (echo '(种子私钥 + 程序输出私钥) % FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F' | tr '[:lower:]' '[:upper:]')) | bc
```

### 方法 2：使用 Python

```python
#!/usr/bin/env python3

# 私钥为64字符十六进制，需要0x前缀
seed_private_key = 0x你的种子私钥
program_private_key = 0x程序输出的私钥

final_private_key = (seed_private_key + program_private_key) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

print(f"最终私钥: {hex(final_private_key)}")
```

## 📊 性能参考

### 不同 GPU 性能对比

|         GPU 型号         | 时钟频率 | 显存频率 | 修改时序 |    速度    | 8 字符匹配时间 |
| :----------------------: | :------: | :------: | :------: | :--------: | :------------: |
|       GTX 1070 OC        | 1950MHz  | 4450MHz  |    否    | 179.0 MH/s |      ~24s      |
|         GTX 1070         | 1750MHz  | 4000MHz  |    否    | 163.0 MH/s |      ~26s      |
|          RX 480          | 1328MHz  | 2000MHz  |    是    | 120.0 MH/s |      ~36s      |
|         RTX 4090         |    -     |    -     |    -     | 1096 MH/s  |      ~3s       |
|   Apple M1 (8 核 GPU)    |    -     |    -     |    -     | 45.0 MH/s  |      ~97s      |
| Apple M1 Max (32 核 GPU) |    -     |    -     |    -     | 172.0 MH/s |      ~25s      |
| Apple M3 Pro (18 核 GPU) |    -     |    -     |    -     |  97 MH/s   |      ~45s      |
| Apple M4 Max (40 核 GPU) |    -     |    -     |    -     |  350 MH/s  |      ~12s      |

### 难度级别参考

#### 容易 (几秒到几分钟)

- `--leading [单字符]`: 以特定字符开头
- `--zeros`: 包含零字符
- `--letters`: 包含字母
- `--numbers`: 包含数字

#### 中等 (几分钟到几小时)

- `--matching [短字符串]`: 匹配 3-4 字符
- `--leading-doubles`: 重复字符对
- `--max-same [字符]`: 最多相同字符
- `--continuous [字符]`: 连续相同字符

#### 困难 (几小时到几天)

- `--matching [长字符串]`: 匹配 5-6 字符
- `--head-tail [模式]`: 头尾匹配
- `--range -m 0 -M 1`: 严格范围限制

#### 极难 (几天到几周)

- `--sandwich [字符]`: 相同字符头尾
- `--matching [很长字符串]`: 匹配 7+字符
- `--mirror`: 镜像地址
- `--contract` 模式的任何困难匹配

## 🔧 故障排除

### 常见问题

#### 1. 编译错误

**通用解决方案：**

```bash
# 检查依赖是否安装完整
make clean && make
```

**macOS 专用解决方案：**

```bash
# 指定 SDK 路径（推荐）
export SDKROOT=$(xcrun --show-sdk-path)
make clean && make

# 如果遇到权限问题
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# 修复 Apple Silicon 编译问题
export MACOSX_DEPLOYMENT_TARGET=11.0
make clean && make

# 如果仍有问题，检查 Xcode 命令行工具
xcode-select --install
```

#### 2. OpenCL 驱动问题

```bash
# 检查 OpenCL 设备
./profanity2 --benchmark -z [任意128字符]

# 如果没有检测到 GPU，检查驱动安装
```

#### 3. Python 脚本错误

```bash
# 安装缺失的依赖
pip3 install --upgrade cryptography

# 如果还有问题，尝试
pip3 install --user cryptography
```

#### 4. 性能过低

**通用解决方案：**

```bash
# 尝试调整工作参数
./profanity2 --inverse-multiple 8192 --leading f -z [公钥]

# 或者降低工作大小
./profanity2 --work 32 --leading f -z [公钥]
```

#### 5. macOS 专用问题

**Apple Silicon 性能优化：**

```bash
# 检查系统活动监视器，确保没有其他应用占用 GPU
# 关闭不必要的应用程序

# 检查电源管理设置
sudo pmset -g thermstate

# 如果 GPU 被限制，可以尝试：
sudo pmset -a gpuswitch 2  # 强制使用独立显卡（如果有）
```

**散热问题解决：**

```bash
# 监控温度
sudo powermetrics -n 1 -i 1000 --samplers smc_temp

# 如果温度过高，降低工作强度
./profanity2 --inverse-multiple 4096 --work 32 --leading f -z [公钥]
```

**电源问题：**

```bash
# 确保使用电源适配器而非电池运行
system_profiler SPPowerDataType | grep "Connected"

# 临时禁用节能模式
sudo pmset -a powernap 0
```

**权限问题：**

```bash
# 给予程序完全磁盘访问权限（系统偏好设置 > 安全性与隐私 > 隐私）
# 或者在终端中运行：
sudo spctl --master-disable  # 临时禁用系统完整性保护
```

## ⚠️ 安全注意事项

1. **私钥安全**：

   - 始终在离线环境中生成和计算私钥
   - 不要使用在线工具计算私钥
   - 妥善保管种子私钥文件

2. **验证结果**：

   - 始终验证生成的私钥对应正确的公钥
   - 在使用前先导入小额资金测试

3. **程序安全**：

   - 从官方渠道下载代码
   - 可以安全地在不可信环境中运行

4. **网络安全**：
   - 生成过程不需要网络连接
   - 私钥计算应在离线环境进行

## 📝 实际使用示例

### 示例 1：生成简单靓号地址

```bash
# 1. 生成种子密钥
python3 gen_eth_key.py

# 2. 生成以 888 开头的地址
./profanity2 --leading 8 -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde

# 3. 等待找到满意的地址后，记录输出的私钥
# 4. 计算最终私钥 = 种子私钥 + 输出私钥
```

### 示例 2：生成复杂头尾匹配地址

```bash
# 生成以 dead 开头，beef 结尾的地址
./profanity2 --head-tail dead,beef -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
```

### 示例 3：生成合约靓号地址

```bash
# 生成合约地址以 0 开头
./profanity2 --contract --leading 0 -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
```

### 示例 4：macOS Apple Silicon 优化使用

```bash
# macOS 完整使用流程
# 1. 验证系统环境
system_profiler SPHardwareDataType | grep "Chip"

# 2. 生成密钥
python3 gen_eth_key.py

# 3. 高性能模式运行（M1 Max/M2 Max/M3 Max/M4 Max）
./profanity2 --leading 8 --inverse-multiple 16384 --work 64 -z [128字符公钥]

# 4. 低功耗模式运行（适合 MacBook 电池使用）
./profanity2 --leading 8 --inverse-multiple 4096 --work 32 -z [128字符公钥]

# 5. 终极性能模式（M4 Max 推荐设置）
./profanity2 --leading 8 --inverse-multiple 32768 --work 128 -z [128字符公钥]
```

**macOS 性能建议：**

- 🔋 **电池模式**：使用较低的 inverse-multiple (4096-8192)
- ⚡ **电源模式**：可以使用最高设置 (16384-32768)
- 🌡️ **温度控制**：如果温度过高会自动降频，建议监控温度
- 📊 **性能监控**：使用活动监视器查看 GPU 使用率

## 📚 其他资源

- [原项目安全漏洞说明](https://blog.1inch.io/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool)
- [OpenCL 安装指南](https://github.com/1inch/profanity2/issues)
- [性能优化建议](SAME_CHAR_COMMANDS.md)

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目基于原始 profanity 项目，遵循相同的许可证条款。

## 🙏 致谢

- 原始 profanity 项目作者：Johan Gustafsson
- Profanity2 改进版本：1inch Network
- 安全性改进和增强功能：社区贡献者

---

**免责声明**：本软件可能包含错误，请始终验证生成的私钥对应正确的公钥。使用前请在测试环境中验证功能的正确性。
