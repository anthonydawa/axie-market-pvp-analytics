#get top from db

import csv
import itertools
import time
import pickle
from group_card_parts import getPartType







def topParts(r):

    with open('db/parts_tally', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[:r]

        return data

def partsCombination():
    # get list of combination that are not 0 on data 
    
    with open('db/parts') as f:
        reader = csv.reader(f)
        data = list(reader)[0]
        # data = ['a','b','c','d','e']

    all_combinations = []


    combinations_object = itertools.combinations(data, 3)
    combinations_list = list(combinations_object)
    all_combinations += combinations_list

    print(all_combinations)  

def c():

    mouth = getPartType('mouth')
    tail = getPartType('tail')
    ears = getPartType('ears')
    eyes = getPartType('eyes')
    back = getPartType('back')
    horn = getPartType('horn')

    all_combinations = []

    mouthc = 0
    for a in mouth:
        for b in tail:
            for c in ears:
                for d in eyes:
                    for e in back:
                        for f in horn:
                            all_combinations.append([a,b,c,d,e,f])
        mouthc += 1
        print('mouth',mouthc)



    with open("all_combos.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        writer.writerows(all_combinations)

        

if __name__ == "__main__":  
    c()