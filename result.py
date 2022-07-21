'''
battle resultt
2:33 PM 6/18/2022

'''


import bs4
import requests
import json
import os, sys, time
from beem import Hive




def r():

  file1 = open('core/acc.txt', 'r')
  l = file1.readlines()


  mao = l[1].strip()
  mao2 = l[3].strip()
  active = l[5].strip()
  currency = l[7].strip()
  ecr_nako = l[9].strip()
  rating_nako = l[11].strip()
  rshares_limit = l[13].strip()
  show_team = l[15].strip()
  ranked_type = l[17].strip()

  
  user = mao
  posting = mao2  

  rb = "https://api.splinterlands.io/players/balances?username="+user
  response = requests.get(rb)
  a = response.text
  f = open('core/balances.json','w')
  f.write(a.strip())
  f.close()

  
  try:
    btsu = "https://steemmonsters.com/battle/history?player="+mao
    link = "https://steemmonsters.com/players/details?name="+mao
    e = requests.get(link).json()
    ee = int(e['capture_rate'])
    bt = requests.get(btsu)
    bts = bt.json()
    bh = bts['battles']

    balance = open('core/balances.json')
    bl = json.load(balance)

    earn_dec = str(bh[0]['reward_dec'])

    
   
    if bl[1]['token'] == "DEC":
      total_dec = str(bl[1]['balance'])
      
    elif bl[2]['token'] == "DEC":
      total_dec = str(bl[2]['balance'])
      
    elif bl[3]['token'] == "DEC":
      total_dec = str(bl[3]['balance'])


    def ranks():
      ranku = "https://api.splinterlands.io/players/details?name="+user


      ra = (ranku)
      usr = requests.get(ra).json()

      rating_dre = usr['rating']
      power_dre = usr['collection_power']

      


      if usr['league'] == 0:
        print("[+] Rank: novice")

      elif usr['league'] == 1:
        print("[+] Rank: Bronze 3")

      elif usr['league'] == 2:
        print("[+] Rank: Bronze 2")

      elif usr['league'] == 3:
        print("[+] Rank: Bronze 1")
        
        
        if rating_dre > 1000:

          if power_dre > 15000:


            for i in range(1001, 1100):
              if rating_dre == i:
                
                try:
 
                  def broadcast_sm_advance_league(hive: Hive, u: str, notify: str):
                    request = {"notify": "false"}

                    trx: dict = hive.custom_json("sm_advance_league", json_data=request,
                                                     required_posting_auths=[user])
                    return trx["trx_id"]


                  file1 = open('core/acc.txt', 'r')
                  l = file1.readlines()


                  maoa = l[1].strip()
                  mao2a = l[3].strip()
                  active = l[5].strip()
                  currency = l[7].strip()
                  ecr_nako = l[9].strip()
                  rating_nako = l[11].strip()
                  rshares_limit = l[13].strip()
                  show_team = l[15].strip()


                  

                  u = maoa
                  p = mao2a
                      
                  hive = Hive(keys=[p])
                  transaction_id = broadcast_sm_advance_league(hive, u, "false")
                  print("[+] Auto Advance Complete")
              
                except:
                    er = "error"
                      
      elif usr['league'] == 4:
        print("[+] Rank: Silver 3")

              

      elif usr['league'] == 5:
        print("[+] Rank: Silver 2")

      elif usr['league'] == 6:
        print("[+] Rank: Silver 1")
        
        if rating_dre > 1900:

          if power_dre > 100000:


            for i in range(1901, 1930):
              if rating_dre == i:
                
                try:
 
                  def broadcast_sm_advance_league(hive: Hive, u: str, notify: str):
                    request = {"notify": "false"}

                    trx: dict = hive.custom_json("sm_advance_league", json_data=request,
                                                     required_posting_auths=[user])
                    return trx["trx_id"]

                  file1 = open('core/acc.txt', 'r')
                  l = file1.readlines()


                  maoa = l[1].strip()
                  mao2a = l[3].strip()
                  active = l[5].strip()
                  currency = l[7].strip()
                  ecr_nako = l[9].strip()
                  rating_nako = l[11].strip()
                  rshares_limit = l[13].strip()
                  show_team = l[15].strip()


                  

                  u = maoa
                  p = mao2a
                      
                  hive = Hive(keys=[p])
                  transaction_id = broadcast_sm_advance_league(hive, u, "false")
                  print("[+] Auto Advance Complete")
              
                except:
                    er = "error"

      elif usr['league'] == 7:
        print("[+] Rank: Gold 3")


      elif usr['league'] == 8:
        print("[+] Rank: Gold 2")

      elif usr['league'] == 9:
        print("[+] Rank: Gold 1")

      elif usr['league'] > 10:
        print("[+] Rank: Diamond above")
    



    

    ranks()
    
        
        
                 
  except:
    print("[!] The public api is down.")
    
    

