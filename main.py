from gather_data import gather_data



if __name__ == "__main__":
    ##creating transfer history


    for i in range(0,100):
        while True:
            try:
                # do stuff
                gather_data()
            except:
                continue
            break