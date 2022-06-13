'''
battle resultt
1:30 PM 6/12/2022

'''


import bs4
import requests
import json
import os, sys, time
from beem import Hive




def r():
  
  def broadcast_sm_advance_league(hive: Hive, user: str, notify: str):
    request = {"notify": "false"}

    trx: dict = hive.custom_json("sm_advance_league", json_data=request,
                                 required_posting_auths=[user])
    return trx["trx_id"]
  
  
  f = open('core/acc.txt')
  n = f.readlines()


  name = n[0]

  res = " " in name

  mao = name.split()[0]
  mao2 = name.split()[1]

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


      if usr['league'] == 0:
        print("[+] Rank: novice")

      elif usr['league'] == 1:
        print("[+] Rank: Bronze 3")

      elif usr['league'] == 2:
        print("[+] Rank: Bronze 2")

      elif usr['league'] == 3:
        print("[+] Rank: Bronze 1")

      elif usr['league'] == 4:
        #hive = Hive(keys=[posting])
        #transaction_id = broadcast_sm_advance_league(hive, user, "false")
        print("[+] Rank: Silver 3")

      elif usr['league'] == 5:
        print("[+] Rank: Silver 2")

      elif usr['league'] == 6:
        print("[+] Rank: Silver 1")

      elif usr['league'] == 7:
        #hive = Hive(keys=[posting])
        #transaction_id = broadcast_sm_advance_league(hive, user, "false")
        print("[+] Rank: Gold 3")

      elif usr['league'] == 8:
        print("[+] Rank: Gold 2")

      elif usr['league'] == 9:
        print("[+] Rank: Gold 1")

      elif usr['league'] > 10:
        print("[+] Rank: Diamond above")
    



    
    if mao == bh[0]['player_1']:
      
      if mao == bh[0]['winner']:
        print("[+] Winner:", bh[0]['winner'], "DEC:", "+" + earn_dec + "/" + total_dec)
        ranks()
        print("[+] Rating:", bh[0]['player_1_rating_final'], "ECR:", ee)
        
        
        
        
        
       
      else:
        
        print("[x] You Lose")
        ranks()
        print("[+] Rating:", bh[0]['player_1_rating_final'], "ECR:", ee)
        
        
      
          

    else:
      if mao == bh[0]['player_2']:
        
        if mao == bh[0]['winner']:
          print("[+] Winner:", bh[0]['winner'], "DEC:", "+" + earn_dec + "/" + total_dec)
          ranks()
          print("[+] Rating:", bh[0]['player_2_rating_final'], "ECR:", ee)
          
          
          
        
             
        else:
          
          print("[x] You Lose", "Rating:")
          ranks()
          print("[+] Rating", bh[0]['player_2_rating_final'], "ECR:", ee)
          

    


    
        
        
                 
  except:
    print("[!] The public api is down.")
    print("[*] Time: ", temp)
    
