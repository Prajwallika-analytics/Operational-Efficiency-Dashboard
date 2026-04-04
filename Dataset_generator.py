import pandas as pd
import numpy as np

np.random.seed(42)
n = 800
regions = ['North','South','East','West','Central']
depts   = ['Operations','Procurement','Logistics','HR','IT']

df = pd.DataFrame({
    'Date':       pd.date_range('2023-01-01',periods=n,freq='D').to_series().sample(n,random_state=42).values,
    'Region':     np.random.choice(regions,n),
    'Department': np.random.choice(depts,n),
    'Expected_Cost': np.random.randint(5000,50000,n),
    'Delay_Days': np.random.choice([0,1,2,3,5,7,10,14],n,
                    p=[.3,.2,.15,.1,.1,.07,.05,.03]),
    'Revenue':    np.random.randint(20000,120000,n),
    'Employee_Count': np.random.randint(10,200,n),
})

df['Actual_Cost'] = (
    df['Expected_Cost'] * np.where(
        df['Region'] == 'North',
        np.random.uniform(1.12,1.25,n),
        np.random.uniform(0.88,1.08,n)
    ) + df['Delay_Days'] * np.random.uniform(80,200,n)
).round(2)

df['Cost_Variance']   = (df['Actual_Cost'] - df['Expected_Cost']).round(2)
df['Profit_Margin']   = (df['Revenue'] - df['Actual_Cost']).round(2)
df['Efficiency_Pct']  = ((df['Revenue'] - df['Actual_Cost']) / df['Revenue'] * 100).round(1)
df['Date']            = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

df = df.sort_values('Date').reset_index(drop=True)
df.to_csv('ops_data.csv', index=False)
print("Dataset created successfully!")