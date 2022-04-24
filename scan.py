import os, sys


import hashlib
import json
import re, sys
import sys
import fileinput

import importlib.util, requests
import requests, zipfile, io
import os, sys, time



os.system('clear')

logo = '''

    \033[1;33m
         _nnnn_                      
        dGGGGMMb     
       @p~qp~~qMb     Splinters! 
       M|@||@) M|   _;
       @,----.JM| -'
      JS^\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMM|   .'
     `-'       `--' 
      Created By:
  Edmark jay Sumampen

'''


def scan():
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("Please wait...")
  f = open('acc.txt')
  n = f.readlines()
  name = n[0]
  res = " " in name
  mao = name.split()[0]
  API2 = "https://api2.splinterlands.com/cards/collection/"+mao
  url = (API2)  
  l = requests.get(url).json()
  total = 1


  
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      name = ca['details']['name']
      old = name.replace(" ", "_").lower()
      new = i['uid']

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

            
#####################################################
def scan2():
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("Please wait...")
  f = open('acc.txt')
  n = f.readlines()
  name = n[0]
  res = " " in name
  mao = name.split()[0]
  API2 = "https://api2.splinterlands.com/cards/collection/"+mao
  url = (API2)  
  l = requests.get(url).json()
  total = 1


  
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      karaan = i['uid']
      new = name.replace(" ", "_").lower()
      name = karaan.split("-")
      old = name[1]

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

####################################################            
def cards():
  os.system('clear')
  f = open('acc.txt')
  n = f.readlines()
  name = n[0]
  res = " " in name
  mao = name.split()[0]
  API2 = "https://api2.splinterlands.com/cards/collection/"+mao
  url = (API2)  
  l = requests.get(url).json()
    
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      name = ca['details']['name']

      print(name + " = " + i['uid'])


      
def zp():
  dl = input("Do you want to doqnload the Team file? [y/n]: ")
  if dl == "y" or dl == "Y" or dl == "yes" or dl == "YES" or dl == "Yes":
    download = "1TM5tWU4oOD77j5B4_l7zb_gZzASnurc1"
    print("Downloading Please wait...")
    r = requests.get("https://drive.google.com/uc?id=" + download + "&export=download")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    menu()

  else:
    print("ready to go")  

def menu():
  os.system('clear')

  print(logo)
  print ("\n\033[1;36m--------------------------")
  print ("(1) Fullname to UID")
  print ("(2) Id to Fullname")
  print ("(3) Download Team File")
  print ("(4) Delete Team File")
  print ("(5) Check cards")
  print ("(6) Exit")
  print ("--------------------------\n")

  option = input("\033[0m[>] Select Element: \033[0m")

  if option == "1":
    try:
      scan()
      print("Fullname to Uid replaced, Success.")
      time.sleep(4)
      menu()
    except:
      print("[!] Please Download Team File first.")

  if option == "2":
    scan2()
    print("Id to Fullname replaced, Success.")
    time.sleep(4)
    menu()
    

  elif option == "3":
    zp()

  elif option == "4":
    os.system('rm -r team')
    menu()

  elif option == "5":
    cards()
    input("\n\nScan Complete..Press Enter to continue...")
    menu()

  elif option == "6":
    print("Thank you for using this Bot.")
    exit()
    

  else:
    print("Invalid command")





menu()
