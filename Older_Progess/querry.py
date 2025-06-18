import pandas as pd

file_path = 'datasets/2023_match_data.xlsx'

df = pd.read_excel(file_path, sheet_name='Main')

grouped = df.groupby('striker')

for striker, group in grouped:
    safe_striker_name = "".join([c if c.isalnum() else "_" for c in striker])
    file_name = f'{safe_striker_name}.csv'
    
    group.to_csv(file_name, index=False)
    
    print(f'Saved {file_name} with {len(group)} rows')

print("All files have been saved.")