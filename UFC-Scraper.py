import requests
import random
import csv
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = 'http://ufcstats.com/statistics/fighters'
session = requests.Session()
timeout_in_seconds = 10

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
]
headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, image/apng, */*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US, en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Request': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'User-Agent': random.choice(user_agents)
}
retry_strategy = Retry(
    total = 5,
    backoff_factor = 1
)
adapter = HTTPAdapter(max_retries = retry_strategy)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_data(url):
    page = session.get(url, headers=headers, timeout=timeout_in_seconds)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

file = open('UFC_Fighters.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(['First', 'Last', 'Nickname', 'Ht.', 'Wt.', 'Reach', 'Stance', 'W', 'L', 'D'])

response = get_data(url)

paginate = response.find_all('li', {'class' : 'b-statistics__paginate-item'}) # Opens the 'All' paginate button
for page in paginate:
    if(page.get_text().strip() == 'All'):
        response = get_data(page.find('a').get('href'))
        break

fighters = response.find_all('tr', {'class' : 'b-statistics__table-row'})
for fighter in fighters:
    fighter_info = []
    info_col = fighter.find_all('td', {'class' : 'b-statistics__table-col'})
    
    for info in info_col:
        fighter_info.append(info.get_text().strip())

    if fighter_info:
        writer.writerow(fighter_info)