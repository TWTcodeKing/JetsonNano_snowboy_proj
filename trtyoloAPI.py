#Reference:**********************************************
# @Time     : 2021/10/13 下午8:35
# @Author   : uiyu
# @File     : trtyoloAPI.py
# @User     : zjutrobot
# @Software: PyCharm
#Reference:**********************************************
import argparse
import pyttsx3
import cv2
import time
from utils.yolo_classes import get_cls_dict

from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
from audio.utils import Speak
from constant import detector_lock,audio_lock

class trtYOLODetector():
    def __init__(self,args,camera):
        self.WINDOW_NAME = 'Transport Detection'
        self.trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)
        self.cls_dict = get_cls_dict(args.category_num)
        self.drawer = BBoxVisualization(self.cls_dict)
        self.vis = BBoxVisualization(self.cls_dict)
        self.Speaker = pyttsx3.init()
        self.camera = camera
        pass


    def predictImage(self,image,threshold):
        boxes, confs, clss = self.trt_yolo.detect(image, threshold)
        return boxes,confs,clss
        pass

    def Detect_passer(self):
        img = self.camera.read()
        if img is None:
            print("Image undetected! Check your camera")
        detector_lock.acquire()
        boxes, confs, clss = self.predictImage(img, threshold=0.5)
        detector_lock.release()
        person_count = 0
        for item in clss:
            if self.cls_dict[item] == 'person':
                person_count += 1
        return person_count


    def Detect_car(self):
        img = self.camera.read()
        if img is None:
            print("Image undetected! Check your camera")
        detector_lock.acquire()
        boxes, confs, clss = self.predictImage(img, threshold=0.5)
        detector_lock.release()
        car_count = 0
        for item in clss:
            if self.cls_dict[item] == 'bicycle':
                car_count += 1
            elif self.cls_dict[item] == 'car':
                car_count += 1
            elif self.cls_dict[item] == 'motorbike_count':
                car_count += 1
            elif self.cls_dict[item] == 'bus':
                car_count += 1
            elif self.cls_dict[item] == 'truck_count':
                car_count += 1
        return car_count


    def Loop_detect_With_Camera(self,conf_th=0.5):
        full_sreen = False
        fps = 0.0
        tic = time.time()
        while True:
            if cv2.getWindowProperty(self.WINDOW_NAME,0) < 0:
                break
            img = self.camera.read()
            if img is None:
                print("Image undetected! Check your camera")
                break
            detector_lock.acquire()
            boxes,confs,clss = self.predictImage(img,conf_th)
            detector_lock.release()
            img = self.vis.draw_bboxes(img,boxes,confs,clss)
            img = show_fps(img,fps)
            cv2.imshow(self.WINDOW_NAME,img)

            #every thing on the road that will move
            person_count = 0
            bicycle_count = 0
            car_count = 0
            motorbike_count = 0
            bus_count = 0
            truck_count = 0
            for item in clss:
                if self.cls_dict[item] == 'person':
                    person_count+=1
                elif self.cls_dict[item] == 'bicycle':
                    bicycle_count +=1
                elif self.cls_dict[item] == 'car':
                    car_count +=1
                elif self.cls_dict[item] == 'motorbike_count':
                    motorbike_count +=1
                elif self.cls_dict[item] == 'bus':
                    bus_count +=1
                elif self.cls_dict[item] == 'truck_count':
                    truck_count +=1

            print("您前方有"+str(person_count)+"个行人")
            if  person_count > 5:
                audio_lock.acquire()
                Speak("前方行人较多,请您注意安全")
                audio_lock.release()
            if bicycle_count + car_count + motorbike_count + bus_count + truck_count >5:
                audio_lock.acquire()
                Speak("前方车辆较多，请您注意安全，慢步行走")
                audio_lock.release()

            toc = time.time()
            curr_fps = 1.0/(toc-tic)
            fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
            tic = toc
            key = cv2.waitKey(1)
            if key == 27:
                break
            elif key == ord('F') or key == ord('f'):
                full_sreen = not full_sreen
                set_display(self.WINDOW_NAME,full_sreen)
        pass
