# find if there are suitable parents 

import csv
from binance.client import Client
from regex import P

from axie_detail_id import axie_detail_id
import credentials
from group_card_parts import getClassEyeEars, getClassParts
client = Client(credentials.API_KEY,credentials.SECRET_KEY)
from filter import marketplace_query
from helper_functions import breed_cost_floor




def pair_metrics(p1,p2,ignoreEyesEars=True):

    passed = {
        "ignoreEyesEars":ignoreEyesEars,
        "eyes":True,
        "ears":True,
        "mouth":True,
        "horn":True,
        "back":True,
        "tail":True,
    }


    if ignoreEyesEars:

        if p1['horn'] + p2['horn'] <= 90:
            passed['horn'] = False
        if p1['mouth'] + p2['mouth'] <= 90:
            passed['mouth'] = False
        if p1['back'] + p2['back'] <= 90:
            passed['back'] = False
        if p1['tail'] + p2['tail'] <= 90:
            passed['tail'] = False

        if False in list(passed.values())[3:]:
            return False
        else:
            return True


    if not ignoreEyesEars: 

        if p1['mouth'] + p2['mouth'] <= 90:
            passed['mouth'] = False
        if p1['horn'] + p2['horn'] <= 90:
            passed['horn'] = False
        if p1['back'] + p2['back'] <= 90:
            passed['back'] = False
        if p1['tail'] + p2['tail'] <= 90:
            passed['tail'] = False
        if p1['eyes'] + p2['eyes'] <= 90:
            passed['eyes'] = False
        if p1['ears'] + p2['ears'] <= 90:
            passed['ears'] = False

        if False in list(passed.values())[1:]:
            return False
        else:
            return True




def purity_metrics(dpart,ignoreEyesEars=True):
    
    passed = {
        "ignoreEyesEars":ignoreEyesEars,
        "eyes":True,
        "ears":True,
        "mouth":True,
        "horn":True,
        "back":True,
        "tail":True,
    }

    MIN_PART_PURITY = 40.625

    if ignoreEyesEars: 

        if dpart['mouth'] <= MIN_PART_PURITY:
            passed['mouth'] = False
        if dpart['horn'] <= MIN_PART_PURITY:
            passed['horn'] = False
        if dpart['back'] <= MIN_PART_PURITY:
            passed['back'] = False
        if dpart['tail'] <= MIN_PART_PURITY:
            passed['tail'] = False

        if False in list(passed.values())[3:]:
            return False
        else:
            return True

    if not ignoreEyesEars: 
        
        if dpart['eyes'] <= MIN_PART_PURITY:
            passed['eyes'] = False
        if dpart['ears'] <= MIN_PART_PURITY:
            passed['ears'] = False
        if dpart['mouth'] <= MIN_PART_PURITY:
            passed['mouth'] = False
        if dpart['horn'] <= MIN_PART_PURITY:
            passed['horn'] = False
        if dpart['back'] <= MIN_PART_PURITY:
            passed['back'] = False
        if dpart['tail'] <= MIN_PART_PURITY:
            passed['tail'] = False

        if False in list(passed.values())[1:]:
            return False
        else:
            return True



 
def build(mpq,ignoreEyesEars=True):

    parents = {}
    
    for axie in mpq:

        if 'sire' not in parents:

            ps = axie['purity']
            
            if purity_metrics(ps,ignoreEyesEars):
                parents['sire'] = axie


        elif 'sire' in parents and 'matron' not in parents:
            
            p1 = parents['sire']['purity']
            p2 = axie['purity']

            
            if purity_metrics(p2,ignoreEyesEars):
                if pair_metrics(p1,p2,ignoreEyesEars):
                    parents['matron'] = axie
                    break

    return parents

def total_breed_profit(p1,p2,fp,times):

    p1_cost = float(p1['price']) * float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
    p2_cost = float(p2['price']) * float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
    total_parent_cost = p1_cost + p2_cost
    total_breed_cost = breed_cost_floor()[times - 1]
    profitable_times = []

    for idx,bc in enumerate(breed_cost_floor(),1):

        costing = fp - bc

        if costing > 0:
            profitable_times.append(costing)
        else: break

    best_breed_times = []

    for idx,t in enumerate(profitable_times,1):
        best_breed_times.append(idx*t)
        
    sold_parent_price =  (p1_cost + p2_cost) - ((p1_cost + p2_cost) * 0.05)
    profit = (fp * times - (fp * times) * 0.05 ) + sold_parent_price - total_parent_cost - (total_breed_cost * times) 

    return profit

#find best times for given pairs
def find_best_times(sire,matron,floor_p):

    profit_list = []

    for times in range(1,8):

        profit_list.append(total_breed_profit(sire,matron,floor_p,times))
        
    profit = {}
    for idx,p in enumerate(profit_list):
        if p <= 0:
            profit['times'] = idx
            profit['amt'] = p
            return profit



#find profitable on csv profitable_breed.csv
def find_profitable_csv(price_range=[0,1_000_000],breed_range=[1,7]):
    with open('db/profitable_breed.csv','r') as f:

        reader = csv.DictReader(f)
        passed = []

        for row in reader:
     
            if price_range[0] <= float(row['price']) <= price_range[1]:
                if breed_range[0] <= int(row['times']) <= breed_range[1]:
                    passed.append(row)
        #list of dict
        return passed

#returns query details for searching 
def axie_parts_id(id,ignoreEyesEars=True,breed=True):
    
    axie_queries = {}
    axs = axie_detail_id(id)

    if ignoreEyesEars:
        
        parts = [
            axs['data']['axie']['parts'][2]['id'],
            axs['data']['axie']['parts'][3]['id'],
            axs['data']['axie']['parts'][4]['id'],
            axs['data']['axie']['parts'][5]['id'],
            ]

    elif not ignoreEyesEars:

        parts = [
            axs['data']['axie']['parts'][0]['id'],
            axs['data']['axie']['parts'][1]['id'],
            axs['data']['axie']['parts'][2]['id'],
            axs['data']['axie']['parts'][3]['id'],
            axs['data']['axie']['parts'][4]['id'],
            axs['data']['axie']['parts'][5]['id'],
            ]


    classes = [axs['data']['axie']['class']]
    speed = [axs['data']['axie']['stats']['speed'],61]
    breedCount = []

    if not breed:

        bc = int(axs['data']['axie']['breedCount'])

        for x in range(bc):
            breedCount.append(x)
        if bc != 0:
            breedCount.append(breedCount[-1] + 1)

    elif breed:
        breedCount.append(0)



    axie_queries['parts'] = parts
    axie_queries['classes'] = classes
    axie_queries['speed'] = speed
    axie_queries['breedCount'] = breedCount

    return axie_queries


if __name__ == "__main__" : 
    # parts = ['horn-anemone','back-anemone','mouth-goda','tail-nimo']
    # breedCount = [0]
    # eth_trades = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
    # floor_price = marketplace_query(parts=parts,breedCount=breedCount)[0]['price'] * eth_trades
    # find_best_times(result['sire'],result['matron'],floor_price)
    # profitables = find_profitable_csv([100,200],[1,3])
    # p_list = [x['id'] for x in profitables]
    axie = axie_parts_id(7015190,True)
    # print([axie_parts_id(x) for x in p_list])
    lcase = [x.lower() for x in axie['classes']]
    addPartByClass = getClassEyeEars(getClassParts(lcase))
    withClassEyesEars = axie['parts'] + addPartByClass
    x = build(marketplace_query(withClassEyesEars,classes=axie['classes'],speed=axie['speed'],breedCount=[0]),False)
    print(x)


