'''
battle result
3:16 PM 5/24/2022

'''


import bs4
import requests
import json
import os, sys, time




def r():
  
  f = open('core/acc.txt')
  n = f.readlines()


  name = n[0]

  res = " " in name

  mao = name.split()[0]
  mao2 = name.split()[1]

  user = mao

  oras = "https://google.com/search?q=ph time"
  request_result = requests.get(oras)
  soup = bs4.BeautifulSoup(request_result.text, "html.parser")
  temp = soup.find("div", class_='BNeawe').text

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
    l = json.load(balance)

    
    total_dec = str(l[2]['balance'])

    



    
    if mao == bh[0]['player_1']:
      earn_dec = str(bh[0]['reward_dec'])
      if mao == bh[0]['winner']:
        print("[+] Winner:", bh[0]['winner'], "Rating:", bh[0]['player_1_rating_final'], "ECR:", ee)
        print("[*] Time: ", temp)
        
       
      else:
        earn_dec = "0"
        print("[x] You Lose", "Rating:", bh[0]['player_1_rating_final'], "ECR:", ee)
        print("[*] Time: ", temp)
        
      
          

    else:
      if mao == bh[0]['player_2']:
        earn_dec = str(bh[0]['reward_dec'])
        if mao == bh[0]['winner']:
          print("[+] Winner:", bh[0]['winner'], "Rating:", bh[0]['player_2_rating_final'], "ECR:", ee)
          print("[*] Time: ", temp)
          
        
             
      else:
        earn_dec = "0"
        print("[x] You Lose", "Rating:", bh[0]['player_2_rating_final'], "ECR:", ee)
        print("[*] Time: ", temp)

    ranku = "https://api.splinterlands.io/players/details?name="+user


    ra = (ranku)
    usr = requests.get(ra).json()


    if usr['league'] == 0:
      print("[+] Rank: novice", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 1:
      print("[+] Rank: Bronze 3", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 2:
      print("[+] Rank: Bronze 2", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 3:
      print("[+] Rank: Bronze 1", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 4:
      print("[+] Rank: Silver 3", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 5:
      print("[+] Rank: Silver 2", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 6:
      print("[+] Rank: Silver 1", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 7:
      print("[+] Rank: Gold 3", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 8:
      print("[+] Rank: Gold 2", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] == 9:
      print("[+] Rank: Gold 1", "DEC:", "+" + earn_dec + "/" + total_dec)

    elif usr['league'] > 10:
      print("[+] Rank: Diamond above", "DEC:", "+" + earn_dec + "/" + total_dec)


    
        
        
                 
  except:
    print("[!] The public api is down.")
    print("[*] Time: ", temp)
    
