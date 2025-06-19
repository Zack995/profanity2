#!/usr/bin/env python3
"""
计算最终私钥
最终私钥 = 种子私钥 + 程序输出私钥 (mod N)
其中 N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
"""

import sys

# secp256k1 的阶数
SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

def calculate_final_private_key(seed_private_key_hex, program_private_key_hex):
    """
    计算最终私钥
    
    Args:
        seed_private_key_hex: 种子私钥（64字符十六进制，不含0x）
        program_private_key_hex: 程序输出私钥（64字符十六进制，不含0x）
    
    Returns:
        最终私钥的十六进制字符串
    """
    
    # 移除可能的0x前缀并转换为整数
    seed_key = seed_private_key_hex.replace('0x', '').replace('0X', '')
    program_key = program_private_key_hex.replace('0x', '').replace('0X', '')
    
    try:
        seed_private_key = int(seed_key, 16)
        program_private_key = int(program_key, 16)
    except ValueError as e:
        print(f"❌ 错误：私钥格式不正确 - {e}")
        return None
    
    # 计算最终私钥
    final_private_key = (seed_private_key + program_private_key) % SECP256K1_ORDER
    
    # 转换为64字符十六进制字符串
    final_private_key_hex = format(final_private_key, '064x')
    
    return final_private_key_hex

def main():
    print("🔑 Profanity2 最终私钥计算器")
    print("=" * 50)
    print()
    
    if len(sys.argv) == 3:
        # 命令行参数模式
        seed_key = sys.argv[1]
        program_key = sys.argv[2]
    else:
        # 交互模式
        print("请输入您的私钥信息（64字符十六进制，可含或不含0x前缀）：")
        print()
        
        seed_key = input("种子私钥（从 key.pem 提取的）: ").strip()
        if not seed_key:
            print("❌ 种子私钥不能为空")
            return
        
        program_key = input("程序输出私钥（profanity2 找到的）: ").strip()
        if not program_key:
            print("❌ 程序输出私钥不能为空")
            return
    
    # 计算最终私钥
    final_key = calculate_final_private_key(seed_key, program_key)
    
    if final_key:
        print("\n" + "=" * 50)
        print("✅ 计算完成！")
        print("=" * 50)
        print(f"种子私钥:     {seed_key.replace('0x', '').replace('0X', '').lower()}")
        print(f"程序输出私钥: {program_key.replace('0x', '').replace('0X', '').lower()}")
        print(f"最终私钥:     {final_key}")
        print(f"最终私钥(0x): 0x{final_key}")
        print()
        print("⚠️  重要提示：")
        print("1. 请使用 '最终私钥' 导入到您的钱包中")
        print("2. 导入时可以使用带0x前缀或不带前缀的格式")
        print("3. 请妥善保管您的私钥，不要泄露给他人")
        print("4. 建议先用小额资金测试确认地址正确")
        print()
    else:
        print("❌ 计算失败，请检查输入的私钥格式")

if __name__ == "__main__":
    main() 