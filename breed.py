from helper_functions import breed_cost_floor

from binance.client import Client
import credentials
client = Client(credentials.API_KEY,credentials.SECRET_KEY)
ETH_PRICE = float(client.get_recent_trades(symbol='ETHUSDT')[0]['price'])



class Breed:

    def __init__(self):

        self.axie_count = 0
        self.balance = 0
        self.axie_cost = 0
        self.parents = []

    def init_parents(self):
        pass 

    def find_breedable(self):
        pass

    def find_pair(self):
        pass

    def breed_loop(self,fp,p1_cost,p2_cost):

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
        # sold_children_price = (fp * best_time - (fp * best_time) * 0.05)
        breeding_expense = total_breed_cost * best_time
        # profit = sold_children_price + sold_parent_price - total_parent_cost - breeding_expense
        next_round = sold_parent_price - total_parent_cost - breeding_expense
        self.balance += next_round
        self.axie_count += best_time
        self.axie_cost = abs(self.balance) / self.axie_count


breed = Breed()
breed.breed_loop(100,120,130)
print(breed.axie_count)
print(breed.balance)
print(breed.axie_cost)
breed.breed_loop(120,130,140)
print(breed.axie_count)
print(breed.balance)
print(breed.axie_cost)







# next_round = sold_parent_price - total_parent_cost - breeding_expense
# print(next_round)
# print('cost of childrens', next_round / 3)
# round2 = 


# print(profitable_times,'profitable_times')
# print(best_breed_times,'best_breed_times')
# print(best_time,'best time')
# print(sold_children_price,'sold_children_price')
# print(sold_parent_price,'sold_parent_price')
# print(total_parent_cost,'total_parent_cost')
# print(breeding_expense,'breeding_expense')
# print(next_round,'next_round')
# print(existing_axie_cost,'existing_axie_cost each')
# print(fp,' fp')
# print(profit,' profit')
