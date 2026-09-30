#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 09:22:53 2025

@author: martinmiranda
"""

import pandas as pd

# Fix paths before migrating
team_path = '../current_stats/team_aggregate.csv'
team_advanced = '../current_stats/team_advanced.csv'
opp_path = '../current_stats/opp_aggregate.csv'
player_path = '../current_stats/player_aggregate.csv'
player_pg = '../current_stats/player_per_game.csv'

ts = pd.read_csv(team_path, index_col=['TEAM'])
ta = pd.read_csv(team_advanced, index_col=['TEAM'])
ps = pd.read_csv(player_path, index_col=['TEAM', 'NO.','PLAYER'])
pg = pd.read_csv(player_pg, index_col=['TEAM', 'NO.','PLAYER'])
os = pd.read_csv(opp_path, index_col=['TEAM'])

df = pd.DataFrame(index=ps.index)
buffer = pd.DataFrame(index=ps.index)

def get_ts(df1, df2, stat):
    stat_name = 'Tm' + stat
    df1[stat_name] = df1.index.get_level_values('TEAM').map(df2[stat])
    return df1

def get_game(df1, stat):
    stat_name = 'Gm' + stat
    df1[stat_name] = df1.index.get_level_values('TEAM').map(game[stat])
    return df1

def get_opp(df1, stat):
    stat_name = 'o' + stat
    df1[stat_name] = df1.index.get_level_values('TEAM').map(os[stat])
    return df1

########## League Averages ##########
lg_pace = ta['PACE'].mean()

df['GP'] = ps['GP']
df['MPG'] = ps['MINS'] /df['GP']

df['SP'] = ((ps['PTS'] + ps['REB'] + 2*ps['AST'] + 2*ps['STL'] + ps['BLK']) * 2 - ps['TO'] + 15*ps['GW']) / ps['GP']
buffer = get_ts(buffer, ts, 'MINS')
buffer = get_ts(buffer, ts, 'GP')
df['aSP'] = df['SP'] * 200/(buffer['TmMINS']/buffer['TmGP'])

buffer['DRE Raw'] = 0.79231 * ps['PTS'] - 0.71944 * (ps['2PA'] - ps['2PM']) - 0.55233 * (ps['3PA'] - ps['3PM']) - 0.15944 * ps['FTA'] + 0.13479 * ps['OFF'] + 0.39960 * ps['DEF'] + 0.54415 * ps['AST'] + 1.68007 * ps['STL'] + 0.76387 * ps['BLK'] - 1.35990 * ps['TO'] - 0.10838 * ps['PF']
buffer['DRE/G'] = buffer['DRE Raw'] / ps['GP']
df['DRE'] = buffer['DRE/G']

df['GmSc'] = ps['PTS'] + 0.4 * ps['FGM'] + 0.7 * ps['OFF'] + 0.3 * ps['DEF'] + ps['STL'] + 0.7 * ps['AST'] + 0.7 * ps['BLK'] - 0.7 * ps['FGA'] - 0.4 * ps['FTM'] - 0.4 * (ps['FTA'] - ps['FTM']) - 0.4 * ps['PF'] - ps['TO']
df['GmSc'] = df['GmSc'] / ps['GP']
df['EFF'] = (ps['PTS'] + ps['REB'] + ps['AST'] + ps['STL'] + ps['BLK'] - (ps['FGA'] - ps['FGM']) - (ps['FTA'] - ps['FTM']) - ps['TO']) / ps['GP']

lg_DRE = (df['DRE'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_GmSc = (df['GmSc'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_EFF = (df['EFF'] * ps['MINS']).sum() / ps['MINS'].sum()
df['DRE+'] = df['DRE']/lg_DRE * 100
df['GmSc+'] = df['GmSc']/lg_GmSc * 100
df['EFF+'] = df['EFF']/lg_EFF * 100

########## PER Calculations ##########
# Getting League and Team Stats

lg_DEF = (ps['DEF'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_REB = (ps['REB'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_OFF = (ps['OFF'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_FTA = (ps['FTA'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_TO = (ps['TO'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_FGA = (ps['FGA'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_PTS = (ps['PTS'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_FTM = (ps['FTM'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_FGM = (ps['FGM'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_AST = (ps['AST'] * ps['MINS']).sum() / ps['MINS'].sum()
lg_PF = (ps['PF'] * ps['MINS']).sum() / ps['MINS'].sum()

team_stats = ['AST', 'FGM']
for stat in team_stats:
    buffer = get_ts(buffer, ts, stat)

# Actual Calculations
factor = (2/3) - (0.5 * lg_AST / lg_FGM) / (2 * (lg_FGM / lg_FTM))
VOP = lg_PTS / (lg_FGA - lg_OFF + lg_TO + 0.44 * lg_FTA)
DRBP = lg_DEF / lg_REB
buffer['uPER'] = ((1/ps['MINS']) *
        (ps['3PM']
         + 2/3 * ps['AST']
         + (2 - factor * (buffer['TmAST'] / buffer['TmFGM'])) * ps['FGM']
         + (ps['FTM'] * 0.5 * (1 + (1 - (buffer['TmAST'] / buffer['TmFGM'])) + 2/3 * (buffer['TmAST'] / buffer['TmFGM'])))
         - VOP * ps['TO']
         - VOP * DRBP * (ps['FGA'] - ps['FGM'])
         - VOP * 0.44 * (0.44 + (0.56 * DRBP)) * (ps['FTA'] - ps['FTM'])
         + VOP * (1 - DRBP) * (ps['DEF'])
         + VOP * DRBP * ps['OFF']
         + VOP * ps['STL']
         + VOP * DRBP * ps['BLK']
         - ps['PF'] * ((lg_FTM / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP)
        )
    )

buffer = get_ts(buffer, ta, 'PACE')
pace_ad = lg_pace / buffer['TmPACE']
buffer['aPER'] = buffer['uPER'] * pace_ad
lg_aPER = (buffer['uPER'] * ps['MINS']).sum() / ps['MINS'].sum()
df['PER'] = buffer['aPER'] * (15/lg_aPER)
#################################################################

########## Win Shares ##########
ws = pd.DataFrame(index=buffer.index)
team_stat = ['BLK','MINS', 'AST', 'FGM', 'PTS', 'FTM', 'FGA', 'FTA', 'OFF', 'TO',
             '3PA', '2PA', 'OFF', '3PM', 'DEF', 'STL', 'PF']
for stat in team_stat:
    buffer = get_ts(buffer, ts, stat)

adv_stat = ['POS', 'PACE']
for stat in adv_stat:
    buffer = get_ts(buffer, ta, stat)
buffer['TmDRtg'] = buffer.index.get_level_values('TEAM').map(ta['DEF'])

opp_stat = ['DEF', 'OFF', 'FGM', 'FGA', 'TO', 'FTA', 'FTM', 'MINS', 'PTS']
for stat in opp_stat:
    buffer = get_opp(buffer, stat)

ws['qAST'] = ((ps['MINS'] / (buffer['TmMINS'] / 5)) * (1.14 * ((buffer['TmAST'] - ps['AST']) / buffer['TmFGM']))) + ((((buffer['TmAST'] / buffer['TmMINS']) * ps['MINS'] * 5 - ps['AST']) / ((buffer['TmFGM'] / buffer['TmMINS']) * ps['MINS'] * 5 - ps['FGM'])) * (1 - (ps['MINS'] / (buffer['TmMINS'] / 5))))
ws['FG_Part'] = ps['FGM'] * (1 - 0.5 * ((ps['PTS'] - ps['FTM']) / (2 * ps['2PA'] + 3 * ps['3PA'])) * ws['qAST'])
ws['AST_Part'] = (
        0.5 * (((buffer['TmPTS'] - buffer['TmFTM']) - (ps['PTS'] - ps['FTM'])) / (2 * (buffer['Tm2PA'] - ps['2PA']) + 3 * (buffer['Tm3PA'] - ps['3PA']))) * ps['AST']
    )

ws['FT_Part'] = (1-(1-(ps['FTM']/ps['FTA']))**2)*0.44*ps['FTA']
ws['Tm_Sc_Poss'] = buffer['TmFGM'] + (1 - (1 - (buffer['TmFTM'] / buffer['TmFTA']))**2) * 0.44 * buffer['TmFTA']
ws['Tm_ORB_Pct'] = buffer['TmOFF'] / (buffer['TmOFF'] + buffer['oDEF'])
ws['Tm_Play_Pct'] = ws['Tm_Sc_Poss'] / (buffer['TmFGA'] + buffer['TmFTA'] * 0.44 + buffer['TmTO'])
ws['Tm_ORB_Wt'] = ((1 - ws['Tm_ORB_Pct']) * ws['Tm_Play_Pct']) / ((1 - ws['Tm_ORB_Pct']) * ws['Tm_Play_Pct'] + ws['Tm_ORB_Pct'] * (1 - ws['Tm_Play_Pct']))
ws['ORB_Part'] = ps['OFF'] * ws['Tm_ORB_Wt'] * ws['Tm_Play_Pct']
ws = ws.fillna(0)
ws['ScPoss'] = (ws['FG_Part'] + ws['AST_Part'] + ws['FT_Part']) * (1 - (buffer['TmOFF'] / ws['Tm_Sc_Poss']) * ws['Tm_ORB_Wt'] * ws['Tm_Play_Pct']) + ws['ORB_Part']

ws['FGxPoss'] = (ps['FGA'] - ps['FGM']) * (1 - 1.07 * ws['Tm_ORB_Pct'])
ws['FTxPoss'] = ((1 - (ps['FTM'] / ps['FTA']))**2) * 0.44 * ps['FTA']
ws = ws.fillna(0)
ws['TotPoss'] = ws['ScPoss'] + ws['FGxPoss'] + ws['FTxPoss'] + ps['TO']

ws['PProd_FG_Part'] = 2 * (ps['FGM'] + 0.5 * ps['3PM']) * (1 - 0.5 * ((ps['PTS'] - ps['FTM']) / (2 * ps['2PA'] + 3 * ps['3PA'])) * ws['qAST'])
ws['PProd_AST_Part'] = 2 * ((buffer['TmFGM'] - ps['FGM'] + 0.5 * (buffer['Tm3PM'] - ps['3PM'])) / (buffer['TmFGM'] - ps['FGM'])) * 0.5 * (((buffer['TmPTS'] - buffer['TmFTM']) - (ps['PTS'] - ps['FTM'])) / (2 * (buffer['Tm2PA'] - ps['2PA']) + 3 * (buffer['Tm3PA'] - ps['3PA']))) * ps['AST']
ws['PProd_ORB_Part'] = ps['OFF'] * ws['Tm_ORB_Wt'] * ws['Tm_Play_Pct'] * (buffer['TmPTS'] / (buffer['TmPTS'] + (1 - (1 - (buffer['TmFTM'] / buffer['TmFTA'])) ** 2) * 0.44 * buffer['TmFTA']))
ws['PProd'] = (ws['PProd_FG_Part'] + ws['PProd_AST_Part'] + ps['FTM']) * (1 - (buffer['TmOFF'] / ws['Tm_Sc_Poss']) * ws['Tm_ORB_Wt'] * ws['Tm_Play_Pct']) + ws['PProd_ORB_Part']
ws = ws.fillna(0)
ws['ORtg'] = 100 * (ws['PProd'] / ws['TotPoss'])
ws['Floor%'] = ws['ScPoss'] / ws['TotPoss'] * 100

ws['DOR%'] = buffer['oOFF'] / (buffer['oOFF'] + buffer['TmDEF'])
ws['DFG%'] = buffer['oFGM'] / buffer['oFGA']
ws['FMWt'] = (ws['DFG%'] * (1 - ws['DFG%'])) / (ws['DFG%'] * (1 - ws['DOR%']) + (1 - ws['DFG%']) * ws['DOR%'])
ws['Stops1'] = ps['STL'] + ps['BLK'] * ws['FMWt'] * (1 - 1.07 * ws['DOR%']) + ps['DEF'] * (1 - ws['FMWt'])
ws['Stops2'] = (((buffer['oFGA'] - buffer['oFGM'] - buffer['TmBLK']) / buffer['TmMINS']) * ws['FMWt'] * (1 - 1.07 * ws['DOR%']) + ((buffer['oTO'] - buffer['TmSTL']) / buffer['TmMINS'])) * ps['MINS'] + (ps['PF'] / buffer['TmPF']) * 0.44 * buffer['oFTA'] * (1 - (buffer['oFTM'] / buffer['oFTA'])) ** 2
ws['Stops'] = ws['Stops1'] + ws['Stops2']
ws['Stop%'] = ws['Stops'] / (buffer['TmPOS'] * (ps['MINS'] / (buffer['TmMINS']/5)))
ws['D_Pts'] = buffer['oPTS'] / (buffer['oFGM'] + (1 - (1 - (buffer['oFTM'] / buffer['oFTA']))**2) * 0.44 * buffer['oFTA'])
ws['DRtg'] = buffer['TmDRtg'] + 0.2 * (100 * ws['D_Pts'] * (1 - ws['Stop%']) - buffer['TmDRtg'])

lg_PTS_per_poss = ts['PTS'].sum() / ta['POS'].sum()
lg_PTS_per_game = ts['PTS'].sum() / ts['GP'].sum()
ws['uMP/W'] =  lg_PTS_per_game * (buffer['TmPACE'] / lg_pace)
ws['POS'] = 0.5 * (ps['FGA'] + (0.44*ps['FTA']) - (1.07 * ps['OFF']) + ps['TO'])

ws['MO'] = ws['PProd'] - 0.875 * lg_PTS_per_poss * ws['POS']
ws['uOWS'] = ws['MO'] / ws['uMP/W']
ws['MD'] = (ps['MINS'] / buffer['TmMINS']) * buffer['TmPOS'] * (1.08 * lg_PTS_per_poss - ((ws['DRtg']) / 100))
ws['uDWS'] = ws['MD'] / ws['uMP/W']
ws['uWS'] = ws['uOWS'] + ws['uDWS']
adjustor = ws['uWS'].sum()/ts['GW'].sum()
ws['OWS'] = ws['uOWS'] / adjustor
ws['DWS'] = ws['uDWS'] / adjustor
ws['WS'] = ws['OWS'] + ws['DWS']
df[['OWS', 'DWS', 'WS']] = ws[['OWS', 'DWS', 'WS']]

#################################

PRL = (11.5 + 11.0 + 10.6 + 10.5 + 10.5) / 5
df['EWA'] = ((ps['MINS'] * (df['PER'] - PRL)) / 67) / 30

"""
########## BPM ##########
bpm = pd.DataFrame(index=ws.index)
# Step 1: Position and Offensive Role Regression
buffer = get_ts(buffer, ts, 'REB')
bpm['REB%'] = ps['REB'] / buffer['TmREB']
bpm['STL%'] = ps['STL'] / buffer['TmSTL']
bpm['PF%'] = ps['PF'] / buffer['TmPF']
bpm['AST%'] = ps['AST'] / buffer['TmAST']
bpm['BLK%'] = ps['BLK'] / buffer['TmBLK']
bpm['Position'] = 2.130 + 8.668 * bpm['REB%'] - 2.486*bpm['STL%'] + 0.992*bpm['PF%'] - 3.536*bpm['AST%'] + 1.667*bpm['BLK%']

