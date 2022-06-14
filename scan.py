'''
scan


update time
12:05 PM 6/6/2022
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



os.system("clear")






try:
  f = open('core/acc.txt')
  n = f.readlines()


  name = n[0]

  res = " " in name

  mao = name.split()[0]
  username = mao
  
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
      print(i['id'], name)

  manual()
           

#################################################### 
def checker():
  try:
    f = open('core/acc.txt')
    n = f.readlines()


    name = n[0]

    res = " " in name

    mao = name.split()[0]
    username = mao
  
    url = "https://api2.splinterlands.com/cards/collection/"+mao
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


  with open('core/cards.txt', 'w') as myfile:
    for i in bb:
      for h in ali:
        if h['id'] == i:
          name = h['name'].replace(" ", "_").lower()
          print(h['id'], name, h['name'])
          myfile.write(str(h['id']) + '\n')
        

  try:
    if h['id']:
      print("[!] Not all cards rented")
  except:
    print("[+] All cards rented")
    scan()

    os.system('python3 main.py')
  

            
    
#####################################################
def scan3():
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("Please wait...")
  f = open('core/acc.txt')
  n = f.readlines()
  name = n[0]
  res = " " in name
  mao = name.split()[0]
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
  os.system('clear')
  f = open('core/acc.txt')
  n = f.readlines()
  name = n[0]
  res = " " in name
  mao = name.split()[0]
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
  os.system('clear')
  logo = '''


  ======================================
  [         SPLINTERS AUTO SCAN        ]
  [          Develop by: Edmark        ]
  [                                    ]
  ======================================

            Welcome: ''' + username + '''

'''
  print(logo)
  
  checker()

  lo = '''
\n-----------------------------------------
  [1] Start  
  [2] Id info
  [3] Check cards
  [4] Apply RB
  [5] Check if Cards rented
  [6] Extract team.zip
  [7] Exit
-------------------------------------------\n

  '''
  
  print(lo)
  

  option = input("[>] Select Option: ")

  if option == "1":
    scan()
    input("Press Enter to Exit...")
    menu()

  elif option == "2":
    os.system('clear')
    manual()
    input("Press Enter to Continue")
    
    menu()
    

  elif option == "3":
    cards()
    input("\n\nScan Complete..Press Enter to continue...")
    menu()

  elif option == "4":
    
    print("[*] Applying rating booster.....")
    rb = "https://pastebin.com/raw/bef1fFeN"
    response = requests.get(rb)
    a = response.text
    f = open('team/earth/Standard.json','w')
    f.write(a.strip())
    f.close()

    print("Rating booster apply success...")
    time.sleep(3)
    menu()

  elif option == "5":
    checker()
    menu()
  

  elif option == "6":
    try:
      with zipfile.ZipFile("team.zip","r") as zip_ref:
        zip_ref.extractall()

    except:
      print("[!] team.zip is not exist in the file.")

  elif option == "7":
    print("Thank you for using this Bot.")
    exit()





menu()

