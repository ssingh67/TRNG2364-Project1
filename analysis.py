import pandas as pd
import matplotlib.pyplot as plt

# Loading Datasets
results = pd.read_csv("datasets/results.csv", na_values=[r"\N"])
drivers = pd.read_csv("datasets/drivers.csv", na_values=[r"\N"])
races = pd.read_csv("datasets/races.csv")
constructors = pd.read_csv("datasets/constructors.csv")

results["points"] = pd.to_numeric(results["points"], errors="coerce")
races["year"] = pd.to_numeric(races["year"], errors="coerce")

# Total points per driver
driver_points = results.groupby("driverId")["points"].sum().reset_index()

# Merge with drivers table
driver_points = driver_points.merge(drivers, on = "driverId")

# Merged: results -> races (to get year) -> constructors (to get names)
merged = results.merge(races[["raceId", "year"]], on = "raceId", how = "left")
merged = merged.merge(constructors[["constructorId", "name"]], on = "constructorId", how = "left")

merged = merged.dropna(subset = ["year", "name", "points"])

# Aggregate constructor points per year
constructor_year_points = (merged.groupby(["year", "name"])["points"].sum().reset_index())

# Creat full name
driver_points["full_name"] = driver_points["forename"] + " " + driver_points["surname"]

# Sort for top 10
top10 = driver_points.sort_values("points", ascending = False).head(10)

# Top 3 Constructors
top_constructors = (constructor_year_points.groupby("name")["points"].sum().sort_values(ascending = False).head(3).index)

top_data = constructor_year_points[constructor_year_points["name"].isin(top_constructors)]

# Pivot
pivot = top_data.pivot(index = "year", columns = "name", values = "points").fillna(0).sort_index()


# Plot
plt.figure()
plt.barh(top10["full_name"], top10["points"])
plt.xlabel("Total Career Points")
plt.ylabel("Driver")
plt.title("Top 10 Drivers by Total Career Points")
plt.gca().invert_yaxis()
plt.tight_layout()

# ============================

# Ensure numeric types for correlation plot
results["grid"] = pd.to_numeric(results["grid"], errors="coerce")
results["position"] = pd.to_numeric(results["position"], errors="coerce")

corr_df = results.dropna(subset=["grid", "position"])


plt.figure(figsize=(8,6), facecolor="white")
plt.scatter(corr_df["grid"], corr_df["position"], alpha=0.3)
plt.xlabel("Starting Grid Position")
plt.ylabel("Final Race Position")
plt.title("Correlation: Grid Position vs Final Position")
plt.tight_layout()
plt.show()

correlation = corr_df["grid"].corr(corr_df["position"])
print("Correlation:", correlation)

# ============================

plt.figure(figsize=(10, 6), facecolor="white")
for col in pivot.columns:
    plt.plot(pivot.index, pivot[col], label=col)

plt.xlabel("Season (Year)")
plt.ylabel("Total Constructor Points")
plt.title("Constructor Points by Season (Top 3 Constructors)")
plt.legend()
plt.tight_layout()
plt.show()