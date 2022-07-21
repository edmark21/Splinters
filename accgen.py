import requests, json

f = open('pastebin.txt', 'r')
l = f.readlines()


url = l[0]



a = requests.get(url).json()
    






def logo():
    c = 0
    for i in a['accounts']:
        n = i['account_name']
        c += 1
    l = f'''


                                    _      _____             __ _       
     /\                            | |    / ____|           / _(_)      
    /  \   ___ ___ ___  _   _ _ __ | |_  | |     ___  _ __ | |_ _  __ _ 
   / /\ \ / __/ __/ _ \| | | | '_ \| __| | |    / _ \| '_ \|  _| |/ _` |
  / ____ \ (_| (_| (_) | |_| | | | | |_  | |___| (_) | | | | | | | (_| |
 /_/____\_\___\___\___/ \__,_|_| |_|\__|  \_____\___/|_| |_|_| |_|\__, |
  / ____|                         | |                              __/ |
 | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __                  |___/ 
 | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|                       
 | |__| |  __/ | | |  __/ | | (_| | || (_) | |                          
  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|                          
                                                                        
                          {c} Tottal Account


    '''
    print(l)

       

      
    
    

  
def main():
    logo()
    n = input("Enter Username: ")
    for i in a['accounts']:
        if n == i['account_name']:
            print("User:", n)
            print("Posting:", i['priv_posting_key'])
            print("Active:", i['priv_active_key'])

            ecr = input("Enter Ecr Limit: ")
            rating = input("Enter Rating Limit: ")
            ranked = input("Enter Ranked Type [Modern or Wild]: ")

    config = f'''#################### USERNAME ###################################
{n}
#################### POSTING_KEY ##############################
{i['priv_posting_key']}
##################### ACTIVE_KEY ################################
{i['priv_active_key']}
####### Currency to use in renting (DEC OR CREDITS) ############
DEC
#################### ECR LIMIT TO STOP THE BOT #################
{ecr}
################ RATING LIMIT TO STOP THE BOT #################
{rating}
################# RSHARES LIMIT TO STOP THE BOT ###############
920882
################ SHOW TEAM SET TRUE or FALSE ##################
FALSE
#################### Modern or Wild Ranked ######################
{ranked}
######################### TOKEN #############################
mubqfJe0
################################################################
'''
    f = open('core/acc.txt', 'w')
    f.write(config)
    f.close
    
    
    

        
main()    
        
            





