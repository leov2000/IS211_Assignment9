import urllib.request as urllib
from bs4 import BeautifulSoup

def get_contents(url):
    result = urllib.urlopen(url).read()
    soup_contents = BeautifulSoup(result, 'lxml')

    return soup_contents 

def merge_links(href_list, string):
    return ''.join(href_list) + string  

def split_link(link, pattern):
    return link.split(pattern)

def main():
    nfl_link = 'http://www.cbssports.com/nfl/stats'
    soup = get_contents(nfl_link)
    touchdown_link = soup.find_all('a', text='Touchdowns')[0]['href']
    link_pattern = '/nfl/stats'
    new_nfl_link = merge_links(split_link(nfl_link, link_pattern), touchdown_link)
    print(new_nfl_link)

if __name__ == '__main__':
    main()