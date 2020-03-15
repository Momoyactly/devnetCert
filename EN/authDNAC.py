import requests, json, urllib3, os
from termcolor import colored
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(verbose=True)
DNAC_IP = os.getenv('DNAC_IP')
DNAC_USER = os.getenv('DNAC_USER')
DNAC_PASS = os.getenv('DNAC_PASS')

def get_auth_token():
    url =  DNAC_IP + "/dna/system/api/v1/auth/token"       
    token = requests.post(url,auth=HTTPBasicAuth(DNAC_USER,DNAC_PASS)).json()['Token']
    print("Token: -> ..."+token[-10:])
    return token


if __name__ == "__main__":
    get_auth_token()