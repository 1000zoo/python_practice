from charset_normalizer import detect
from digi.xbee.devices import *
from datetime import datetime
import interface
import os

PORT = 'COM6'
BAUD_RATE = 9600

LANE = "lane2"          #주행 차선
VEHICLE_ID = "12나3456" #차량 번호
WEB_ADDRESS = "http://28no8114.cns-link.net"
DETECTED = False         #차량 감지

WebServerAddress = "/var/www/html/"

#main
def main():
    global isCallbackOn
    global userInfo
    global broadbee
    interface.main_if()
    broadbee = XBeeDevice(PORT, BAUD_RATE)

    try:
        broadbee.open()
        userInfo = init_user()
        lane_check()
        broadbee.add_data_received_callback(data_receive_callback)

        if is_detected():
            data_broadcast()
        else:
            print("not dectected...")
        input()
        # time.sleep(5)
        print("end of the function")
            
    except InvalidOperatingModeException as err:
        print(err)

#감지 확인 함수
def is_detected():
    return DETECTED

#수신용 callback 함수
def data_receive_callback(xbee_message):
    interface.data_receive_callback_if()
    dataReceived = string_to_dict(xbee_message.data.decode())
    print(datetime.now())
    print(dataReceived)
    if dataReceived["lane"] == userInfo["lane"]:
        print("same lane")
        if dataReceived["dataType"] == "broadcast":
            data_send_reactive(dataReceived)
            qqq = userInfo["web"]
            csv2 = (31.23123, 127.213232)
            k = requests.get(dataReceived["web"] + "/giveinfo.php?webid=" + qqq + "," + csv2)
            
        elif dataReceived["dataType"] == "react":
            fir_time = os.path.getmtime(WebServerAddress + "webid.txt")
            while True:
                if(fir_time != os.path.getmtime(WebServerAddress + "webid.txt")):
                    ss = open(WebServerAddress + "webid.txt", "r")
                    aa = str(ss.readline())
    else:
        print("diff lane")
        print(dataReceived["lane"], userInfo["lane"])

#감지 시 송신용 함수
def data_broadcast():
    interface.data_braodcast_if()
    userInfo["dataType"] = "broadcast"
    broadbee.send_data_broadcast(str(userInfo))

#수신 시 송신용 함수
def data_send_reactive(data):
    interface.data_send_reactive_if()
    print("reacting to %s" % data["nodeId"])
    userInfo["dataType"] = "react"
    net = broadbee.get_network()
    reac = net.discover_device(data["nodeId"])
    broadbee.send_data(reac, str(userInfo))

#사용자 정보를 초기화 해주는 함수
def init_user():
    interface.init_user_if()
    ui = {"vehicleId" : VEHICLE_ID, "web" : WEB_ADDRESS,
        "nodeId" : broadbee.get_node_id(), "dataType" : "None"}
    return ui

def lane_check():
    userInfo["lane"] = LANE

def string_to_dict(s):
    dic = {}
    s = s.strip("{""}")
    ls = s.split(",")
    for w in ls:
        try:    
            w = w.split(":")
            dic[w[0].strip(" '")] = w[1].strip(" '")
        except IndexError as err:
            print(err)
            return
    return dic
    
if __name__ == '__main__':
    main()