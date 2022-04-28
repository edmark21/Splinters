import requests, os
from beem import Hive


os.system('clear')
import os,sys, requests, json, time

c_l = open('cards.txt')
API2 = "https://api2.splinterlands.com"

logo = '''\033[0;35m


  ======================================
  [ SPLINTERS AUTO RENT MULTIPLE CARDS ]
  [        Develop by: Edmark          ]
  ======================================
\033[0;36m
        [1] Auto
        [2] Manual


'''



try:
  f = open('acc.txt')
  n = f.readlines()


  name = n[0]

  res = " " in name

  mao = name.split()[0]
  posting = name.split()[-1]
  active = name.split()[-2]
  
  username = mao

  #  your posting keyword and active keyword
  passwords = [posting, active]

except:
  print("[!] Incorrect account...")
  input("\n\n\n\n[?] Press Enter to continue.....")
  sys.exit()  
  

hive = Hive(keys=passwords)


url = "https://api.splinterlands.io/cards/get_details"
l = requests.get(url).json()

fi = open('cards.txt')








############################





      
      
      

      


          

    
    

      
def main():
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
          print("\033[1;33m", count, player, 'rented\033[1;36m', i['name'], "\033[1;32mSuccessfully.")
        



        
    
    def sulod():
      for i in l:
        if i['id'] == ci:
          cards_sorted = get_rent_cards_xp(i['id'], i['editions'], False, 1, 50)
          for card_sorted in cards_sorted:
            if verify(card_sorted.market_id, card_sorted.uid, card_sorted.detail_id):
              rent_card(username, [card_sorted.market_id], 1, 'DEC')
              break  
            print('no available cards')

    sulod()      
    


############################################
def main2():
  ci = int(input("Enter card Id: "))
  
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
        print("\033[1;33m",player, 'rented\033[1;36m', i['name'], "\033[1;32mSuccessfully.")
    
     
    
    
    


  def sulod():
    for i in l:
      if i['id'] == ci:
        
        cards_sorted = get_rent_cards_xp(i['id'], i['editions'], False, 1, 50)
        
    

        for card_sorted in cards_sorted:
          if verify(card_sorted.market_id, card_sorted.uid, card_sorted.detail_id):
            rent_card(username, [card_sorted.market_id], 1, 'DEC')
            main2()
        print('no available cards')
  sulod()
  

def menu():
  os.system('clear')
  print(logo)
  option = input("\033[0;32mSelect Option: \033[1;33m")
  if option == "1":
    main()
    input("\n\nRent Complete, Please Enter To Continue..")
  elif option == "2":
    main2()
    input("\n\nRent Complete, Please Enter To Continue..")
  else:
    print("Invalid command")
    time.sleep(4)
    menu()

menu()

