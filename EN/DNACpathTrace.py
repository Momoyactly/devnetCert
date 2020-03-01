import requests, json, urllib3
from authDNAC import get_auth_token
from termcolor import colored

from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

urllib3.disable_warnings()
token = get_auth_token() 


def createPathTraceytask():
    print("*"*50)
    url = "https://sandboxdnac2.cisco.com/api/v1/flow-analysis" 
    header = {'x-auth-token': token, 'content-type' : 'application/json'} 
    payload = {"destIP": "10.10.20.81","sourceIP": "10.10.20.82"}
    response = requests.post( url, headers=header, json = payload).json()["response"]
    print(response)

if __name__ == "__main__":
    createPathTraceytask()

