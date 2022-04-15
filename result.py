
import requests
import json
import os, sys, time
from datetime import datetime
import pytz









def r():
  
  time.sleep(5)
  f = open('acc.txt')
  n = f.readlines()


  name = n[0]

  res = " " in name

  mao = name.split()[0]
  mao2 = name.split()[-1]

  user = mao

  datetime_india = datetime.now(pytz.timezone('Asia/Manila'))


  
  
  try:
    
    btsu = "https://steemmonsters.com/battle/history?player="+mao
    link = "https://steemmonsters.com/players/details?name="+mao
    e = requests.get(link).json()
    ee = int(e['capture_rate'])
    bt = requests.get(btsu)
    bts = bt.json()
    bh = bts['battles']



    
    if mao == bh[0]['player_1']:
      if mao == bh[0]['winner']:
        print("\033[1;32m[+] Winner:" + "\033[1;33m", bh[0]['winner'], "\033[0;35mDec:\033[0;35m", bh[0]['reward_dec'], "\033[1;33mRating:", bh[0]['player_1_rating_final'], "\033[1;32mECR:", ee)
        print (datetime_india.strftime('[+] %Y:%m:%d %H:%M:%S'))
        
       
      else:
        print("\033[0;31m[x] You Lose\033[1;37m", "\033[1;33mRating:", bh[0]['player_1_rating_final'], "\033[1;32mECR:", ee)
        print (datetime_india.strftime('[+] %Y:%m:%d %H:%M:%S'))
        
      
          

    else:
      if mao == bh[0]['player_2']:
        if mao == bh[0]['winner']:
          print("\033[1;32m[+] Winner:" + "\033[1;33m", bh[0]['winner'], "\033[0;35mDec:\033[0;35m", bh[0]['reward_dec'], "\033[1;33mRating:", bh[0]['player_2_rating_final'], "\033[1;32mECR:", ee)
          print (datetime_india.strftime('[+] %Y:%m:%d %H:%M:%S'))
          
        
             
      else:
        print("\033[0;31m[x] You Lose\033[1;37m", "\033[1;33mRating:", bh[0]['player_2_rating_final'], "\033[1;32mECR:", ee)
        print (datetime_india.strftime('[+] %Y:%m:%d %H:%M:%S'))
        
        
                 
  except:
    print("\033[0;31m[!] The public api is down.")
    print (datetime_india.strftime('[+] %Y:%m:%d %H:%M:%S'))
    

