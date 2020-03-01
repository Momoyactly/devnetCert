import requests

def get_auth_token():
    headers = {'Authorization': 'Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE='}
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'       
    token = requests.post(url,headers=headers).json()['Token']
    print("Token: ->",token[-5:])
    return token

if __name__ == "__main__":
    get_auth_token()