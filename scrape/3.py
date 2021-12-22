from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img',
                     {'src': re.compile('\.\.\/img\/gifts\/img.*\.jpg')})
for image in images:
    print(image['src'])
# next_siblings
# children
# descendants
# previous_siblings
# parents
# for child in bs.find('table', {'id': 'giftList'}).descendants:
#     print(child)
