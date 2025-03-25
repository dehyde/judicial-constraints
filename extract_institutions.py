import pandas as pd
import numpy as np

# Read V-Dem data (this might take some time as it's a large file)
print('Reading V-Dem data...')
vdem = pd.read_csv('V-Dem-CY-Full+Others-v15.csv', low_memory=False)

# Get the maximum year for each country
print('Processing data...')
# Let's focus on recent data - after 2000
vdem_recent = vdem[vdem['year'] >= 2000].copy()
latest_year = vdem_recent.groupby('country_name')['year'].max().reset_index()
vdem_latest = pd.merge(vdem_recent, latest_year, on=['country_name', 'year'])

# Select only the columns we need
selected_cols = [
    'country_name', 'year',
    'v2x_jucon', 'v2xlg_legcon', 'v2x_accountability',
    'v2juhcind', 'v2x_feduni'
]

# Create a new DataFrame with these columns
institutions_df = vdem_latest[selected_cols].copy()

# Rename columns to be more descriptive
institutions_df.rename(columns={
    'v2x_jucon': 'judicial_constraints',
    'v2xlg_legcon': 'legislative_constraints',
    'v2x_accountability': 'accountability_index',
    'v2juhcind': 'high_court_independence',
    'v2x_feduni': 'federalism_index'
}, inplace=True)

# Convert non-numeric values to NaN
numeric_cols = ['judicial_constraints', 'legislative_constraints', 'accountability_index', 
                'high_court_independence', 'federalism_index']
for col in numeric_cols:
    institutions_df[col] = pd.to_numeric(institutions_df[col], errors='coerce')

# Add a 'power_distribution_index' as an average of all mechanisms
institutions_df['power_distribution_index'] = institutions_df[numeric_cols].mean(axis=1)

# Fill NaN values with the mean of each column
for col in numeric_cols + ['power_distribution_index']:
    institutions_df[col] = institutions_df[col].fillna(institutions_df[col].mean())

# Sort by country name
institutions_df = institutions_df.sort_values('country_name')

# Save to CSV
print('Saving to file...')
institutions_df.to_csv('power_distribution_institutions.csv', index=False)
print('Done!') 