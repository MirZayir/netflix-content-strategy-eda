import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("netflix_cleaned.csv")

# --- 1. Print Key Portfolio Metrics ---
movies = df[df["type"] == "Movie"]
shows = df[df["type"] == "TV Show"]

print("=== NETFLIX CATALOG KPIs ===")
print(f"Total Titles: {len(df):,}")
print(f"Movies: {len(movies):,} ({len(movies)/len(df)*100:.1f}%) | TV Shows: {len(shows):,} ({len(shows)/len(df)*100:.1f}%)")
print(f"Peak Year Added: {df['year_added'].value_counts().idxmax()} ({df['year_added'].value_counts().max():,} titles)")
print(f"Median Movie Runtime: {movies['duration_num'].median():.0f} mins (Mean: {movies['duration_num'].mean():.1f} mins)")
print(f"Single-Season TV Shows: {(shows['duration_num'] == 1).mean()*100:.1f}%")
print("\nTop 5 Producing Countries:")
print(df[df["primary_country"] != "Unknown"]["primary_country"].value_counts().head(5))
print("\nTop 5 Primary Genres:")
print(df["primary_genre"].value_counts().head(5))

# --- 2. Build 4-Panel Executive Visual Summary ---
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("Netflix Content Strategy & Catalog Analysis (2008–2021)", fontsize=16, fontweight="bold", y=0.98)

# Chart 1: Content Added Over Time (Movies vs TV Shows)
yearly = df[df["year_added"] >= 2015].groupby(["year_added", "type"]).size().unstack(fill_value=0)
yearly.plot(kind="line", marker="o", linewidth=2.5, ax=axes[0, 0], color=["#E50914", "#221F1F"])
axes[0, 0].set_title("Annual Content Additions by Format (2015–2021)", fontweight="bold")
axes[0, 0].set_xlabel("Year Added")
axes[0, 0].set_ylabel("Titles Added")
axes[0, 0].legend(title="Format")

# Chart 2: Top 10 Producing Countries
top_countries = df[df["primary_country"] != "Unknown"]["primary_country"].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, ax=axes[0, 1], color="#E50914")
axes[0, 1].set_title("Top 10 Content-Producing Countries", fontweight="bold")
axes[0, 1].set_xlabel("Number of Titles")
axes[0, 1].set_ylabel("")

# Chart 3: Top 10 Primary Genres
top_genres = df["primary_genre"].value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, ax=axes[1, 0], color="#221F1F")
axes[1, 0].set_title("Top 10 Primary Genres", fontweight="bold")
axes[1, 0].set_xlabel("Number of Titles")
axes[1, 0].set_ylabel("")

# Chart 4: Maturity Rating Distribution
top_ratings = df["rating"].value_counts().head(8)
sns.barplot(x=top_ratings.index, y=top_ratings.values, ax=axes[1, 1], color="#B81D24")
axes[1, 1].set_title("Catalog Breakdown by Maturity Rating", fontweight="bold")
axes[1, 1].set_xlabel("Rating")
axes[1, 1].set_ylabel("Number of Titles")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("netflix_eda_summary.png", dpi=300)
print("\nSaved chart: netflix_eda_summary.png")