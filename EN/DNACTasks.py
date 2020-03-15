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
    interfaces={}
    interfaces["response"]=[]
    for device in devices:
        print("Device Id: ",device)
        deviceInterfaces = {}
        deviceInterfaces["deviceId"] = device
        deviceInterfaces["data"] = []
        for intf in devices_if:
            interface = {}
            if intf["deviceId"] == device:
                interface["port"]=intf["portName"]
                interface["status"]=intf["adminStatus"]
                interface["id"]=intf["id"]
                if intf["adminStatus"] == "UP":
                    print(colored(intf["portName"],"green"))
                elif intf["adminStatus"] == "DOWN":
                    print(colored(intf["portName"],"red"))
                else :
                    print(colored(intf["portName"],"yellow"))
                deviceInterfaces["data"].append(interface)
        interfaces["response"].append(deviceInterfaces)
    return interfaces

def createPathTraceytask(token,DNAC_IP,destIP="10.10.20.81",sourceIP="10.10.20.82"):
    print("*"*50)
    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"destIP": destIP,"sourceIP": sourceIP}
    taskUrl = requests.post( url, headers=header, json = payload).json()["response"]["url"]
    return taskUrl

def getPathTraceytask(token,DNAC_IP,taskUrl=createPathTraceytask(token,DNAC_IP)):
    print("*"*50)
    url = DNAC_IP + taskUrl
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    pathTraceData = requests.get(url, headers=header).json()["response"]
    imprimible = []
    for netElement in pathTraceData["networkElementsInfo"]:
        imprimibleTemp = []
        try:
            imprimibleTemp.append(netElement["ingressInterface"]["physicalInterface"]["name"])
        except :
            pass
        imprimibleTemp.append(netElement["name"].upper())
        try:
            imprimibleTemp.append(netElement["egressInterface"]["physicalInterface"]["name"])
        except :
            pass
        imprimible.append("\n".join(imprimibleTemp))
    print("\n      v\n      v\n".join(imprimible))
    return pathTraceData

if __name__ == "__main__":
    getPathTraceytask(token,DNAC_IP)