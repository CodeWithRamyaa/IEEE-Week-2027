import pandas as pd
import matplotlib.pyplot as plt

# Load sample data
df = pd.read_csv("sample_data.csv")

# Calculate average usage for each platform
usage = df.groupby("Platform")["Daily_Usage_Hours"].mean()

# Display results
print("Average Daily Social Media Usage:")
print(usage)

# Create bar graph
usage.plot(kind="bar")

plt.title("Average Social Media Usage by Platform")
plt.xlabel("Social Media Platform")
plt.ylabel("Average Usage (Hours)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()