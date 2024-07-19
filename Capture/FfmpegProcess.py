import subprocess


class FfmpegProcess:
    def __init__(self, config):
        self.command = [
            'ffmpeg',
            '-f', 'v4l2',
            '-i', '/dev/video0',
            '-f', config['encoder'],
            '-b:v', config['bit_rate'],
            '-c:v', config['decoder'],
            '-r', config['frame_rate'],
            '-s', config['size'],
            '-'
        ]

        self.ffmpeg_process = None

    def run(self):
        self.ffmpeg_process = subprocess.Popen(self.command, stdout=subprocess.PIPE)

    def read(self):
        return self.ffmpeg_process.stdout.read(32768)

    def stop(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()