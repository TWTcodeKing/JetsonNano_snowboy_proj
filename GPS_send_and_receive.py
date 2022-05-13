#Reference:**********************************************
# @Time     : 2021/12/21 下午6:37
# @Author   : uiyu
# @File     : GPS_send_and_receive.py
# @User     : zjutrobot
# @Software: PyCharm
#Reference:**********************************************

#import gpds
import requests
import json
server_url = "127.0.0.0:5000"
headers = {"content-type":"application/json;charset=utf8"}
def Gps_position_receive():
    '''
    receive the GPS data from hardware and store it,don't send immediately when receive one data
    :return:
    '''
    GPS_Position = None
    return GPS_Position
    pass


def Gps_position_sent():
    '''
    sent a GPS position to server
    :return:
    '''
    try:
        GPS_Position = Gps_position_receive()
        AssertionError:GPS_Position != None
        GPS_Position = json.dump({'gps':{'latitude':'N30','longtitude':'E120'}})
        r = requests.post(server_url,GPS_Position,headers=headers)
        print(r.text)
    except:
        print("Nothing received")
        pass
    pass