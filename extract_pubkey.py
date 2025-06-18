from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

with open("pub.pem", "rb") as f:
    pub_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

numbers = pub_key.public_numbers()
x = numbers.x
y = numbers.y

# 转为64字节（128字符）十六进制字符串
x_hex = format(x, '064x')
y_hex = format(y, '064x')

pure_pubkey_hex = x_hex + y_hex
print(pure_pubkey_hex)
print(f"长度: {len(pure_pubkey_hex)}")
