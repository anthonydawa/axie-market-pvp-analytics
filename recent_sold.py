import requests

def recent_sold():

    endpoint = "https://graphql-gateway.axieinfinity.com/graphql"


    GetRecentlyAxiesSold = {

    "operationName": "GetRecentlyAxiesSold",
    "variables": {
        "from": 0,
        "size": 20
    },
    "query": "query GetRecentlyAxiesSold($from: Int, $size: Int) {\n  settledAuctions {\n    axies(from: $from, size: $size) {\n      total\n      results {\n        ...AxieSettledBrief\n        transferHistory {\n          ...TransferHistoryInSettledAuction\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieSettledBrief on Axie {\n  id\n  name\n  image\n  class\n  breedCount\n  __typename\n}\n\nfragment TransferHistoryInSettledAuction on TransferRecords {\n  total\n  results {\n    ...TransferRecordInSettledAuction\n    __typename\n  }\n  __typename\n}\n\nfragment TransferRecordInSettledAuction on TransferRecord {\n  from\n  to\n  txHash\n  timestamp\n  withPrice\n  withPriceUsd\n  fromProfile {\n    name\n    __typename\n  }\n  toProfile {\n    name\n    __typename\n  }\n  __typename\n}\n"
    }

    request = requests.Session()
    response = request.post(endpoint,headers={'Content-Type': 'application/json'}, json = GetRecentlyAxiesSold)


    fetched_data = response.json()

    return fetched_data

## get id and price

if __name__ == "__main__":
    x = recent_sold()
    print(recent_sold())