import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_season_games(team):
    team_url = 'https://fbref.com' + team['href']
    team_page = requests.get(team_url)
    soup_games = bs(team_page.content, 'html.parser')

    games_list = soup_games.select(
        '#ks_sched_all > tbody:nth-child(4) > tr')

    team_games_df = pd.DataFrame(columns=[
                                 'competition', 'date', 'venue', 'result', 'goals_for', 'goals_against', 'opponent'])

    for game in games_list:
        competition = game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > th:nth-child(1) > a:nth-child(1)').text
        date = game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(4) > a:nth-child(1)').text
        venue = game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(6)').text
        result = game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(7)').text

        if re.search(r'\d+\((\d+)\)', game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(8)').text):
            goals_for = int(re.search(r'\d+\((\d+)\)', game.select_one(
                '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(8)').text).group(1))
            goals_against = int(re.search(r'\d+\((\d+)\)', game.select_one(
                '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(9)').text).group(1))
        else:
            goals_for = int(game.select_one(
                '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(8)').text)
            goals_against = int(game.select_one(
                '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(9)').text)
        
        if game.select_one(
            '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(10) > a:nth-child(1)'):
            opponent = game.select_one(
                '#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(10) > a:nth-child(1)').text
        else:
           opponent = game.select_one('#ks_sched_all > tbody:nth-child(4) > tr > td:nth-child(10) > a:nth-child(2)').text


        team_games_df = team_games_df.append(
            {'competition':competition, 'date':date, 'venue':venue, 'result':result, 'goals_for':goals_for, 'goals_against':goals_against, 'opponent':opponent}, ignore_index=True)
    
    return team_games_df



def get_participating_teams():
    fbref_url = "https://fbref.com/en/comps/8/2102/2018-2019-UEFA-Champions-League-Stats"
    fbref_page = requests.get(fbref_url)
    soup = bs(fbref_page.content, 'html.parser')

    champions_18_19_teams = []

    teams_list = soup.select(
        "table > tbody:nth-child(4) > tr > td:nth-child(2) > a:nth-child(2)")

    for team in teams_list:
        if team.text not in champions_18_19_teams:
            print("Inicando raspagem " + team.text + ':') 
            export_to_csv = get_season_games(team).to_csv(r'./' + team.text + '.csv', index=None, header=True)
            champions_18_19_teams.append(team.text)

            
        




# champions_18_19_teams = champions_18_19_teams.append({"name": team.text.strip(), "ref_link": link}, ignore_index=True)
