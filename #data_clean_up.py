#data_clean_up
#data cleaning for voters & turnedout voters

import pandas as pd
import os

# Load the dataset, skipping the first row (header)
df = pd.read_csv('datasets/voters_turnedoutvotes.csv', skiprows=[0])

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Check for missing data
missing_data = df.isna().sum()

# Convert columns to appropriate data types
numeric_columns = df.columns[2:]  # Assuming columns from 1983 onwards are numeric
df[numeric_columns] = df[numeric_columns].replace({',': ''}, regex=True).astype(float)

# Create a year column
df['year'] = df.columns.str.extract(r'(\d{4})')  # Extract year as a string

# Handle missing values in the 'year' column by filling them with 0
df['year'] = df['year'].fillna('0')

# Convert "NA" strings to actual NaN values
df = df.replace('NA', pd.NA)

# Convert the 'year' column to integers
df['year'] = df['year'].astype(int)

# Calculate percentages or other derived metrics
df['voter_turnout_percent'] = df['voters'] / df['electors'] * 100

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_voters_turnedoutvotes.csv', index=False)