import json

import requests
import bs4

#https://api.splinterlands.io/players/details?name=kiokizz

file = open("acc.txt")

user = file.read()

try:
  url = 'https://api.splinterlands.io/players/balances?username='+user

  data = requests.get(url)
  dataa = json.loads(data.content.decode())

  q = "https://api.splinterlands.io/players/quests?username="+user

  dat = requests.get(q)
  da = json.loads(dat.content.decode())
  quest = str(da[0]['completed_items'])
except:
  print(" Player not found!.")



l = '''\033[1;32m

        [1] Play
        [2] Stats
        [3] Battle History
        [4] Account Settings
        [5] Custom Cards/mana

'''

lo = '''\033[1;31m

  _________      .__  .__        __                       
 /   _____/_____ |  | |__| _____/  |_  ___________  ______
 \_____  \\____ \|  | |  |/    \   __\/ __ \_  __ \/  ___/
 /        \  |_> >  |_|  |   |  \  | \  ___/|  | \/\___ \ 
/_______  /   __/|____/__|___|  /__|  \___  >__|  /____  >
        \/|__|                \/          \/           \/ 
                    Created By: Edmarkz
                            Beta
''' 
                      



def main():
  print(lo)
  try:
    print("\033[1;32m                     User: " + dataa[3]['player'])
    print("\033[1;33m   Credits: " + str(dataa[1]['balance']) + "\033[0;35m  DEC: " + str(dataa[0]['balance']) + "\033[1;36m  SPS: " + str(dataa[3]['balance']) + "\033[1;33m  Gold: " + str(dataa[5]['balance']))
    print("   Quest: " + str(da[0]['name']) + " " + quest + "/5")
  except:
    print("\033[1;31m Account Not Found!....")
  
  print(l)

  
main()
menu = input("\033[1;34mSelect option [1-5]: ")

if menu == '1':
  print()


file1.close()  
