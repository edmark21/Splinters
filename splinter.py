import hashlib
import json, requests
import string
import time

from secrets import choice
from typing import List
import os, sys
import requests
from beem import Hive

import datetime



API2 = "https://api2.splinterlands.com"
BASE_BATTLE = "https://battle.splinterlands.com"


  

  



def main():
  def broadcast_find_match(hive: Hive, user: str, match_type: str, on_chain: bool):
    hive = hive if on_chain else copy_hive(hive, user)

    trx_id = None
    trx: dict = hive.custom_json("sm_find_match", json_data={"match_type": match_type},
                                 required_posting_auths=[user])
    if not on_chain:
        trx = post_battle_transaction(trx)
        if trx["success"]:
            trx_id = trx["id"]
    else:
        trx_id = trx["trx_id"]

    return trx_id


  def broadcast_submit_team(hive: Hive, user: str, trx_id: str, team: List[str], secret: str,on_chain: bool):
    hive = hive if on_chain else copy_hive(hive, user)

    hash = generate_team_hash(team[0], team[1:], secret)

    request = {"trx_id": trx_id, "team_hash": hash}
    trx: dict = hive.custom_json("sm_submit_team", json_data=request,
                                 required_posting_auths=[user])
    trx_id = None
    if not on_chain:
        trx = post_battle_transaction(trx)
        if trx["success"]:
            trx_id = trx["id"]
    else:
        trx_id = trx["trx_id"]

    return trx_id, hash


  def broadcast_reveal_team(hive: Hive, user: str, team: List[str], secret: str, trx_id, hash, on_chain: bool):
    hive = hive if on_chain else copy_hive(hive, user)

    request = {"trx_id": trx_id, "team_hash": hash, "summoner": team[0], "monsters": team[1:],
               "secret": secret}
    trx: dict = hive.custom_json("sm_team_reveal", json_data=request,
                                 required_posting_auths=[user])

    trx_id = None
    if not on_chain:
        trx = post_battle_transaction(trx)
        if trx["success"]:
            trx_id = trx["id"]
    else:
        trx_id = trx["trx_id"]

    return trx_id


  def generate_secret(length=10):
    return ''.join(choice(string.ascii_letters + string.digits) for i in range(length))


  def generate_team_hash(summoner, monsters, secret):
    m = hashlib.md5()
    m.update((summoner + ',' + ','.join(monsters) + ',' + secret).encode("utf-8"))
    team_hash = m.hexdigest()
    return team_hash


  def get_battle_status(battle_id: str):
    url: str = API2 + "/battle/status?id=" + battle_id
    return requests.get(url).json()


  def get_battle_result(battle_id: str):
    url: str = API2 + "/battle/result?id=" + battle_id
    return requests.get(url).json()


  def copy_hive(hive: Hive, user: str):
    private_key = hive.wallet.getPostingKeyForAccount(user)
    return Hive(nobroadcast=True, keys=[private_key])


  
  def post_battle_transaction(trx: dict):
    url: str = BASE_BATTLE + "/battle/battle_tx"
    trx: str = json.dumps(trx)
    return requests.post(url, data={"signed_tx": trx}).json()


  
  


  try:
    f = open('acc.txt')
    n = f.readlines()


    name = n[0]

    res = " " in name

    mao = name.split()[0]
    mao2 = name.split()[-1]

    user = mao
    hive = Hive(keys=[mao2])
    transaction_id = broadcast_find_match(hive, user, "Ranked", False)
    print("\n\n\033[1;33m[*] Staring ")
    resp = get_battle_status(transaction_id)


    

  
  except:
    print("[!] Incorrect account...")
    input("\n\n\n\n[?] Press Enter to continue.....")
    sys.exit()

  
  




  
