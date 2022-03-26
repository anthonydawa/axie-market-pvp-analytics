from re import X


from binance.client import Client
from axie_detail_id import axie_detail_id
import credentials
client = Client(credentials.API_KEY,credentials.SECRET_KEY)
from binance.enums import *

def usd_to_eth():
    pass
def eth_to_usd():
    pass
def build_axie_details(axie):
    pass
def get_unique_axie(axie_list):
    pass

def breed_cost_floor():

    slp_trades = float(client.get_recent_trades(symbol='SLPUSDT')[0]['price'])
    axs_trades = float(client.get_recent_trades(symbol='AXSUSDT')[0]['price'])
    slp_costs = [900,1350,2250,3600,5850,9450,15300]
    cumulative = []
    price = []
    avg = []

    for x,_ in enumerate(slp_costs):

        total = ((slp_costs[x] * slp_trades) * 2) + (axs_trades / 2 )
        price.append(total)
        cumulative.append(sum(price))
        avg.append( cumulative[-1]/(x+1) )
        
    return avg


def get_purity(axie):

    cls = axie['data']['axie']['class']
    card_cls = axie['data']['axie']['parts']
    p_score = 0

    for card in card_cls:
        if cls == card['class']:
            p_score += 100/6
    
    return p_score



if __name__ == "__main__":
    # axie_info = axie_detail_id(3013361)
    # get_purity(axie_info)
    print(breed_cost_floor())


