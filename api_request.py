import requests
import csv
    


endpoint = 'https://api.axietech.info/leaderboard/v3'
request = requests.Session()
response = request.get(endpoint)
fetched_data = response.json()

# keys = fetched_data[0].keys()
values = [[x['roninAddress'],x['elo'],x['rank']] for x in fetched_data]
print(values)
for v in values:
    with open('db/v3_leaderboards_100.csv', 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(values)