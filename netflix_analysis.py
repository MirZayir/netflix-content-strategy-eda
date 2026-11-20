import pandas as pd

# 1. Load dataset
df = pd.read_csv("netflix_titles.csv")

# 2. Handle missing values cleanly
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")
df = df.dropna(subset=["date_added", "duration"]).copy()

# 3. Parse dates & extract time features
df["date_added"] = pd.to_datetime(df["date_added"].str.strip())
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()

# 4. Separate primary country, primary genre & numeric duration
df["primary_country"] = df["country"].apply(lambda x: x.split(",")[0].strip())
df["primary_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0].strip())
df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(int)

# 5. Export cleaned dataset for Power BI & verification
df.to_csv("netflix_cleaned.csv", index=False)
print("Cleaned shape:", df.shape)
print("\nYear Added Range:", df["year_added"].min(), "to", df["year_added"].max())