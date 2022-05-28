# find if there are suitable parents 

import csv
import random
import time
from binance.client import Client
from agp_py import AxieGene

from axie_detail_id import axie_detail_id
import credentials
from group_card_parts import getClassEyeEars, getClassParts
client = Client(credentials.API_KEY,credentials.SECRET_KEY)
from filter import get_part_purity, marketplace_query, percent_purity
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

        if p1['horn'] + p2['horn'] < 90:
            passed['horn'] = False
        if p1['mouth'] + p2['mouth'] < 90:
            passed['mouth'] = False
        if p1['back'] + p2['back'] < 90:
            passed['back'] = False
        if p1['tail'] + p2['tail'] < 90:
            passed['tail'] = False

        if False in list(passed.values())[3:]:
            return False
        else:
            return True


    if not ignoreEyesEars: 

        if p1['mouth'] + p2['mouth'] < 90:
            passed['mouth'] = False
        if p1['horn'] + p2['horn'] < 90:
            passed['horn'] = False
        if p1['back'] + p2['back'] < 90:
            passed['back'] = False
        if p1['tail'] + p2['tail'] < 90:
            passed['tail'] = False
        if p1['eyes'] + p2['eyes'] < 90:
            passed['eyes'] = False
        if p1['ears'] + p2['ears'] < 90:
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

        if dpart['mouth'] < MIN_PART_PURITY:
            passed['mouth'] = False
        if dpart['horn'] < MIN_PART_PURITY:
            passed['horn'] = False
        if dpart['back'] < MIN_PART_PURITY:
            passed['back'] = False
        if dpart['tail'] < MIN_PART_PURITY:
            passed['tail'] = False

        if False in list(passed.values())[3:]:
            return False
        else:
            return True

    if not ignoreEyesEars: 
        
        if dpart['eyes'] < MIN_PART_PURITY:
            passed['eyes'] = False
        if dpart['ears'] < MIN_PART_PURITY:
            passed['ears'] = False
        if dpart['mouth'] < MIN_PART_PURITY:
            passed['mouth'] = False
        if dpart['horn'] < MIN_PART_PURITY:
            passed['horn'] = False
        if dpart['back'] < MIN_PART_PURITY:
            passed['back'] = False
        if dpart['tail'] < MIN_PART_PURITY:
            passed['tail'] = False

        if False in list(passed.values())[1:]:
            return False
        else:
            return True

def find_listing_price(id,ignoreEyesEars):

    if ignoreEyesEars:
        price = marketplace_query()
    elif not ignoreEyesEars:
        price = marketplace_query()

    return price


def build_sire(sire_id,sire_cost_usd,ignoreEyesEars=True):

    sire = axie_detail_id(sire_id)

    axie = sire['data']['axie']
    axie_genes = axie['genes']
    hex_string = axie_genes

    gene = AxieGene(hex_string,256)

    if ignoreEyesEars:
        parts = [ x['id'] for x in axie['parts'][2:]]
    elif not ignoreEyesEars:
        parts = [ x['id'] for x in axie['parts']]

    

    if sire_cost_usd:

        axie_stats = {
        "purity" : get_part_purity(gene,ignoreEyesEars,parts),
        "percent_purity" : percent_purity(get_part_purity(gene,ignoreEyesEars,parts),ignoreEyesEars),
        "id" : axie['id'] ,
        "price" : sire_cost_usd,
        "gene" : gene.genes
        }     

    elif not sire_cost_usd:

        axie_stats = {
        "purity" : get_part_purity(gene,ignoreEyesEars,parts),
        "percent_purity" : percent_purity(get_part_purity(gene,ignoreEyesEars,parts),ignoreEyesEars),
        "id" : axie['id'] ,
        "price" : axie['auction']['currentPriceUSD'],
        "gene" : gene.genes
        }   


    eyes = axie_stats['gene']['eyes']['d']['partId']
    ears = axie_stats['gene']['ears']['d']['partId']
    mouth = axie_stats['gene']['mouth']['d']['partId']
    horn = axie_stats['gene']['horn']['d']['partId']
    back = axie_stats['gene']['back']['d']['partId']
    tail = axie_stats['gene']['tail']['d']['partId']
    cls = axie_stats['gene']['cls']
    speed = axie_stats['stats']['speed']
    
    if ignoreEyesEars:
        build(marketplace_query(parts=[mouth,horn,back,tail],classes=[cls],speed=[speed,61]),axie_stats)
    elif not ignoreEyesEars:
        build(marketplace_query(parts=[eyes,ears,mouth,horn,back,tail],classes=[cls]),axie_stats)

    return axie_stats


