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

def get_table_body(soup):
    return soup.find('table', attrs = {'class': 'data'})

def get_players(soup):
    return soup.find_all('tr', attrs = {'class': ['row1', 'row2']})[:20]

def get_player_details(soup):
    return [row.find_all('td') for row in soup]

def get_indicies(player_list):
    return (player_list[0].text, player_list[1].text, player_list[2].text, player_list[6].text)

def print_player_details(soup):
    for i, player_row in enumerate(soup):
        (name, position, team, touch_down) = get_indicies(player_row)
        
        print(f'#{i+1} - {name} plays in {team} as a {position} and has scored {touch_down} touchdowns.')

def main():
    nfl_url = 'http://www.cbssports.com/nfl/stats'
    nfl_main_contents = get_contents(nfl_url)

    touchdown = get_touchdowns(nfl_main_contents)
    touchdown_url = merge_links(split_link(nfl_url, '/nfl/stats'), touchdown)
    touchdown_contents = get_contents(touchdown_url)

    players_table = get_table_body(touchdown_contents)
    player_table_rows = get_players(players_table)
    player_details = get_player_details(player_table_rows)

    print_player_details(player_details)

if __name__ == '__main__':
    main()