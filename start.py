import pandas as pd
from datetime import datetime
from datetime import timedelta
from urllib.request import Request
from urllib.request import urlopen

from helper import *
from bs4 import BeautifulSoup as soup



class Start:

    upcoming_matches_url = 'https://www.hltv.org/matches'
    hdr = {'User-Agent' : 'Mozilla/5.0'}
    test = 0
    max_time_from_now = timedelta(hours=6)

    def __init__(self):
        #self.match_odds = pd.read_csv("MatchOdds.csv", error_bad_lines=False)
        self.test = 0

    def main(self):


        req = Request(self.upcoming_matches_url, headers= self.hdr)
        u_client = urlopen(req)
        matches_html = u_client.read()
        u_client.close()
        now = datetime.now()

        matches_soup = soup(matches_html, 'html.parser')
        upcoming_matches = matches_soup.find_all('div', class_='upcoming-matches')
        matches_soon = []

        for div in upcoming_matches[0].find_all('div', class_='match-day'):

            dates = div.find('span', class_='standard-headline')
            match_time = datetime.strptime(dates.text, '%Y-%m-%d')
            #print(match_time)

            for match in div.find_all('a'):
                #print(match['href'])
                time = match.find('div', class_='time')
                time = time.text.split(':')
                match_time = match_time.replace(hour= int(time[0]), minute= int(time[1]))
                time_from_now = match_time - now
                #print(match_time)
                #print(time_from_now)

                #print(match)
                #print('\n')

                if time_from_now < self.max_time_from_now:
                    matches_soon.append(match['href'])

        #print(matches_soon)
        for match in matches_soon:
            self.scrape_match_page(match)
            break #remove l8r



    def scrape_match_page(self,match_url):

        url = 'https://www.hltv.org' + match_url
        print(url)

        req = Request(self.upcoming_matches_url, headers= self.hdr)
        u_client = urlopen(req)
        match_html = u_client.read()
        u_client.close()

        match_soup = soup(match_html, 'html.parser')

        betting_table = match_soup.find_all('div', class_='betting standard-box padding')
        print(match_soup)


        #print(upcoming_matches)

    #existingMatchIDs = get_existing_data("matchIDs", 1)


if __name__ == "__main__":
    x = Start()
    x.main()