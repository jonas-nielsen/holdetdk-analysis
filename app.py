import general_stats
import readme_panel
import player_stats
import streamlit as st

#menu items
options = { 'Readme': readme_panel.show_panel,
            'Overall stats': general_stats.show_panel,
            'Player stats': player_stats.show_panel,
            }

st.sidebar.header('Select dashboard:')
option = st.sidebar.radio(options=list(options.keys()), index=0, label="")

options[option]()