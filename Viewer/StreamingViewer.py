import json
import socket
import configparser
import time

from StreamingDecode import cv_show


conf = configparser.ConfigParser()
conf.read('config.ini')
stream_config = conf['streaming']
def json_streaming_config():
    config = {}
    for key in stream_config:
        config[key] = stream_config[key]

    config['decoder'] = conf['encoder'][stream_config['encoder']]
    return config

def net_protocols():
    if stream_config['type'].lower() == 'tcp':
        return socket.SOCK_STREAM
    else:
        return socket.SOCK_DGRAM





if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.connect(('192.168.43.28',8989))
    target = ('192.168.43.28',8989)
    config = json.dumps(json_streaming_config())
    sock.sendto(bytes(config.encode('utf-8')),target)

    #启动视图程序
    data = b''

    while True:
        print("start")
        packet,addr = sock.recvfrom(32768)
        print(packet,addr)
        if not packet:
            continue
        data += packet
        print('begin show')

        data,status = cv_show(conf['encoder'][stream_config['encoder']],data)

        if not status:
            sock.sendto(b"STOP",target)
            break

    sock.close()