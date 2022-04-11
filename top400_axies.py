import csv

from axie_detail_id import axie_detail_id
from helper_functions import get_purity
from agp_py import AxieGene



def get_top400_axies():

    with open('leaderboards_axies.csv') as f:
        reader = csv.reader(f)
        data = list(reader)

        with open('db/top400_axie_details.csv', 'w') as f:
            f.write('id,eyes,ears,mouth,horn,back,tail,class,breedcount,speed\n')

        for axie in data:

            for ax in axie:

                try:
                    axie_details = {
                        "owner":"",
                        "id":"",
                        "eyes":"",
                        "ears":"",
                        "mouth":"",
                        "horn":"",
                        "back":"",
                        "tail":"",
                        "class":"",
                        "breedCount":"",
                        "speed":""

                    }

                    axie_info = axie_detail_id(ax)['data']['axie']
                    hex_gene = axie_info['genes']
                    gene = AxieGene(hex_gene,256)

                    axie_details['owner'] = axie_info['owner']
                    axie_details['id'] = ax    
                    axie_details['breedCount'] = str(axie_info['breedCount'])
                    axie_details['class'] = axie_info['class']
                    axie_details['eyes'] = gene.genes['eyes']['d']['partId']
                    axie_details['ears'] = gene.genes['ears']['d']['partId']
                    axie_details['mouth'] = gene.genes['mouth']['d']['partId']
                    axie_details['horn'] = gene.genes['horn']['d']['partId']
                    axie_details['back'] = gene.genes['back']['d']['partId']
                    axie_details['tail'] = gene.genes['tail']['d']['partId']
                    axie_details['speed'] = str(axie_info['stats']['speed'])

                    with open('db/top400_axie_details.csv', 'a') as f:

                        arr = list(axie_details.values())
                        strfy = ','.join(arr)
                        fstring = strfy + '\n'
                        f.writelines(fstring)
                        print(arr)
                except:
                    pass






if __name__ == "__main__":
    get_top400_axies()