bpm['TSA'] = 2 * (ps['FGA'] + 0.44*ps['FTA'])
bpm['P/TSA'] = ps['PTS'] / bpm['TSA']
ts['TSA'] = 2 * (ts['FGA'] + 0.44*ts['FTA'])
ts['P/TSA'] = ts['PTS'] / ts['TSA']
ts['TreshP'] = ts['P/TSA'] - 0.33
bpm = get_ts(bpm, ts, 'TreshP')
bpm['TreshP'] = bpm['P/TSA'] - bpm['TmTreshP']
bpm['Tresh%'] = bpm['TreshP'] / 0.33
bpm['Off Role'] = 6 - 6.642 * bpm['AST%'] - 8.544 * bpm['Tresh%']
"""

game = ts + os
game_stats = ['PTS', 'FGM', 'FTM', 'FGA', 'FTA', 'DEF', 'OFF', 'AST', 'STL', 'BLK', 'PF', 'TO']
for stat in game_stats:
    buffer = get_game(buffer, stat)
buffer['PIE num'] = ps['PTS'] + ps['FGM'] + ps['FTM'] - ps['FGA'] - ps['FTA'] + ps['DEF'] + ps['OFF']/2 + ps['AST'] + ps['STL'] + ps['BLK']/2 - ps['PF'] - ps['TO']
buffer['PIE den'] = buffer['GmPTS'] + buffer['GmFGM'] + buffer['GmFTM'] - buffer['GmFGA'] - buffer['GmFTA'] + buffer['GmDEF'] + buffer['GmOFF']/2 + buffer['GmAST'] + buffer['GmSTL'] + buffer['GmBLK']/2 - buffer['GmPF'] - buffer['GmTO']
buffer['PIE'] = buffer['PIE num'] / buffer['PIE den'] * 100
df['PIE'] = buffer['PIE']

# Total Player Possessions
buffer['Q'] = 5 * ps['MINS'] * ts['AST']/ts['MINS'] - ps['AST']
buffer['R'] = 5 * ps['MINS'] * ts['FGM']/ts['MINS'] - ps['AST']
buffer = get_ts(buffer, ta, 'OREB%')
buffer['POS'] = ps['FGA'] - (ps['FGA'] - ps['FGM']) * buffer['TmOREB%']/100 + 0.37 * ps['AST'] * buffer['Q']/buffer['R'] + ps['TO'] + 0.44 * ps['FTA']
buffer['POS/G'] = buffer['POS']/ps['GP']
buffer = get_ts(buffer, ta, 'POS')
buffer = get_ts(buffer, ts, 'MINS')
buffer['POS%'] = 100 * buffer['POS'] / ((ps['MINS'] / (buffer['TmMINS'] / 5)) * buffer['TmPOS'])
df[['POS/G','POS%']] = buffer[['POS/G','POS%']]

# Usage Rate
buffer['USG%'] = 100 * ((ps['FGA'] + 0.44 * ps['FTA'] + ps['TO']) * buffer['TmMINS']/5) / (ps['MINS'] * buffer['TmPOS'])
df['USG%'] = buffer['USG%']

# Scoring Metrics
cols = ['EFG%', 'TS%', 'PPWS', 'eTS%', 'ePPWS', 'FTR']
buffer['EFG%'] = (ps['FGM'] + 0.5 * ps['3PM']) / ps['FGA'] * 100
buffer['TS%'] = ps['PTS'] / (2 * (ps['FGA'] + 0.44 * ps['FTA'])) * 100
buffer['PPWS'] = ps['PTS'] / (ps['FGA'] + 0.44 * ps['FTA'])
buffer['eTS%'] = ps['PTS'] / (2 * (ps['FGA'] + ps['3PA'] + 0.44 * ps['FTA'])) * 100
buffer['ePPWS'] = ps['PTS'] / (ps['FGA'] + 0.5 * ps['3PA'] + 0.44 * ps['FTA'])
buffer['FTR'] = ps['FTA'] / ps['FGA']
df[cols] = buffer[cols]

# Touches
buffer = get_ts(buffer, ts, 'FTA')
buffer = get_ts(buffer, ts, 'Fls on:')
buffer['Touches'] = ps['FGA'] + ps['TO'] + (ps['FTA'] / (buffer['TmFTA'] / buffer['TmFls on:'])) + ps['AST']/0.17
buffer['Touches/G'] = buffer['Touches'] / ps['GP']
df['T/G'] = buffer['Touches/G']

buffer['%Pass'] = 100 * (ps['AST'] / 0.17) / buffer['Touches']
buffer['%Shoot'] = 100 * ps['FGA'] / buffer['Touches']
buffer['%Fouled'] = 100 * (ps['FTA'] / (buffer['TmFTA'] / buffer['TmFls on:'])) / buffer['Touches']
buffer['%TO'] = 100 * ps['TO'] / buffer['Touches']
df[['%Pass', '%Shoot', '%Fouled', '%TO']] = buffer[['%Pass', '%Shoot', '%Fouled', '%TO']]

# Playmaking Metrics
buffer = get_ts(buffer, ts, 'FGM')
buffer = get_ts(buffer, ta, 'PACE')
df['AST/TO'] = ps['AST'] / ps['TO']
df['Econ'] = (ps['AST'] + ps['STL'] - ps['TO']) / ps['GP']
df['PPR'] = (lg_pace / buffer['TmPACE']) * (((ps['AST'] * 2/3) - ps['TO']) / ps['MINS']) * 100
df['AR'] = ps['AST'] / buffer['POS'] * 100
df['pAST%'] = ps['AST'] / (((ps['MINS'] / (buffer['TmMINS'] / 5)) * buffer['TmFGM']) - ps['FGM']) * 100
df['hAST%'] = ps['AST'] / (ps['FGA'] + (0.44 * ps['FTA']) + ps['AST'] + ps['TO'])
df['TOR'] = ps['TO'] / buffer['POS'] * 100
df['hTO%'] = ps['TO'] / (ps['FGA'] + (0.44 * ps['FTA']) + ps['AST'] + ps['TO'])

# Rebounding and Defense Metrics
cols = ['REB', 'OFF', 'DEF']
for stat in cols:
    buffer = get_opp(buffer, stat)
    buffer = get_ts(buffer, ts, stat)
df['STL%'] = ps['STL'] / buffer['POS'] * 100
df['BLK%'] = ps['BLK'] / buffer['POS'] * 100
df['REB%'] = (ps['REB'] * buffer['TmMINS']/5) / (ps['MINS'] * (buffer['TmREB'] + buffer['oREB'])) * 100
df['OREB%'] = (ps['OFF'] * buffer['TmMINS']/5) / (ps['MINS'] * (buffer['TmOFF'] + buffer['oDEF'])) * 100
df['DREB%'] = (ps['DEF'] * buffer['TmMINS']/5) / (ps['MINS'] * (buffer['TmDEF'] + buffer['oOFF'])) * 100
