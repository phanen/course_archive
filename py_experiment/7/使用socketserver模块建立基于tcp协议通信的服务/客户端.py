from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8082))
# 通信循环
while True:
    sdata = input("请输入要发送的数据:")
    if sdata == 'q':
        break
    client.send(sdata.encode('utf-8'))
    data = client.recv(1024)
    print(data.decode())
client.close()
