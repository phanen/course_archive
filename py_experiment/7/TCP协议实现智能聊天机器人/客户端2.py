import socket
import sys
import hmac, os

secret_key = b'python password'


def conn_auth(s):
    """
    验证客户端到服务器的链接
    :param conn:
    :return:
    """
    msg = s.recv(32)
    h = hmac.new(secret_key, msg, "md5")
    digest = h.digest()
    s.sendall(digest)


# 服务端主机IP地址和端口号
HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # 连接服务器
    s.connect((HOST, PORT))
except Exception as e:
    print('Server not found or not open')
    sys.exit()

conn_auth(s)

while True:
    c = input('Input the content you want to send:')
    try:
        # 发送数据
        s.sendall(c.encode())
        # 从服务端接收数据
        data = s.recv(1024)
    except:
        break
    data = data.decode()
    print('Received:', data)
    if c.lower() == 'bye' or c.lower() == 'you can quit':
        break
# 关闭连接
s.close()