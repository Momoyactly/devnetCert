import requests, os
from authViptela import get_auth_token
from dotenv import load_dotenv
print("*"*50)

load_dotenv(verbose=True)
ViptelaIP = os.getenv('ViptelaIP')
sesion = get_auth_token()

def getDevices(sesion,ViptelaIP=ViptelaIP,imprimir=False):
    url = ViptelaIP+"/dataservice/device"
    response = sesion.get(url,verify=False).json()
    if imprimir:
        data = response["data"]
        for device in data:
            print("hostname:",device["host-name"])
            print("IP      :",device["local-system-ip"])
            print("Model   :",device["device-model"])
            print("")
    return response["data"]

def getDevicesCounters(sesion,ViptelaIP=ViptelaIP,imprimir=False):
    url = ViptelaIP+"/dataservice/device/counters"
    response = sesion.get(url,verify=False).json()
    if imprimir:
        data = response["data"]
        for device in data:
            print("system-ip:",device["system-ip"])
            print("rebootCount:",device["rebootCount"])
            print("crashCount:",device["crashCount"])
            print("")
    return response["data"]


def getInterfaces(sesion,ViptelaIP=ViptelaIP,imprimir=False):
    url = ViptelaIP+"/dataservice/statistics/interface"
    response = sesion.get(url,verify=False).json()
    if imprimir:
        data = response["data"]
        for device in data:
            print("vdevice_name:",device["vdevice_name"])
            print("interface:   ",device["interface"])
            print("oper_status: ",device["oper_status"])
            print("")
    return response["data"]

if __name__ == "__main__":
    getInterfaces(sesion,imprimir=True)
    