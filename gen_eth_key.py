from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_keypair():
    # 生成secp256k1私钥
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    
    # 保存私钥为PEM格式
    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("私钥已保存到 key.pem")

    # 导出公钥
    public_key = private_key.public_key()
    with open("pub.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("公钥已保存到 pub.pem")

    # 提取公钥的 x, y 坐标，并输出 128 字符 hex
    numbers = public_key.public_numbers()
    x_hex = format(numbers.x, '064x')
    y_hex = format(numbers.y, '064x')
    pure_pubkey_hex = x_hex + y_hex
    print(f"公钥128字符hex: {pure_pubkey_hex}")
    print(f"长度: {len(pure_pubkey_hex)} 字符")

if __name__ == "__main__":
    generate_keypair()
