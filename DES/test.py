from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def pycryptodome_AES_CBC(data):
    """pycryptodome库的实现"""

    def pycryptodome_encrypt(data, key, iv):
        '''pycryptodome库 的加密'''
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        return encrypted_data

    def pycryptodome_decrypt(encrypted_data, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        tmp = cipher.decrypt(encrypted_data)
        data = unpad(tmp, AES.block_size)
        return data

    key = get_random_bytes(16)  # 随机生成16字节（即128位）的加密密钥
    iv = get_random_bytes(16)
    print(key)
    print(iv)
    encrypted_data = pycryptodome_encrypt(data, key, iv)
    return pycryptodome_decrypt(encrypted_data, key, iv)


if __name__ == '__main__':
    # 测试使用 pycryptodome库实现 AES_CBC 加密解密
    test_data = b"I am a student from shandongUniversityasdasd"
    out1 = pycryptodome_AES_CBC(test_data)
    print(out1)
