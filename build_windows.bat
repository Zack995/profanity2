@echo off
REM Profanity2 Windows 构建脚本
REM 支持 Visual Studio 2019/2022 和 MinGW

echo ==============================================
echo Profanity2 Windows 构建脚本
echo ==============================================

REM 检查是否安装了CMake
cmake --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 CMake，请先安装 CMake
    echo 下载地址: https://cmake.org/download/
    pause
    exit /b 1
)

REM 检查是否安装了Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 创建构建目录
if exist build rmdir /s /q build
mkdir build
cd build

echo.
echo 正在配置项目...
echo.

REM 尝试使用 Visual Studio 构建
cmake .. -G "Visual Studio 16 2019" -A x64 2>nul
if %errorlevel% equ 0 (
    echo 使用 Visual Studio 2019 构建...
    cmake --build . --config Release
    goto :copy_files
)

REM 尝试使用 Visual Studio 2022
cmake .. -G "Visual Studio 17 2022" -A x64 2>nul
if %errorlevel% equ 0 (
    echo 使用 Visual Studio 2022 构建...
    cmake --build . --config Release
    goto :copy_files
)

REM 尝试使用 MinGW
cmake .. -G "MinGW Makefiles" 2>nul
if %errorlevel% equ 0 (
    echo 使用 MinGW 构建...
    cmake --build .
    goto :copy_files
)

REM 尝试使用 Ninja
cmake .. -G "Ninja" 2>nul
if %errorlevel% equ 0 (
    echo 使用 Ninja 构建...
    cmake --build .
    goto :copy_files
)

echo.
echo 错误: 未找到合适的构建工具
echo 请安装以下任一工具:
echo - Visual Studio 2019/2022 with C++ workload
echo - MinGW-w64
echo - Ninja build system
echo.
pause
exit /b 1

:copy_files
echo.
echo 正在复制文件...

REM 复制可执行文件到根目录
if exist bin\Release\profanity2.exe (
    copy bin\Release\profanity2.exe ..\profanity2.exe
    echo 可执行文件已复制到: profanity2.exe
) else if exist bin\profanity2.exe (
    copy bin\profanity2.exe ..\profanity2.exe
    echo 可执行文件已复制到: profanity2.exe
) else if exist profanity2.exe (
    copy profanity2.exe ..\profanity2.exe
    echo 可执行文件已复制到: profanity2.exe
) else (
    echo 警告: 未找到 profanity2.exe
)

REM 复制OpenCL文件
copy ..\profanity.cl ..\profanity.cl >nul 2>&1
copy ..\keccak.cl ..\keccak.cl >nul 2>&1

cd ..

echo.
echo ==============================================
echo 构建完成！
echo ==============================================
echo.
echo 使用方法:
echo 1. 首先生成密钥: python gen_eth_key.py
echo 2. 运行程序: profanity2.exe --help
echo.
echo 示例命令:
echo profanity2.exe --leading f -z [您的128字符公钥]
echo.
pause 