from time import time
import requests
from agp_py import AxieGene







def constructQuery():
    query = "query GetAxieBriefList($criteria: AxieSearchCriteria) { "
    for i in range(30):
        query += f'ax{i}: axies(auctionType: Sale, sort: PriceAsc, criteria: $criteria, from: {i * 100}, size: 100) '
        query += "{ results { id genes auction { currentPrice } } }\n"
    query += " }"
    return query


def percent_purity(purity,ignoreEyesEars):

    if ignoreEyesEars:

        return ((purity['mouth'] + purity['horn'] + purity['back'] + purity['tail']) / 4 ) * 2

    elif not ignoreEyesEars:

        return ((purity['eyes'] + purity['ears']+ purity['mouth'] + purity['horn'] + purity['back'] + purity['tail']) / 6 ) * 2
        


def get_part_purity(genes,ignore_eyes_ears,build):

    purity = {
        "eyes": 0,
        "ears": 0,
        "horn": 0,
        "mouth": 0,
        "back": 0,
        "tail": 0,
    }

    if ignore_eyes_ears:

        if genes.genes['tail']['d']['partId'] in build:
            purity['tail'] += 37.5
        if genes.genes['mouth']['d']['partId'] in build:
            purity['mouth'] += 37.5
        if genes.genes['horn']['d']['partId'] in build:
            purity['horn'] += 37.5
        if genes.genes['back']['d']['partId'] in build:
            purity['back'] += 37.5


        if genes.genes['tail']['r1']['partId'] in build:
            purity['tail'] += 9.375
        if genes.genes['mouth']['r1']['partId'] in build:
            purity['mouth'] += 9.375
        if genes.genes['horn']['r1']['partId'] in build:
            purity['horn'] += 9.375
        if genes.genes['back']['r1']['partId'] in build:
            purity['back'] += 9.375

        if genes.genes['tail']['r2']['partId'] in build:
            purity['tail'] += 3.125
        if genes.genes['mouth']['r2']['partId'] in build:
            purity['mouth'] += 3.125
        if genes.genes['horn']['r2']['partId'] in build:
            purity['horn'] += 3.125
        if genes.genes['back']['r2']['partId'] in build:            
            purity['back'] += 3.125


    elif not ignore_eyes_ears:

        if genes.genes['eyes']['d']['partId'] in build:
            purity['eyes'] += 37.5
        if genes.genes['ears']['d']['partId'] in build:
            purity['ears'] += 37.5
        if genes.genes['tail']['d']['partId'] in build:
            purity['tail'] += 37.5
        if genes.genes['mouth']['d']['partId'] in build:
            purity['mouth'] += 37.5
        if genes.genes['horn']['d']['partId'] in build:
            purity['horn'] += 37.5
        if genes.genes['back']['d']['partId'] in build:
            purity['back'] += 37.5
        
        if genes.genes['eyes']['r1']['partId'] in build:
            purity['eyes'] += 9.375
        if genes.genes['ears']['r1']['partId'] in build:
            purity['ears'] += 9.375
        if genes.genes['tail']['r1']['partId'] in build:
            purity['tail'] += 9.375
        if genes.genes['mouth']['r1']['partId'] in build:
            purity['mouth'] += 9.375
        if genes.genes['horn']['r1']['partId'] in build:
            purity['horn'] += 9.375
        if genes.genes['back']['r1']['partId'] in build:
            purity['back'] += 9.375

        if genes.genes['eyes']['r2']['partId'] in build:
            purity['eyes'] += 3.125
        if genes.genes['ears']['r2']['partId'] in build:
            purity['ears'] += 3.125
        if genes.genes['tail']['r2']['partId'] in build:
            purity['tail'] += 3.125
        if genes.genes['mouth']['r2']['partId'] in build:
            purity['mouth'] += 3.125
        if genes.genes['horn']['r2']['partId'] in build:
            purity['horn'] += 3.125
        if genes.genes['back']['r2']['partId'] in build:            
            purity['back'] += 3.125

    return purity

def fix_args(arg):
    if arg == []:
        return ""
    else: 
        return arg

def marketplace_query(parts=[],classes=[],breedCount=[0,1,2,3,4,5,6,7],pureness=[1,2,3,4,5,6],ignoreEyesEars=False,morale=[27,61],hp=[27,61],skill=[27,61],speed=[27,61]):
    
    if parts == []:
        parts = []

    if classes == []:
        classes = ["Aquatic","Reptile","Beast","Mech","Dusk","Dawn","Plant","Bug","Bird"]

    if breedCount == []:
        breedCount=[0,1,2,3,4,5,6,7]

    elif breedCount != []:
        format_bc = []
        bc = breedCount[0]
        for x in range(bc):
            format_bc.append(x)
        format_bc.append(format_bc[-1] + 1)
        breedCount = format_bc



    if pureness == []:
        pureness=[1,2,3,4,5,6]
    elif pureness != []:
        format_pr = []
        pr = pureness[0]
        for x in range(pr):
            format_pr.append(x)
        format_pr.append(format_pr[-1] + 1)
        pureness = format_pr


    if ignoreEyesEars == []:
        ignoreEyesEars=False

    if morale == []:
        morale=[27,61]

    if hp == []:
        hp=[27,61]

    if skill == []:
        skill=[27,61]

    if speed == []:
        speed=[27,61]

    
    parts = fix_args(parts)
    classes = fix_args(classes)
    breedCount = fix_args(breedCount)
    pureness = fix_args(pureness)
    ignoreEyesEars = fix_args(ignoreEyesEars)
    morale = fix_args(morale)
    hp = fix_args(hp)
    skill = fix_args(skill)
    speed = fix_args(speed)

    endpoint = "https://axieinfinity.com/graphql-server-v2/graphql"


    body = {
        "operationName": "GetAxieBriefList",
        "variables": {"criteria": {"classes": classes, "breedCount": breedCount, "pureness": pureness, "parts": parts, "morale":morale, "hp":hp, "skill":skill, "speed":speed}},
        "query": constructQuery()
    }
    
    request = requests.Session()
    response = request.post(endpoint,headers={'Content-Type': 'application/json'}, json = body)
    
    if 200 <= response.status_code <= 299:

        fetched_data = response.json()

        filtered_axie = []
        
        for i in range(30):

            f = f'ax{i}'

            for axie in fetched_data['data'][f]['results']:

                axie_genes = axie['genes']
                hex_string = axie_genes

                try:

                    gene = AxieGene(hex_string,256)

                    str_price = float(axie['auction']['currentPrice'][:-14]) / 10000
                    
                    axie_stats = {
                        "purity" : get_part_purity(gene,ignoreEyesEars,parts),
                        "percent_purity" : percent_purity(get_part_purity(gene,True,parts),True),
                        "id" : axie['id'] ,
                        "price" : str_price,
                        "gene" : gene.genes
                    }       

                    filtered_axie.append(axie_stats)   

                    
                except Exception as e:
                    print("error parsing", axie['id'], e)
        
        return filtered_axie






