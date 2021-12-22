import socket

if __name__ == '__main__':
    ip = '192.168.254.246'
    frm = 443 # 端口范围起点
    to = 446 # 端口范围终点
    for pt in range(frm, to + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, pt))  # 尝试连接
            print(f'{ip}:{pt} OPEN')
        except:
            print(f'{ip}:{pt} CLOSED')
        finally: # 断开连接
            s.close()
