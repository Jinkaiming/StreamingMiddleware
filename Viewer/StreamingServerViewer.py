import socket
import cv2
import numpy as np
import configparser
conf = configparser.ConfigParser()
conf.read('config.ini')
server_info = conf['server']


server_ip = '0.0.0.0'  # 监听所有网络接口
server_port = int(server_info['port'])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((server_ip, server_port))
    # server_socket.listen(1)
    print(f"Listening on {server_ip}:{server_port}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        data = b''
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

            # 检测 MJPEG 数据中的帧分隔符 (JPEG 文件的结尾标志)
            start_idx = data.find(b'\xff\xd8')  # JPEG 文件的起始标志
            end_idx = data.find(b'\xff\xd9')    # JPEG 文件的结束标志

            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                jpg_data = data[start_idx:end_idx + 2]
                data = data[end_idx + 2:]

                # 将 JPEG 数据解码为图像
                frame = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                if frame is not None:
                    cv2.imshow('MJPEG Stream', frame)

                    if cv2.waitKey(1) == 27:  # 按下 'Esc' 键退出
                        break

        cv2.destroyAllWindows()
