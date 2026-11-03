import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("sample_data.csv")

# Count usage purposes
purpose_counts = df["Main_Purpose"].value_counts()

# Display results
print("Social Media Usage by Purpose:")
print(purpose_counts)

# Create pie chart
plt.figure(figsize=(7, 7))

plt.pie(
    purpose_counts,
    labels=purpose_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Purpose of Social Media Usage")
plt.tight_layout()
plt.show()