import requests, json, urllib3, os
from authDNAC import get_auth_token
from termcolor import colored
from dotenv import load_dotenv

DNAC_IP = os.getenv('DNAC_IP')
token = get_auth_token(DNAC_IP=DNAC_IP) 
defaultCommandToRun = ["show ver | inc Software", "show clock"]


def getDevices(token,DNAC_IP=DNAC_IP,imprimir= False,idsArray=False):
    print("*"*50)
    url = DNAC_IP + "/api/v1/network-device" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    device_list = requests.get(url, headers=header,verify=False).json()
    ids = []
    for device in device_list["response"]:
        if imprimir:
            deviceType = " ".join(device["type"].split(" ")[1:3])
            print(deviceType,"Time Up: ",device["upTime"])
        if idsArray:
            ids.append(device["id"])
    if idsArray:
        return ids
    else:
        return device_list["response"]

def getDeviceByIP(token,DNAC_IP=DNAC_IP,IP="10.10.20.51"):
    print("*"*50)
    url = DNAC_IP + "/dna/intent/api/v1/network-device/ip-address/"+ IP
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    device = requests.get(url, headers=header,verify=False).json()
    return device["response"]

def getDeviceIntF(token,DNAC_IP=DNAC_IP,devices=getDevices(token)):
    print("*"*50)
    url = DNAC_IP + "/api/v1/interface"
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    devices_if = requests.get(url, headers=header,verify=False).json()["response"]
    interfaces={}
    interfaces["response"]=[]
    for device in devices:
        print("Device Id: ",device["id"])
        deviceInterfaces = {}
        deviceInterfaces["deviceId"] = device["id"]
        deviceInterfaces["data"] = []
        for intf in devices_if:
            interface = {}
            if intf["deviceId"] == device["id"]:
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


def commandRunner(token,DNAC_IP=DNAC_IP,ids=getDevices(token,idsArray=True),commands=defaultCommandToRun):
    print("*"*50)
    url = DNAC_IP + "/dna/intent/api/v1/network-device-poller/cli/read-request"
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"name": "show ver","commands":commands,"deviceUuids" : ids}
    device = requests.post(url, headers=header,json=payload,verify=False).json()
    return device

def getTaskById(token,DNAC_IP=DNAC_IP,taskId=commandRunner(token)):
    print("*"*50)
    url = DNAC_IP + "/dna/intent/api/v1/task/"+ taskId
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    device = requests.post(url, headers=header,verify=False).json()
    return device["response"]

def createPathTraceytask(token,DNAC_IP,destIP="10.10.20.81",sourceIP="10.10.20.82"):
    print("*"*50)
    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"destIP": destIP,"sourceIP": sourceIP}
    taskUrl = requests.post( url, headers=header, json = payload).json()["response"]["url"]
    return taskUrl

def getPathTraceytask(token,DNAC_IP=DNAC_IP,taskUrl=createPathTraceytask(token,DNAC_IP)):
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

def getTemplates(token,DNAC_IP=DNAC_IP):
    print("*"*50)
    url = DNAC_IP + "/dna/intent/api/v1/template-programmer/template"
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    templates = requests.get(url, headers=header,verify=False).json()
    ids = []
    for template in templates:
        ids.append(template["templateId"])
    return ids

def getTemplateById(token,idi,DNAC_IP=DNAC_IP,imprimir=False):
    print("*"*50)
    url = DNAC_IP + "/dna/intent/api/v1/template-programmer/template/"+idi
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    template = requests.get(url, headers=header,verify=False).json()
    params = []
    for parameter in template["templateParams"]:
        params.append(parameter["parameterName"])
        if imprimir:
            print(parameter["parameterName"],parameter["dataType"],parameter["required"])
    return params


if __name__ == "__main__":
    print(getTemplateById(token,idi="ae8c6f3c-8698-417c-b21f-38eeb8b4770c",imprimir=True))