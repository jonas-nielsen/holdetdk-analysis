import requests
import json
import pandas as pd
import os

def get_metadata(hard_refresh = False):
    cachepath = os.path.join("data", 'players.json')
    if(not os.path.exists(cachepath)) or hard_refresh:
        player_identities_resp = requests.get('https://fs-api.swush.com/tournaments/356?appid=holdet&culture=da')
        player_identities = json.loads(player_identities_resp.text)
        with open(cachepath, 'w') as outfile:
                json.dump(player_identities, outfile)
    else:
        with open(cachepath, 'r') as outfile:
            player_identities = json.load(outfile)

    teams = {}
    for team in player_identities['teams']:
        teams[team['id']] = team
        teams[team['id']]['team'] = team['id']
        teams[team['id']]['team-name'] = team['name']
        teams[team['id']]['team-abbr'] = team['abbreviation']    

    teams_pd = pd.DataFrame.from_dict(teams, orient='index')
    #st.write(teams_pd)


    persons = {}
    for person in player_identities['persons']:
        persons[person['id']] = person
        persons[person['id']]['person'] = person['id']
        persons[person['id']]['fullname'] = " ".join([person['firstname'], person['lastname']])

    persons_pd = pd.DataFrame.from_dict(persons, orient='index')

    players_list = {}
    for player in player_identities['players']:
        person_id = player['person']['id']    
        players_list[person_id] = player
        players_list[person_id]['player_id'] = player['id']
        players_list[person_id]['person'] = player['person']['id']
        players_list[person_id]['team'] = player['team']['id']
        players_list[person_id]['position'] = player['position']['id']
        

    players_pd = pd.DataFrame.from_dict(players_list, orient='index')

    all_players_and_persons = pd.merge(persons_pd[['firstname', 'lastname', 'fullname', 'person']], players_pd, on='person', how='outer')
    all_meta_data = pd.merge(all_players_and_persons, teams_pd[['team-name', 'team-abbr', 'team']], on='team', how='outer')
    all_meta_data['player_desc'] = all_meta_data['fullname'] + ", " + all_meta_data['team-abbr']
    return all_meta_data

def get_round_data(rounds_ids = range(2, 18), hard_refresh = False):    
    rounds = {}
    


    for round in rounds_ids:
        cachepath = os.path.join("data", str(round))
        if(not os.path.exists(cachepath)) or hard_refresh:
            players_resp = requests.get('https://fs-api.swush.com/games/536/rounds/{}/statistics?appid=holdet&culture=da'.format(round))
            rounds[round] = json.loads(players_resp.text)
            with open(cachepath, 'w') as outfile:
                json.dump(rounds[round], outfile)
        else:
            with open(cachepath, 'r') as outfile:
                rounds[round] = json.load(outfile)    


    # Process all of the rounds - put all values in a pandas dataframe, indexed by value id (also has round id and player id)
    i = 0
    entries = {}
    for round in rounds_ids:
        for player in rounds[round]:
            entries[player['values']['id']] = player['values']
            entries[player['values']['id']]['player_id'] = player['player']['id']
            entries[player['values']['id']]['round'] = round        

    all_rounds = pd.DataFrame.from_dict(entries, orient='index')     
    return all_rounds