def build(mpq,sire=None,ignoreEyesEars=True):
    parents = {}

    if sire:
        parents['sire'] = sire

    for axie in mpq:

        if 'sire' not in parents:

            ps = axie['purity']
            
            if purity_metrics(ps,ignoreEyesEars):
                parents['sire'] = axie
                print('found sire')


        elif 'sire' in parents and 'matron' not in parents:
            
            p1 = parents['sire']['purity']
            p2 = axie['purity']

            if purity_metrics(p2,ignoreEyesEars):
                if pair_metrics(p1,p2,ignoreEyesEars):
                    parents['matron'] = axie
                    print('found matron')
                    break

    if 'sire' in parents and 'matron' not in parents:
        parents['matron'] = {"price":0,"id":0}
        print('found sire no matron')
        return parents

    elif 'sire' not in parents and 'matron' not in parents:
        print('found no sire no matron')
        return {}
    
    elif 'sire' in parents and 'matron' in parents:
        print('found sire and matron')
        return parents





def total_breed_profit(p1,p2,fp):

    if p1['price'] and p2['price']:

        ETH_PRICE = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
        p1_cost = float(p1['price']) * ETH_PRICE
        p2_cost = float(p2['price']) * ETH_PRICE
        total_parent_cost = p1_cost + p2_cost

        profitable_times = []

        for idx,bc in enumerate(breed_cost_floor(),1):

            costing = fp - bc

            if costing > 0:
                profitable_times.append(costing)
            else: break

        best_breed_times = []

        for idx,t in enumerate(profitable_times,1):
            best_breed_times.append(idx*t)

        best_time = best_breed_times.index(max(best_breed_times)) + 1
        total_breed_cost = breed_cost_floor()[best_time - 1]

        sold_parent_price =  (fp + fp) - ((fp + fp) * 0.05)
        sold_children_price = (fp * best_time - (fp * best_time) * 0.05)
        breeding_expense = total_breed_cost * best_time
        profit = sold_children_price + sold_parent_price - total_parent_cost - breeding_expense
        tbc = sold_parent_price - total_parent_cost - breeding_expense
        existing_axie_cost = abs(tbc) / best_time
        # next_round = sold_parent_price - total_parent_cost - breeding_expense
        # print(next_round)
        # print('cost of childrens', next_round / 3)
        # round2 = 
        print(profitable_times,'profitable_times')
        print(best_breed_times,'best_breed_times')
        print(best_time,'best time')
        print(sold_children_price,'sold_children_price')
        print(sold_parent_price,'sold_parent_price')
        print(total_parent_cost,'total_parent_cost')
        print(breeding_expense,'breeding_expense')
        print(tbc,'tbc')
        print(existing_axie_cost,'existing_axie_cost each')
        print(fp,' fp')
        print(profit,' profit')



        


        return profit


    else:
        profit = 0
        return profit 

#find best times for given pairs
def find_best_times(sire,matron,floor_p):


    if floor_p:
        profit_list = []

        for times in range(1,8):

            profit_list.append(total_breed_profit(sire,matron,floor_p,times))


        profit = {}

        max_profit = max(profit_list) 
        idx = profit_list.index(max_profit)
        
        profit['times'] = idx
        profit['amt'] = max_profit
        return profit

    # for idx,p in enumerate(profit_list):
    #     if p <= 0:
    #         profit['times'] = idx
    #         profit['amt'] = p
    #         return profit_list



#find profitable on csv profitable_breed.csv
def find_profitable_csv(market,price_range=[0,1_000_000],breed_range=[1,7]):

    if market:

        csv_path = 'db/profitable_breed.csv'
        with open(csv_path,'r') as f:
            reader = csv.DictReader(f)
            passed = []

            for row in reader:
            
                if price_range[0] <= float(row['price']) <= price_range[1]:
                    if breed_range[0] <= int(row['times']) <= breed_range[1]:
                        passed.append(row)
                        
            return [ x['id'] for x in passed ]

    elif not market:  

        csv_path = 'db/top400_axie_details_clean.csv'
        with open(csv_path,'r') as f:
            reader = csv.DictReader(f)


            return [row['id'] for row in reader]







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


        # lcase = [x.lower() for x in [axs['data']['axie']['class']]]
        # addPartByClass = getClassEyeEars(getClassParts(lcase))
        # axie_queries['parts'] = parts + addPartByClass

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


