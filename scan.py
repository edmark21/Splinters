'''
scan


update time
2:34 PM 6/18/2022
'''


import os, sys


import hashlib
import json
import re, sys
import sys
import fileinput

import importlib.util, requests
import requests, zipfile, io
import os, sys, time
import zipfile
from urllib.request import urlopen



if os.name == 'nt':
  clear = os.system('cls')
  
else:
  clear = os.system('clear')
  

clear 

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'



try:

  file1 = open('core/acc.txt', 'r')
  l = file1.readlines()


  mao = l[1].strip()
  username = mao
  token = l[19].strip()
  
  url = "https://api2.splinterlands.com/cards/collection/"+mao
  response = requests.get(url)
  a = response.text

  quest_url = "https://api.splinterlands.io/players/quests?username="+username
  quest_url_response = urlopen(quest_url)
  quest_info = json.loads(quest_url_response.read())

  f = open('core/cards_collection.json','w')

  f.write(a)
  f.close()
except:
  print("[!] Please login first in core/acc.txt")  


try:
    url = f"https://pastebin.com/raw/{token}"
    response = requests.get(url)
    a = response.text
    if a == "active":
        print()
    else:
        print("[!] Your Subscription is Expired")
        input("[*] Reason: Out of contract")
        exit()
              
except:
    input("[!] There's an error")
    exit()
  





###################################################
cards = open('core/allcards.json')
c = json.load(cards)

def scan():
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("[+] Please wait...")
  allc = open('core/cards_collection.json')
  l = json.load(allc)
  total = 1


  
  for i in l['cards']:
    ids = i['card_detail_id']
    uids = i['uid']
    for a in c:
      if ids == a['id']:
        #print(ids, uids, a['name'].replace(" ", "_").lower())
        old = a['name'].replace(" ", "_").lower() #name
        new = uids #uid

        for content in co:
          #sulod sa team folder
          sulod = os.listdir(pf+content)
          total = 1

          for content_folder in sulod:
            counter = 0
            #sulod sa mga folder sa team

            with open(pf + content + "/" +content_folder, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)

            with open(pf + content + "/" + content_folder, "w", encoding="utf-8") as newfile:
              newfile.write(result)

  print("\n[+] Fullname to Uid replaced, Success.")
  

########################################################        
def manual():
  cards = open('core/allcards.json')
  l = json.load(cards)
  
  c = int(input("\nEnter card Id: "))
  
  
  for i in l:
    if i['id'] == c:
      name = i['name'].replace(" ", "_").lower()
      print(i['id'], name, i['color'])

  manual()
           

#################################################### 
def checker():
  try:

    file1 = open('core/acc.txt', 'r')
    l = file1.readlines()


    uname = l[1].strip()
    username = uname
  
    url = "https://api2.splinterlands.com/cards/collection/"+username
    response = requests.get(url)
    a = response.text

    f = open('core/cards_collection.json','w')

    f.write(a)
    f.close()
  except:
    print("[!] Please login first in core/acc.txt")  


  al = open('core/allcards.json')
  ali = json.load(al)

  f = open('core/checker.txt')
  cards = f.readlines()

  mycards = open('core/cards_collection.json')
  mc = json.load(mycards)

  quest_url = "https://api.splinterlands.io/players/quests?username="+username
  quest_url_response = urlopen(quest_url)
  quest_info = json.loads(quest_url_response.read())



  ca = []

  for i in cards:
    a = int(i.strip())
    b = ca.append(a)




  csl = []
  for i in mc['cards']:
    c = i['card_detail_id']
    a = csl.append(c)
    




  bb = [ x for x in ca if not x in csl ]
  listToStr = ' '.join([str(elem) for elem in bb])

  
     
    
#####################################################
def scan3():
  
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("Please wait...")

  file1 = open('core/acc.txt', 'r')
  l = file1.readlines()

  mao = l[1].strip()

  allc = open('core/cards_collection.json')
  l = json.load(allc)
  total = 1


  
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      name = ca['details']['name']
      new = name.replace(" ", "_").lower()
      old = i['uid']

      for content in co:
        #sulod sa team folder
        sulod = os.listdir(pf+content)
        total = 1

        for content_folder in sulod:
          
          counter = 0
          #sulod sa mga folder sa team


          with open(pf + content + "/" +content_folder, "r", encoding="utf-8") as file:
            result = file.read()
            counter  = result.count(old)
            result = result.replace(old, new)
      
          with open(pf + content + "/" + content_folder, "w", encoding="utf-8") as newfile:
            newfile.write(result)
      
          if counter:
            total+=1

###################################################            
def cards():
  clear

  file1 = open('core/acc.txt', 'r')
  l = file1.readlines()

  mao = l[1].strip()
  
  allc = open('core/cards_collection.json')
  l = json.load(allc)
  count = 0
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      name = ca['details']['name']
      
      count += 1
      print(count, name + " = " + i['uid'])


      
def zp():
  dl = input("Do you want to doqnload the Team file? [y/n]: ")
  if dl == "y" or dl == "Y" or dl == "yes" or dl == "YES" or dl == "Yes":
    download = "17pRHW6I25PaVwFTpSLX20UzL0KjOwlwQ"
    print("Downloading Please wait...")
    r = requests.get("https://drive.google.com/uc?id=" + download + "&export=download")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    menu()

  else:
    print("ready to go")  

def menu():
  clear
  logo = '''


  ======================================
  [         SPLINTERS AUTO SCAN        ]
  [          Develop by: Edmark        ]
  [                                    ]
  ======================================

            Welcome: ''' + username + '''

'''
  print(logo)
  #here
  checker()
  
  

  lo = '''
\n-----------------------------------------
  [1] Start            [8] Transfer(comming soon)
  [2] Id info          [9] Exit
  [3] Check cards
  [4] Apply RB Modern
  [5] Apply RB Wild
  [6] Check if Cards rented
  [7] Extract team.zip
  
-------------------------------------------\n

  '''
  
  print(lo)
  

  option = input("[>] Select Option: ")

  if option == "1":
    try:
      scan()
    except:
      print("[!] Please Extract the team.zip")


    input("Press Enter to Exit...")
    menu()

  elif option == "2":
    clear
    manual()
    input("Press Enter to Continue")
    
    menu()
    

  elif option == "3":
    cards()
    input("\n\nScan Complete..Press Enter to continue...")
    menu()

  elif option == "4":
    
    print("[*] Applying rating booster.....")
    rb = "https://pastebin.com/raw/Lk5yTre9"
    response = requests.get(rb)
    a = response.text
    f = open('team/life/Standard.json','w')
    f.write(a.strip())
    f.close()

    print("Modern Rating booster apply success...")
    time.sleep(3)
    menu()  

  elif option == "5":
    
    print("[*] Applying rating booster.....")
    rb = "https://pastebin.com/raw/bef1fFeN"
    response = requests.get(rb)
    a = response.text
    f = open('team/earth/Standard.json','w')
    f.write(a.strip())
    f.close()

    print("Wild Rating booster apply success...")
    time.sleep(3)
    menu()

  elif option == "6":
    checker()
    menu()
  

  elif option == "7":
    try:
      with zipfile.ZipFile("team.zip","r") as zip_ref:
        zip_ref.extractall()
        print("Ectract Complete.")
        menu()

    except:
      print("[!] team.zip is not exist in the file.")

  elif option == "9":
    print("Thank you for using this Bot.")
    exit()





menu()

