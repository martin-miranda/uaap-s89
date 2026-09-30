#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:04:15 2025

@author: martinmiranda
"""

import pandas as pd
import sys

game_id = int(sys.argv[1])
current_path = "../current_stats/team_aggregate.csv"
add_path = "../game_logs/game_{0}_teams.csv".format(game_id)

current_df = pd.read_csv(current_path, index_col=['TEAM'])
add_df = pd.read_csv(add_path, index_col=['TEAM'])

df = current_df.add(add_df, fill_value=0)
df['FG %'] = df.apply(lambda row: row['FGM'] / row['FGA'] * 100 if row['FGA'] != 0 else 0, axis=1)
df['2P %'] = df.apply(lambda row: row['2PM'] / row['2PA'] * 100 if row['2PA'] != 0 else 0, axis=1)
df['3P %'] = df.apply(lambda row: row['3PM'] / row['3PA'] * 100 if row['3PA'] != 0 else 0, axis=1)
df['FT %'] = df.apply(lambda row: row['FTM'] / row['FTA'] * 100 if row['FTA'] != 0 else 0, axis=1)
df['STK'] = df['BLK'] + df['STL']

copy_col = ['FG %', '2P %', '3P %', 'FT %', 'GP', 'GW']
pg_df = df.div(df['GP'], axis=0)
pg_df[copy_col] = df[copy_col]

# For opponent stats
current_opp = "../current_stats/opp_aggregate.csv"
cur_opp_df = pd.read_csv(current_opp, index_col=['TEAM'])
add_opp_df = add_df.copy()
add_opp_df.iloc[0], add_opp_df.iloc[1] = add_df.iloc[1].copy(), add_df.iloc[0].copy()

opp_df = cur_opp_df.add(add_opp_df, fill_value=0)
opp_df['FG %'] = opp_df.apply(lambda row: row['FGM'] / row['FGA'] * 100 if row['FGA'] != 0 else 0, axis=1)
opp_df['2P %'] = opp_df.apply(lambda row: row['2PM'] / row['2PA'] * 100 if row['2PA'] != 0 else 0, axis=1)
opp_df['3P %'] = opp_df.apply(lambda row: row['3PM'] / row['3PA'] * 100 if row['3PA'] != 0 else 0, axis=1)
opp_df['FT %'] = opp_df.apply(lambda row: row['FTM'] / row['FTA'] * 100 if row['FTA'] != 0 else 0, axis=1)
opp_df['STK'] = opp_df['BLK'] + opp_df['STL']

opp_pg_df = opp_df.div(opp_df['GP'], axis=0)
opp_pg_df[copy_col] = opp_df[copy_col]

col_names = [
        'GP', 'MINS', 'PTS', 'SCP', 'OFF', 'DEF', 'REB', 'AST', 'TO', 'PTO', 'STL', 'BLK',
        'STK', 'FGM', 'FGA', 'FG %', '2PM', '2PA', '2P %', '3PM', '3PA', '3P %',
        'FTM', 'FTA', 'FT %', 'PF', 'Fls on:', '+/-', 'PIP', 'PP', 'FBP', 'STP', 'BP', 'BL', 'GW'
    ]

df = df[col_names]
pg_df = pg_df[col_names]
opp_df = opp_df[col_names]
opp_pg_df = opp_pg_df[col_names]

df.to_csv('../current_stats/team_aggregate.csv')
pg_df.to_csv('../current_stats/team_per_game.csv')
opp_df.to_csv('../current_stats/opp_aggregate.csv')
opp_pg_df.to_csv('../current_stats/opp_per_game.csv')

df.to_csv('../team_stats/team_aggregate_{0}.csv'.format(game_id))
pg_df.to_csv('../team_stats/team_per_game_{0}.csv'.format(game_id))
opp_df.to_csv('../team_stats/opp_aggregate_{0}.csv'.format(game_id))
opp_pg_df.to_csv('../team_stats/opp_per_game_{0}.csv'.format(game_id))