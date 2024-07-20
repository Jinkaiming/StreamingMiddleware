import socket
import json
from FfmpegProcess import FfmpegProcess

class ListenServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.target = ('0.0.0.0', 8989)
        self.sock.bind(self.target)
        self.status = True
        self.streaming_conn = False
        self.ffmpeg = None
    def start(self):
        self.sock.listen(5)
        while self.status:
            conn, addr = self.sock.accept()
            print(conn,addr)
            try:
                # 接受信息
                message = conn.recv(65536)
                print(addr)
                if not message:
                    continue
                config = json.loads(message)
                print('Get Config',config)
                if config:
                    self.flash_data(config,conn)
            except Exception as e:
                print("Error:",e)
            finally:
                if self.ffmpeg:
                    self.ffmpeg.stop()


    def flash_data(self,config,conn):
        # start a stream sock
        stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ffmpeg = FfmpegProcess(config)
        self.ffmpeg.run()
        conn.setblocking(False)
        while True:
            data = self.ffmpeg.read()
            if not data:
                break
            stream_socket.sendto(data,(config['ip'],int(config['port'])))
            try:
                data= conn.recv(1024)
                print('STOP Message',data )
                if data and data.decode().strip() =='STOP':
                    print("stop!")
                    self.ffmpeg.stop()
                    return False
            except BlockingIOError as e:
                pass








def stop(self):
    self.status = False


if __name__ == '__main__':
    server = ListenServer()
    server.start()
