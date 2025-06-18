# Profanity2 Windows 安装和使用指南

## 📋 系统要求

### 最低要求

- **操作系统**: Windows 10/11 (64 位)
- **内存**: 4GB RAM
- **显卡**: 支持 OpenCL 1.2 或更高版本的 GPU
- **存储**: 至少 2GB 可用空间

### 推荐配置

- **操作系统**: Windows 11 (64 位)
- **内存**: 8GB RAM 或更多
- **显卡**: NVIDIA GTX 1060 或 AMD RX 580 或更高
- **存储**: 4GB 可用空间（SSD 推荐）

## 🛠️ 快速安装

### 方法 1：自动安装（推荐）

1. **以管理员身份运行 PowerShell**

   ```powershell
   # 右键点击开始菜单 -> Windows PowerShell (管理员)
   # 或按 Win+X，选择 "Windows PowerShell (管理员)"
   ```

2. **运行自动安装脚本**

   ```powershell
   .\install_dependencies.ps1
   ```

3. **构建项目**
   ```cmd
   build_windows.bat
   ```

### 方法 2：手动安装

#### 步骤 1：安装必需软件

1. **Visual Studio Build Tools 2022**

   - 下载：https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
   - 安装时选择：C++ 生成工具、CMake 工具

2. **CMake 3.10+**

   - 下载：https://cmake.org/download/
   - 选择 "Add CMake to system PATH"

3. **Python 3.7+**

   - 下载：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

4. **Git（可选）**
   - 下载：https://git-scm.com/download/win

#### 步骤 2：安装 GPU 驱动

根据您的显卡类型下载最新驱动：

- **NVIDIA**: https://www.nvidia.com/drivers/
- **AMD**: https://www.amd.com/support/
- **Intel**: https://www.intel.com/content/www/us/en/support/articles/000005524/

#### 步骤 3：验证安装

打开命令提示符并运行：

```cmd
cmake --version
python --version
git --version
```

## 🚀 编译和运行

### 1. 获取代码

```cmd
git clone https://github.com/Zack995/profanity2.git
cd profanity2
```

### 2. 构建项目

#### 使用批处理脚本（推荐）

```cmd
build_windows.bat
```

#### 手动构建

```cmd
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
cd ..
```

### 3. 生成密钥

```cmd
python gen_eth_key.py
```

输出示例：

```
私钥已保存到 key.pem
公钥已保存到 pub.pem
公钥128字符hex: df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
长度: 128 字符
```

### 4. 运行程序

```cmd
# 查看帮助
profanity2.exe --help

# 生成以 'f' 开头的地址
profanity2.exe --leading f -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde

# 基准测试
profanity2.exe --benchmark -z df49896fb5c9aea080e0d931be39495b6c726a7739b69cc08ac7481ca4b3a2687e606e91c646e45c516645a8881e34290fc57313c81f6ee87b659b3da5033fde
```

## 🎯 Windows 特定优化

### GPU 性能优化

1. **NVIDIA GPU 优化**

   ```cmd
   # 确保使用高性能模式
   nvidia-smi -pm 1

   # 最大化 GPU 时钟频率
   nvidia-smi -ac 4004,1911
   ```

2. **AMD GPU 优化**

   - 使用 AMD Radeon Software 启用 "Gaming Mode"
   - 确保显卡温度不超过 85°C

3. **Intel GPU 优化**
   - 更新到最新的 Intel Graphics Driver
   - 在 Intel Graphics Control Panel 中设置为高性能模式

### 电源管理

在 Windows 电源选项中：

1. 打开"控制面板" -> "电源选项"
2. 选择"高性能"电源计划
3. 设置"关闭硬盘"为"从不"
4. 设置"睡眠"为"从不"

### 防火墙设置

如果 Windows 防火墙阻止程序运行：

1. 打开"Windows 安全中心"
2. 选择"防火墙和网络保护"
3. 点击"允许应用通过防火墙"
4. 添加 `profanity2.exe` 到允许列表

## 🔧 故障排除

### 常见问题

#### 1. 编译错误

**错误**: `MSB8020: The build tools for v142 (Platform Toolset = 'v142') cannot be found`

