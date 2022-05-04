import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 接收端机器的IP地址
addr = ('127.0.0.1', 666)

while True:
    rqs = input("input your request to sever..")
    if rqs == "nothing more":
        s.close()
        break
    s.sendto(rqs.encode(), addr)
    ans, addr = s.recvfrom(1024)
    print(f"sever time{addr}:\n" + ans.decode())