######## if ang find match is maabot og 7 sec e restart niya ang code og e run osab
  
  balik = 0
  try:
    
    while type(resp) == str or type(resp) == dict and not resp["opponent_player"]:
      resp = get_battle_status(transaction_id)
      print("\033[0;36m[*]" + "\033[1;37m Finding Match")
      time.sleep(2)
    
    
    
    
    
      balik += 1
      if balik == 8:
        print("[?] Reloading")
        time.sleep(2)
        main()

      

      

      

        
  except:
    print("[..] Refreshing")
    time.sleep(2)
    main()
    
    
  


  
    



      
      
  
    
    
  def send():

    secret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user,  transaction_id, team, secret, False)

    broadcast_reveal_team(hive, user, team, secret, transaction_id, team_hash, False)


  
    secret = gensecret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user, transaction_id, team, secret, False)

    bat()
    r()



    main()





  url = (API2 + "/battle/status?id=" + transaction_id)
  l = requests.get(url).json()  



  def bat():
    
    url = (API2 + "/battle/status?id=" + transaction_id)
    l = requests.get(url).json()

  
    print("\033[0;32m[+]" + "\033[1;37m Match Found")
    time.sleep(1)

    a = ["Red", "White", "Blue", "Green", "Black", "Gold"]

  
    b = l['inactive'].split(',')
  

    b = [ x for x in a if not x in b ] 

    listToStr = ' '.join([str(elem) for elem in b])
  
    try:
      print("\033[1;32m[?]"+"\033[0;36m Active Element\033[0;35m ", "["+listToStr+"]")

      print("\033[1;35m[>] " + "\033[0;34m" + l['player'] + "\033[1;37m vs \033[0;31m" + l['opponent_player'] + " = " + "\033[0;32mManacap: " + str(l['mana_cap']) + " => " + "Ruleset: " + l['ruleset'])
      
    except:
      print("Something error is happening.")
      time.sleep(2)
      main()

  
    
    
  




  def r():
    try:
      de = datetime.datetime.now()
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
          print (de.strftime("[+] %a, %b %d, %Y %I:%M:%S %p"))
          main()
                        
        else:
          print("\033[0;31m[x] You Lose\033[1;37m", "\033[1;33mRating:", bh[0]['player_1_rating_final'], "\033[1;32mECR:", ee)
          print (de.strftime("[+] %a, %b %d, %Y %I:%M:%S %p"))
          main()
          

      else:
        
        if mao == bh[0]['player_2']:
          
          if mao == bh[0]['winner']:
            
            print("\033[1;32m[+] Winner:" + "\033[1;33m", bh[0]['winner'], "\033[0;35mDec:\033[0;35m", bh[0]['reward_dec'], "\033[1;33mRating:", bh[0]['player_2_rating_final'], "\033[1;32mECR:", ee)
            print (de.strftime("[+] %a, %b %d, %Y %I:%M:%S %p"))
            main()
             
        else:
          print("\033[0;31m[x] You Lose\033[1;37m", "\033[1;33mRating:", bh[0]['player_2_rating_final'], "\033[1;32mECR:", ee)
          print (de.strftime("[+] %a, %b %d, %Y %I:%M:%S %p"))
          main()
                 
    except:
      print("\033[0;31m[!] The public api is down.")
      print (de.strftime("[+] %a, %b %d, %Y %I:%M:%S %p"))
      main()
         
  
      



  
  




  
    
  
  


  
    

  


  
  
  
 

  
      #team here ex: card1, card2, card
  if l['ruleset'] == "Standard":
    #url = requests.get("https://pastebin.com/raw/JXEFarAt")
    url= requests.get("https://pastebin.com/raw/JXEFarAt")
    text = url.text
    setteam = json.loads(text)

    #fi = open("Standard.json")
    #setteam = json.load(fi)
    
    if str(l['mana_cap']) == "12":
      team = (setteam['12'])
      send()
    
    elif str(l['mana_cap']) == "13":
      team = (setteam['13'])
      send()

    elif str(l['mana_cap']) == "14":
      team = (setteam['14'])
      send()

    elif str(l['mana_cap']) == "15":
      team = (setteam['15'])
      send()

    elif str(l['mana_cap']) == "16":
      team = (setteam['16'])
      send()
    
    elif str(l['mana_cap']) == "17":
      team = (setteam['17'])
      send()

    elif str(l['mana_cap']) == "18":
      team = (setteam['18'])
      send()

    elif str(l['mana_cap']) == "19":
      team = (setteam['19'])
      send()

    elif str(l['mana_cap']) == "20":
      team = (setteam['20'])
      send()

    elif str(l['mana_cap']) == "21":
      team = (setteam["21"])
      send()

    elif str(l['mana_cap']) == "22":
      team = setteam['22']
      send()

    elif str(l['mana_cap']) == "23":
      team = setteam['23']
      send()

    elif str(l['mana_cap']) == "24":
      team = (setteam['24'])
      send()

    elif str(l['mana_cap']) == "25":
      team = (setteam['25'])
      send()

    elif str(l['mana_cap']) == "26":
      team = (setteam['26'])
      send()

    elif str(l['mana_cap']) == "27":
      team = (setteam['27'])
      send()

    elif str(l['mana_cap']) == "28":
      team = (setteam['28'])
      send()

    elif str(l['mana_cap']) == "29":
      team = (setteam['29'])
      send()

    elif str(l['mana_cap']) == "30":
      team = (setteam['30'])
      send()


    else:
      team = (setteam['99'])
      send()
    
    
    
    



  
  
  
  
  
  
  


main()


  



