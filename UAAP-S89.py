import streamlit as st
import os
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
pd.options.display.float_format = "{:,.2f}".format

ts = pd.read_csv('./current_stats/team_aggregate.csv', index_col=['TEAM'])
# Column Lists
with open('cols_pb.txt', 'r') as file:
    pb_cols = [line.strip() for line in file]
with open('cols_pa.txt', 'r') as file:
    pa_cols = [line.strip() for line in file]
with open('cols_tb.txt', 'r') as file:
    tb_cols = [line.strip() for line in file]
with open('cols_ta.txt', 'r') as file:
    ta_cols = [line.strip() for line in file]

teams={}
with open('colors.txt','r') as file:
    for line in file:
        line = line.rstrip('\n')
        if ':' in line:
            team, color = line.split(':',1)
            teams[team] = color

with open('title.txt', 'r') as file:
    title = [line.strip() for line in file]

st.set_page_config(
    page_title='{0}'.format(title[0]),
    page_icon=':basketball:',
    layout='wide'
)

st.title(title[0])
carl = "https://twitter.com/mc_miranda34"
pong = "https://twitter.com/ompongski"
st.link_button(label='By Carl Miranda (@mc_miranda34)', url=carl, type='primary', icon=':material/person:')
st.link_button(label='Raw Box Scores from Pong Ducanes (@ompongski)', url=pong, type='primary', icon=':material/insert_chart:')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(['Player Per-Game Stats', 'Player Per-30 Minute Stats', 'Player Advanced Stats', 'Player Comparison', 'Player Trajectory', 'Team Per-Game Stats', 'Opponent Per-Game Stats', 'Team Advanced Stats', 'Team Comparison', 'Glossary'])

cm = sns.dark_palette("green", as_cmap=True)
r_cm = sns.dark_palette("green", as_cmap=True, reverse=True)

