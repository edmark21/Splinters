'''
version 2.1 release
2:31 PM 6/18/2022

'''



import hashlib
import bs4
import json, requests
import string
import time


from secrets import choice
from typing import List
import os, sys
from beem import Hive
from result import *
from datetime import datetime


import os.path
from os import path
from urllib.request import urlopen

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

  
try:
    url = "https://pastebin.com/raw/mubqfJe0"
    response = requests.get(url)
    a = response.text
    if a == "active":
        print()
    else:
        print("This App is no longer Supported\nPlease Contact the Developer.")
        print("Reason: Out of contract")
        time.sleep(5)
        exit()
              
except:
    exit()



if os.name == 'nt':
  clear = os.system('cls')
else:
  clear = os.system('clear')

clear

check = path.exists('team')

if check == True:
  print()
else:
  print("[!] Pls Extract The team.zip")
  input("\n[! ]Press enter to exit..")
  exit()
  

API2 = "https://api2.splinterlands.com"
BASE_BATTLE = "https://battle.splinterlands.com"



file1 = open('core/acc.txt', 'r')
l = file1.readlines()


uname = l[1].strip()
posting = l[3].strip()
active = l[5].strip()
currency = l[7].strip()
ecr_nako = l[9].strip()
rating_nako = l[11].strip()
rshares_limit = l[13].strip()
show_team = l[15].strip()

