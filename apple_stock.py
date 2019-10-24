import urllib.request as urllib
from bs4 import BeautifulSoup

def get_contents(url):
    result = urllib.urlopen(url).read()
    soup_contents = BeautifulSoup(result, "html5lib")
    return soup_contents 

def get_container(soup):
    return soup.find('div', attrs = {'class': 'historical-data', 'data-symbol': 'AAPL', 'data-asset-class': 'Stocks', 'data-full': '1'})

def get_table(soup):
    return soup.find_all('tr', attrs = {'class': 'historical-data__row'})

def main():
    nasdaq_url = 'https://www.nasdaq.com/symbol/aapl/historical'
    nasdaq_main_contents = get_contents(nasdaq_url)
    nasdaq_table = get_container(nasdaq_main_contents)
    
    print(nasdaq_main_contents)

if __name__ == '__main__':
    main()
