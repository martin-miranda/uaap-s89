#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:26:56 2025

@author: martinmiranda
"""
first_game = 1
last_game = 29

import subprocess
from pathlib import Path
import shutil

directory = Path('../current_stats')

# Iterate over all files in the directory and remove them
for file in directory.iterdir():
    if file.is_file():
        file.unlink()

print('Deleted current stats')
print('-----')
print('')

source_dir = '../blanks'
shutil.copytree(source_dir, directory, dirs_exist_ok=True)
print('Copied blank templates')
print('------')
print('')

for game_id in range(first_game,last_game + 1):
    print('Running scripts for Game {0}'.format(game_id))

    subprocess.run(['python', 'player_basic.py', str(game_id)])
    print('Player Basic Stats completed.')

    subprocess.run(['python', 'team_basic.py', str(game_id)])
    print('Team Basic Stats completed.')

    subprocess.run(['python', 'team_advanced.py', str(game_id)])
    print('Team Advanced Stats completed.')

    subprocess.run(['python', 'player_advanced.py', str(game_id)])
    print('Player Advanced Stats completed.')

    # Spacer
    print('-----')
    print('')
