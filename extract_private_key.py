#!/usr/bin/env python3
"""
从 key.pem 文件中提取私钥的十六进制字符串
用于与 profanity2 程序输出进行私钥计算
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def extract_private_key():
    try:
        # 读取私钥文件
        with open("key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        
        # 使用正确的方法获取私钥数值
        # 将私钥序列化为DER格式，然后提取私钥数值
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # 从DER格式中提取32字节的私钥
        # PKCS8 DER格式中，私钥在特定位置
        # 查找私钥的起始位置（通常在尾部32字节）
        private_key_bytes = private_bytes[-32:]  # 取最后32字节
        
        # 但更安全的方法是使用 private_numbers()
        try:
            private_numbers = private_key.private_numbers()
            private_value = private_numbers.private_value
        except AttributeError:
            # 如果 private_numbers() 也不行，尝试其他方法
            print("❌ 错误：无法提取私钥数值，请检查 cryptography 库版本")
            print("尝试使用以下命令更新库：pip3 install --upgrade cryptography")
            return None
        
        # 确保私钥在有效范围内
        if private_value <= 0 or private_value >= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
            print("❌ 错误：私钥值超出有效范围")
            return None
        
        # 转换为64字符十六进制字符串（32字节 = 64个十六进制字符）
        private_key_hex = format(private_value, '064x')
        
        print("从 key.pem 提取的种子私钥:")
        print(f"私钥: {private_key_hex}")
        print(f"长度: {len(private_key_hex)} 字符")
        
        # 验证长度
        if len(private_key_hex) != 64:
            print(f"❌ 警告：私钥长度不正确！应该是64字符，实际是{len(private_key_hex)}字符")
            return None
            
        print()
        print("✅ 私钥提取成功！")
        print("⚠️  重要提示：")
        print("1. 这是您的种子私钥，请妥善保管")
        print("2. 最终私钥 = 种子私钥 + 程序输出私钥")
        print("3. 只有计算出的最终私钥才能导入钱包")
        print()
        
        return private_key_hex
        
    except FileNotFoundError:
        print("❌ 错误：找不到 key.pem 文件")
        print("请先运行 'python3 gen_eth_key.py' 生成密钥对")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        print(f"错误类型：{type(e)}")
        return None

def verify_key_pair():
    """验证密钥对的一致性"""
    try:
        # 读取私钥
        with open("key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        
        # 读取公钥
        with open("pub.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
        # 从私钥导出公钥
        derived_public_key = private_key.public_key()
        
        # 比较公钥
        original_numbers = public_key.public_numbers()
        derived_numbers = derived_public_key.public_numbers()
        
        if (original_numbers.x == derived_numbers.x and 
            original_numbers.y == derived_numbers.y):
            print("✅ 密钥对验证成功：私钥和公钥匹配")
            
            # 显示128字符公钥hex
            x_hex = format(original_numbers.x, '064x')
            y_hex = format(original_numbers.y, '064x')
            pubkey_hex = x_hex + y_hex
            print(f"对应的128字符公钥: {pubkey_hex}")
            print(f"公钥长度: {len(pubkey_hex)} 字符")
            
            return True
        else:
            print("❌ 错误：私钥和公钥不匹配")
            return False
            
    except Exception as e:
        print(f"❌ 密钥对验证失败：{e}")
        return False

def alternative_extract():
    """备用的私钥提取方法"""
    try:
        import subprocess
        print("\n🔧 尝试使用 OpenSSL 方法提取私钥...")
        
        # 使用 openssl 命令提取私钥
        result = subprocess.run([
            'openssl', 'ec', '-in', 'key.pem', '-text', '-noout'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            private_key_lines = []
            capturing = False
            
            for line in lines:
                if 'priv:' in line:
                    capturing = True
                    # 提取第一行的十六进制数据
                    if ':' in line:
                        hex_part = line.split(':', 1)[1].strip()
                        private_key_lines.append(hex_part)
                elif capturing and (':' in line or line.strip().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'))):
                    private_key_lines.append(line.strip())
                elif capturing and ('pub:' in line or 'ASN1 OID:' in line):
                    break
            
            # 合并所有十六进制字符
            hex_string = ''.join(private_key_lines).replace(':', '').replace(' ', '').replace('\n', '')
            
            if len(hex_string) == 64:
                print(f"✅ OpenSSL 方法成功提取私钥: {hex_string}")
                return hex_string
            else:
                print(f"❌ OpenSSL 提取的私钥长度不正确: {len(hex_string)} 字符")
                print(f"提取的内容: {hex_string}")
        else:
            print(f"❌ OpenSSL 命令失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ OpenSSL 方法失败: {e}")
    
    return None

if __name__ == "__main__":
    print("🔑 私钥提取和验证工具")
    print("=" * 50)
    
    # 提取私钥
    private_key_hex = extract_private_key()
    
    # 如果主要方法失败，尝试备用方法
    if not private_key_hex:
        private_key_hex = alternative_extract()
    
    if private_key_hex:
        print("\n" + "=" * 50)
        print("🔍 验证密钥对一致性")
        print("=" * 50)
        verify_key_pair()
    else:
        print("\n❌ 所有方法都失败了，请检查：")
        print("1. key.pem 文件是否存在且格式正确")
        print("2. cryptography 库版本：pip3 install --upgrade cryptography")
        print("3. 是否安装了 openssl 命令行工具") 