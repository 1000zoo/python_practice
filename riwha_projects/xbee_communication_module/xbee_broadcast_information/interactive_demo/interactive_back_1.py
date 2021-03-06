from charset_normalizer import detect
from digi.xbee.devices import *
from datetime import datetime
import interface

PORT = 'COM5'
BAUD_RATE = 9600

LANE = "lane2"          #주행 차선
VEHICLE_ID = "97가1006" #차량 번호
WEB_ADDRESS = "localhost:8080/97ga1006"
DETECTED = True         #차량 감지

#main
def main():
    global isCallbackOn
    global userInfo
    global broadbee
    isCallbackOn = False
    interface.main_if()
    broadbee = XBeeDevice(PORT, BAUD_RATE)

    try:
        broadbee.open()
        userInfo = init_user()
        lane_check()
        broadbee.add_data_received_callback(data_receive_callback)

        if is_detected():
            data_broadcast()  #송신보내는 자신의 ID
        else:
            print(("not dectected..."))
        input()

    except InvalidOperatingModeException as err:
        print(err)

    print("end of the function")

#감지 확인 함수
def is_detected():
    return DETECTED

#수신용 callback 함수
def data_receive_callback(xbee_message):
    # interface.data_receive_callback_if()
    dataReceived = string_to_dict(xbee_message.data.decode())
    print(str(datetime.now()) + "\n" + str(dataReceived))
    if dataReceived["lane"] == userInfo["lane"]:
        print("same lane")
        if not is_detected():
            data_send_reactive(dataReceived)
    else:
        print("diff lane")
        print(dataReceived["lane"], userInfo["lane"])
    isCallbackOn = False

#감지 시 송신용 함수
def data_broadcast():
    # interface.data_braodcast_if()
    broadbee.send_data_broadcast(str(userInfo))

#수신 시 송신용 함수
def data_send_reactive(data):
    # interface.data_send_reactive_if()
    print("reacting to %s" % data["nodeId"])
    net = broadbee.get_network()
    reac = net.discover_device(data["nodeId"])
    broadbee.send_data(reac, str(userInfo))

#사용자 정보를 초기화 해주는 함수
def init_user():
    interface.init_user_if()
    ui = {"vehicleId" : VEHICLE_ID, "web" : WEB_ADDRESS,
        "nodeId" : broadbee.get_node_id()}
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