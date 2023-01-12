import json 
import requests
import argparse
from colorama import *
import sys
import os


api_path = "ApiKey.json"


# STANDART RENK KODLARI

color_red = Fore.RED
color_blue = Fore.BLUE
color_green = Fore.GREEN
color_reset = Fore.RESET


AllArgumants = argparse.ArgumentParser()
AllArgumants.add_argument("--ip",required=True,help="Hedef host ip adresi. --ip '1.1.1.1'")
argumanlar = vars(AllArgumants.parse_args())
input_ip = argumanlar["ip"]

if not os.path.exists("log/") and not os.path.isdir("log/"):
    os.mkdir("log")

a = "-"*20
def GetIpQuery(ip_addrs):
    with open(api_path,"r") as KeyFile:
        al_keys = json.load(KeyFile)
        if al_keys["ipinfo.io"] == "NULL":
            return "LUTFEN ipinfo.io API KEYINIZI ApiKey.json A GIRINIZ"
        
        ipinfoApiKey = al_keys["ipinfo.io"]
        MainUrl = f"https://ipinfo.io/{ip_addrs}?token={ipinfoApiKey}"
        IpQuery = requests.get(url=MainUrl,timeout=10)
        
        if IpQuery.status_code == 200:
            IpQuery = json.loads(IpQuery.text)
            return IpQuery
        else:
            return False

def IpQueryWithShodan(ip_addrs):
    with open(api_path,"r") as KeyFile:
        al_keys = json.load(KeyFile)
        if al_keys["api.shodan.io"] == "NULL":
            return 1
        ApiKey = al_keys["api.shodan.io"]
        MainUrl = f"https://api.shodan.io/shodan/host/{ip_addrs}?key={ApiKey}"
        IpQuery = requests.get(url=MainUrl,timeout=10)
        if IpQuery.status_code == 200:
            IpQuery = json.loads(IpQuery.text)
            return IpQuery
        else:
            return False


ipAddrs = GetIpQuery(input_ip)
ShodanQuery = IpQueryWithShodan(input_ip)

if ipAddrs == "LUTFEN ipinfo.io API KEYINIZI ApiKey.json A GIRINIZ":
    print(f"{color_red}LUTFEN ipinfo.io API KEYINIZI ApiKey.json A GIRINIZ{color_reset}")
    
elif ipAddrs == False:
    print(f"{color_red}Sorgu başarısız!{color_reset}")
else:

    print(f"{color_blue}{a}{color_reset}")
    print(f"{color_blue}| Vendor: ipinfo.io{color_reset}")
    print(f"{color_blue}{a}{color_reset}")

    for key in ipAddrs:
        key_values = ipAddrs[key]
        print(f"{color_blue}| {key}:{color_green} {key_values}{color_reset}")
    print(f"{color_blue}{a}{color_reset}")
            
if ShodanQuery == 1:
    print(f"\n{color_blue}{a}{color_reset}")
    print(f"{color_blue}Vendor: shodan.io{color_reset}")
    print(f"{color_blue}{a}{color_reset}")
    print(f"{color_blue}| {color_red}Api key not found!{color_reset}")
    print(f"{color_blue}{a}{color_reset}")
elif ShodanQuery == False:
    print(f"{color_red}Sorgu başarısız!{color_reset}")
else:
    print(f"\n{color_blue}{a}{color_reset}")
    print(f"{color_blue}| Vendor: shodan.io{color_reset}")
    print(f"{color_blue}{a}{color_reset}")
                
    for key in ShodanQuery:
        if key == "data":
            filename = f"RawDatFor-{input_ip}.txt"
            with open(f"log/{filename}","w") as file:
                data = ShodanQuery[key]
                file.write(str(data))
                continue

        kay_values = ShodanQuery[key]
        print(f"{color_blue}| {key}:{color_green} {kay_values}{color_reset}")
    print(f"{color_blue}{a}{color_reset}")  



