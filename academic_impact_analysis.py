import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("sample_data.csv")

# Count academic impact responses
impact_counts = df["Academic_Impact"].value_counts()

# Display results
print("Academic Impact Analysis:")
print(impact_counts)

# Create bar chart
impact_counts.plot(kind="bar")

plt.title("Reported Academic Impact of Social Media")
plt.xlabel("Academic Impact")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()