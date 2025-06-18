import pandas as pd

# Load the Excel file
file_path = "C:/Users/01abh/Desktop/Projects/datasets/updated_match_data.xlsx"
df = pd.read_excel(file_path)

# Ensure required columns exist
required_columns = {'striker', 'venue', 'bowler', 'runs_off_bat', 'ball'}
if required_columns.issubset(df.columns):
    # Filter out strikers who have played less than 50 balls
    balls_faced = df.groupby('striker')['ball'].count()
    eligible_strikers = balls_faced[balls_faced >= 50].index
    df = df[df['striker'].isin(eligible_strikers)]
    
    # Calculate average runs scored by striker at each venue
    venue_avg = df.groupby(['striker', 'venue'])['runs_off_bat'].mean().reset_index()
    venue_avg = df.groupby(['striker', 'venue'])['runs_off_bat'].mean().reset_index()
    venue_avg.rename(columns={'runs_off_bat': 'avg_runs_venue'}, inplace=True)
    
    # Calculate average runs scored by striker against each bowler
    bowler_avg = df.groupby(['striker', 'bowler'])['runs_off_bat'].agg(['mean', 'sum']).reset_index()
    bowler_balls = df.groupby(['striker', 'bowler'])['ball'].count().reset_index()
    bowler_avg = pd.merge(bowler_avg, bowler_balls, on=['striker', 'bowler'], how='left')
    bowler_avg.rename(columns={'mean': 'avg_runs_bowler', 'sum': 'total_runs_bowler', 'ball': 'total_balls_faced'}, inplace=True)
    bowler_avg.rename(columns={'mean': 'avg_runs_bowler', 'sum': 'total_runs_bowler'}, inplace=True)
    
    # Compute player-wise correlation (striker-level correlation)
    bowler_correlation = df.groupby(['striker', 'bowler'])[['runs_off_bat', 'ball']].corr().iloc[0::2, -1].reset_index()
    bowler_correlation = bowler_correlation.rename(columns={bowler_correlation.columns[-1]: 'bowler_correlation'})[['striker', 'bowler', 'bowler_correlation']]
    venue_correlation = df.groupby(['striker', 'venue'])[['runs_off_bat', 'ball']].corr().iloc[0::2, -1].reset_index()
    venue_correlation = venue_correlation.rename(columns={venue_correlation.columns[-1]: 'venue_correlation'})[['striker', 'venue', 'venue_correlation']]
    
    # Compute venue-wise correlation
    venue_correlation = df.groupby(['striker', 'venue'])[['runs_off_bat', 'ball']].corr().iloc[0::2, -1].reset_index()
    venue_correlation = venue_correlation.rename(columns={venue_correlation.columns[-1]: 'venue_correlation'})[['striker', 'venue', 'venue_correlation']]
    venue_correlation.rename(columns={'runs_off_bat': 'venue_correlation'}, inplace=True)
    
    # Merge correlations with the respective dataframes
    venue_avg = pd.merge(venue_avg, venue_correlation, on=['striker', 'venue'], how='left')
    bowler_avg = pd.merge(bowler_avg, bowler_correlation, on=['striker', 'bowler'], how='left')
    
    # Save venue relation data
    venue_file = "C:/Users/01abh/Desktop/Projects/datasets/analysis/venue_relation.xlsx"
    venue_avg[['striker', 'venue', 'avg_runs_venue', 'venue_correlation']].to_excel(venue_file, index=False)
    
    # Save bowler relation data
    bowler_file = "C:/Users/01abh/Desktop/Projects/datasets/analysis/baller_relation.xlsx"
    bowler_avg[['striker', 'bowler', 'avg_runs_bowler', 'total_runs_bowler', 'total_balls_faced', 'bowler_correlation']].to_excel(bowler_file, index=False)
    
    print(f"Venue relation data saved as {venue_file}")
    print(f"Bowler relation data saved as {bowler_file}")
else:
    print("Required columns are missing from the dataset.")
