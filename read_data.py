import pandas as pd

# Read the CSV file
df = pd.read_csv("sample_data.csv")

# Display the dataset
print("SOCIAL MEDIA USAGE DATA")
print(df)

# Display basic information
print("\nDataset Information:")
print(df.info())

# Display statistical summary
print("\nStatistical Summary:")
print(df.describe())