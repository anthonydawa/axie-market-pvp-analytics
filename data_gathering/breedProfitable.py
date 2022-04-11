import csv

def breedProfitable():

    with open("db/profitable_breed.csv", "w") as f:
        pass

    with open('C:/Users/antho/Desktop/breed-bot/db/axie_tx_clean', 'r') as f:

        reader = csv.reader(f)
        data = list(reader)[1:]

        l = []

        for prices in data:
            for idx,d in enumerate(prices):
                if d:
                    if float(d) > 0:
                        if idx > 0:
                            newp = ','.join(prices)
                            rmp = newp.replace('.0','')
                            ff = rmp + ',' + str(idx) + '\n'
                            l.append(ff)

                    else: break

    with open("db/profitable_breed.csv", "a", newline="\n") as f:


        newl = ''.join(l)
        f.write(newl)

        print('files written')

    print('done finding breed profitable')

    with open('db/profitable_breed.csv', 'r') as f:

        reader = csv.reader(f)
        tbc = list(reader)[1:]

        srt = sorted(tbc, key = lambda x : int(x[-1]))

    with open('db/profitable_breed.csv', 'w',newline='\n') as f:
        f.write('id,1,2,3,4,5,6,7,time,price,times\n')
        writer = csv.writer(f)
        writer.writerows(srt)    

if __name__ == "__main__":  
    breedProfitable()



