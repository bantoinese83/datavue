import pandas as pd

# Load the CSV file into a DataFrame to inspect its structure
df = pd.read_csv('/Users/doepesci/Desktop/DataVue/CSV/healthcare_data.csv')

# Print the first few rows to check the data
print(df.head())

# Check DataFrame info to understand data types
print(df.info())
