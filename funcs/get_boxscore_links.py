import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor

def get_boxscore_links(url, url_team_name, start_year, end_year):
    urls = []
    for year in range(start_year, end_year + 1):
        urls.append(url + str(year))

    # get box score links from schedule pages
    def fetch(url):
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        # return [f'https://{url_team_name}.com' + a['href'] for a in soup.find_all('a', href=True) if 'boxscore' in a['href']]
        return [f'https://{url_team_name}.edu' + a['href'] for a in soup.find_all('a', href=True) if 'boxscore' in a['href'] and "target" not in a.attrs]
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch, urls))
        
    return [x for xs in results for x in xs]
