from netmiko import ConnectHandler 

cisco = { 
      'device_type': 'cisco_ios', 
      'host': '172.16.1.104', 
      'username': 'joarriag', 
      'password': 'cisco', 
      }  

net_connect = ConnectHandler(**cisco) 
print(net_connect.find_prompt())
print(net_connect.send_command("show ip int brief"))