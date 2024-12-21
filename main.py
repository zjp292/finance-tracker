# get most recent activity csv file
    # create secondary script (host on a server?) 
    # to remind me to get the most up to date data

# parse through the data
    # create spending / income break down
    # visualize the data 

# create spending categories possible

import pandas as pd
import matplotlib.pyplot as plt
import os
import constants

df = pd.read_csv('activity-csv-data/Chase2809_Activity_20241216.CSV')
df = df.dropna(axis=1)
#print(df)

df['Posting Date'] = pd.to_datetime(df['Posting Date'])

df['Year'] = df['Posting Date'].dt.year
df['Month'] = df['Posting Date'].dt.month

monthly_data = df.groupby(['Year' , 'Month']).agg({'Amount': 'sum'}).reset_index()
print(monthly_data)
monthly_data['Year-Month'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str)

income = df[df['Type'] == 'Credit'].groupby(['Year', 'Month'])['Amount'].sum()
expenses = df[df['Type'] == 'Debit'].groupby(['Year', 'Month'])['Amount'].sum()


plt.plot(monthly_data['Year-Month'], monthly_data['Amount'], marker='o')
plt.title('Monthly Spending Trend')
plt.xlabel('Month')
plt.ylabel('Total Amount ($)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()




