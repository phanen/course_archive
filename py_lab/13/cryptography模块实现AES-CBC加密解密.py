import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def my_padding(data: bytes, blockSize=16):
    """将数据进行填充"""
    return data + b'\0' * ((blockSize - len(data) % blockSize) % blockSize)


def my_unpadding(data: bytes):
    """删除填充"""
    return data.rstrip(b'\0')


def encrypt_CBC(key, plaintext, iv):
    """cryptography 实现 AES-CBC加密"""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(my_padding(plaintext)) + encryptor.finalize()
    return ciphertext


def decrypt_CBC(key, ciphertext, iv):
    """cryptography 实现 AES-CBC解密"""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = my_unpadding(decryptor.update(ciphertext) + decryptor.finalize())
    return plaintext


if __name__ == '__main__':
    key = os.urandom(32)
    iv = os.urandom(16)
    plaintext = b"I am a cyberspace security student from  Shandong University"
    ciphertext = encrypt_CBC(key, plaintext, iv)
    print(ciphertext)
    cc = decrypt_CBC(key, ciphertext, iv)
    print(cc)