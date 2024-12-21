# get most recent activity csv file
    # create secondary script (host on a server?) 
    # to remind me to get the most up to date data

# parse through the data
    # create spending / income break down
    # visualize the data 

# create spending categories possible

import pandas as pd
import matplotlib.pyplot as plt

income_keywords = ['WELLS FARGO BANK PAYRLL', 'Aires', 'Zelle']


# read csv data into dataframe
df = pd.read_csv('activity-csv-data/Chase2809_Activity_20241216.CSV')

# drop null/nan values
df = df.dropna(axis=1)

# change the posting date type to datetime
df['Posting Date'] = pd.to_datetime(df['Posting Date'])

# get year and month data
df['Year'] = df['Posting Date'].dt.year
df['Month'] = df['Posting Date'].dt.month


monthly_data = df.groupby(['Year' , 'Month']).agg({'Amount': 'sum'}).reset_index()

monthly_data['Year-Month'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str)


#income = df[df['Description'].str.contains('|'.join(income_keywords))]
income = df[(df['Details'] == 'CREDIT') &
            df['Description'].str.contains('|'.join(income_keywords))]

income = income.groupby(['Year', 'Month'])['Amount'].sum()


expenses = df[(df['Details'] == 'DEBIT') & 
              (~df['Description'].str.contains('Transfer', case=True, na=False))]
expenses = expenses.groupby(['Year', 'Month'])['Amount'].sum()

delta = income + expenses

print('income: ', income)
print('expenses: ', expenses)
print('diff change: ', delta)