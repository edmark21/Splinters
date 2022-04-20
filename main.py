import hashlib
import json, requests
import string
import time
from result import *

from secrets import choice
from typing import List
import os, sys
import requests
from beem import Hive

from datetime import datetime
import pytz

import os.path
from os import path

os.system('clear')

API2 = "https://api2.splinterlands.com"
BASE_BATTLE = "https://battle.splinterlands.com"


logo = '''\033[1;32m

  ██████  ██▓███   ██▓     ██▓ ███▄    █ ▄▄▄█████▓▓█████  ██▀███    ██████ 
▒██    ▒ ▓██░  ██▒▓██▒    ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▒██    ▒ 
░ ▓██▄   ▓██░ ██▓▒▒██░    ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒░ ▓██▄   
  ▒   ██▒▒██▄█▓▒ ▒▒██░    ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒
▒██████▒▒▒██▒ ░  ░░██████▒░██░▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒██████▒▒
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░░▒ ░     ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░
░  ░  ░  ░░         ░ ░    ▒ ░   ░   ░ ░   ░         ░     ░░   ░ ░  ░  ░  
      ░               ░  ░ ░           ░             ░  ░   ░           ░  
                                                                           

                                                                  

                        Developed by:
                          [ WCWE ]


'''
print(logo)


check = path.exists('team')

if check == True:
  print()
else:
  print("\033[0;31m[!] Pls download team folder first")
  input("\033[0;35m\n\nPress enter to exit..")
  exit()
  



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
    time.sleep(5)
    main()
    
    
  


  
    



      
      
  
    
    
  def send():

    oras = datetime.now(pytz.timezone('Asia/Manila'))

    secret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user,  transaction_id, team, secret, False)

    broadcast_reveal_team(hive, user, team, secret, transaction_id, team_hash, False)


  
    secret = gensecret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user, transaction_id, team, secret, False)
    
    bat()
    print("[+] Team Submited", oras.strftime(' %Y:%m:%d %H:%M:%S [+]'))
    time.sleep(2)
    r()
    time.sleep(3)



    main()





  url = (API2 + "/battle/status?id=" + transaction_id)
  l = requests.get(url).json()  



  def bat():
    
    urls = (API2 + "/battle/status?id=" + transaction_id)
    lx = requests.get(urls).json()

  
    print("\033[0;32m[+]" + "\033[1;37m Match Found")
    time.sleep(1)

    a = ["Red", "White", "Blue", "Green", "Black", "Gold"]

  
    b = l['inactive'].split(',')
  

    b = [ x for x in a if not x in b ] 

    listToStr = ' '.join([str(elem) for elem in b])
  
    try:
      print("\033[1;32m[?]"+"\033[0;36m Active Element\033[0;35m ", "["+listToStr+"]")

      print("\033[1;35m[>] " + "\033[0;34m" + lx['player'] + "\033[1;37m vs \033[0;31m" + lx['opponent_player'] + " = " + "\033[0;32mManacap: " + str(lx['mana_cap']) + " => " + "Ruleset: " + lx['ruleset'])
      
    except:
      print("Something error is happening.")
      time.sleep(2)
      main()

  
    
    
  




  
         
  
      




  url = (API2 + "/battle/status?id=" + transaction_id)

  a = ["Red", "White", "Blue", "Green", "Black", "Gold"]

  
  b = l['inactive'].split(',')
  

  b = [ x for x in a if not x in b ] 

  aa = ' '.join([str(elem) for elem in b])   


  

#################[standard]##########################      

  def rule():
    if l['ruleset'] == "Standard":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/standard.json")
        setteamm = json.load(fn)


      elif "White" in aa:
        fn = open("team/life/standard.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/standard.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/standard.json")
        setteamm = json.load(fn)


        

      return setteamm  
##################[armored up]########################
    elif l['ruleset'] == "Armored Up":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/armored_up.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/standard.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/standard.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/standard.json")
        setteamm = json.load(fn)

      

      return setteamm  
###################[aim true]#######################
    elif l['ruleset'] == "Aim True":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/aim_true.json")
        setteamm = json.load(fn)


      elif "White" in aa:
        fn = open("team/life/aim_true.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/aim_true.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/aim_true.json")
        setteamm = json.load(fn)

      return setteamm  


###################[backtobasics]####################
    elif l['ruleset'] == "Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)	
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      return setteamm  

###################[Broken Arrows]####################
    elif l['ruleset'] == "Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      return setteamm        


###################[Close Range]####################
    elif l['ruleset'] == "Close Range":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      return setteamm         


###################[Earthquake]####################
    elif l['ruleset'] == "Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)

      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      return setteamm      


###################[Equaliser]####################
    elif l['ruleset'] == "Equaliser":
      if "Green" in aa:
        fn = open("team/earth/equaliser.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equaliser.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equaliser.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equaliser.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equaliser.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equaliser.json")
        setteamm = json.load(fn)

      return setteamm      
      
###################[Equal Opportunity]####################
    elif l['ruleset'] == "Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      return setteamm      


###################[Even Stevens]####################
    elif l['ruleset'] == "Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      return setteamm          


