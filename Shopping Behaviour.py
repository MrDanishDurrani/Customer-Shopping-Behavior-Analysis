import pandas as pd
df= pd.read_csv("customer_shopping_behavior.csv")
#print(df.tail(5))

#print("\n---Raw Data---")
#print(df)
#print(df.info())
#print(df.columns)
#print(df.describe(include="all"))
#print(df.isnull().sum())
# To Remove null values
#df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
#print(df.isnull().sum())
#print(df.describe(include="all"))
# Snake casing
df.columns= df.columns.str.lower()
df.columns= df.columns.str.replace(' ','_')
df = df.rename( columns={ 'purchase_amount_(usd)': 'purchase_amount'})
#print(df.columns)
# Age Group
labels=['Young_Adult', 'Adult', 'Middle_aged', 'Senior']
df['age_group'] =pd.qcut(df['age'], q=4, labels=labels)
#df[['age','age_group']].head(10)
#print(df.head(10))
# New column purchase frequency days
frequency_maping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_maping)
#print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))
#Comparison B/T columns
#print(df[['discount_applied','promo_code_used']].head(10))
# Remove one Column
df=df.drop('promo_code_used',axis=1)
#print(df.columns)
#print(df.head)

from sqlalchemy import create_engine

# Step 1: PostgreSQL credentials

username = "postgres"
password = "Danish123"
host = "localhost"
port = "5432"
database = "customer_behavior"

# Step 2: Create connection

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# Step 3: Load cleaned DataFrame into PostgreSQL

table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

# Step 4: Confirmation

print(
    f"Data successfully loaded into table '{table_name}' "
    f"in database '{database}'."
)
