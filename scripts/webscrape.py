#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 15:06:47 2025

@author: martinmiranda
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

first_game = 8
last_game = 10

for game_id in range(first_game, last_game + 1):
    url = f"https://uaap.livestats.ph/tournaments/uaap-season-89-men-s-basketball?game_id={game_id}"
    response = requests.get(url)
    print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    boxscore_divs = soup.find_all('div', class_='boxscorewrap')
    print(len(boxscore_divs))

    boxscore_data = []
    headers = boxscore_divs[0].find_all('th')
    header_names = [header.text.strip() for header in headers]
    header_names = header_names[:-4]

    team_data = []

    for index, boxscore_div in enumerate(boxscore_divs):
        rows = boxscore_div.find_all('tr')
        team_boxscore = []
        for row in rows:
            cols = row.find_all('td')
            cols_text = [col.text.strip() for col in cols]
            if cols_text:
                team_boxscore.append(cols_text)

        team_data.append(team_boxscore)

    df_1 = pd.DataFrame(team_data[0], columns=header_names)
    df_2 = pd.DataFrame(team_data[1], columns=header_names)

    team_names = [team_code.text.strip() for team_code in soup.find_all('div', class_='team_code')]
    team_names = team_names[:2]

    df_1.insert(0,'TEAM', team_names[0])
    df_2.insert(0,'TEAM', team_names[1])
    df_1 = df_1.drop(columns=["POS"])
    df_2 = df_2.drop(columns=["POS"])

    team_stats_divs = soup.find_all('div', class_='team-stats')

    def extract_team_stats(stats_div):
        #stat_titles = [span.text.strip() for span in stats_div.find_all('span', class_='team-stat-title')]
        stat_titles = ["PTO", "PIP", "SCP", "BP", "BL", "PP", "FBP", "STP"]
        stat_values = [span.text.strip() for span in stats_div.find_all('span') if span.text.strip().isdigit()]
        data = {stat_titles[i]: [int(stat_values[i])] for i in range(len(stat_titles))}

        return pd.DataFrame(data)

    df_team_1 = extract_team_stats(team_stats_divs[0])
    df_team_2 = extract_team_stats(team_stats_divs[1])

    def move_totals(df1, df2):
        last_row = df1.iloc[-1].drop(['NO.', 'PLAYER'])
        last_row_df = last_row.to_frame().T
        df2_dict = df2.iloc[0].to_dict()
        for column, value in df2_dict.items():
            last_row_df[column] = value
        return last_row_df

    df_team_1 = move_totals(df_1, df_team_1)
    df_team_2 = move_totals(df_2, df_team_2)

    df_1 = df_1.iloc[:-2]
    df_2 = df_2.iloc[:-2]

    df_1['GP'] = 1
    df_2['GP'] = 1
    df_team_1['GP'] = 1
    df_team_2['GP'] = 1

    if df_team_1.iloc[0]['+/-'] > df_team_2.iloc[0]['+/-']:
        df_1['GW'] = 1
        df_2['GW'] = 0
        df_team_1['GW'] = 1
        df_team_2['GW'] = 0
    else:
        df_1['GW'] = 0
        df_2['GW'] = 1
        df_team_1['GW'] = 0
        df_team_2['GW'] = 1

    df_players = pd.concat([df_1, df_2])
    df_teams = pd.concat([df_team_1, df_team_2])

    def convert(df):
        df['MINS'] = df['MINS'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60 )

        df[['FGM', 'FGA']] = df['FG'].str.split('-', expand=True)
        df.insert(df.columns.get_loc('FG') + 1, 'FGM', df.pop('FGM'))
        df.insert(df.columns.get_loc('FG') + 2, 'FGA', df.pop('FGA'))
        df[['2PM', '2PA']] = df['2P'].str.split('-', expand=True)
        df.insert(df.columns.get_loc('2P') + 1, '2PM', df.pop('2PM'))
        df.insert(df.columns.get_loc('2P') + 2, '2PA', df.pop('2PA'))
        df[['3PM', '3PA']] = df['3P'].str.split('-', expand=True)
        df.insert(df.columns.get_loc('3P') + 1, '3PM', df.pop('3PM'))
        df.insert(df.columns.get_loc('3P') + 2, '3PA', df.pop('3PA'))
        df[['FTM', 'FTA']] = df['FT'].str.split('-', expand=True)
        df.insert(df.columns.get_loc('FT') + 1, 'FTM', df.pop('FTM'))
        df.insert(df.columns.get_loc('FT') + 2, 'FTA', df.pop('FTA'))
        df = df.drop(columns = ['FG', '2P', '3P', 'FT'])

        numeric_cols = ['PTS', 'FGM', 'FGA', 'FG %', '2PM', '2PA', '2P %', '3PM', '3PA', '3P %', 'FTM', 'FTA', 'FT %',
                        'OFF', 'DEF', 'REB', 'AST', 'TO', 'STL', 'BLK', 'PF', 'Fls on:', '+/-']

        df[numeric_cols] = df[numeric_cols].astype(float)
        return df

    df_players = convert(df_players)
    df_teams = convert(df_teams)

    df_players.to_csv('../game_logs/game_{0}_players.csv'.format(game_id), index = False)
    df_teams.to_csv('../game_logs/game_{0}_teams.csv'.format(game_id), index = False)
    print('Game {0} saved'.format(game_id))
