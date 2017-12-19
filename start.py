import pandas as pd
from urllib.request import Request
from urllib.request import urlopen

from helper import *
from bs4 import BeautifulSoup as soup



class Start:

    matches_url = 'https://www.hltv.org/matches'
    hdr = {'User-Agent' : 'Mozilla/5.0'}
    test = 0

    def __init__(self):
        #self.match_odds = pd.read_csv("MatchOdds.csv", error_bad_lines=False)
        self.test = 0

    def main(self):

        req = Request(self.matches_url, headers= self.hdr)
        u_client = urlopen(req)
        matches_html = u_client.read()
        u_client.close()

        matches_soup = soup(matches_html, 'html.parser')
        upcoming_matches = matches_soup.find_all('div', class_='upcoming-matches')

        for div in upcoming_matches[0].find_all('div', class_='match-day'):
            # print(type(div))
            # print(div.get('class'))
            dates = div.find_all('span', class_='standard-headline')
            print(dates[0].text)

            for match in div.find_all('a'):
                print(match['href'])
                time = match.find('div', class_='time')
                print(time)
                #print(match)
                print('\n')

                # for link in match.find_all('href'):
                #     print(link)





        #print(upcoming_matches)

    #existingMatchIDs = get_existing_data("matchIDs", 1)


if __name__ == "__main__":
    x = Start()
    x.main()