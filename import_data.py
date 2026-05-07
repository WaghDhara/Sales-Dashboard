import pandas as pd
from sqlalchemy import create_engine, text

print("Data Import Tool")

engine = create_engine("sqlite:///sales.db")

# Create table if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS imported_sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            region TEXT,
            sales_amount INTEGER,
            units INTEGER,
            import_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """))

# Sample data for import (you can later replace this with a real CSV file)
data = {
    "product": ["Keyboard", "Mouse", "Headset", "Laptop", "Monitor"],
    "region": ["North", "South", "East", "West", "North"],
    "sales_amount": [1200, 800, 1500, 42000, 18000],
    "units": [50, 120, 30, 12, 25]
}
df = pd.DataFrame(data)

# Simple cleaning
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce").fillna(0)

# Load into database
df.to_sql("imported_sales", engine, if_exists="append", index=False)
print(f"✅ Loaded {len(df)} rows into the database")

# Show what was imported
result = pd.read_sql(text("SELECT * FROM imported_sales ORDER BY sales_amount DESC"), engine)
print(result)