import numpy as np
import cv2
import socket
import configparser
conf = configparser.ConfigParser()
conf.read('config.ini')
server_info = conf['server']

# TCP 套接字设置
TCP_IP = "0.0.0.0"  # 监听所有 IP 地址
TCP_PORT = int(server_info['port'])  # 与发送端相同的端口号
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

conn, addr = sock.accept()

while True:
    # 接收数据
    data = b''
    while True:
        packet = conn.recv(65536)
        if not packet:

            break
        print('packet')
        data += packet

    if not data:
        break

    # 解码 JPEG
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 显示帧
    if frame is not None:
        cv2.imshow('Received Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭窗口和套接字
cv2.destroyAllWindows()
conn.close()
sock.close()
