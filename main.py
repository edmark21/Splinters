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

if os.name == 'nt':
  os.system('cls')
else:
  os.system('clear')

API2 = "https://api2.splinterlands.com"
BASE_BATTLE = "https://battle.splinterlands.com"




logo = '''\033[1;32m

 ███████╗██████╗ ██╗     ██╗███╗   ██╗████████╗███████╗██████╗ ███████╗
 ██╔════╝██╔══██╗██║     ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝
 ███████╗██████╔╝██║     ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝███████╗
 ╚════██║██╔═══╝ ██║     ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗╚════██║
 ███████║██║     ███████╗██║██║ ╚████║   ██║   ███████╗██║  ██║███████║
 ╚══════╝╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
                                                     
                       [ Beta version ]              
               


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
    main()

  
  dm = "https://api2.splinterlands.com/players/outstanding_match?username="+user


  detect = requests.get(dm).json()





  
  balik = 1
  reload = 1
  try:
    while type(resp) == str or type(resp) == dict and not resp["opponent_player"]:
      resp = get_battle_status(transaction_id)
      print("\033[0;36m[*]" + "\033[1;37m Finding Match")
      time.sleep(2)
      balik += 1
      reload += 1

      
      if balik == 8:
        
        print("[?] Reloading")
        time.sleep(5)
        main() 
      
    


      
  except:
    print("[..] Refreshing")
    time.sleep(10)
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
    #time.sleep(2)
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

      print("\033[1;35m[>] " + "\033[0;34m" + lx['player'] + "\033[1;37m vs \033[0;31m" + lx['opponent_player'] + " = " + "\033[0;32mManacap: " + str(lx['mana_cap']) + " => " + "\n    Ruleset: " + lx['ruleset'])
      
    except:
      print("Something error is happening.")
      time.sleep(2)
      main()

  
    
    
  




  
         
  
      




  url = (API2 + "/battle/status?id=" + transaction_id)

  a = ["Red", "White", "Blue", "Green", "Black", "Gold"]

  
  b = l['inactive'].split(',')
  

  b = [ x for x in a if not x in b ] 

  aa = ' '.join([str(elem) for elem in b])   


  
################[single]############
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

      elif "Black" in aa:
        fn = open("team/death/standard.json")
        setteamm = json.load(fn)
      
      elif "White" in aa:
        fn = open("team/life/standard.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/standard.json")
        setteamm = json.load(fn)



        

      return setteamm  
##################[armored up]########################
    elif l['ruleset'] == "Armored Up":
      if "Blue" in aa:
        fn = open("team/water/armored_up.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/earth/armored_up.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/armored_up.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/armored_up.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/armored_up.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/armored_up.json")
        setteamm = json.load(fn)


      

      
      return setteamm  
###################[aim true]#######################
    elif l['ruleset'] == "Aim True":
      if "Green" in aa:
        fn = open("team/earth/aim_true.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/aim_true.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/aim_true.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/aim_true.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/aim_true.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/aim_true.json")
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
        
      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
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

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)


      return setteamm        


###################[Close Range]####################
    elif l['ruleset'] == "Close Range":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)


      return setteamm         


###################[Earthquake]####################
    elif l['ruleset'] == "Earthquake":
      if "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)
        
      elif "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)

      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)

      return setteamm      


###################[Equalizer]####################
    elif l['ruleset'] == "Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)
      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)


      return setteamm      
      
###################[Equal Opportunity]####################
    elif l['ruleset'] == "Equal Opportunity":
      if "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
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

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)


      return setteamm          


###################[Explosive Weaponry]####################
    elif l['ruleset'] == "Explosive Weaponry":
      if "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
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

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)


      return setteamm  

###################[Healed Out]####################
    elif l['ruleset'] == "Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)


      return setteamm   




###################[Heavy Hitters]####################
    elif l['ruleset'] == "Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)


      return setteamm   


###################[Holy Protection]####################
    elif l['ruleset'] == "Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
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

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
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

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
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

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
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

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
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

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)


      return setteamm     

###################[Noxious Fumes]####################
    elif l['ruleset'] == "Noxious Fumes":
      if "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)


      return setteamm     

###################[Odd Ones Out]####################
    elif l['ruleset'] == "Odd Ones Out":
      if "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)


      return setteamm      


###################[Reverse Speed]####################
    elif l['ruleset'] == "Reverse Speed":
      if "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
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

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)


      return setteamm     


###################[Silenced Summoners]####################
    elif l['ruleset'] == "Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)


      return setteamm     


###################[Spreading Fury]####################
    elif l['ruleset'] == "Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)


      return setteamm     


###################[Stampede]####################
    elif l['ruleset'] == "Stampede":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)


      return setteamm    


###################[Super Sneak]####################
    elif l['ruleset'] == "Super Sneak":
      if "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)
        
      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
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

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
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

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)


      return setteamm     

###################[Unprotected]####################
    elif l['ruleset'] == "Unprotected":
      if "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
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

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)


      return setteamm

###################[Weak Magic]####################
    elif l['ruleset'] == "Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
      
      
      return setteamm    
  

#########################################
############[Double]################



###################[Weak Magic]####################
    elif l['ruleset'] == "Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
      
      
      return setteamm    

###################################################
###########[DOUBLE RULESET]########################
#############[Part 1]#############################      
###################[Aim True]####################
    elif l['ruleset'] == "Aim True|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
      
      
      return setteamm   

      
    elif l['ruleset'] == "Aim True|Close Range":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
      
      
      return setteamm   
    elif l['ruleset'] == "Aim True|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Stampede":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Aim True|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
      
      
      return setteamm
 
###################[Armored up]####################
    elif l['ruleset'] == "Armored Up|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Close Range":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Stampede":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Armored Up|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
      
      
      return setteamm
      
###################[Back To Basics]####################  

    elif l['ruleset'] == "Back To Basics|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Close Range":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Little League":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Stampede":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm
    elif l['ruleset'] == "Back To Basics|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
      
      
      return setteamm

###################[Broken Arows]####################  

    elif l['ruleset'] == "Broken Arrows|Aim True":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
      
    elif l['ruleset'] == "Broken Arrows|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
        
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Back to Basics":
      
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Stampede":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Broken Arrows|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm

###################[Close Range]####################  

    elif l['ruleset'] == "Close Range|Aim True":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Stampede":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Close Range|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm

###################[Earthquake]####################  

    elif l['ruleset'] == "Earthquake|Aim True":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Close Range":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Little League":
      
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
      
    elif l['ruleset'] == "Earthquake|Lost Legendaries":
      
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Stampede":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Earthquake|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###################[Equal Opportunity]####################  

    elif l['ruleset'] == "Equal Opportunity|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Close Range":
      if "Green" in aa:
        fn = open("team/earth/close_range.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/close_range.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/close_range.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/close_range.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/close_range.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/close_range.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Stampede":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equal Opportunity|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm



#############[Equalizer]############################# 
 
    elif l['ruleset'] == "Equalizer|Aim True":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Close Range":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Stampede":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Equalizer|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[Even Stevens]############################# 

    elif l['ruleset'] == "Even Stevens|Aim True":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Close Range":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Stampede":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Even Stevens|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm




#############[Part 2]############################# 
#############[Explosive Weaponry]#################     


    elif l['ruleset'] == "Explosive Weaponry|Aim True":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Close Range":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Stampede":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Explosive Weaponry|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/explosive_weaponry.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/explosive_weaponry.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/explosive_weaponry.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[Fog of War]#################   

    elif l['ruleset'] == "Fog of War|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Close Range":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Stampede":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Fog of War|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[Healed Out#################   

    elif l['ruleset'] == "Healed Out|Aim True":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Close Range":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Explosive Weaponry":   
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Stampede":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Healed Out|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[Heavy Hitters]#################   

    elif l['ruleset'] == "Heavy Hitters|Aim True":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Close Range":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Stampede":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Heavy Hitters|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/heavy_hitters.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/heavy_hitters.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/heavy_hitters.json")
        setteamm = json.load(fn)
        
      
      return setteamm


      
#############[Holy Protection]#################   

    elif l['ruleset'] == "Holy Protection|Aim True":
      
      if "Green" in aa:
        
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Close Range":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Stampede":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Holy Protection|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/holy_protection.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/holy_protection.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/holy_protection.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/holy_protection.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/holy_protection.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/holy_protection.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[Holy Protection]#################  
      
    elif l['ruleset'] == "Keep Your Distance|Aim True":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Close Range":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Keep Your Distance|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm


      
#############[Little League]#################  

    elif l['ruleset'] == "Little League|Aim True":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Close Range":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Little League|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Little League|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Stampede":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Little League|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm

#############[Lost Legendaries]#################        

    elif l['ruleset'] == "Lost Legendaries|Aim True":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Close Range":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Stampede":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Legendaries|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm




      
#############[Lost Magic]#################        

    elif l['ruleset'] == "Lost Magic|Aim True":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Close Range":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Stampede":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Lost Magic|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm


#############[part 3]#################    
#############[Melee Mayhem]#################            



    elif l['ruleset'] == "Melee Mayhem|Aim True":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Close Range":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Melee Mayhem|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Stampede":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Melee Mayhem|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    
    elif l['ruleset'] == "Melee Mayhem|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm

#############[Noxious Fumes]#################  

    elif l['ruleset'] == "Noxious Fumes|Aim True":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Close Range":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Stampede":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Noxious Fumes|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm



      
#############[Odd Ones Out]#################  


    elif l['ruleset'] == "Odd Ones Out|Aim True":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Close Range":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Stampede":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Odd Ones Out|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm



#############[Reverse Speed]#################  


    elif l['ruleset'] == "Reverse Speed|Aim True":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Close Range":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Stampede":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Reverse Speed|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm



#############[Rise of the Commons]#################  
    
    elif l['ruleset'] == "Rise of the Commons|Aim True":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Close Range":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Stampede":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Rise of the Commons|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm




###########[Silenced Summoners]#################  

    elif l['ruleset'] == "Silenced Summoners|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Close Range":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Stampede":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Silenced Summoners|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###########[Spreading Fury]################# 


    elif l['ruleset'] == "Spreading Fury|Aim True":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Close Range":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/equal_opportunity.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equal_opportunity.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equal_opportunity.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Stampede":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Spreading Fury|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/spreading_fury.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/spreading_fury.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/spreading_fury.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/spreading_fury.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###########[Stampede]################# 


    elif l['ruleset'] == "Stampede|Aim True":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/back_to_basics.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/back_to_basics.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/back_to_basics.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/back_to_basics.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Close Range":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/fog_of_war.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/fog_of_war.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/fog_of_war.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/fog_of_war.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/silenced_summoners.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/silenced_summoners.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/silenced_summoners.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Stampede|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/stampede.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/stampede.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/stampede.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/stampede.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/stampede.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/stampede.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###########[Super Sneak]################# 

    elif l['ruleset'] == "Super Sneak|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Close Range":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Stampede":
      if "Green" in aa:
        fn = open("team/earth/super_sneak.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/super_sneak.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/super_sneak.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/super_sneak.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/super_sneak.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/super_sneak.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Super Sneak|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###########[Taking Sides]################# 

    elif l['ruleset'] == "Taking Sides|Aim True":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Close Range":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Stampede":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Target Practice":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Taking Sides|Weak Magic":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm


###########[Target Practice]#################
    
    elif l['ruleset'] == "Target Practice|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Close Range":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Stampede":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Target Practice|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/target_practice.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/target_practice.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/target_practice.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/target_practice.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/target_practice.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/target_practice.json")
        setteamm = json.load(fn)
        
      
      return setteamm

###########[Unprotected]#################

    elif l['ruleset'] == "Unprotected|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Close Range":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Earthquake":

      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Lost Magic":
      if "Green" in aa:
        fn = open("team/earth/lost_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Stampede":
      if "Green" in aa:
        fn = open("team/earth/unprotected.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/unprotected.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/unprotected.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/unprotected.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/unprotected.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/unprotected.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Unprotected|Up Close & Personal":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm




###########[Up Close & Personal]#################


    elif l['ruleset'] == "Up Close & Personal|Aim True":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Armored Up":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Back to Basics":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Equal Opportunity":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Fog of War":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Silenced Summoners":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Stampede":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Super Sneak":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Up Close & Personal|Unprotected":
      if "Green" in aa:
        fn = open("team/earth/up_close_and_personal.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/up_close_and_personal.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/up_close_and_personal.json")
        setteamm = json.load(fn)
        
      
      return setteamm





    
###########[Weak Magic]#################



    elif l['ruleset'] == "Weak Magic|Broken Arrows":
      if "Green" in aa:
        fn = open("team/earth/broken_arrows.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/broken_arrows.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/broken_arrows.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/broken_arrows.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Close Range":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Earthquake":
      if "Green" in aa:
        fn = open("team/earth/earthquake.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/earthquake.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/earthquake.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/earthquake.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/earthquake.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/earthquake.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Equalizer":
      if "Green" in aa:
        fn = open("team/earth/equalizer.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/equalizer.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/equalizer.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/equalizer.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/equalizer.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/equalizer.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Even Stevens":
      if "Green" in aa:
        fn = open("team/earth/even_stevens.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/even_stevens.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/even_stevens.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/even_stevens.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/even_stevens.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/even_stevens.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Explosive Weaponry":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Healed Out":
      if "Green" in aa:
        fn = open("team/earth/healed_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/healed_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/healed_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/healed_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/healed_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/healed_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Heavy Hitters":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Holy Protection":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Keep Your Distance":
      if "Green" in aa:
        fn = open("team/earth/keep_your_distance.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/keep_your_distance.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/keep_your_distance.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Little League":
      if "Green" in aa:
        fn = open("team/earth/little_league.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/little_league.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/little_league.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/little_league.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/little_league.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/little_league.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Lost Legendaries":
      if "Green" in aa:
        fn = open("team/earth/lost_legendaries.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/lost_legendaries.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/lost_legendaries.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Melee Mayhem":
      if "Green" in aa:
        fn = open("team/earth/melee_mayhem.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/melee_mayhem.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/melee_mayhem.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Noxious Fumes":
      if "Green" in aa:
        fn = open("team/earth/noxious_fumes.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/noxious_fumes.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/noxious_fumes.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Odd Ones Out":
      if "Green" in aa:
        fn = open("team/earth/odd_ones_out.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/odd_ones_out.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/odd_ones_out.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Reverse Speed":
      if "Green" in aa:
        fn = open("team/earth/reverse_speed.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/reverse_speed.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/reverse_speed.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/reverse_speed.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Rise of the Commons":
      if "Green" in aa:
        fn = open("team/earth/rise_of_the_commons.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/rise_of_the_commons.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/rise_of_the_commons.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Spreading Fury":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Stampede":
      if "Green" in aa:
        fn = open("team/earth/weak_magic.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/weak_magic.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/weak_magic.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/weak_magic.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/weak_magic.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/weak_magic.json")
        setteamm = json.load(fn)
        
      
      return setteamm
    elif l['ruleset'] == "Weak Magic|Taking Sides":
      if "Green" in aa:
        fn = open("team/earth/taking_sides.json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/taking_sides.json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/taking_sides.json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/taking_sides.json")
        setteamm = json.load(fn)

      elif "White" in aa:
        fn = open("team/life/taking_sides.json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/taking_sides.json")
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


  elif str(l['mana_cap']) == "99":
    try:
      team = (setteam['99'])
      send()
      
    except:
      print("cant submit team")
      exit()

  



    
main()
    
