import pandas as pd
from datetime import datetime
from datetime import timedelta
from urllib.request import Request
from urllib.request import urlopen
from cache import get_html

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
            ret = self.scrape_match_page(match)
            if ret != 0:
                break #remove l8r


    def scrape_match_page(self,match_url):

        url = 'https://www.hltv.org' + match_url
        print(url)
        match_id = url.split('/')[4]
        print(match_id)
        match_html = get_html(url,True)
        match_soup = soup(match_html, 'html.parser')

        team1 = match_soup.find('div',class_='team1-gradient')
        team2 = match_soup.find('div', class_='team2-gradient')

        print (team2)

        team1_id = team1.find('a')
        team2_id = team2.find('a')

        if team1_id:
            team1_id = team1_id['href'].split('/')[2]
        else:
            print('error no team id')
            return 0

        if team2_id:
            team2_id= team2_id['href'].split('/')[2]
        else:
            print('error no team id')
            return 0

        print(team1_id)
        print(team2_id)

        betting_div = match_soup.find('div', class_='betting standard-box padding')
        if betting_div == 'None':
            print('error no betting table')
            return 0

        betting_table = betting_div.find('table')
        #print(betting_table)
        table_rows = betting_table.find_all('tr')

        columns = ['Team_1_ID', 'Team_2_ID']

        match_odds_dataframe = pd.DataFrame([[team1_id, team2_id]], columns=columns)
        # match_odds_dataframe['Team_1_ID'] = int(team1_id)
        # match_odds_dataframe['Team_2_ID'] = int(team2_id)
        #match_odds_dataframe = match_odds_dataframe.append()
        match_odds_dataframe.index = [match_id] #insert match id
        #print(match_odds_dataframe.head(1))

        for tr in table_rows:


            #geoprovider = tr['id']
            #print(tr)

            if(str(tr.get('id')).split('_')[0] == 'geoprovider'):
                agency = str(tr.get('id')).split('_')[1]
                odds = tr.find_all('td', class_='odds-cell border-left')
                if odds:
                    #print(odds[0].text)
                    #print('\n')
                    team1_odds = odds[0].text
                    team2_odds = odds[2].text

                    match_odds_dataframe['%s_team1' % agency] = team1_odds
                    match_odds_dataframe['%s_team2' % agency] = team2_odds


        print(match_odds_dataframe.head(1))
                #print(agency)

        #print(upcoming_matches)

    #existingMatchIDs = get_existing_data("matchIDs", 1)


if __name__ == "__main__":
    x = Start()
    x.main()