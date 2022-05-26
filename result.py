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
        print("[+] Rank: novice =>", temp)

      elif usr['league'] == 1:
        print("[+] Rank: Bronze 3 =>", temp)

      elif usr['league'] == 2:
        print("[+] Rank: Bronze 2 =>", temp)

      elif usr['league'] == 3:
        print("[+] Rank: Bronze 1 =>", temp)

      elif usr['league'] == 4:
        print("[+] Rank: Silver 3 =>", temp)

      elif usr['league'] == 5:
        print("[+] Rank: Silver 2 =>", temp)

      elif usr['league'] == 6:
        print("[+] Rank: Silver 1 =>", temp)

      elif usr['league'] == 7:
        print("[+] Rank: Gold 3 =>", temp)

      elif usr['league'] == 8:
        print("[+] Rank: Gold 2 =>", temp)

      elif usr['league'] == 9:
        print("[+] Rank: Gold 1 =>", temp)

      elif usr['league'] > 10:
        print("[+] Rank: Diamond above =>", temp)
    



    
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
    
