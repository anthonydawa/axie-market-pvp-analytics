import pandas as pd


def removeDupes():

    file_name = 'C:/Users/antho/Desktop/breed-bot/db/axie_details'
    file_name_output = 'C:/Users/antho/Desktop/breed-bot/db/axie_details_clean'

    df = pd.read_csv(file_name, sep=",")
    df.drop_duplicates(subset=None, inplace=True)
    df.to_csv(file_name_output, index=False,header=['id','breedCount','purityPercent','class','eyes','ears','mouth','horn','back','tail','c'])

    file_name2 = 'C:/Users/antho/Desktop/breed-bot/db/axie_tx'
    file_name_output2 = 'C:/Users/antho/Desktop/breed-bot/db/axie_tx_clean'

    df2 = pd.read_csv(file_name2, sep=",")
    df2.drop_duplicates(subset=None, inplace=True)
    df2.to_csv(file_name_output2, index=False, header=['id','1','2','3','4','5','6','7','time','price'])

    file_name3 = 'C:/Users/antho/Desktop/breed-bot/db/profitable_breed.csv'
    file_name_output3 = 'C:/Users/antho/Desktop/breed-bot/db/profitable_breed_clean.csv'

    df3 = pd.read_csv(file_name3, sep=",")
    df3.drop_duplicates(subset=None, inplace=True)
    df3.to_csv(file_name_output3, index=False, header=['id','1','2','3','4','5','6','7','time','price','times'])

    file_name4 = 'C:/Users/antho/Desktop/breed-bot/db/top400_axie_details.csv'
    file_name_output4 = 'C:/Users/antho/Desktop/breed-bot/db/top400_axie_details_clean.csv'

    df4 = pd.read_csv(file_name4, sep=",")
    df4.drop_duplicates(subset=None, inplace=True)
    df4.to_csv(file_name_output4, index=False, header=['address','id','eyes','ears','mouth','horn','back','tail','class','breedcount','speed'])

    print('removeDupes done')

if __name__ == "__main__":    
    removeDupes()