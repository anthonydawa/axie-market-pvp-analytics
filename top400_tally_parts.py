import csv

def top400_tally():
    
    with open("db/top400_axie_details.csv", "r") as f:
        reader = csv.DictReader(f)
        axie_list = list(reader)
    
    
    for ax in axie_list:
        print(ax)



if __name__ == "__main__":
    top400_tally()