def main():
  now = datetime.now()
  
  def r_e():
    
    #####rating
    url_r = "https://api.splinterlands.io/players/details?name="+uname
    uri = requests.get(url_r).json()
    m_rating = uri['rating']

    ######ecr
    url_e = "https://api.splinterlands.io/players/balances?username="+uname
    result_e = requests.get(url_e).json()


    if int(m_rating) > int(rating_nako):
      input(style.RED+"[+] Rating limit detected.")
      exit()

    for i in result_e:
      if i['token'] == "ECR":
        ecr = str(i['balance'])
        pila = len(ecr)
        if pila == 4:
          ecr_int = int(ecr[0]+ecr[1])
          print(style.GREEN+"\n[+] " + str(uname) + " " + str(ecr_int) + "% ECR")
          if ecr_int < int(ecr_nako):
            print("[+] ECR Limit Detected")
            exit()

        elif pila == 3:
          print("\n[+] " + str(uname) + " " + str(ecr[0])+"% ECR")

  r_e()

  


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


  
  
  
  user = uname
  hive = Hive(keys=posting)
  quest_url = "https://api.splinterlands.io/players/quests?username="+user
  quest_url_response = urlopen(quest_url)
  quest_info = json.loads(quest_url_response.read())

  
  
  try:
    api = "https://api2.splinterlands.com/players/outstanding_match?username=" + user
    d = requests.get(api).json()
    transaction_id = d['id']

    print("\n\n[*] Reconnecting Wild Ranked... ")
    resp = get_battle_status(transaction_id)
  except:
    print(style.RED+"[!] No Match Found!")
    time.sleep(2)
    exit()


  dm = "https://api2.splinterlands.com/players/outstanding_match?username="+user


  detect = requests.get(dm).json()

  
  balik = 1
  print(style.YELLOW+"[*] Reconnecting in Wild format..")
  
  try:
    while type(resp) == str or type(resp) == dict and not resp["opponent_player"]:
      resp = get_battle_status(transaction_id)
      time.sleep(2)
      balik += 1

      
      if balik == 8:
        
        print("[?] Reloading")
        if detect['match_type'] == "Ranked":
          os.system('python3 dm-wild.py')
          #os.system('clear')
        time.sleep(5)
        main()

      
  except:
    print("[..] Refreshing")
    time.sleep(6)
    os.system('python3 dm-wild.py')
    main()
    
    
  
    
  def send():


    secret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user,  transaction_id, team, secret, False)

    broadcast_reveal_team(hive, user, team, secret, transaction_id, team_hash, False)

    secret = gensecret = generate_secret()
    trx_id, team_hash = broadcast_submit_team(hive, user, transaction_id, team, secret, False)
    
    bat()
    
    allcards = open("core/allcards.json")
    ac = json.load(allcards) 
    if show_team == "TRUE":
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
      print("[=>]", total, "=> Total\n")
    
    print("[+] Team Submited")

    print("[+] Getting Battle Result.")
    
      
    def refresh_data():

      url = "https://api.splinterlands.io/battle/history?player="+uname
      url_json = requests.get(url).json()
      result_json = url_json['battles'][0]
      return result_json


    c = 0
    while True:
      refresh = refresh_data()
      time.sleep(2)
      c += 1
      if c == 13:
        print(style.CYAN+"[?] It Takes too long to get the result.")
        break

      if refresh['battle_queue_id_1'] == transaction_id:
        break

      elif refresh['battle_queue_id_2'] == transaction_id:
        break

      else:
        lg = ("Loading")


    sa = refresh_data()


    r()
    if sa['battle_queue_id_1'] == transaction_id:
      if sa['winner'] == uname:
        print(style.GREEN+'[+] Winner:', sa['winner'], "Dec:", sa['reward_dec'])
        print("[+] Rating", sa['player_1_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])

      elif sa['winner'] == "DRAW":
        print(style.RESET+"[=] Draw")
        print("[+] Rating", sa['player_1_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])
        
      else:
        print(style.RED+"[!] You Lose")
        print("[+] Rating", sa['player_1_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])
      
      

      
      
    elif sa['battle_queue_id_2'] == transaction_id:
      if sa['winner'] == uname:
        print(style.GREEN+'[+] Winner:', sa['winner'], "Dec:", sa['reward_dec'])
        print("[+] Rating", sa['player_2_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])

      elif sa['winner'] == "DRAW":
        print(style.RESET+"[=] Draw")
        print("[+] Rating", sa['player_2_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])
        
      else:
        print(style.RED+"[!] You Lose")
        print("[+] Rating", sa['player_2_rating_final'])
        urlt = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Manila"
        relo = requests.get(urlt).json()
        print("[+] Time:", relo['date'], relo['time'])
      

      
    
      
    





  def bat():
    print("[+] Match Found")
    a = ["Red", "White", "Blue", "Green", "Black", "Gold"]
    b = resp['inactive'].split(',')
    b = [ x for x in a if not x in b ] 
    listToStr = ' '.join([str(elem) for elem in b])
    print(style.MAGENTA+"[?]", "["+listToStr+"]")
    print("[>] " + resp['player'] + " vs " + resp['opponent_player'] + "\n" + "[>] Manacap: " + str(resp['mana_cap']) + "\n[>] Ruleset: " + resp['ruleset'])




  a = ["Red", "White", "Blue", "Green", "Black", "Gold"]
  b = resp['inactive'].split(',')
  b = [ x for x in a if not x in b ] 
  listToStr = ' '.join([str(elem) for elem in b])
################[single]############
#################[all rules]##########################      

  def rule():
    if resp['ruleset'] == resp['ruleset']:
      change = resp['ruleset'].replace("|", "_")

      for qst in quest_info:
      
        if qst['name'] == "lyanna":
          print(style.GREEN+"[+] Earth Quest Detetced.")
          e_t = "earth"
          c_t = "Green"

        elif qst['name'] == "pirate":
          print(style.BLUE+"[+] Water Quest Detetced.")
          e_t = "water"
          c_t = "Blue"

        else:
          print(style.MAGENTA+"[+] Activating Rating Booster mode")
          e_t = "earth"
          c_t = "Green"
          
    
    #
      if c_t in listToStr:
        fn = open("team/"+e_t+"/"+change+".json")
        setteamm = json.load(fn)
        
      return setteamm

  
  setteam = rule()


####################################################   
      
  if str(resp['mana_cap']) == str(resp['mana_cap']):
    try:
      team = (setteam[str(resp['mana_cap'])])
      send()
      time.sleep(2)
      exit()
      
      

    except:
      print(style.RED+"[!] Cant submit team")
      print("[!] Reconnecting.....")
      os.system("python3 dm-wild.py")
      main()
   

    
main()
