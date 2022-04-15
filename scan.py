
import hashlib
import json
import re, sys
import sys
import fileinput

import requests, os



os.system('clear')


def mains():
  sys.stdout = open("output.txt", "w")
  f = open('team.txt')
  c = 11


  
  for i in f:
    c += 1
   
    print(c, i)
  sys.stdout.close()

def main():
  user = input("Enter user: ")
  API2 = "https://api2.splinterlands.com/cards/collection/"+user

  url = (API2)
  



 
  
  l = requests.get(url).json()

  
  for i in l['cards']:
    cn = "https://api.splinterlands.io/cards/find?ids=" + i['uid']
    u = (cn)
    c = requests.get(u).json()
    for ca in c:
      name = ca['details']['name']
      res = "-" in i['uid']
      mao1 = name.split()[-1]

      
      print(name + " = " + i['uid'])
      s = i['uid'].split('-')
      #print(s[1], "=", i['uid'])

      search_text = s[1]
      replace_text = i['uid']

      with open('team.txt', 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(search_text, replace_text))

  mains()


      
        
          

    


  
    

main()



