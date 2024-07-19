import subprocess
import socket
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
stream_info = conf['streaming']


ffmpeg_command = [
    'ffmpeg',
    '-f', 'v4l2',
    '-i', '/dev/video0',
    '-f', stream_info['encoder'],
    '-b:v', stream_info['bit_rate'],
    '-c:v',conf['encoder'][stream_info['encoder']],
    '-r',stream_info['frame_rate'],
    '-s',stream_info['size'],
    '-'
]




if __name__ == '__main__':

    #监听消息，
    #接受配置
    #更具配置将数据流刷新到对应设备上去

    #监听关闭指令，关闭ffpmeg

    server_info = conf['server']
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect((server_info['ip'],int(server_info['port'])))
    ffmpeg_process = subprocess.Popen(ffmpeg_command,stdout=subprocess.PIPE)

    try:
        while True:
            #send streaming
            data = ffmpeg_process.stdout.read(65536)
            if not data:
                break

            sock.sendall(data)

    except Exception as e:
        print(e)

    finally:
        ffmpeg_process.terminate()
        sock.close()
