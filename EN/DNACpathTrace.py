import requests, json, urllib3, os
from authDNAC import get_auth_token
from termcolor import colored
from dotenv import load_dotenv

load_dotenv(verbose=True)
DNAC_IP = os.getenv('DNAC_IP')
urllib3.disable_warnings()
token = get_auth_token() 


def createPathTraceytask():
    print("*"*50)
    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"destIP": "10.10.20.81","sourceIP": "10.10.20.82"}
    taskUrl = requests.post( url, headers=header, json = payload).json()["response"]["url"]
    return taskUrl

def getPathTraceytask(taskUrl=createPathTraceytask()):

    url = DNAC_IP+"/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    responseData = requests.get(url, headers=header).json()["response"]
    return responseData


if __name__ == "__main__":
    getPathTraceytask()

