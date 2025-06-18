import pandas as pd

# Load the Excel file
file_path = "C:/Users/01abh/Desktop/Projects/datasets/match_data.xlsx"
df = pd.read_excel(file_path, sheet_name='Main')

# Ensure required columns exist
if {'match_id', 'innings', 'striker', 'runs_off_bat', 'extras'}.issubset(df.columns):
    # Calculate total runs for each row
    df['total_runs'] = df['runs_off_bat'] + df['extras']
    
    # Compute cumulative runs inning-wise per match
    df['cumulative_total_runs'] = df.groupby(['match_id', 'innings'])['total_runs'].cumsum()
    
    # Compute cumulative runs for each batsman per match
    df['striker_cumulative_runs'] = df.groupby(['match_id', 'striker'])['runs_off_bat'].cumsum()
    
    # Save the updated DataFrame back to an Excel file
    output_file = "C:/Users/01abh/Desktop/Projects/datasets/updated_match_data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Updated file saved as {output_file}")
else:
    print("Required columns are missing from the dataset.")