import requests

def axie_detail_id(id):

    endpoint = "https://graphql-gateway.axieinfinity.com/graphql"


    body = {
    "operationName": "GetAxieDetail",
    "variables": {
        "axieId": id
    },

    "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
    }

    request = requests.Session()
    response = request.post(endpoint,headers={'Content-Type': 'application/json'}, json = body)
    print('rate limit',response.headers['RateLimit-Remaining'])
    fetched_data = response.json()

    return fetched_data

## get id and price

if __name__ == "__main__":
    x = axie_detail_id(11295336)
    print(x['data']['axie'].keys())
    print(x['data']['axie']['birthDate'])



    # print(x['data']['axie']['stats']['speed'])
    # print(x['data']['axie']['parts'][0]['id'])
    # print(x['data']['axie']['parts'][1]['id'])
    # print(x['data']['axie']['parts'][2]['id'])
    # print(x['data']['axie']['parts'][3]['id'])
    # print(x['data']['axie']['parts'][4]['id'])
    # print(x['data']['axie']['parts'][5]['id'])
    # print(x['data']['axie']['breedCount'])
    # print(x['data']['axie']['class'])

    # print(x['data']['axie']['parts'][2:])
    # print(len(x['data']['axie']['parts'][2:]))
    print(x['data']['axie']['stats']['speed'])


    # xx = [ x['id'] for x in x['data']['axie']['parts'][2:]]
    
    # print(xx)


    # breedCount
    # stats
    # parts

 