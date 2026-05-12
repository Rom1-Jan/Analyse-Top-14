import requests
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


def generate_json_file():
    #Permet d'effectuer la requête à l'API et de crée le fichier json de stockage
    
    top14_id = 4430
    all_matches = []

    for journee in range(1, 27):
        response = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventsround.php?id={top14_id}&r={journee}&s=2025-2026")
        data = response.json()
        
        if data['events']:
            all_matches.extend(data['events'])
            print(f"Journée {journee} : {len(data['events'])} matchs récupérés")
        else:
            print(f"Journée {journee} : aucun match")


    final_data = {"events": all_matches}

    with open('autreProjet/top14_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)


def load_data():
    """Charge le fichier avec nos données
    """
    with open('autreProjet/top14_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_df(data):
    """Créer les dataframes

    Args:
        data (dict): 
    """
    matches = []
    teams = []
    team_id_inserted = set()
    for event in data['events']:
        
        matches.append({
            'match_id': event['idEvent'],
            'journée': event['intRound'],
            'date': event['dateEvent'],
            'id_home_team': event['idHomeTeam'], 
            'id_away_team': event['idAwayTeam'],
            'home_score': event.get('intHomeScore'),
            'away_score': event.get('intAwayScore'),
            'winner': get_winner(event)
        })
        
        team_id = event['idHomeTeam']
        if team_id not in team_id_inserted:
            team_id_inserted.add(team_id)
            teams.append({
                'team_id':event['idHomeTeam'],
                'team_name':event['strHomeTeam'],
                'team_stadium':event['strVenue'],
                'badge_url': event['strHomeTeamBadge']
            })

    df_matches = pd.DataFrame(matches)
    df_teams = pd.DataFrame(teams)
    
    df_teams.loc[df_teams['team_name'] == 'US Montauban', 'team_stadium'] = 'Stade de Sapiac'
    df_teams.loc[df_teams['team_name'] == 'Montpellier Hérault Rugby', 'team_stadium'] = 'Septeo Stadium'
    df=pd.DataFrame(data)
    return df_matches, df_teams

def get_winner(data):
    home = data.get('intHomeScore')
    away = data.get('intAwayScore')
    
    if home is None or away is None:
        return 'Not played'
    if int(home) > int(away):
        return data['idHomeTeam']
    elif int(home) < int(away):
        return data['idAwayTeam']
    else:
        return 'Equality'

def get_home_away_win(team_id):
    home = df_matches[df_matches['id_home_team'] == team_id]
    away = df_matches[df_matches['id_away_team'] == team_id]
    
    return {
        'Home': {
            'victoires': len(home[home['winner'] == team_id]),
            'defaites': len(home[(home['winner'] != team_id) & (home['winner'] != 'Not played')]),
            'non_joues': len(home[home['winner'] == 'Not played'])
        },
        'Away': {
            'victoires': len(away[away['winner'] == team_id]),
            'defaites': len(away[(away['winner'] != team_id) & (away['winner'] != 'Not played')]),
            'non_joues': len(away[away['winner'] == 'Not played'])
        }
    }
    
def add_coord(df_teams):
    stades_coords = {
        '135332': {'lat': 45.78933, 'lon': 3.10615},
        '135339': {'lat': 43.62194, 'lon': 1.41556},
        '135337': {'lat': 48.84320, 'lon': 2.25293},
        '135328': {'lat': 43.48545, 'lon': -1.47940},
        '135331': {'lat': 43.61092, 'lon': 2.25271},
        '135341': {'lat': 45.72377, 'lon': 4.83225},
        '135334': {'lat': 43.59288, 'lon': 3.84812},
        '135336': {'lat': 48.89565, 'lon': 2.22955},
        '135338': {'lat': 43.11900, 'lon':5.93656},
        '137384': {'lat': 43.30952, 'lon':-0.31692},
        '135340': {'lat': 46.15830, 'lon':-1.17836},
        '135329': {'lat': 44.82917, 'lon': -0.59806},
        '137386': {'lat': 42.71549, 'lon': 2.88997},
        '141952': {'lat': 44.01021, 'lon': 1.35174},
    }

    for index, elt in df_teams.iterrows():
        team_id = elt['team_id']
        df_teams.loc[index, 'latitude'] = stades_coords[team_id]['lat']
        df_teams.loc[index, 'longitude'] = stades_coords[team_id]['lon']

def get_current_ranking():
    all_classements = {}

    for journee in range(1, 27):
        id_journee = 11608 - journee
        url = f"https://www.rugbyrama.fr/resultats/rugby/top-14/phase-reguliere/classements/{id_journee}/journee-{journee}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        lignes = soup.find_all('li', class_='li_idalgo_content_standing')
        classement_general = lignes[1:15]
        
        classement = []
        for i, ligne in enumerate(classement_general):
            classement.append({
                'position': i + 1,
                'equipe': ligne.find('a', class_='a_idalgo_content_standing_name').text,
                'points': ligne.find('span', class_='span_idalgo_content_standing_points').text,
                'victoires': ligne.find('span', class_='span_idalgo_content_standing_win').text,
                'nulls': ligne.find('span', class_='span_idalgo_content_standing_draw').text,
                'défaites': ligne.find('span', class_='span_idalgo_content_standing_lost').text,
                'bo': ligne.find('span', class_='span_idalgo_content_standing_bo').text,
                'bd': ligne.find('span', class_='span_idalgo_content_standing_bd').text,
            })
        
        all_classements[journee] = classement
        print(f"Journée {journee} récupérée")

    with open('autreProjet/classements.json', 'w', encoding='utf-8') as f:
        json.dump(all_classements, f, ensure_ascii=False, indent=2)
            

def json_to_csv():
    with open('autreProjet/classements.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    for journee, classement in data.items():
        for equipe in classement:
            equipe['journee'] = journee
            rows.append(equipe)

    df_classements = pd.DataFrame(rows)
    df_classements.to_csv('autreProjet/classements.csv', index=False)


if __name__ == "__main__":
    generate_json_file()
    data=load_data()
    df_matches, df_teams = create_df(data)
    add_coord(df_teams)
    #get_current_ranking()
    #json_to_csv()
    df_matches.to_csv('autreProjet/top14_matches.csv', index=False)
    df_teams.to_csv('autreProjet/top14_teams.csv', index=False)
    #print(df_teams)
    #print(df_matches[df_matches['id_away_team']=='135339'])
    #print(df_matches)
    #print(get_home_away_win('135339'))