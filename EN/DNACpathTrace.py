import requests, json, urllib3
from authDNAC import get_auth_token
from termcolor import colored

urllib3.disable_warnings()
token = get_auth_token() 

