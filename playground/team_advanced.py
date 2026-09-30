#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 22:41:04 2025

@author: martinmiranda
"""

import pandas as pd

team_path = '../current_stats/team_aggregate.csv'
opp_path = '../current_stats/opp_aggregate.csv'
player_path = '../current_stats/player_aggregate.csv'
team_per_game = '../current_stats/team_per_game.csv'

ts = pd.read_csv(team_path, index_col = ['TEAM'])
os = pd.read_csv(opp_path, index_col = ['TEAM'])
ps = pd.read_csv(player_path, index_col = ['TEAM', 'NO.', 'PLAYER'])
tpg = pd.read_csv(team_per_game, index_col = ['TEAM'])

df = pd.DataFrame(index=ts.index)
df['POS'] = 0.5 * ((ts['FGA'] + 0.44 * ts['FTA'] - 1.07 * (ts['OFF'] / (ts['OFF'] + os['DEF'])) * (ts['FGA'] - ts['FGM'] + ts['TO']))
                    + (os['FGA'] + 0.44 * os['FTA'] - 1.07 * (os['OFF'] / (os['OFF'] + ts['DEF'])) * (os['FGA'] - os['FGM'] + os['TO'])))

# Pace of Play
df['PACE'] = 200 / ts['MINS'] * df['POS']
df['OFF'] = ts['PTS'] / df['POS'] * 55
df['DEF'] = os['PTS'] / df['POS'] * 55
df['NET'] = df['OFF'] - df['DEF']

# Scoring Efficiency Metrics
df['EFG%'] = (ts['FGM'] + 0.5 * ts['3PM']) / ts['FGA'] * 100
df['TS%'] = (ts['PTS'] / (2 * (ts['FGA'] + (0.44 * ts['FTA'])))) * 100
df['PPWS'] = ts['PTS'] / (ts['FGA'] + (0.44 * ts['FTA']))
df['FTR'] = ts['FTA']/ts['FGA']

# Playmaking Metrics
df['AR'] = ts['AST'] / df['POS'] * 100
df['TOR'] = ts['TO'] / df['POS'] * 100

# Rebounding and Defense Metrics
df['STL%'] = ts['STL'] / df['POS'] * 100
df['BLK%'] = ts['BLK'] / df['POS'] * 100
df['REB%'] = ts['REB'] / (ts['REB'] + os['REB']) * 100
df['OREB%'] = ts['OFF'] / (ts['OFF'] + os['DEF']) * 100
df['DREB%'] = ts['DEF'] / (ts['DEF'] + os['OFF']) * 100

# Performance Metrics
# Construction of Opponent Metrics for FFI
odf = pd.DataFrame(index=df.index)
odf['EFG%'] = (os['FGM'] + 0.5 * os['3PM'])/os['FGA'] * 100
odf['TOR'] = os['TO'] / df['POS'] * 100
odf['OREB%'] = os['OFF'] / (os['OFF'] + ts['DEF']) * 100
odf['FTR'] = os['FTA'] / os['FGA']

df['FFI'] = (0.3 * df['EFG%']/100 - 0.075 * df['TOR']/100 + 0.075 * df['OREB%']/100 + 0.05 * df['FTR']
            -0.3 * odf['EFG%']/100 + 0.075 * odf['TOR']/100 + 0.075 * odf['OREB%']/100 - 0.05 * odf['FTR']) * 100

df['HHI'] = ps.groupby('TEAM')['PTS'].apply(lambda x: (x**2).sum()) / ts['PTS']**2
df['Py-W'] = ts['PTS']**16.5 / (ts['PTS']**16.5 + os['PTS']**16.5) * ts['GP']
df['Py-L'] = ts['GP'] - df['Py-W']