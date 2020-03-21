import requests, json, urllib3, os
from termcolor import colored
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(verbose=True)
DNAC_IP = os.getenv('DNAC_IP')
DNAC_USER = os.getenv('DNAC_USER')
DNAC_PASS = os.getenv('DNAC_PASS')
urllib3.disable_warnings()

def get_auth_token( DNAC_IP=DNAC_IP,DNAC_USER=DNAC_USER,DNAC_PASS=DNAC_PASS):
    url =  DNAC_IP + "/dna/system/api/v1/auth/token"       
    token = requests.post(url,auth=HTTPBasicAuth(DNAC_USER,DNAC_PASS)).json()
    print("Token: -> ..."+token)
    return token['Token']


if __name__ == "__main__":
    get_auth_token(DNAC_IP="https://dcloud-dna-center-inst-rtp.cisco.com",DNAC_USER="demo",DNAC_PASS="demo1234!")