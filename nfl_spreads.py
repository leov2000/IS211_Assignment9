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

def get_all_tables(soup):
    """
    A function that finds all table elements with the attrs: col = 4, width = 580

    Parameters: soup(str)

    Returns: A list of table items.
    """
    
    return soup.find_all('table', attrs = {'cols': '4', 'width': '580'})

def merge_tables(soup_list):
    """
    A function that retrieves all tr elements from the table list. Then it flattens out
    the list structure.

    Parameters: soup_list(list[str])

    Returns: A list of row items.
    """

    tr_result = [get_rows(table) for table in soup_list]
    flatten_result = [item for sublist in tr_result for item in sublist]

    return flatten_result
    
def get_rows(soup):
    """
    A function that finds all tr elements

    Parameters: soup(str)

    Returns: A list of tr items.
    """

    return soup.find_all('tr')[1:]

def get_td(soup):
    """
    A function that finds all td elements

    Parameters: soup(str)

    Returns: A list of td items.
    """

    return soup.find_all('td')

def get_indicies(team_list):
    """
    A getter function that retrieves pertinent keys

    Parameters: team_list(list[str])

    Returns: A tuple of strings.
    """

    return (team_list[0].text, team_list[1].text, team_list[2].text, team_list[3].text)

def print_rows(soup):
    """
    A printer function

    Parameters: soup(list[str])

    Prints: a formatted string with the date, favorite, spread and under_dog
    """

    result = []
    for i, team_row in enumerate(soup):
        table_cells = get_td(team_row)
        (date, fav, spread, under_dog) = get_indicies(table_cells)
        
        format_string = f'#{i+1} - The under dogs, the {under_dog} have a a spread of {spread} with the favorite being {fav} on {date}.'
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

    with open('nfl_spreads_result.json', 'w') as json_file:
        json.dump(meta_dict, json_file, indent=4, default=str)


def main():
    """
    The main function that bootstraps the app.

        Parameters: None

        Returns: None
    """

    nfl_url = 'http://www.footballlocks.com/nfl_point_spreads.shtml'
    nfl_main_contents = get_contents(nfl_url)

    all_tables = get_all_tables(nfl_main_contents)
    team_tables = merge_tables(all_tables)

    result = print_rows(team_tables)
    write_results(result)

if __name__ == '__main__':
    main()