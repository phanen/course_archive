import time

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def main1():
    key = int("133457799bbcdff1", 16).to_bytes(length=8, byteorder="little")
    cipher = DES.new(key, DES.MODE_ECB)
    # 格式化测试集
    lst = []
    with open("testbench.txt", "r") as f:
        for plain_ in f:
            lst.append(int(plain_).to_bytes(length=8, byteorder="little"))

    ret = []
    t1 = time.time()
    for plain in lst:
        ret.append(cipher.encrypt(plain))

    # 重新生成测试集
    # for _ in range(1000):
    #     cipher.encrypt(get_random_bytes(8))
    print(f"Time measured: {time.time() - t1}")
    return ret


if __name__ == '__main__':
    ret = main1()
    # print(ret)

# def DES_encrypt(data, key):
#     '''pycryptodome库 的加密'''
#     cipher = DES.new(key, DES.MODE_ECB)
#     encrypted_data = cipher.encrypt(pad(data, DES.block_size))
#     return encrypted_data

# def DES_decrypt(encrypted_data, key):
#     cipher = DES.new(key, DES.MODE_ECB)
#     tmp = cipher.decrypt(encrypted_data)
#     data = unpad(tmp, DES.block_size)
#     return data

# key = get_random_bytes(8)  # 随机生成16字节（即128位）的加密密钥
