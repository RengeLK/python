###################################################
## Aukro watching script
## By Renge. v1.6 2023
###################################################
## This script uses requests for API requests and
## ntfy to send the alerts. Enjoy!
###################################################
import requests
from termcolor import cprint
from dotenv import load_dotenv
import time, os

############
## SETUP  ##
############
load_dotenv()
cprint("Aukro watching script --- By Renge. v1.6", "blue")
cprint("Make sure you have configured the .env!", "yellow")
# aid = input("PLease enter the Aukro listing ID: ")
# topic = input("Please enter the ntfy topic name: ")
aid = os.getenv("AUKRO_ID")
topic = os.getenv("NTFY_TOPIC")
chtime = os.getenv("CHECK_TIME")

hedrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}
inr = requests.get(f'https://aukro.cz/backend-web/api/offers/{aid}/offerDetail', headers=hedrs)

try:
    m_state = inr.json()['state'] # str, ACTIVE or ENDED
    if m_state == "ENDED":
        cprint("This auction has ended. Please choose another one.", "red")
        exit()
except Exception as error:
    cprint("An unknown error has occurred. Check what happened, fix it, and try again.", "yellow")
    cprint(error, "red")
    exit()

m_wcount = str(inr.json()['watchingUserCount']) # int
m_dcount = str(inr.json()['displayedCount']) # int
m_bcount = str(inr.json()['biddersCount']) # int
m_price = str(round(inr.json()['price']['amount'])) # float?? int?? idfk anymore (rounded due to possible float)
m_bname = inr.json()['highestBidderAnonymizedLogin'] # str
m_name = inr.json()['name'] # str
m_etext = inr.json()['endingTimeText'] # str
m_etextb = False # send 5 minute notification only once

requests.post(f'https://ntfy.sh/{topic}',
    data=f'{m_name}, {m_price} Kč by "{m_bname}", {m_bcount} bidders, {m_wcount} followers, {m_dcount} displays. Ending in {m_etext}'.encode("UTF-8"),
    headers={
        "Title": "Script has been set up!",
        "Priority": "default",
        "Tags": "beginner"
    })
cprint("Script has been set up correctly! Now looping..", "green")

############
## LOOP   ##
############
while True:
    try:
        r = requests.get(f'https://aukro.cz/backend-web/api/offers/{aid}/offerDetail', headers=hedrs)

        r_state = r.json()['state']
        r_wcount = str(r.json()['watchingUserCount'])
        r_dcount = str(r.json()['displayedCount'])
        r_bcount = str(r.json()['biddersCount'])
        r_price = str(round(r.json()['price']['amount']))
        r_bname = r.json()['highestBidderAnonymizedLogin']
        r_name = r.json()['name']
        r_etext = r.json()['endingTimeText']

        ## New bidder
        if r_price != m_price:
            requests.post(f'https://ntfy.sh/{topic}',
                data=f'{r_bname} has raised the price to {r_price} Kč!'.encode("UTF-8"),
                headers={
                    "Title": "Someone bidded!",
                    "Priority": "high",
                    "Tags": "exclamation"
                })
            m_price = r_price
            ct = time.localtime()
            ctime = time.strftime("%H:%M:%S", ct)
            cprint(f'New bidder - {ctime}', "green")
        
        ## New follower
        if r_wcount != m_wcount:
            if int(r_wcount) < int(m_wcount):
                tdatw = "Someone unfollowed!"
            else:
                tdatw = "New follower!"
            requests.post(f'https://ntfy.sh/{topic}',
                data=f'There are now {r_wcount} followers. Cool!'.encode("UTF-8"),
                headers={
                    "Title": tdatw,
                    "Priority": "default",
                    "Tags": "eye"
                })
            m_wcount = r_wcount
            ct = time.localtime()
            ctime = time.strftime("%H:%M:%S", ct)
            cprint(f'New follower - {ctime}', "green")

        ## New display
        if r_dcount != m_dcount:
            requests.post(f'https://ntfy.sh/{topic}',
                data=f'There are now {r_dcount} displays. Cool!'.encode("UTF-8"),
                headers={
                    "Title": "New display!",
                    "Priority": "low",
                    "Tags": "window"
                })
            m_dcount = r_dcount
            ct = time.localtime()
            ctime = time.strftime("%H:%M:%S", ct)
            cprint(f'New display - {ctime}', "green")

        ## Auction ends soon
        if m_etextb == False:
            if r_etext == "5 minut":
                requests.post(f'https://ntfy.sh/{topic}',
                    data="The homestretch is here! Watch now!".encode("UTF-8"),
                    headers={
                        "Title": f'Auction ends in 5 minutes!',
                        "Priority": "high",
                        "Tags": "bell"
                    })
                m_etextb = True
                ct = time.localtime()
                ctime = time.strftime("%H:%M:%S", ct)
                cprint(f'Auction ends soon - {ctime}', "green")

        ## Auction ended
        if r_state == "ENDED":
            if r_bname == "...":
                tdat = 'Nobody won. gg'
            else:
                tdat = f'{r_bname} has won for {r_price} Kč. gg'
            requests.post(f'https://ntfy.sh/{topic}',
                data=tdat.encode("UTF-8"),
                headers={
                    "Title": "Auction closed!",
                    "Priority": "high",
                    "Tags": "construction"
                })
            ct = time.localtime()
            ctime = time.strftime("%H:%M:%S", ct)
            cprint(f'Auction ended - {ctime}', "green")
            exit()

    except Exception as error:
        ct = time.localtime()
        ctime = time.strftime("%H:%M:%S", ct)
        cprint(f'An unknown error has occurred. Check what happened, fix it, and try again. - {ctime}', "yellow")
        cprint(error, "red")
        exit()

    ct = time.localtime()
    ctime = time.strftime("%H:%M:%S", ct)
    print(f'Checked. - {ctime}')
    time.sleep(int(chtime))