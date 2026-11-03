import pandas as pd
import matplotlib.pyplot as plt

# Load sample dataset
df = pd.read_csv("sample_data.csv")

# Count platform usage
platform_counts = df["Platform"].value_counts()

# Display results
print("Social Media Platform Usage:")
print(platform_counts)

# Find the most commonly used platform
most_used = platform_counts.idxmax()

print("\nMost commonly used platform:", most_used)

# Create visualization
platform_counts.plot(kind="bar")

plt.title("Most Commonly Used Social Media Platforms")
plt.xlabel("Platform")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()