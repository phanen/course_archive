import socket

# 使用IPV4协议，使用UDP协议传输数据
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 666))  # 绑定端口和端口号，空字符串表示本机任何可用IP地址
# 接受请求
while True:
    rqs, addr = s.recvfrom(1024)
    # 处理请求
    if rqs.decode().lower() == 'time':  # 发送系统当前时间
        s.sendto(str(time.ctime()).encode(), addr)
    elif rqs.decode().lower() == 'quit':
        s.close()
        break
    else:
        s.sendto("No such service".encode(), addr)
