'''
version 2 release
1:27 PM 6/12/2022

'''



import hashlib
import bs4
import json, requests
import string
import time


from secrets import choice
from typing import List
import os, sys
import requests
from beem import Hive
from result import *

import os.path
from os import path



os.system('clear')


API2 = "https://api2.splinterlands.com"
BASE_BATTLE = "https://battle.splinterlands.com"

f = open('core/acc.txt')
n = f.readlines()


name = n[0]

res = " " in name

uname = name.split()[0]
ecr_nako = name.split()[4]
rating_nako = name.split()[5]





check = path.exists('team')

if check == True:
  print()
else:
  print("[!] Pls download team folder first")
  input("\nPress enter to exit..")
  exit()
  



def main():
  def r_e():
    #####rating
    url_r = "https://api.splinterlands.io/players/details?name="+uname
    uri = requests.get(url_r).json()
    m_rating = uri['rating']

    ######ecr
    url_e = "https://api.splinterlands.io/players/balances?username="+uname
    result_e = requests.get(url_e).json()


    if int(m_rating) > int(rating_nako):
      input("[+] Rating limit detected.")
      exit()

    for i in result_e:
      if i['token'] == "ECR":
        ecr = str(i['balance'])
        pila = len(ecr)
        if pila == 4:
          ecr_int = int(ecr[0]+ecr[1])
          print("\n[+]", ecr_int + "%")
          if ecr_int < int(ecr_nako):
            print("[+] ECR Limit Detected")
            exit()

        elif pila == 3:
          print(ecr[0]+"%")

  r_e()

  
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
    f = open('core/acc.txt')
    n = f.readlines()


    name = n[0]

    res = " " in name

    mao = name.split()[0]
    mao2 = name.split()[1]
    
 

    user = mao
    hive = Hive(keys=[mao2])

    

    
    transaction_id = broadcast_find_match(hive, user, "Ranked", False)
    print("\n\n[*] Starting ")
    resp = get_battle_status(transaction_id)


  
  except:
    print("[!] Incorrect account...")
    print("[*] Troubleshooting......\n")
    time.sleep(1)
    main()

  
  
  dm = "https://api2.splinterlands.com/players/outstanding_match?username="+user


  detect = requests.get(dm).json()

  
  balik = 1
  print("[*] Finding Match")
  
  try:
    while type(resp) == str or type(resp) == dict and not resp["opponent_player"]:
      resp = get_battle_status(transaction_id)
      time.sleep(2)
      balik += 1

      
      if balik == 8:
        
        print("[?] Reloading")
        if detect['match_type'] == "Ranked":
          os.system('python3 dm.py')
          #os.system('clear')
        time.sleep(5)
        main()

      
  except:
    print("[..] Refreshing")
    time.sleep(6)
    os.system('python3 dm.py')
    main()
    
    
  
    
  def send():


    secret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user,  transaction_id, team, secret, False)

    broadcast_reveal_team(hive, user, team, secret, transaction_id, team_hash, False)

    secret = gensecret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user, transaction_id, team, secret, False)
    
    bat()
    '''
    allcards = open("core/allcards.json")
    ac = json.load(allcards) 
    
    total = 0
    for i in team:
      
      t = i.split('-')
      ids = int(t[1])
      for a in ac:
        if a['id'] == ids:
          m = a['stats']['mana']

          if type(m) == list:
            print("[=>]", m[0], i, "=>", a['name'])
            total += m[0]
          else:
            print("[=>]", m, i, "=>", a['name'])
            total += m
    print("[=>]", total, "=> Total")
    '''
    print("[+] Team Submited")
    r()





  def bat():

    print("\n[+] Match Found")
    a = ["Red", "White", "Blue", "Green", "Black", "Gold"]
    b = resp['inactive'].split(',')
    b = [ x for x in a if not x in b ] 
    listToStr = ' '.join([str(elem) for elem in b])
    print("[?]", "["+listToStr+"]")
    print("[>] " + resp['player'] + " vs " + resp['opponent_player'] + "\n" + "[>] Manacap: " + str(resp['mana_cap']) + "\n[>] Ruleset: " + resp['ruleset'] + "\n")





################[single]############
#################[all rules]##########################      

  def rule():
    if resp['ruleset'] == resp['ruleset']:
      change = resp['ruleset'].replace("|", "_")
      if "Green" in aa:
        fn = open("team/earth/"+change+".json")
        setteamm = json.load(fn)
      
      elif "Blue" in aa:
        fn = open("team/water/"+change+".json")
        setteamm = json.load(fn)

      elif "Red" in aa:
        fn = open("team/fire/"+change+".json")
        setteamm = json.load(fn)

      elif "Black" in aa:
        fn = open("team/death/"+change+".json")
        setteamm = json.load(fn)
      
      elif "White" in aa:
        fn = open("team/life/"+change+".json")
        setteamm = json.load(fn)

      elif "Gold" in aa:
        fn = open("team/dragon/"+change+".json")
        setteamm = json.load(fn)


      return setteamm  



####################################################   
      
  if str(l['mana_cap']) == str(l['mana_cap']):
    try:
      team = (setteam[str(l['mana_cap'])])
      send()
    except:
      print("cant submit team")
      print("Reconnecting.....")
      time.sleep(1)
      os.system("python3 dm.py")
      main()
   

    
main()
  
