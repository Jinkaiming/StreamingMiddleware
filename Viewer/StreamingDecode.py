import cv2
import numpy as np

def mjpeg(data):
    start_idx = data.find(b'\xff\xd8')  # JPEG 文件的起始标志
    end_idx = data.find(b'\xff\xd9')  # JPEG 文件的结束标志
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        jpg_data = data[start_idx:end_idx + 2]
        data = data[end_idx + 2:]
        # 将 JPEG 数据解码为图像
        frame = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('MJPEG Stream', frame)
            if cv2.waitKey(1) == 27:  # 按下 'Esc' 键退出
                cv2.destroyAllWindows()
                return (data,False)

    return (data,True)


def cv_show(encoder,data):
    if encoder == 'mjpeg':
        return mjpeg(data)