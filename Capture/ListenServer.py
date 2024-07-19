import socket
import json
from FfmpegProcess import FfmpegProcess

class ListenServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.target = ('0.0.0.0', 8989)
        self.sock.bind(self.target)
        self.status = True
        self.streaming_conn = False
        self.ffmpeg = None
    def start(self):
        while self.status:
            try:
                # 接受信息
                message,addr = self.sock.recvfrom(65536)
                print(addr)
                if not message:
                    continue
                config = json.loads(message)

                if config:
                    self.flash_data(config)
            except Exception as e:
                print("Error:",e)
            finally:
                if self.ffmpeg:
                    self.ffmpeg.stop()


    def flash_data(self,config):
        print(config)
        self.ffmpeg = FfmpegProcess(config)
        self.ffmpeg.run()
        print('run')
        while True:
            data = self.ffmpeg.read()
            print('read')

            if not data:
                break
            self.sock.sendto(data,self.target)
            data , addr= self.sock.recvfrom(1024)
            print( 'read2',data , addr)
            if data and data.decode().strip() =='STOP':
                print("stop!")
                self.ffmpeg.stop()
                break






def stop(self):
    self.status = False


if __name__ == '__main__':
    server = ListenServer()
    server.start()
