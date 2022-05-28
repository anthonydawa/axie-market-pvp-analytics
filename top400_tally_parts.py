import csv
import pandas as pd
import re
import matplotlib.pyplot as plt

def top400_tally():
    
    with open("db/sold_axies_data/axie_details/Apr-14-2022.csv", "r") as f:
        reader = csv.DictReader(f)
        axie_list = list(reader)
    for ax in axie_list:
        print(ax)

def dt():
    leaderboard_df = pd.read_csv("db/sold_axies_data/axie_details/Apr-28-2022.csv")
    leaderboard_df.columns = ['id','breedcount','purity','class','eyes','ears','mouth','horn','back','tail','time']
    # aqua_class_df = leaderboard_df.loc[leaderboard_df['class'] == 'Aquatic']
    return leaderboard_df


def visualize_build(df):

  top_builds = {}

  print(df[df["class"] == "Aquatic"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Beast"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Plant"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Bird"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Bug"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Reptile"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Dusk"]["Build"].value_counts()[10::-1])
  print(df[df["class"] == "Mech"]["Build"].value_counts()[10::-1])
  
  top_builds['aquatic'] = df[df["class"] == "Aquatic"]["Build"].value_counts().to_dict()
  top_builds['beast'] = df[df["class"] == "Beast"]["Build"].value_counts().to_dict()
  top_builds['plant'] = df[df["class"] == "Plant"]["Build"].value_counts().to_dict()
  top_builds['bird'] = df[df["class"] == "Bird"]["Build"].value_counts().to_dict()
  top_builds['bug'] = df[df["class"] == "Bug"]["Build"].value_counts().to_dict()
  top_builds['reptile'] = df[df["class"] == "Reptile"]["Build"].value_counts().to_dict()
  top_builds['dusk'] = df[df["class"] == "Dusk"]["Build"].value_counts().to_dict()
  top_builds['mech'] = df[df["class"] == "Mech"]["Build"].value_counts().to_dict()

  return top_builds

def generate_card_build(row):
  row["Build"] = row["back"] + "," + row["mouth"] + "," + row["horn"] + "," + row["tail"]
  return row

def card_build(df):
  df = df.apply(generate_card_build, axis=1)
  df = df.drop(["eyes", "ears", "back", "mouth", "horn", "tail"], axis=1)
  return df




if __name__ == "__main__":
    df_build = card_build(dt())
    visualize_build(df_build)