**解决方案**:

```cmd
# 安装 Visual Studio 2019 生成工具
choco install visualstudio2019buildtools -y
```

**错误**: `Could NOT find OpenCL`

**解决方案**:

```cmd
# 更新 GPU 驱动程序
# NVIDIA: 下载 GeForce Experience
# AMD: 下载 AMD Radeon Software
```

#### 2. 运行时错误

**错误**: `No OpenCL devices found`

**解决方案**:

1. 确保 GPU 驱动程序是最新版本
2. 重启计算机
3. 检查设备管理器中 GPU 是否正常工作

**错误**: `Access is denied`

**解决方案**:

```cmd
# 以管理员身份运行命令提示符
# 或者给程序添加防火墙例外
```

#### 3. 性能问题

**问题**: GPU 使用率低

**解决方案**:

1. 关闭其他 GPU 密集型应用程序
2. 设置 Windows 为高性能模式
3. 使用以下参数调整性能：

```cmd
# 降低工作负载
profanity2.exe --inverse-multiple 8192 --work 32 --leading f -z [公钥]

# 提高工作负载（仅适用于高端 GPU）
profanity2.exe --inverse-multiple 32768 --work 128 --leading f -z [公钥]
```

### GPU 特定优化

#### NVIDIA GPU

```cmd
# 查看 GPU 信息
nvidia-smi

# 设置最大性能模式
nvidia-smi -pm 1
nvidia-smi -ac 4004,1911
```

#### AMD GPU

- 使用 AMD WattMan 超频工具
- 确保 GPU 温度控制在合理范围

#### Intel GPU

- 仅适用于支持 OpenCL 的新款 Intel GPU
- 性能相对较低，建议用于测试

## 📊 性能基准

### 典型性能数据

|  GPU 型号  | 平均速度  | 8 字符匹配时间 |        推荐设置         |
| :--------: | :-------: | :------------: | :---------------------: |
|  RTX 4090  | 1096 MH/s |      ~3s       | inverse-multiple: 32768 |
|  RTX 3080  | 650 MH/s  |      ~7s       | inverse-multiple: 16384 |
|  GTX 1070  | 163 MH/s  |      ~26s      | inverse-multiple: 8192  |
| RX 6800 XT | 520 MH/s  |      ~8s       | inverse-multiple: 16384 |
|   RX 580   | 145 MH/s  |      ~30s      | inverse-multiple: 8192  |

### 性能测试命令

```cmd
# 运行基准测试（推荐每次使用前运行）
profanity2.exe --benchmark -z [任意128字符公钥]

# 测试不同难度级别
profanity2.exe --leading 0 -z [公钥]  # 容易
profanity2.exe --matching dead -z [公钥]  # 中等
profanity2.exe --head-tail abc,def -z [公钥]  # 困难
```

## 💡 使用技巧

### 1. 批量生成

创建批处理文件 `batch_generate.bat`：

```cmd
@echo off
for /l %%i in (1,1,10) do (
    echo 正在运行第 %%i 次生成...
    profanity2.exe --leading f -z [您的公钥] --timeout 300
)
```

### 2. 日志记录

```cmd
profanity2.exe --leading f -z [公钥] > log.txt 2>&1
```

### 3. 后台运行

```cmd
start /b profanity2.exe --leading f -z [公钥]
```

### 4. 多实例运行

```cmd
# 终端1
profanity2.exe --leading 8 -z [公钥1]

# 终端2
profanity2.exe --leading 9 -z [公钥2]
```

## 🔒 安全建议

1. **离线使用**: 断开网络连接运行程序
2. **密钥安全**: 妥善保管 `key.pem` 文件
3. **验证结果**: 使用钱包验证生成的地址
4. **备份重要**: 多地备份密钥文件

## 📞 获取帮助

如果遇到问题：

1. 查看 [GitHub Issues](https://github.com/Zack995/profanity2/issues)
2. 检查 Windows 事件查看器中的错误日志
3. 运行 `profanity2.exe --benchmark` 诊断 GPU 问题
4. 确保所有驱动程序都是最新版本

---

**注意**: 本程序仅用于教育和研究目的。使用前请确保了解相关风险。
