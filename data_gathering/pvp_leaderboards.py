import requests

def leaderboards_400_data():

    endpoint = 'https://game-api.axie.technology/toprank?offset=0&limit=400'
    request = requests.Session()
    response = request.get(endpoint)
    fetched_data = response.json()

    with open('db/leaderboards_ronin.csv','w') as f:
        pass

    with open('db/leaderboards_axies.csv','w') as f:
        pass

    with open('db/leaderboards_ronin.csv','a') as f:
        
        for items in fetched_data['items']:
            ronin = items["client_id"]
            f.writelines(f'{ronin}\n')
            get_player_axies(ronin)


def get_player_axies(ronin):

    endpoint = f'https://game-api.axie.technology/logs/pvp/{ronin}'
    request = requests.Session()
    response = request.get(endpoint)
    fetched_data = response.json() 

    battle_data = fetched_data['battles'][0]

    if battle_data['first_client_id'] == ronin:
        t1 = battle_data['first_team_fighters']
        with open('db/leaderboards_axies.csv','a') as f:
            f.writelines(f'{t1[0]},{t1[1]},{t1[2]}\n')

    elif battle_data['second_client_id'] == ronin:
        t2 = battle_data['second_team_fighters']
        with open('db/leaderboards_axies.csv','a') as f:
            f.writelines(f'{t2[0]},{t2[1]},{t2[2]}\n')       

if __name__ == "__main__":    
    leaderboards_400_data()
