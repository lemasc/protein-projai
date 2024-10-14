import pandas as pd
import random
import time

df = None
url = 'https://docs.google.com/spreadsheets/d/1_9AZb7hF7494ZyhKx-bTCcLHByKm0uXBq_pBInU1E84/export?gid=191160001&format=csv'
fetch_at = 0

def split_to_list(string):
  return [x.strip() for x in string.split(",")]

def get_df(use_cached = True):
    global df, fetch_at
    if use_cached and df is not None:
        return df
    df = pd.read_csv(url, converters={"ingredients": split_to_list})
    fetch_at = time.time()
    return df

def random_food():
    df = get_df()
    num_of_rows = df.shape[0]
    random_index = random.randint(0, num_of_rows - 1)
    data_at_index = df.iloc[random_index]
    return data_at_index.to_dict()