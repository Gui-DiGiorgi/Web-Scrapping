# thanks to RetributionByRevenue (https://github.com/RetributionByRevenue) for the functions to extract the data from the sites

import urllib3
from bs4 import BeautifulSoup
from time import time, sleep, ctime
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

def get_coin_gecko(info_center, coin):
    
    response = http.request('GET', 'https://www.coingecko.com/en/coins/bitcoin')
    coin_string = BeautifulSoup(response.data,features="lxml")  # Note the use of the .data property
    coin_string = str(coin_string)

    search_start = 'data-coin-symbol="btc" data-price-btc="1.0" data-target="price.price">$'
    search_end = '</span>\n<span class="live-percent-change ml-1"'

    coin_info_start = coin_string.find(search_start)
    coin_info_end = coin_string.find(search_end,coin_info_start)
    coin_info = coin_string[coin_info_start:coin_info_end]
    coin_info = coin_info[len(search_start):].replace(",","")
    
    try:
        coin_price = float(coin_info)
    except:
        return None
    
    return coin_price
    
def get_coin_binance(info_center, coin):
    
    response = info_center.request('GET', 'https://info.binance.com/en/currencies/{}'.format(coin))
    coin_string = BeautifulSoup(response.data,features="lxml")  # Note the use of the .data property
    coin_string = str(coin_string)

    search_start = 'ix71fe-7'
    checking = [17,"$"]
    price_len = 8
    
    matches = [m.start() for m in re.finditer(search_start, coin_string)]

    start_location = None

    for i in matches:
        if coin_string[i+checking[0]] == checking[1]:
            start_location = i
            break
            
    if start_location == None:
        return None

    right_location = start_location+checking[0]+1 
            
    coin_info = coin_string[right_location:right_location+price_len]

    coin_price = float(coin_info)

    return coin_price

interval = 90

coin_functions = [get_coin_binance, get_coin_gecko]

function_n = 0

print("Current Time\tTime After Start(s)\tPrice($USD)")

start = time()
      
all_prices = []
        
while True:
    
    lag = time()

    new_coin = get_coin_binance(http,"bitcoin")
    
    while new_coin == None:
        
        function_n = 1 - function_n
        
        new_coin = coin_functions[function_n](http,"bitcoin")

    new_coin = round(new_coin,2)

    lag = time()-lag
    
    time_s = round(time()-start-lag)
    
    print("{0}\t{1}\t{2}".format(ctime(start+time_s),time_s,new_coin))
    
    all_prices.append(new_coin)
    
    sleep(interval-lag)
