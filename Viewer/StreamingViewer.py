import json
import socket
import configparser
import time

from StreamingDecode import cv_show


conf = configparser.ConfigParser()
conf.read('config.ini')
stream_config = conf['streaming']
def json_streaming_config():
    ret = {}
    for key in stream_config:
        ret[key] = stream_config[key]

    ret['decoder'] = conf['encoder'][stream_config['encoder']]
    ret['ip'] = conf['local']['ip']
    return json.dumps(ret)

def net_protocols():
    if stream_config['type'].lower() == 'tcp':
        return socket.SOCK_STREAM
    else:
        return socket.SOCK_DGRAM





if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.43.28',8989))
    target = ('192.168.43.28',8989)
    config = json_streaming_config()
    sock.sendall(bytes(config.encode('utf-8')))

    #启动视图程序
    data = b''
    stream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    stream_sock.bind(('0.0.0.0',int(stream_config['port'])))


    while True:
        print("Wait Stream..")
        packet,addr = stream_sock.recvfrom(32768)
        print("Get Stream!")
        if not packet:
            continue
        data += packet
        print('Begin show')

        data,status = cv_show(conf['encoder'][stream_config['encoder']],data)
        if not status:
            sock.sendall(b"STOP")
            break

    sock.close()