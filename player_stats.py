import streamlit as st
import pandas as pd
import plotly.express as px
import prep_data
import numpy as np


def show_panel():
    '''
    Do a few basic statistics on individual playesr. The user can select
    a specific player in the sidebar (team->player), and then get
    graphs on growth over time, popularity over time, best round, worst round,
    etc.
    '''
    st.markdown('''
                    # Individual player stats
                    Select a player in the sidebar to get stats for him
                ''')

    hard_refresh = st.button("Hard refresh")

    all_meta_data = prep_data.get_metadata(hard_refresh)
    all_rounds = prep_data.get_round_data(hard_refresh=hard_refresh)
    all_rounds_w_meta = pd.merge(
        all_meta_data, all_rounds, on='player_id', how='inner')

    clubs = all_meta_data['team-name'].unique()
    clubs.sort()
    club = st.sidebar.selectbox('Team', clubs, index=0)
    players = all_meta_data[all_meta_data['team-name']
                            == club]['fullname'].unique()
    players.sort()
    player_name = st.sidebar.selectbox('Player', players, index=0)

    get_player_rounds = all_rounds_w_meta[all_rounds_w_meta['fullname'] == player_name]

    

    st.markdown('''
        ### Growth of *{}* over time
    '''.format(player_name))    
    fig = px.bar(get_player_rounds.assign(growth_perf=lambda x: np.floor(x.growth / 100000)),
                 x='round',
                 y='growth',
                 color='growth_perf',
                 hover_name='player_desc',
                 color_continuous_scale='Bluered_r',
                 template='plotly_white')
    st.plotly_chart(fig)

    st.markdown('''
        ### Value-change (index) of *{}* over time
    '''.format(player_name))    
    fig = px.bar(get_player_rounds.assign(index_value=lambda x: x.totalGrowth/x.value, index=lambda x: x.index/100),
                 x='round',
                 y='index_value',
                 hover_name='player_desc',
                 color_continuous_scale='Bluered_r',
                 template='plotly_white')
    st.plotly_chart(fig)    

    st.markdown('''
        ### Popularity of *{}* over time
    '''.format(player_name))
    fig = px.bar(get_player_rounds,
                 x='round',
                 y='popularity',
                 color="player_desc",
                 hover_name="player_desc",
                 template='plotly_white')
    st.plotly_chart(fig)


    st.markdown('''
        ### Trade trend for *{}* over time
    '''.format(player_name))    
    fig = px.bar(get_player_rounds,
                 x='round',
                 y='trend',
                 hover_name='player_desc',
                 color_continuous_scale='Bluered_r',
                 template='plotly_white')
    st.plotly_chart(fig)