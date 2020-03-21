import requests, os, urllib3, urllib.parse, json
from dotenv import load_dotenv 
from requests.auth import HTTPBasicAuth 
from termcolor import colored

class baseRestAPI:
    def __init__(self, url, username, password,loginPath):
        self.url = url
        self.loginPath = loginPath
        self.session = {}
        self.headers =  {'content-type' : 'application/json'} 
        self.login(username, password) 
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def login(self, username, password):
        #Login Method    
        urlFull =  self.url + self.loginPath   
        self.headers["x-auth-token"] = requests.post(urlFull,auth=HTTPBasicAuth(username,password)).json()["Token"]

    def getRequest(self, actionPath):
        #GET request
        data = requests.get(self.url+actionPath, headers=self.headers,verify=False).json()
        return data

    def post_request(self, actionPath, payload):
        #POST request
        data = requests.post(self.url+actionPath, data=payload, headers=self.headers, verify=False).json()
        return data

class DNACRestAPI(baseRestAPI):
    def __init__(self, url, username, password):
        baseRestAPI.__init__(self, url, username, password,loginPath="/dna/system/api/v1/auth/token")

    def getDevices(self,imprimir=False,fullInfo=False):
        device_list = self.getRequest("/api/v1/network-device")
        ids = []
        for device in device_list["response"]:
            if imprimir:
                deviceType = " ".join(device["type"].split(" ")[1:3])
                print(deviceType,"Time Up: ",device["upTime"])
            if not fullInfo:
                ids.append(device["id"])
        if fullInfo:
            return device_list["response"]
        else:
            return ids
    
    def getDeviceByIP(self,IP="10.10.20.51",imprimir=False,fullInfo=False):
        device= self.getRequest("/dna/intent/api/v1/network-device/ip-address/"+IP)
        return device["response"]

    def getDeviceIntF(self, devices, imprimir=False, fullInfo=False):
        devices_if = self.getRequest("/api/v1/interface")
        interfaces={}
        interfaces["response"]=[]
        for device in devices:
            if imprimir: print("Device Id: ",device["id"])
            deviceInterfaces = {}
            deviceInterfaces["deviceId"] = device["id"]
            deviceInterfaces["data"] = []
            for intf in devices_if["response"]:
                interface = {}
                if intf["deviceId"] == device["id"]:
                    interface["port"]   = intf["portName"]
                    interface["status"] = intf["adminStatus"]
                    interface["id"]     = intf["id"]
                    if imprimir:
                        if   intf["adminStatus"] == "UP"  : print(colored(intf["portName"],"green" ))
                        elif intf["adminStatus"] == "DOWN": print(colored(intf["portName"],"red"   ))
                        else                              : print(colored(intf["portName"],"yellow"))
                    deviceInterfaces["data"].append(interface)
            interfaces["response"].append(deviceInterfaces)
        return interfaces

if __name__ == "__main__":
    load_dotenv(verbose=True)
    DNAC_IP = os.getenv('DNAC_IP')
    DNAC_USER = os.getenv('DNAC_USER')
    DNAC_PASS = os.getenv('DNAC_PASS')
    DNAC = DNACRestAPI(DNAC_IP,DNAC_USER,DNAC_PASS)
    DNAC.getDeviceIntF(devices=DNAC.getDevices(fullInfo=True))