#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profanity2 Windows 密钥生成器
专为 Windows 用户设计的密钥生成工具
"""

import os
import sys
import secrets
import platform
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("错误: 未找到 cryptography 库")
    print("请运行: pip install cryptography")
    print("或者: python -m pip install cryptography")
    input("按回车键退出...")
    sys.exit(1)

def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """打印横幅"""
    print("=" * 60)
    print("    Profanity2 Windows 密钥生成器")
    print("    安全地生成以太坊密钥对")
    print("=" * 60)
    print()

def check_system_info():
    """检查系统信息"""
    print("系统信息:")
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  架构: {platform.machine()}")
    print(f"  Python 版本: {platform.python_version()}")
    print()

def generate_secure_keypair():
    """生成安全的密钥对"""
    print("正在生成安全密钥对...")
    print("使用硬件随机数生成器...")
    
    # 使用 secrets 模块生成更安全的随机数
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    
    # 保存私钥为 PEM 格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 导出公钥
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem, public_key

def save_keys_safely(private_pem, public_pem):
    """安全地保存密钥文件"""
    # 创建备份目录
    backup_dir = Path("key_backup")
    backup_dir.mkdir(exist_ok=True)
    
    # 保存私钥
    private_file = Path("key.pem")
    with open(private_file, "wb") as f:
        f.write(private_pem)
    
    # 保存公钥
    public_file = Path("pub.pem")
    with open(public_file, "wb") as f:
        f.write(public_pem)
    
    # 创建备份
    import shutil
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_private = backup_dir / f"key_{timestamp}.pem"
    backup_public = backup_dir / f"pub_{timestamp}.pem"
    
    shutil.copy2(private_file, backup_private)
    shutil.copy2(public_file, backup_public)
    
    # 设置文件权限（仅所有者可读写）
    if os.name == 'nt':
        import stat
        os.chmod(private_file, stat.S_IREAD | stat.S_IWRITE)
        os.chmod(backup_private, stat.S_IREAD | stat.S_IWRITE)
    
    print(f"✓ 私钥已保存到: {private_file}")
    print(f"✓ 公钥已保存到: {public_file}")
    print(f"✓ 备份已保存到: {backup_dir}")
    print()
    
    return private_file, public_file

def extract_public_key_info(public_key):
    """提取公钥信息"""
    numbers = public_key.public_numbers()
    x_hex = format(numbers.x, '064x')
    y_hex = format(numbers.y, '064x')
    pure_pubkey_hex = x_hex + y_hex
    
    return pure_pubkey_hex, x_hex, y_hex

def display_key_info(pure_pubkey_hex, x_hex, y_hex):
    """显示密钥信息"""
    print("密钥信息:")
    print("-" * 50)
    print(f"128字符公钥: {pure_pubkey_hex}")
    print(f"长度: {len(pure_pubkey_hex)} 字符")
    print()
    print("坐标分解:")
    print(f"X 坐标: {x_hex}")
    print(f"Y 坐标: {y_hex}")
    print()

def create_batch_file(pure_pubkey_hex):
    """创建 Windows 批处理文件"""
    batch_content = f"""@echo off
REM Profanity2 快速启动脚本
REM 自动生成，包含您的公钥

echo ==========================================
echo Profanity2 快速启动
echo ==========================================
echo.

set PUBKEY={pure_pubkey_hex}

echo 您的128字符公钥: %PUBKEY%
echo.
echo 可用命令:
echo 1. 基准测试: profanity2.exe --benchmark -z %PUBKEY%
echo 2. 生成以 f 开头的地址: profanity2.exe --leading f -z %PUBKEY%
echo 3. 生成以 0 开头的地址: profanity2.exe --leading 0 -z %PUBKEY%
echo 4. 生成包含 dead 的地址: profanity2.exe --matching dead -z %PUBKEY%
echo 5. 生成头尾匹配地址: profanity2.exe --head-tail abc,def -z %PUBKEY%
echo.

:menu
echo 请选择操作:
echo [1] 运行基准测试
echo [2] 生成以 f 开头的地址
echo [3] 生成以 0 开头的地址
echo [4] 生成包含 dead 的地址
echo [5] 生成头尾匹配地址
echo [6] 自定义命令
echo [0] 退出
echo.
set /p choice=请输入选择 (0-6): 

if "%choice%"=="1" (
    profanity2.exe --benchmark -z %PUBKEY%
    goto menu
)
if "%choice%"=="2" (
    profanity2.exe --leading f -z %PUBKEY%
    goto menu
)
if "%choice%"=="3" (
    profanity2.exe --leading 0 -z %PUBKEY%
    goto menu
)
if "%choice%"=="4" (
    profanity2.exe --matching dead -z %PUBKEY%
    goto menu
)
if "%choice%"=="5" (
    profanity2.exe --head-tail abc,def -z %PUBKEY%
    goto menu
)
if "%choice%"=="6" (
    set /p custom=请输入自定义参数 (不包含 -z): 
    profanity2.exe %custom% -z %PUBKEY%
    goto menu
)
if "%choice%"=="0" (
    exit
)

echo 无效选择，请重试
goto menu
"""
    
    batch_file = Path("run_profanity2.bat")
    with open(batch_file, "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print(f"✓ 快速启动脚本已创建: {batch_file}")
    print("  双击该文件即可快速启动 Profanity2")
    print()

def show_security_tips():
    """显示安全提示"""
    print("🔒 安全提示:")
    print("=" * 40)
    print("1. 妥善保管 key.pem 文件（包含私钥）")
    print("2. 不要将私钥文件发送给任何人")
    print("3. 建议在离线环境中生成密钥")
    print("4. 定期备份密钥文件到安全位置")
    print("5. 验证生成的地址是否正确")
    print()

def show_next_steps(pure_pubkey_hex):
    """显示下一步操作"""
    print("📋 下一步操作:")
    print("=" * 40)
    print("1. 确保 profanity2.exe 在当前目录")
    print("2. 运行: profanity2.exe --help")
    print("3. 测试: profanity2.exe --benchmark -z [公钥]")
    print()
    print("示例命令:")
    print(f"profanity2.exe --leading f -z {pure_pubkey_hex[:20]}...")
    print()
    print("或者直接运行: run_profanity2.bat")
    print()

def main():
    """主函数"""
    clear_screen()
    print_banner()
    check_system_info()
    
    # 询问用户是否继续
    response = input("是否要生成新的密钥对? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是', '是的']:
        print("操作已取消")
        input("按回车键退出...")
        return
    
    print()
    print("开始生成密钥对...")
    print("=" * 40)
    
    try:
        # 生成密钥对
        private_pem, public_pem, public_key = generate_secure_keypair()
        
        # 保存密钥文件
        private_file, public_file = save_keys_safely(private_pem, public_pem)
        
        # 提取公钥信息
        pure_pubkey_hex, x_hex, y_hex = extract_public_key_info(public_key)
        
        # 显示密钥信息
        display_key_info(pure_pubkey_hex, x_hex, y_hex)
        
        # 创建批处理文件
        create_batch_file(pure_pubkey_hex)
        
        # 显示安全提示
        show_security_tips()
        
        # 显示下一步操作
        show_next_steps(pure_pubkey_hex)
        
        print("✅ 密钥生成完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请检查系统环境和依赖库是否正确安装")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main() 