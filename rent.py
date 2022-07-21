'''
rent
1:30 PM 6/12/2022

'''


import requests, os, sys
from beem import Hive


if os.name == 'nt':
  clear = os.system('cls')
else:
  clear = os.system('clear')

clear 
import os,sys, requests, json, time

c_l = open('core/cards.txt')
c = 0
for i in c_l:
  c += 1
  
API2 = "https://api2.splinterlands.com"





try:

  file1 = open('core/acc.txt', 'r')
  l = file1.readlines()


  mao = l[1].strip()
  posting = l[3].strip()
  active = l[5].strip()
  kwarta = l[7].strip()
  ecr_nako = l[9].strip()
  rating_nako = l[11].strip()
  rshares_limit = l[13].strip()
  show_team = l[15].strip()
  token = l[19].strip()



  username = mao

  #  your posting keyword and active keyword
  passwords = [posting, active]

except:
  print("[!] Incorrect account...")
  input("\n\n\n\n[?] Press Enter to continue.....")
  sys.exit()  
  

hive = Hive(keys=passwords)



try:
    url = f"https://pastebin.com/raw/{token}"
    response = requests.get(url)
    a = response.text
    if a == "active":
        print()
    else:
        print("[!] Your Subscription is Expired")
        input("[*] Reason: Out of contract")
        exit()
              
except:
    input("[!] There's an error")
    exit()
  

logo = f'''


  ======================================
  [ SPLINTERS AUTO RENT MULTIPLE CARDS ]
  [        Develop by: Edmark          ]
  ======================================

         Login as: {username}
              
        [1] Auto [''' + str(c) + ''' cards pending]
        [2] Manual
        [3] Settings
        [4] Exit


'''

url = "https://api.splinterlands.io/cards/get_details"
l = requests.get(url).json()

fi = open('core/cards.txt')








############################





      
      
      

      


          

    
    

      
def main():
  
  try:
    class Card:
      market_id = ''
      uid = ''
      detail_id = 0
      price = 0

      def __init__(self, m, u, d, p):
        self.market_id = m
        self.uid = u
        self.detail_id = d
        self.price = p

      def __lt__(self, other):
        return self.price < other.price


    def get_rent_cards_xp(card_id: int, edition: int, gold: bool, xp: int, price: float) -> list:
      url = API2 + "/market/for_rent_by_card"
      request: dict = {"card_detail_id": card_id,
                     "gold": gold,
                     "edition": edition}
      rent_cards = requests.get(url, params=request).json()
      cards = [card for card in rent_cards if card.get("xp") >= xp and float(card.get("buy_price")) <= price]
      v_cards = []
      for c in cards:
          v_cards.append(Card(c.get('market_id'), c.get('uid'), c.get('card_detail_id'), float(c.get('buy_price'))))
      v_cards.sort()
      return v_cards

    def verify(market_id: str, uid: str, card_detail_id: int) -> bool:
      url = API2 + "/market/validateListing"
      request: dict = {"card_detail_id": card_detail_id,
                     "uid": uid,
                     "market_id": market_id}
      return requests.get(url, params=request).json().get('isValid')




    count = 0
    for zaw in fi:
      count += 1
      ci = int(zaw.strip())
      def rent_card(player: str, card_ids: list, days: int, currency: str):
        for i in l:
          if i['id'] == ci:
            data: dict = {"items": card_ids,
                  "currency": currency,
                  "days": days,
                  "app": "splinterlands/0.7.139"}
            hive.custom_json("sm_market_rent", data, required_auths=[player], required_posting_auths=[])
            print(count, player, 'rented', i['name'], "Successfully.")
        



        
    
      def sulod():
        for i in l:
          if i['id'] == ci:
            cards_sorted = get_rent_cards_xp(i['id'], i['editions'], False, 1, 50)
            for card_sorted in cards_sorted:
              if verify(card_sorted.market_id, card_sorted.uid, card_sorted.detail_id):
                rent_card(username, [card_sorted.market_id], 1, kwarta)
                break  
              print('no available cards')

      sulod()

  except:
    print("\n___________________")
    print("[!] Not enough RC.")
    print("___________________")
    input("\n\nPlease power up your RC and\nPress enter to continue...")
    main()

  
    
    


############################################
def main2():
  ci = int(input("Enter card Id: "))
  try:
    class Card:
      market_id = ''
      uid = ''
      detail_id = 0
      price = 0

      def __init__(self, m, u, d, p):
          self.market_id = m
          self.uid = u
          self.detail_id = d
          self.price = p

      def __lt__(self, other):
          return self.price < other.price


    def get_rent_cards_xp(card_id: int, edition: int, gold: bool, xp: int, price: float) -> list:
      url = API2 + "/market/for_rent_by_card"
      request: dict = {"card_detail_id": card_id,
                       "gold": gold,
                       "edition": edition}
      rent_cards = requests.get(url, params=request).json()
      cards = [card for card in rent_cards if card.get("xp") >= xp and float(card.get("buy_price")) <= price]
      v_cards = []
      for c in cards:
          v_cards.append(Card(c.get('market_id'), c.get('uid'), c.get('card_detail_id'), float(c.get('buy_price'))))
      v_cards.sort()
      return v_cards

    def verify(market_id: str, uid: str, card_detail_id: int) -> bool:
      url = API2 + "/market/validateListing"
      request: dict = {"card_detail_id": card_detail_id,
                       "uid": uid,
                       "market_id": market_id}
      return requests.get(url, params=request).json().get('isValid')


    def rent_card(player: str, card_ids: list, days: int, currency: str):
      for i in l:
        if i['id'] == ci:
          data: dict = {"items": card_ids,
                    "currency": currency,
                    "days": days,
                    "app": "splinterlands/0.7.139"}
          hive.custom_json("sm_market_rent", data, required_auths=[player], required_posting_auths=[])
          print(player, 'rented', i['name'], "Successfully.")
      
       
      
      
      


    def sulod():
      for i in l:
        if i['id'] == ci:
          
          cards_sorted = get_rent_cards_xp(i['id'], i['editions'], False, 1, 50)
          
      

          for card_sorted in cards_sorted:
            if verify(card_sorted.market_id, card_sorted.uid, card_sorted.detail_id):
              rent_card(username, [card_sorted.market_id], 1, kwarta)
              main2()
          print('no available cards')
    sulod()
  except:
    print("\n___________________")
    print("[!] Not enough RC.")
    print("___________________")
    input("\n\nPlease power up your RC and\nPress enter to continue...")
    main2()
    
  

  
def menu():

  print(logo)
  option = input("[?] Select Option: ")
  if option == "1":
    main()
    input("\n\nRent Complete, Please Enter To Continue..")
  elif option == "2":
    main2()
    input("\n\nRent Complete, Please Enter To Continue..")
  elif option == "3":
    exit()
    
  else:
    print("Invalid command")
    time.sleep(4)
    menu()

menu()
