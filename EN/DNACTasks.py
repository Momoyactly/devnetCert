import requests, json, urllib3, os
from authDNAC import get_auth_token
from termcolor import colored
from dotenv import load_dotenv

load_dotenv(verbose=True)
DNAC_IP = os.getenv('DNAC_IP')
urllib3.disable_warnings()
token = get_auth_token() 


def getDevices(token,DNAC_IP):
    print("*"*50)
    url = DNAC_IP + "/api/v1/network-device" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    device_list = requests.get(url, headers=header,verify=False).json()["response"]
    ids = []
    for device in device_list:
        deviceType = " ".join(device["type"].split(" ")[1:3])
        print(deviceType,"Time Up: ",device["upTime"])
        ids.append(device["id"])
    return ids

def getDeviceIntF(token,DNAC_IP,devices=getDevices(token,DNAC_IP)):
    print("*"*50)
    url = DNAC_IP + "/api/v1/interface"
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


def createPathTraceytask(token,DNAC_IP):
    print("*"*50)
    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"destIP": "10.10.20.81","sourceIP": "10.10.20.82"}
    taskUrl = requests.post( url, headers=header, json = payload).json()["response"]["url"]
    return taskUrl

def getPathTraceytask(token,DNAC_IP,taskUrl=createPathTraceytask(token,DNAC_IP)):
    print("*"*50)
    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    responseData = requests.get(url, headers=header).json()["response"]
    return responseData

if __name__ == "__main__":
    getDeviceIntF(token,DNAC_IP)
    getPathTraceytask(token,DNAC_IP)