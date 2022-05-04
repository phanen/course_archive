from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt(data, public_key) -> bytes:
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))  # 实例化加密套件
    encrypted_data = cipher.encrypt(data)  # 加密
    return encrypted_data


def decrypt(encrypted_data, private_key) -> bytes:
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))  # 实例化加密套件
    data = cipher.decrypt(encrypted_data)  # 解密
    return data


if __name__ == '__main__':
    # 生密钥
    key = RSA.generate(1024)
    private_key = key.export_key()  # 提取私钥
    public_key = key.publickey().export_key()  # 提取公钥
    print(public_key,private_key)
    test_data = b"I am a student from shandong university"

    a = encrypt(test_data, public_key)
    b = decrypt(a, private_key)

    print(a)
    print(b)