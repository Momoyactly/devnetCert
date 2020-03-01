import requests, os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DNAC_IP = os.getenv('DNAC_IP')

def get_auth_token():
    headers = {'Authorization': 'Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE='}
    url =  DNAC_IP + "/dna/system/api/v1/auth/token"       
    token = requests.post(url,headers=headers).json()['Token']
    print("Token: ->",token[-5:])
    return token

if __name__ == "__main__":
    get_auth_token()