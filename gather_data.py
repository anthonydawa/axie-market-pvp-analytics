

import time
from axie_detail_id import axie_detail_id
from agp_py import AxieGene
from helper_functions import breed_cost_floor, get_purity
from recent_sold import recent_sold

def gather_data():

    recent_sold_axies = recent_sold()['data']['settledAuctions']['axies']['results']

    for axie in recent_sold_axies:

        axie_details = {

            "id":"",
            "priceUsd":"",
            "eyes":"",
            "ears":"",
            "mouth":"",
            "horn":"",
            "back":"",
            "tail":"",
            "class":"",
            "breedCount":"",
            "purity":"",
            "transactionTime":""

        }
        
        axie_info = axie_detail_id(axie['id'])
        hex_gene = axie_info['data']['axie']['genes']
        gene = AxieGene(hex_gene,256)
        price_usd = axie['transferHistory']['results'][0]['withPriceUsd']

        axie_details['id'] = axie['id']    
        axie_details['breedCount'] = axie['breedCount']
        axie_details['purity'] = get_purity(axie_info)
        axie_details['class'] = axie['class']
        axie_details['eyes'] = gene.genes['eyes']['d']['partId']
        axie_details['ears'] = gene.genes['ears']['d']['partId']
        axie_details['mouth'] = gene.genes['mouth']['d']['partId']
        axie_details['horn'] = gene.genes['horn']['d']['partId']
        axie_details['back'] = gene.genes['back']['d']['partId']
        axie_details['tail'] = gene.genes['tail']['d']['partId']
        axie_details['transactionTime'] = axie['transferHistory']['results'][0]['timestamp']
        axie_details['priceUsd'] = axie['transferHistory']['results'][0]['withPriceUsd']

        
        floorDiff = [ str(int( round( float(price_usd) - x , 1) )) for x in breed_cost_floor()]
        strfloor = ",".join(floorDiff)



        with open('db/axie_details', 'a') as f:
            f.write(f"{axie_details['id']},{axie_details['breedCount']},{int(axie_details['purity'])},{axie_details['class']},{axie_details['eyes']},{axie_details['ears']},{axie_details['mouth']},{axie_details['horn']},{axie_details['back']},{axie_details['tail']},{axie_details['transactionTime']}\n")

        with open('db/axie_tx', 'a') as f:
            f.write(f"{axie_details['id']},{strfloor},{axie_details['transactionTime']},{ int(round(float(axie_details['priceUsd']),1))}\n")


def collect_sold_raw():

    recent_sold_axies = recent_sold()['data']['settledAuctions']['axies']['results']

    
    with open('recent_sold_raw.csv','a') as f:
        
        for axie in recent_sold_axies:
            csvformat = f'{axie["id"]},{axie["class"]},{axie["breedCount"]},{axie["transferHistory"]["results"][0]["timestamp"]},{axie["transferHistory"]["results"][0]["withPriceUsd"]}\n'
            f.writelines(csvformat)

    # to get id only
    # str(axie_details['id']) in [previous_data['id'] for previous_data in previous_data if 'id' in previous_data]
    



if __name__ == "__main__":
    collect_sold_raw()
