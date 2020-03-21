import requests, os, urllib3, urllib.parse
from dotenv import load_dotenv
print("*"*50)

load_dotenv(verbose=True)
ViptelaIP = os.getenv('ViptelaIP')
ViptelaUSER = urllib.parse.quote(os.getenv('ViptelaUSER'))
ViptelaPASS = urllib.parse.quote(os.getenv('ViptelaPASS'))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_auth_token(ViptelaIP=ViptelaIP,ViptelaUSER=ViptelaUSER,ViptelaPASS=ViptelaPASS):
    url = ViptelaIP + "/j_security_check"
    payload = 'j_username={}&j_password={}'.format(ViptelaUSER,ViptelaPASS)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    sesion = requests.session()
    response = sesion.post( url, headers=headers, data = payload,verify=False)
    if not response.ok or response.text:
        print("login failure")
        import sys
        sys.exit(1)
    else:
        print("Login Worked")
        return sesion


if __name__ == "__main__":
    sesion = get_auth_token()

