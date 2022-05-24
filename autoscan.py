import os, sys, json

cards = open('core/allcards.json')
c = json.load(cards)

def scan():
  path = "team"
  co = os.listdir(path)
  pf = "team/"
  print("Please wait...")
  allc = open('core/cards_collection.json')
  l = json.load(allc)
  total = 1


  
  for i in l['cards']:
    ids = i['card_detail_id']
    uids = i['uid']
    for a in c:
      if ids == a['id']:
        #print(ids, uids, a['name'].replace(" ", "_").lower())
        old = a['name'].replace(" ", "_").lower() #name
        new = uids #uid

        for content in co:
          #sulod sa team folder
          sulod = os.listdir(pf+content)
          total = 1

          for content_folder in sulod:
            counter = 0
            #sulod sa mga folder sa team

            with open(pf + content + "/" +content_folder, "r", encoding="utf-8") as file:
              result = file.read()
              counter  = result.count(old)
              result = result.replace(old, new)

            with open(pf + content + "/" + content_folder, "w", encoding="utf-8") as newfile:
              newfile.write(result)

            if counter:
              total+=1

  print("\n[+] Fullname to Uid replaced, Success.")
  

              

            
            
        

scan()
