#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:34:03 2025

@author: martinmiranda
"""

import pandas as pd
import sys

game_id = int(sys.argv[1])
current_path = "../current_stats/player_aggregate.csv"
add_path = "../game_logs/game_{0}_players.csv".format(game_id)

current_df = pd.read_csv(current_path, index_col=['TEAM', 'NO.', 'PLAYER'])
add_df = pd.read_csv(add_path, index_col=['TEAM', 'NO.', 'PLAYER'])

df = current_df.add(add_df, fill_value=0)
df['FG %'] = df.apply(lambda row: row['FGM'] / row['FGA'] * 100 if row['FGA'] != 0 else 0, axis=1)
df['2P %'] = df.apply(lambda row: row['2PM'] / row['2PA'] * 100 if row['2PA'] != 0 else 0, axis=1)
df['3P %'] = df.apply(lambda row: row['3PM'] / row['3PA'] * 100 if row['3PA'] != 0 else 0, axis=1)
df['FT %'] = df.apply(lambda row: row['FTM'] / row['FTA'] * 100 if row['FTA'] != 0 else 0, axis=1)
df['STK'] = df['BLK'] + df['STL']

copy_col = ['FG %', '2P %', '3P %', 'FT %', 'GP', 'GW']
pg_df = df.div(df['GP'], axis=0)
pg_df[copy_col] = df[copy_col]

mins_df = df.div(df['MINS'], axis=0) * 30
mins_df[copy_col] = df[copy_col]

col_names = [
        'GP', 'MINS', 'PTS', 'OFF', 'DEF', 'REB', 'AST', 'TO', 'STL', 'BLK',
        'STK', 'FGM', 'FGA', 'FG %', '2PM', '2PA', '2P %', '3PM', '3PA', '3P %',
        'FTM', 'FTA', 'FT %', 'PF', 'Fls on:', '+/-', 'GW'
    ]

df = df[col_names]
pg_df = pg_df[col_names]
mins_df = mins_df[col_names]

df.to_csv("../current_stats/player_aggregate.csv")
pg_df.to_csv("../current_stats/player_per_game.csv")
mins_df.to_csv("../current_stats/player_per_30.csv")

df.to_csv("../player_stats/player_aggregate_{0}.csv".format(game_id))
pg_df.to_csv("../player_stats/player_per_game_{0}.csv".format(game_id))
mins_df.to_csv("../player_stats/player_per_30_{0}.csv".format(game_id))

grouped = {team: group for team, group in df.groupby(level='TEAM')}
for team, group in grouped.items():
    group.to_csv('../per_team/{0}_pb.csv'.format(team))

grouped = {team: group for team, group in pg_df.groupby(level='TEAM')}
for team, group in grouped.items():
    group.to_csv('../per_team/{0}_pg.csv'.format(team))

grouped = {team: group for team, group in mins_df.groupby(level='TEAM')}
for team, group in grouped.items():
    group.to_csv('../per_team/{0}_p30.csv'.format(team))
