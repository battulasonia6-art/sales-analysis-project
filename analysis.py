import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("SuperMarket_Analysis.csv")

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- CHECKING MISSING VALUES ---")
print(df.isnull().sum())

# -------------------------------
# DATA CLEANING
# -------------------------------

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'])

# Create new columns
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Create Revenue column
df['Revenue'] = df['Unit price'] * df['Quantity']

print("\n--- CLEANED DATA SAMPLE ---")
print(df.head())

# Save cleaned data
df.to_csv("cleaned_data.csv", index=False)

print("\n✅ Cleaned data saved as cleaned_data.csv")

# -------------------------------
# ANALYSIS
# -------------------------------

# Top Products
top_products = df.groupby('Product line')['Revenue'].sum().sort_values(ascending=False)

print("\n--- TOP PRODUCTS ---")
print(top_products)

# Monthly Sales
monthly_sales = df.groupby('Month')['Revenue'].sum()

print("\n--- MONTHLY SALES ---")
print(monthly_sales)

# City Sales
city_sales = df.groupby('City')['Revenue'].sum().sort_values(ascending=False)

print("\n--- CITY SALES ---")
print(city_sales)

# -------------------------------
# SAVE GRAPHS (IMPORTANT)
# -------------------------------

# Top Products Graph
plt.figure()
top_products.plot(kind='bar', title='Top Product Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_products.png")

# Monthly Sales Graph
plt.figure()
monthly_sales.plot(kind='line', title='Monthly Sales Trend')
plt.tight_layout()
plt.savefig("monthly_sales.png")

# City Sales Graph
plt.figure()
city_sales.plot(kind='bar', title='Sales by City')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("city_sales.png")

print("\n✅ Graphs saved successfully!")