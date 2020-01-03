# The secret of simple web scrapping (I mean simple because it doesn't execute JavaScript) is to find the structure of the information
# that you want, and see on what class (or other type of element that identify it as unique) it is in. There are a lot of 'divs' in
# the html, so this example will look for the 'div' which contains a class "fl-l score" that then will have the text which corresponds to
# the score of this anime. The HTML structure can be found by doing Ctrl+Shift+I on Chrome
# I recommend executing this on a console that won't vanish as soon as the code executes so you can see that last print

import requests
from bs4 import BeautifulSoup

URL = "https://myanimelist.net/anime/22865/Rokujouma_no_Shinryakusha"

headers = {"user-agent": 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find('div', {'class' :"fl-l score"}).get_text()

print(title.strip())
