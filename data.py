import csv
import os
import pandas as pd

class Data():

    def __init__(self):
        self.csv_paths = None
        self.all_data = None
        self.handle_csv()

    def handle_csv(self):

        path = 'db/sold_axies_data/axie_details/'
        files = os.listdir(path)
        paths = [ path + x for x in files]
        self.csv_paths = paths
        combined_data = []

        for p in paths:
            with open(p,'r') as f:
                reader = csv.reader(f)
                data = list(reader)
                for x in data:
                    combined_data.append(x)

        self.all_data = combined_data
        
        with open("db/sold_axies_data/axie_details/combined.csv", "w", newline="\n") as f:
            writer = csv.writer(f)
            writer.writerows(combined_data)

    # def popular_build(self):
        

if __name__ == "__main__":
    data = Data()
    print(data.csv_paths)
