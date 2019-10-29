import urllib.request as urllib
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_contents(url):
    """
    A function that triggers the request and passes it on to BeautifulSoup

    Parameters: url(str)

    Returns: A string representing the html.
    """

    result = urllib.urlopen(url).read()
    soup_contents = BeautifulSoup(result, 'lxml')

    return soup_contents 

def merge_links(href_list, string):
    """
    A function that joins two strings into a link

    Parameters: 
        href_list(list[str])
        string(str)

    Returns: A string representing a link.
    """

    return ''.join(href_list) + string  

def split_link(url, pattern):
    """
    A function that splits a url string given a pattern.

    Parameters: 
        url(str)
        pattern(str)

    Returns: A list of strings.
    """

    return url.split(pattern)

def get_touchdowns(soup):
    """
    A function that finds all touchdown links

    Parameters: soup(str)

    Returns: A list of href items.
    """

    return soup.find_all('a', text='Touchdowns')[0]['href']

def get_table_body(soup):
    """
    A function that finds a table element with the attr of class = data

    Parameters: soup(str)

    Returns: A string.
    """

    return soup.find('table', attrs = {'class': 'data'})

def get_players(soup):
    """
    A function that finds all tr elements with class = row1 or class = row2.

    Parameters: soup(str)

    Returns: A limited list of 20 items.
    """

    return soup.find_all('tr', attrs = {'class': ['row1', 'row2']})[:20]

def get_player_details(soup):
    """
    A function that finds all td elements.

    Parameters: soup(str)

    Returns: A list of td items.
    """

    return [row.find_all('td') for row in soup]

def get_indicies(player_list):
    """
    A getter function that retrieves pertinent keys

    Parameters: player_list(list[str])

    Returns: A tuple of strings.
    """

    return (player_list[0].text, player_list[1].text, player_list[2].text, player_list[6].text)

def print_player_details(soup):
    """
    A printer function

    Parameters: soup(list[str])

    Prints: a formatted string with the name, team, touch_down
    """

    result = []

    for i, player_row in enumerate(soup):
        (name, position, team, touch_down) = get_indicies(player_row)
        
        format_string = f'#{i+1} - {name} plays in {team} as a {position} and has scored {touch_down} touchdowns.'
        print(format_string)

        result.append(format_string)
    
    return result

def write_results(result_list):
    """
    An std output function

    Parameters: result_list(list[str])

    Outputs: a formatted string with the results.
    """

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    meta_dict = {
        'results': result_list,
        'time_stamp': timestamp
    }

    with open('football_stats_result.json', 'w') as json_file:
        json.dump(meta_dict, json_file, indent=4, default=str) 

def main():
    """
    The main function that bootstraps the app.

        Parameters: None

        Returns: None
    """

    nfl_url = 'http://www.cbssports.com/nfl/stats'
    nfl_main_contents = get_contents(nfl_url)

    touchdown = get_touchdowns(nfl_main_contents)
    touchdown_url = merge_links(split_link(nfl_url, '/nfl/stats'), touchdown)
    touchdown_contents = get_contents(touchdown_url)

    players_table = get_table_body(touchdown_contents)
    player_table_rows = get_players(players_table)
    player_details = get_player_details(player_table_rows)

    result = print_player_details(player_details)
    write_results(result)

if __name__ == '__main__':
    main()