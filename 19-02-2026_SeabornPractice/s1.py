import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Manually Generate Data
# Line/Scatter data
x_days = [1, 2, 3, 4, 5, 6, 7]
y_revenue = [150, 200, 180, 300, 250, 400, 380]

# Category data
regions = ['North', 'South', 'East', 'West']
sales = [4500, 5200, 3900, 6100]

# Distribution/Outlier data
# Normal distribution with some high outliers at the end
performance_scores = [65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 120, 130]

# 2. Create DataFrames
df_line = pd.DataFrame({"Day": x_days, "Revenue": y_revenue})
df_bar = pd.DataFrame({"Region": regions, "Sales": sales})
df_dist = pd.DataFrame({"Scores": performance_scores})

# 3. Setup the Visual Dashboard (2 Rows, 2 Columns)
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Seaborn Practice', fontsize=20)

# Plot 1: Line Plot (Trends)
sns.lineplot(ax=axes[0, 0], x="Day", y="Revenue", data=df_line, marker="o", color="blue")
axes[0, 0].set_title("Daily Revenue Trend")

# Plot 2: Bar Plot (Comparisons)
sns.barplot(
    ax=axes[0, 1],
    x="Region",
    y="Sales",
    data=df_bar,
    palette="viridis",
    hue="Region",
    legend=False
)
axes[0, 1].set_title("Regional Sales Comparison")

#Plot 3: Histogram (Frequency)
sns.histplot(ax=axes[1, 0], data=df_dist, x="Scores", kde=True, color="orange")
axes[1, 0].set_title("Performance Score Distribution")

# Plot 4: Box Plot (Outlier Detection)
sns.boxplot(ax=axes[1, 1], y="Scores", data=df_dist, color="lightgreen")
axes[1, 1].set_title("Outlier Identification")

# 4. Final Formatting
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
plt.show()