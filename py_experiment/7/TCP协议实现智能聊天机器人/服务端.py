import socket
from os.path import commonprefix
import threading

import hmac, os


def conn_auth(conn):
    '''
    认证客户端链接
    :param conn:
    :return:
    '''
    secret_key = b'python password'
    print('开始验证新链接的合法性')
    msg = os.urandom(32)
    conn.sendall(msg)
    h = hmac.new(secret_key, msg, "md5")
    digest = h.digest()
    respone = conn.recv(len(digest))
    return hmac.compare_digest(respone, digest)


def data_handler(s, conn):
    words = {'how are you ?': 'Fine,thank you.',
             'how old are you ?': '19',
             'what is your name ?': 'nxh',
             "what's your name ?": 'pardon?',
             'where do you work ?': 'no work',
             'bye': 'Bye',
             "sever quit": "quiting.........",
             'quit': 'OK, have a rest'}
    threshold = 1
    if not conn_auth(conn):  # 认证失败
        print('该链接不合法,关闭')
        conn.close()
        return
    print('链接合法,开始通信')
    while True:
        data = conn.recv(1024).decode()
        if not data:  # 客户端退出，不再发数据
            conn.close()
            # quitflag = 1
            break
        if data.lower() == 'sever quit':
            conn.close()
            s.close()
            # quitflag = 2
            break
        print('Received message:', data)
        # 尽量猜测对方要表达的真正意思
        m = 0
        key = ''
        for k in words.keys():
            # 删除多余的空白字符
            data = ' '.join(data.split())
            # 与某个“键”非常接近，就直接返回
            if len(commonprefix([k, data])) > len(k) * 0.7:
                key = k
                break

            # 使用选择法，选择一个重合度较高的“键”
            length = len(set(data.split()) & set(k.split()))
            if length > m:
                m = length
                key = k
        else:
            if m < threshold:  # 小于阈值，则不匹配
                key = ""
        # 选择合适的信息进行回复
        conn.sendall(words.get(key, 'Sorry.').encode())


#

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定socket
s.bind((HOST, PORT))
# 开始监听一个客户端连接
s.listen(5)
print('Listening on port:', PORT)

thread_list = []
while True:
    try:
        conn, addr = s.accept()
    except:
        break
    print('Connected by', addr)
    # 起线程
    t = threading.Thread(target=data_handler, args=(s, conn,))
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()

print("Stop the server....")

# 	基本的服务端实现：
# 1. s = socket.socket()
# 2. s.bind()
# 3. s.listen()
# 4. conn, addr = s.accept()
# 5. conn.recv(1024)
# 6. conn.sendall()
# 7. conn.close()
# 8. s.close()
# 	基本的客户端实现：
# Server:
# 1. s = socket.socket()
# 2. s.bind()
# 3. s.listen()
# 4. conn, addr = s.accept()
# 5. conn.recv(1024)
# 6. conn.sendall()
# 7. conn.close()
# 8. s.close()
