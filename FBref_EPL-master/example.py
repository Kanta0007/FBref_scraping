import pandas as pd

df = pd.read_csv("sample.csv")

df['new_column'] = [2, 4, 5]

df = df.append("sample.csv", index = False)

print(df)