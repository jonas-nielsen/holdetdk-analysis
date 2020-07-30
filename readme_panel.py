import streamlit as st
import prep_data


def show_panel():

    st.markdown('''
    # Holdet.dk analysis
    This allows you to explore the Premier League datasets from Holdet.dk in slightly more depth than their own app allows.
    
    You can select a set of stats to explore in the sidebar to the right. If you haven't already, you should start by fetching datasets below:
    ''')

    if st.button("Refresh data"):
        st.write("Refreshing metadata - this might take 30 seconds... 🚶‍♂️🏃‍♂️🚴")
        prep_data.get_round_data(hard_refresh=True)
        prep_data.get_metadata(hard_refresh=True)

    with open('README.md', 'r') as file:
        data = file.read()
    st.markdown('''
    # Project README
    ''')
    st.markdown(data)