###################[Explosive Weaponry]####################
    elif l['ruleset'] == "Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      return setteamm    

###################[Fog of War]####################
    elif l['ruleset'] == "Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      return setteamm  

###################[Healed Out]####################
    elif l['ruleset'] == "Healed Out":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      return setteamm   




###################[Heavy Hitters]####################
    elif l['ruleset'] == "Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      return setteamm   


###################[Holy Protection]####################
    elif l['ruleset'] == "Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      return setteamm   
    

###################[Keep Your Distance]####################
    elif l['ruleset'] == "Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      return setteamm   
    

  
###################[Little League]####################
    elif l['ruleset'] == "Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      return setteamm   

###################[Lost Legendaries]####################
    elif l['ruleset'] == "Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      return setteamm         

###################[Lost Magic]####################
    elif l['ruleset'] == "Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      return setteamm      


###################[Melee Mayhem]####################
    elif l['ruleset'] == "Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      return setteamm     

###################[Noxious Fumes]####################
    elif l['ruleset'] == "Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      return setteamm     

###################[Odd Ones Out]####################
    elif l['ruleset'] == "Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      return setteamm      


###################[Reverse Speed]####################
    elif l['ruleset'] == "Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Rise of the Commons]####################
    elif l['ruleset'] == "Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Silenced Summoners]####################
    elif l['ruleset'] == "Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Spreading Fury]####################
    elif l['ruleset'] == "Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Stampede]####################
    elif l['ruleset'] == "Stampede":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      return setteamm    


###################[Super Sneak]####################
    elif l['ruleset'] == "Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Taking Sides]####################
    elif l['ruleset'] == "Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      return setteamm     


###################[Target Practice]####################
    elif l['ruleset'] == "Target Practice":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      return setteamm     

###################[Unprotected]####################
    elif l['ruleset'] == "Unprotected":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      return setteamm           


###################[Up Close and Personal]####################
    elif l['ruleset'] == "Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      return setteamm

###################[Weak Magic]####################
    elif l['ruleset'] == "Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/standard.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/standard.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      
      
      return setteamm    
  




  

  
##############[team]###########################  
  try:
    setteam = rule()
  except:
    print("No Team for this rulset/element")
  

      
####################################################   
      
  if str(l['mana_cap']) == "12":
    try:
      team = (setteam['12'])
      send()
    except:
      print("cant submit team")
      exit()
   
    
  elif str(l['mana_cap']) == "13":
    try:
      team = (setteam['13'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "14":
    try:
      team = (setteam['14'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "15":
    try:
      team = (setteam['15'])
      send()
    except:
      print("cant submit team")
      exit()
      
   

  elif str(l['mana_cap']) == "16":
    try:
      team = (setteam['16'])
      send()
    except:
      print("cant submit team")
      exit()
   
    
  elif str(l['mana_cap']) == "17":
    try:
      team = (setteam['17'])
      send()
      
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "18":
    try:
      team = (setteam['18'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "19":
    try:
      team = (setteam['19'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "20":
    try:
      team = (setteam['20'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "21":
    try:
      team = (setteam['21'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "22":
    try:
      team = (setteam['22'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "23":
    try:
      team = (setteam['23'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "24":
    try:
      team = (setteam['24'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "25":
    try:
      team = (setteam['25'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "26":
    try:
      team = (setteam['26'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "27":
    try:
      team = (setteam['27'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "28":
    try:
      team = (setteam['28'])
      send()
    except:
      print("cant submit team")
      exit()

  elif str(l['mana_cap']) == "29":
    try:
      team = (setteam['29'])
      send()
    except:
      print("cant submit team")
      exit()
   

  elif str(l['mana_cap']) == "30":
    try:
      team = (setteam['30'])
      send()
    except:
      print("cant submit team")
      exit()
   


  elif str(l['mana_cap']) == "31":
    try:
      team = (setteam['31'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "32":
    try:
      team = (setteam['32'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "33":
    try:
      team = (setteam['33'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "34":
    try:
      team = (setteam['34'])
      send()
    except:
      print("cant submit team")
      exit()



  elif str(l['mana_cap']) == "35":
    try:
      team = (setteam['35'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "36":
    try:
      team = (setteam['36'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "37":
    try:
      team = (setteam['37'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "38":
    try:
      team = (setteam['38'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "39":
    try:
      team = (setteam['39'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "40":
    try:
      team = (setteam['40'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "42":
    try:
      team = (setteam['42'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "43":
    try:
      team = (setteam['43'])
      send()
    except:
      print("cant submit team")
      exit()



  elif str(l['mana_cap']) == "44":
    try:
      team = (setteam['44'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "45":
    try:
      team = (setteam['45'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "46":
    try:
      team = (setteam['46'])
      send()
    except:
      print("cant submit team")
      exit()


  elif str(l['mana_cap']) == "47":
    try:
      team = (setteam['47'])
      send()
    except:
      print("cant submit team")
      exit()


  else:
    try:
      team = (setteam['99'])
      send()
    except:
      print("cant submit team")
      exit()

  



    

    
main()
