'''
CHECK IF RENTED OR NOT
3:16 PM 5/24/2022
'''


import os, sys, requests, json

al = open('core/allcards.json')
ali = json.load(al)

f = open('core/cards.txt')
cards = f.readlines()

mycards = open('core/cards_collection.json')
mc = json.load(mycards)




ca = []

for i in cards:
    a = int(i.strip())
    b = ca.append(a)




csl = []
for i in mc['cards']:
    c = i['card_detail_id']
    a = csl.append(c)
    




bb = [ x for x in ca if not x in csl ]
listToStr = ' '.join([str(elem) for elem in bb])




l = '''\n
+---------------------------------+
|   You Dont have this cards yet  |
+---------------------------------+

'''
print(l)
for i in bb:
    #print(listToStr)
    for h in ali:
        if h['id'] == i:
            name = h['name'].replace(" ", "_").lower()
            print(h['id'], name)



    
input("\n\nPress Enter to exit...")
            
    

