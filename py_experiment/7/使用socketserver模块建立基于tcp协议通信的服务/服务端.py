import socketserver


# 自定义类用来处理通信循环
class MyTCPhanler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                print('-->收到客户端的消息: ', data)
                self.request.send(data.upper())
            except ConnectionResetError:
                break
        self.request.close()


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8082), MyTCPhanler)
    server.serve_forever()  # 链接循环
