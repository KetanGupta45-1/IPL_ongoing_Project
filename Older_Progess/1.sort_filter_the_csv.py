import pandas as pd

df = pd.read_csv("match_data_full.csv")


df['Date'] = pd.to_datetime(df['Date'])
df['Over'] = df['Over'].astype(float)
df['Innings'] = df['Innings'].astype(str)

df = df.sort_values(by=['Date', 'Innings', 'Over'], ascending=[False, True, True])

df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
df = df[(df["Date"].dt.year >= 2023) & (df["Date"].dt.year <= 2024)]

import ast
def extract_extras(extra_str):
    try:
        extras_dict = ast.literal_eval(extra_str)  # Convert string to dictionary
        return extras_dict.get("wides", 0) + extras_dict.get("noballs", 0) + extras_dict.get("legbyes", 0)
    except (ValueError, SyntaxError):
        return 0  

df["Extras"] = df["Extras"].apply(extract_extras)

df1 = df
df1.to_csv("matches_23-24.csv")