import requests

API_KEY = '7044e52e619745f4bbaff76588b5fc5e'
url = 'https://api.football-data.org/v4/competitions/PL/matches'

headers = {
    'X-Auth-Token': API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    matches = data['matches']
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        match_date = match['utcDate']
        print('{} vs {} on {}'.format(home_team, away_team, match_date))
else:
    print('Error fetching data', response.status_code)
