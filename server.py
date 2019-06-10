from flask import Flask
import threading
import socket
import time

#工作线程处理客户端请求
def tplink(sock, addr):
    print("success connect to %s:%s"%(addr));
    sock.send("hello "+addr)
    while True:
        buffer = sock.recv(1024)
        time.sleep(1)
        if not buffer or buffer.decode("utf-8") == "exit":
            sock.send("goodbye")
            break
    sock.close()
    print("connect from %s:%s closed"%(addr) )

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('127.0.0.1',9999))
    sock.listen(5)
    print("Waiting for client")

    while True:
        s,addr = sock.accept()
        t = threading.Thread(target = tplink , args = (s, addr) )
        t.start()
        

