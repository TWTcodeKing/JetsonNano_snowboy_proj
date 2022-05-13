from trtyoloAPI import trtYOLODetector
from utils.camera import add_camera_args, Camera
from utils.display import open_window
import argparse
import cv2
import threading
from GPS_send_and_receive import Gps_position_receive,Gps_position_sent
from audio.utils import Speak,Listen
import time
from audio import snowboydecoder
import signal
from constant import detector_lock,audio_lock
from touch import PAJ7620U2



base_command = ['周围人流情况','周围车辆情况','周围路况']
class BlinderDog():
    def __init__(self,detector,body):
        self.eyes = detector
        self.body = body
    def EarFunction(self):
        def signal_handler(signal, frame):
            global interrupted
            interrupted = True

        def interrupt_callback():
            global interrupted
            return interrupted

        model = './resources/models/snowboy.umdl'
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
        print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=self.AudioModule,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)

        detector.terminate()
    def Get_Gesture(self):
        command = self.body.check_gesture()
        if command == base_command[0]:
            car_count = self.eyes.Detect_passer()
            audio_lock.acquire()
            Speak("您的前方有" + str(car_count) + "个行人")
            audio_lock.release()
        elif command == '车辆数量':
            car_count = self.eyes.Detect_car()
            audio_lock.acquire()
            Speak("您的前方有" + str(car_count) + "辆车")
            audio_lock.release()
        else:
            pass #do nothing if no correct command received

    def AudioModule(self):

        Speak("有什么能够帮助你的吗?")
        words = Listen()

        flag = False
        if words == base_command[0]:
            flag = True
            detector_lock.acquire()
            man_count = self.eyes.Detect_passer
            detector_lock.release()
            audio_lock.acquire()
            Speak("您的前方有" + str(man_count) + "个行人")
            audio_lock.release()
            pass
        elif words == base_command[1]:
            flag = True
            detector_lock.acquire()
            car_count = self.eyes.Detect_car()
            detector_lock.release()
            audio_lock.acquire()
            Speak("您的前方有"+str(car_count)+"辆车")
            audio_lock.release()
            pass


        if not flag:
            if "人流" in words:
                detector_lock.acquire()
                man_count = self.eyes.Detect_passer()
                detector_lock.release
                audio_lock.acquire()
                Speak("您的前方有" + str(man_count) + "个行人")
                audio_lock.release()
                pass

            elif "车流" in words:
                detector_lock.release()
                car_count = self.eyes.Detect_car()
                detector_lock.release()
                audio_lock.acquire()
                Speak("您的前方有" + str(car_count) + "辆车")
                audio_lock.release()
                pass



def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args





class DetectorThread(threading.Thread):  # 继承父类threading.Thread
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
       open_window(detector.WINDOW_NAME, 'Transport Demo', cam.img_width, cam.img_height)
       BlinderDog.eyes.Loop_detect_With_Camera(cam)
       BlinderDog.eyes.cam.release()
       cv2.destroyAllWindows()

class GestureThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while 1:
            time.sleep(5)
            Dog.Get_Gesture()


class GPSThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while 1:
            Gps_position_sent()


if __name__=='__main__':
    args=parse_args()
    cam = Camera(args)
    detector = trtYOLODetector(args,cam)
    body = PAJ7620U2()
    Dog = BlinderDog(detector,body)
    del detector
    if not cam.isOpened():
        raise SystemExit('Camera not open')

    Tdetector= DetectorThread(1,'eyes')
    TGPS = GPSThread(3,'GPS')
    Tbody = GPSThread(2,'gesture')

    Dog.EarFunction()
    Tdetector.start()
    TGPS.start()
    Tbody.start()

    Tdetector.join()
    TGPS.join()
    Tbody.join()

