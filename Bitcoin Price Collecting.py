# This code prints the bitcoin price from the binance site each 40 and 80 seconds (time it updates the price)
# It only prints if the price changes, but the chance of it staying the same down to cents is very low, so it ends up printing
# the price each 40 and 80 seconds. The format of the printing is that so when copying it to the notepad and copying it from there,
# it will be ready for excel pasting, as it will land each value in an unique cell

# It uses two classes, because the site changes the class it uses to print the price on the HTML, so it needs to catch when it finds an
# error with the reading and update the class to the right one

# Do what you want with the data, I still didn't crack the code to start trading correctly

import requests
from bs4 import BeautifulSoup
import time

def right_class(url_html):
    
    html_classes = ["ix71fe-7 gWWmzg","ix71fe-7 kYeyaS"]
        
    n = 0

    while n == 0:
        
        infos = []

        for html in html_classes:
            infos.append(url_html.find('div', {'class' :html}))
        
        for i,j in zip(infos,html_classes):
            if i!=None:
                html_class_final = j
                n = 1
                break
            
    return html_class_final

URL = "https://info.binance.com/en/currencies/bitcoin"

headers = {"user-agent": 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

run = True

page = requests.get(URL, headers=headers)

trade_soup = BeautifulSoup(page.content, 'html.parser')

current_class = right_class(trade_soup)
    
info = trade_soup.find('div', {'class' :current_class}).get_text()

old_og_price = float(info.strip()[1:])

start_time = time.time()


print("{0}\t{1}".format("Time","Price"))


while run:

    page = requests.get(URL, headers=headers)

    trade_soup = BeautifulSoup(page.content, 'html.parser')
    
    try:

        info = trade_soup.find('div', {'class' :current_class}).get_text()
        
    except:

        current_class = right_class(trade_soup)

        info = trade_soup.find('div', {'class' :current_class}).get_text()
    
    og_price = float(info.strip()[1:])
    
    if og_price != old_og_price:
        
        now = round(time.time()-start_time)
        
        old_og_price = og_price

        price = int(round(og_price))
        
        print("{0}\t{1}".format(now,price))