with tab1:
    st.header('All Players', divider='gray')
    df = pd.read_csv('./current_stats/player_per_game.csv', index_col=['TEAM', 'NO.', 'PLAYER'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MINS'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='grey')
        df = pd.read_csv('./per_team/{0}_pg.csv'.format(team), index_col=['TEAM', 'NO.', 'PLAYER'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(df)

with tab2:
    st.header('All Players', divider='gray')
    df = pd.read_csv('./current_stats/player_per_30.csv', index_col=['TEAM', 'NO.', 'PLAYER'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MINS'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='gray')
        df = pd.read_csv('./per_team/{0}_p30.csv'.format(team), index_col=['TEAM', 'NO.', 'PLAYER'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(df)

with tab3:
    st.markdown('*Note for SP: Penalties are not included due to inavailability of data.*')
    st.markdown('*Note for WS: Values are re-normalized every after game. This should not affect rankings.*')
    st.header('All Players', divider='gray')
    df = pd.read_csv('./current_stats/player_advanced.csv', index_col=['TEAM', 'NO.', 'PLAYER'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MPG'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pa_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TOR','hTO%', 'DRtg']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='gray')
        df = pd.read_csv('./per_team/{0}_pa.csv'.format(team), index_col=['TEAM', 'NO.', 'PLAYER'])
        df = df.reindex(columns=pa_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TOR','DRtg']).format("{:.2f}")
        st.write(df)

with tab4:
    st.header('Player Comparison', divider='gray')
    st.markdown('Use this tab to compare two or more players more easily. You may search for your chosen players by typing their last name or team below.')
    st.markdown('*This page uses the same data as in other tabs. Refer to notes in other tabs if necessary.*')
    df1 = pd.read_csv('./current_stats/player_per_game.csv', index_col=['TEAM', 'NO.', 'PLAYER'])
    df2 = pd.read_csv('./current_stats/player_per_30.csv', index_col=['TEAM', 'NO.', 'PLAYER'])
    df3 = pd.read_csv('./current_stats/player_advanced.csv', index_col=['TEAM', 'NO.', 'PLAYER'])

    row_indices = st.multiselect(
        "Select Players:",
        options=df3.index.tolist(),
        default=[]
    )

    if row_indices:
        st.header("Player Per-Game Stats")
        frozen_df1 = df1.loc[row_indices]
        frozen_df1 = frozen_df1.reindex(columns=pb_cols)
        frozen_df1 = frozen_df1.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df1)
        st.header("Player Per-30 Stats")
        frozen_df2 = df2.loc[row_indices]
        frozen_df2 = frozen_df2.reindex(columns=pb_cols)
        frozen_df2 = frozen_df2.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df2)
        st.header("Player Advanced Stats")
        frozen_df3 = df3.loc[row_indices]
        frozen_df3 = frozen_df3.reindex(columns=pa_cols)
        frozen_df3 = frozen_df3.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TOR','hTO%','DRtg']).format("{:.2f}")
        st.write(frozen_df3)

with tab5:
    """
    st.header('Player Trajectory')
    st.markdown('Use this tab to see the trajectory of a player\'s statistic across his games played, and compare it to the trajectory of the league average.')
    st.markdown('*This page uses the same data as in other tabs. Refer to notes in other tabs if necessary.*')

    st.header('Player Per-Game Stats')
    df1 = pd.read_csv('./current_stats/player_advanced.csv', index_col=['PLAYER'])
    df1 = df1.reindex(columns=pb_cols)
    col1, col2 = st.columns(2)
    with col1:
        target_player = st.selectbox(
            label='Select Player',
            options=df1.index.tolist(),
            index=None,
            placeholder='Select Player'
        )
    with col2:
        stat = st.selectbox(
            label='Select Stat',
            options=df1.columns.tolist(),
            index=None,
            placeholder='Select Stat'
        )

    if stat != None and target_player != None:
        base_directory = './player_stats/'
        league_player = 'League'
        player_data = pd.DataFrame(columns=['GP', stat])
        league_data = pd.DataFrame(columns=['GP', stat])

        game_directories = [d for d in os.listdir(base_directory) if d.startswith('./player_stats/player_per_game')]
        game_directories.sort()
        print(game_directories)

        for game_dir in game_directories:
            game_directory = os.path.join(base_directory, game_dir)
            file_path = os.path.join(game_directory, 'player_per_game.csv')
            df = pd.read_csv(game_dir, index_col=['PLAYER'])
            if target_player in df.index:
                player_game_data = df.loc[target_player, ['GP', stat]]
                player_data = pd.concat([player_data, player_game_data.to_frame().T])
            if league_player in df.index:
                league_game_data = df.loc[league_player, ['GP', stat]]
                league_data = pd.concat([league_data, league_game_data.to_frame().T])
        player_data = player_data.drop_duplicates(subset='GP', keep='first', inplace=True)
        player_data = player_data.sort_values(by='GP')
        league_data = league_data.drop_duplicates(subset='GP', keep='first')
        league_data = league_data.sort_values(by='GP')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=player_data['GP'], y=player_data[stat], mode='lines+markers',
                                 name=target_player, line=dict(color='green', width=2),
                                 marker=dict(size=6, color='green', symbol='circle')))
        fig.add_trace(go.Scatter(x=league_data['GP'], y=league_data[stat], mode='lines',
                                 name='League Average', line=dict(color='blue', width=2)))

        fig.update_layout(xaxis_title='Games Played (GP)', yaxis_title=stat, showlegend=True, template='plotly')
        st.plotly_chart(fig)

    st.header('Advanced Stats')
    df3 = pd.read_csv('./current_stats/player_advanced.csv', index_col=['PLAYER'])
    df3 = df3.reindex(columns=pa_cols)
    col1, col2 = st.columns(2)
    with col1:
        target_player = st.selectbox(
            label='Select Player',
            options=df3.index.tolist(),
            index=None,
            placeholder='Select Player'
        )
    with col2:
        stat = st.selectbox(
            label='Select Stat',
            options=df3.columns.tolist(),
            index=None,
            placeholder='Select Stat'
        )

    if stat != None and target_player != None:
        base_directory = './player_stats'
        league_player = 'League'
        player_data = pd.DataFrame(columns=['GP', stat])
        league_data = pd.DataFrame(columns=['GP', stat])

        game_directories = [d for d in os.listdir(base_directory) if d.startswith('player_advanced')]
        game_directories.sort()

        for game_dir in game_directories:
            game_directory = os.path.join(base_directory, game_dir)
            file_path = os.path.join(game_directory, 'advanced_stats.csv')
            df = pd.read_csv(file_path, index_col=['PLAYER'])
            if target_player in df.index:
                player_game_data = df.loc[target_player, ['GP', stat]]
                player_data = pd.concat([player_data, player_game_data.to_frame().T])
            if league_player in df.index:
                league_game_data = df.loc[league_player, ['GP', stat]]
                league_data = pd.concat([league_data, league_game_data.to_frame().T])

        player_data = player_data.drop_duplicates(subset='GP', keep='first')
        player_data = player_data.sort_values(by='GP')
        league_data = league_data.drop_duplicates(subset='GP', keep='first')
        league_data = league_data.sort_values(by='GP')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=player_data['GP'], y=player_data[stat], mode='lines+markers',
                                 name=target_player, line=dict(color='green', width=2),
                                 marker=dict(size=6, color='green', symbol='circle')))
        fig.add_trace(go.Scatter(x=league_data['GP'], y=league_data[stat], mode='lines',
                                 name='League Average', line=dict(color='blue', width=2)))

        fig.update_layout(xaxis_title='Games Played (GP)', yaxis_title=stat, showlegend=True, template='plotly')
        st.plotly_chart(fig)
        """

with tab6:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('./current_stats/team_per_game.csv', index_col=['TEAM'])
    df['W'] = df['GW']
    df['L'] = df['GP'] - df['GW']
    df['W%'] = df['W'] / df['GP']
    df = df.reindex(columns=tb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['L','TO','PF']).format("{:.2f}")
    st.write(df)

with tab7:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('./current_stats/opp_per_game.csv', index_col=['TEAM'])
    df = df.reindex(columns=tb_cols)
    df = df.drop(labels=['W','L','W%','MINS'], axis=1)
    df = df.style.background_gradient(cmap=r_cm, axis=0).background_gradient(cmap=cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)

with tab8:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('./current_stats/team_advanced.csv', index_col=['TEAM'])
    df = df.reindex(columns=ta_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['DEF','TOR', 'hTO%', 'HHI','Py-L']).format("{:.2f}")
    st.write(df)

with tab9:
    st.header('Team Comparison', divider='gray')
    st.markdown('Use this tab to compare two or more teams more easily.')
    df1 = pd.read_csv('./current_stats/team_per_game.csv', index_col='TEAM')
    df2 = pd.read_csv('./current_stats/opp_per_game.csv', index_col='TEAM')
    df3 = pd.read_csv('./current_stats/team_advanced.csv', index_col='TEAM')

    row_indices = st.multiselect(
        "Select Teams:",
        options=df1.index.tolist(),
        default=[]
    )

    if row_indices:
        st.header("Team Per-Game Stats")
        frozen_df1 = df1.loc[row_indices]
        frozen_df1 = frozen_df1.reindex(columns=tb_cols)
        frozen_df1 = frozen_df1.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df1)
        st.header("Opponent Stats")
        frozen_df2 = df2.loc[row_indices]
        frozen_df2 = frozen_df2.reindex(columns=tb_cols)
        frozen_df2 = frozen_df2.drop(labels=['W','L','W%','MINS'], axis=1)
        frozen_df2 = frozen_df2.style.background_gradient(cmap=r_cm, axis=0).background_gradient(cmap=cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df2)
        st.header("Team Advanced Stats")
        frozen_df3 = df3.loc[row_indices]
        frozen_df3 = frozen_df3.reindex(columns=ta_cols)
        frozen_df3 = frozen_df3.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['DEF','TOR', 'hTO%', 'HHI','Py-L']).format("{:.2f}")
        st.write(frozen_df3)

with tab10:
    with open('Glossary.md','r') as f:
        markdown_content = f.read()
        st.markdown(markdown_content)
