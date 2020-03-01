import requests, json, urllib3
from authDNAC import get_auth_token
from termcolor import colored

urllib3.disable_warnings()
token = get_auth_token() 


def getDevices():
    print("*"*50)
    url = "https://sandboxdnac.cisco.com/api/v1/network-device" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    device_list = requests.get(url, headers=header,verify=False).json()["response"]
    ids = []
    for device in device_list:
        deviceType = " ".join(device["type"].split(" ")[1:3])
        print(deviceType,"Time Up: ",device["upTime"])
        ids.append(device["id"])
    print("*"*50)
    return ids

def getDeviceIntF(devices=getDevices()):
    print("*"*50)
    url = "https://sandboxdnac.cisco.com/api/v1/interface"
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    devices_if = requests.get(url, headers=header,verify=False).json()["response"]
    for device in devices:
        print("Device Id: ",device)
        for intf in devices_if:
            if intf["deviceId"] == device:
                if intf["adminStatus"] == "UP":
                    print(colored(intf["portName"],"green"))
                elif intf["adminStatus"] == "DOWN":
                    print(colored(intf["portName"],"red"))
                else :
                    print(colored(intf["portName"],"yellow"))

    print("*"*50)


if __name__ == "__main__":
    getDeviceIntF(["1cfd383a-7265-47fb-96b3-f069191a0ed5"])