import time
from gather_data import collect_sold_raw, gather_data



if __name__ == "__main__":
    ##creating transfer history



    while True:
        try:
            # do stuff
            print('gathering')
            gather_data()
            time.sleep(0.5)
        except Exception as e: 
            print(e)
            continue
