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

logo2 = '''\033[1;33m

[*********************************]
     [1] Fullname to Card Id 
     [2] Card Id to Fullname
     [3] Id to Fullname
         (440 to tarsa)
     [4] Lastname to Id
     [5] Convert to Json

     [6] Back <
[*********************************]


'''

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




'''



#####################################################
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
    download = "1OhuMCDerie1_1_2wK7nJDiUmqntcZuU2"
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
  print("\033[1;36mElements Available:\033[1;36m ")
  print ("\n--------------------------")
  print ("(1) Earth")
  print ("(2) Water")
  print ("(3) Fire")
  print ("(4) Light")
  print ("(5) Death")
  print ("(6) Dragon")
  print ("\n(7) Download Team File")
  print ("(8) Delete Team File")
  print ("(9) Check cards")
  print ("--------------------------\n")

  option = input("\033[0m[>] Select Element: \033[0m")

  if option == "1":
    element = "team/earth/"
    

  elif option == "2":
    element = "team/water/"

  elif option == "3":
    element = "team/fire/"

  elif option == "4":
    element = "team/life/"

  elif option == "5":
    element = "team/death/"

  elif option == "6":
    element = "team/dragon/"

  elif option == "7":
    zp()

  elif option == "8":
    os.system('rm -r team')
    menu()

  elif option == "9":
    cards()
    input("\n\nScan Complete..Press Enter to continue...")
    menu()
    
    

  else:
    print("Invalid command")


  
  

  
    
  
  def scan():
    print("Please wait...")
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

        old = name.replace(" ", "_").lower()
        

        new = i['uid']


        def ilisan():
          fp = element
          path = os.listdir(fp)
          total = 1
        
          for content in path:
            counter = 0
            with open(fp + content, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)
      
            with open(fp + content, "w", encoding="utf-8") as newfile:
              newfile.write(result)
      
            if counter:
            
              total+=1
        

      

        ilisan()

  
        
      
      
      
        
  def scan2():
    
    dir_list = os.listdir(element)
    print("Please wait..")
    7
    for i in dir_list:
      
      f = open(element+i)
      c = 11
      stdoutOrigin=sys.stdout
      a = i.replace(".txt", "")
      sys.stdout = open(element+a+".json", "w")
      os.system('rm -r ' + element+i)
      for i in f:
        c +=1

        print(c, i)


      sys.stdout.close()
      sys.stdout=stdoutOrigin   
  
  

      
    

  def reverse():
    print("Please wait...")


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

        
        old = i['uid']

        new = name.replace(" ", "_").lower()
        

      
      


        def ilisan():
          fp = element
          path = os.listdir(fp)
          total = 1
        
          for content in path:
            counter = 0
            with open(fp + content, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)
      
            with open(fp + content, "w", encoding="utf-8") as newfile:
              newfile.write(result)
      
            if counter:
            
              total+=1
        

      

        ilisan()

      
        
    





  def ntln():
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
        karaan = i['uid']
        
        
        new = name.replace(" ", "_").lower()
        name = karaan.split("-")
        old = name[1]


        def ilisan():
          fp = element
          path = os.listdir(fp)
          total = 1
        
          for content in path:
            counter = 0
            with open(fp + content, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)
      
            with open(fp + content, "w", encoding="utf-8") as newfile:
              newfile.write(result)
      
            if counter:
            
              total+=1


        ilisan()

        res = i['uid'].split("-")

  
  def ltf():
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
        karaan = i['uid']
        
        
        new = name.replace(" ", "_").lower()
        try:
          ln = name.split(' ')
          old = ln[1].lower()
        except:
          ln = name.split(' ')
          old = ln[0].lower()


        def ilisan():
          fp = element
          path = os.listdir(fp)
          total = 1
        
          for content in path:
            counter = 0
            with open(fp + content, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)
      
            with open(fp + content, "w", encoding="utf-8") as newfile:
              newfile.write(result)
      
            if counter:
            
              total+=1


        ilisan()

        res = i['uid'].split("-")
  
  
  
  

  
  def main():
    os.system('clear')
    print(logo2)
    
   

    s = input("\033[1;36m[>] Select option: \033[0m")

    if s == "1":
      scan()
      main()

    elif s == "2":
      reverse()
      main()


    elif s == "3":
      ntln()
      main()

    elif s == "4":
      ltf()
      main()

    elif s == "5":
      scan2()
      main()


    elif s == "6":
      menu()
      
      


    else:
      print("invalid command...")
      time.sleep(2)
      menu()


  main()




    



menu()
