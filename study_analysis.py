import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load sample data
df = pd.read_csv("sample_data.csv")

# Calculate average study hours by usage group
df["Usage_Group"] = pd.cut(
    df["Daily_Usage_Hours"],
    bins=[0, 3, 5, 10],
    labels=["Low Usage", "Medium Usage", "High Usage"]
)

study = df.groupby(
    "Usage_Group", observed=False
)["Study_Hours"].mean()

print("Average Study Hours by Social Media Usage:")
print(study)

# Create graph
study.plot(kind="bar")

plt.title("Social Media Usage vs Study Hours")
plt.xlabel("Social Media Usage Group")
plt.ylabel("Average Study Hours")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()