# single query make
def execute(origin=False,market=False):  

    if not origin:

        profitable_id = find_profitable_csv(market=market,price_range=[50,1000])

        for axid in profitable_id:

            random_number = random.randint(12,13)
            print(f'sleeping {random_number}s')
            time.sleep(random_number)
            

            try:
                axie = axie_parts_id(axid,True)
                eth_trades = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])

                try:
                    floor_price = marketplace_query(parts=axie['parts'],classes=axie['classes'])[0]['price'] * eth_trades
                except:
                    floor_price = 0

         
                parents = build(marketplace_query(parts=axie['parts'],classes=axie['classes'],speed=axie['speed'],breedCount=[0]),True)

                if parents:
                    
                    result = find_best_times(parents['sire'],parents['matron'],floor_price)
                    str_parts = ','.join(axie['parts'])

                    with open('db/profitable_pairs.csv', 'a') as f:
                        f.write(f'{axid},{result["times"]},{int(result["amt"])},{axie["classes"][0]},{str_parts},{axie["speed"][0]},{parents["sire"]["id"]},{parents["matron"]["id"]},{int(floor_price)},{int(time.time())}\n')
            except:
                pass


    elif origin:

        profitable_id = find_profitable_csv(market=market,price_range=[50,1000])

        for axid in profitable_id:

            random_number = random.randint(12,13)
            print(f'sleeping {random_number}s')
            time.sleep(random_number)
            

            try:
                axie = axie_parts_id(axid,False)
                eth_trades = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
             
                try:
                    floor_price = marketplace_query(parts=axie['parts'],classes=axie['classes'],ignoreEyesEars=False)[0]['price'] * eth_trades
                except:
                    floor_price = 0

              
                parents = build(marketplace_query(parts=axie['parts'],classes=axie['classes'],breedCount=[0],ignoreEyesEars=False),False)

                if parents:
                    
                    result = find_best_times(parents['sire'],parents['matron'],floor_price)
                    str_parts = ','.join(axie['parts'])

                 
                    with open('db/profitable_pairs_origin.csv', 'a') as f:
                        f.write(f'{axid},{result["times"]},{int(result["amt"])},{axie["classes"][0]},{str_parts},{parents["sire"]["id"]},{parents["matron"]["id"]},{int(floor_price)},{int(time.time())}\n')
            except:
                pass

if __name__ == "__main__" : 

    # mysire = build_sire(11295336,True)
    # mouth = mysire['gene']['mouth']['d']['partId']
    # horn = mysire['gene']['horn']['d']['partId']
    # back = mysire['gene']['back']['d']['partId']
    # tail = mysire['gene']['tail']['d']['partId']
    # cls = mysire['gene']['cls']

    # print(mysire['gene']['cls'])

    # execute(origin=False,market=False)


    p1 =  185 / float(client.get_recent_trades(symbol='ETHUSDT')[0]['price']) 
    p2 = 157 / float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
    r1 = total_breed_profit({"price":p1},{"price":p2},100)
    # remove_child_sold = r1 - (fp + fp - ( (fp+fp)*0.05) )
    print(r1)

    # print(r1 + 216)


    # x = {0R
    #     "y":123123
    # }
    # y = {
    #     "xzz":0,
    #     "asdas":0
    # }


    # if x and y:
    #     print(x,y)


    # x = [1,2,3,4,5]
    # x.index(max(x))
    # profitables = find_profitable_csv([100,200],[1,3])
    # p_list = [x['id'] for x in profitables]
    # f_list = [axie_parts_id(x) for x in p_list]
    # axie = axie_parts_id(p_list[0],True)
    # lcase = [x.lower() for x in axie['classes']]
    # addPartByClass = getClassEyeEars(getClassParts(lcase))
    # withClassEyesEars = axie['parts'] + addPartByClass
    # eth_trades = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])
    # floor_price = marketplace_query(parts=withClassEyesEars,speed=axie['speed'])[0]['price'] * eth_trades
    # parents = build(marketplace_query(withClassEyesEars,classes=axie['classes'],speed=axie['speed'],breedCount=[0]),False)  
    # print(find_best_times(parents['sire'],parents['matron'],floor_price))

# {'eyes': 46.875, 'ears': 46.875, 'horn': 50.0, 'mouth': 50.0, 'back': 40.625, 'tail': 46.875}
# {'eyes': 46.875, 'ears': 40.625, 'horn': 40.625, 'mouth': 40.625, 'back': 40.625, 'tail': 46.875}