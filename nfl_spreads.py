import urllib.request as urllib
from bs4 import BeautifulSoup

def get_contents(url):
    result = urllib.urlopen(url).read()
    soup_contents = BeautifulSoup(result, 'lxml')

    return soup_contents 

def get_all_tables(soup):
    return soup.find_all('table', attrs = {'cols': '4', 'width': '580'})

def merge_tables(soup_list):
    tr_result = [get_rows(table) for table in soup_list]
    flatten_result = [item for sublist in tr_result for item in sublist]

    return flatten_result
    
def get_rows(soup):
    return soup.find_all('tr')[1:]

def get_td(soup):
    return soup.find_all('td')

def get_indicies(team_list):
    return (team_list[0].text, team_list[1].text, team_list[2].text, team_list[3].text)

def print_rows(soup):
    for i, team_row in enumerate(soup):
        table_cells = get_td(team_row)
        (date, fav, spread, under_dog) = get_indicies(table_cells)
        
        print(f'#{i+1} - The under dogs, the {under_dog} have a a spread of {spread} with the favorite being {fav} on {date}.')

def main():
    nfl_url = 'http://www.footballlocks.com/nfl_point_spreads.shtml'
    nfl_main_contents = get_contents(nfl_url)

    all_tables = get_all_tables(nfl_main_contents)
    team_tables = merge_tables(all_tables)

    print_rows(team_tables)

if __name__ == '__main__':
    main()