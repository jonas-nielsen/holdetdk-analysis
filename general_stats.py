import streamlit as st
import pandas as pd
import plotly.express as px
import prep_data

def show_panel():
    '''
    Show a panel with data across all teams and players.
    '''
    st.markdown("# HOLDET.DK STATS")

    hard_refresh = st.button("Hard refresh")

    all_meta_data = prep_data.get_metadata(hard_refresh)

    all_rounds = prep_data.get_round_data(hard_refresh=hard_refresh)

    if st.checkbox("Show example metadata"):
        st.write(all_meta_data)

    if st.checkbox("Show example rounds:"):
        st.write(all_rounds.tail())

    st.markdown('''
                    # What players been the most profitable per round?
                    Let's find the player with the higest growth for each round.
                    ''')
    profit_per_round = all_rounds.copy().groupby(['round']).idxmax()
    profit_per_round['id'] = profit_per_round['growth']
    profit_per_round = pd.merge(profit_per_round['id'], all_rounds, on='id', how='inner')
    profit_per_round = pd.merge(profit_per_round, all_meta_data, on='player_id', how='inner')    
    fig = px.bar(profit_per_round,
                            x='round',
                            y='growth',
                            color="player_desc",
                            hover_name="player_desc",    
                            template='plotly_white')    
    st.plotly_chart(fig)
    st.write("The average highest growth pr. round has been {}".format(profit_per_round['growth'].mean()))