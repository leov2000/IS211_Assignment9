import urllib.request as urllib
from bs4 import BeautifulSoup

def get_contents(url):
    result = urllib.urlopen(url).read()
    soup_contents = BeautifulSoup(result, 'lxml')

    return soup_contents 

def merge_links(href_list, string):
    return ''.join(href_list) + string  

def split_link(url, pattern):
    return url.split(pattern)

def get_touchdowns(soup):
    return soup.find_all('a', text='Touchdowns')[0]['href']

def main():
    nfl_url = 'http://www.cbssports.com/nfl/stats'
    soup = get_contents(nfl_url)
    touchdown = get_touchdowns(soup)
    link_pattern = '/nfl/stats'
    touchdown_url = merge_links(split_link(nfl_url, link_pattern), touchdown)

if __name__ == '__main__':
    main()