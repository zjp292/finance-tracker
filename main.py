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

def plotExpenses_barGraph(df):
    plt.figure(figsize=(10,6))
    plt.bar(df['Year-Month'], df['Amount'], color='red')
    
    plt.xlabel('Month')
    plt.ylabel('Amount in Dollars')
    plt.title('Expenses by month.')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def expenseTable_byMonth(df, month, year):
    # check if month in bounds
    if not (1 <= month <= 12):
        print('Month not in bounds')
        return
    
    month_expense = df[(df['Month'] == month) 
                       & (df['Year'] == year)
                       & (df['Details'] == 'DEBIT')
                       & ~df['Description'].str.contains('Transfer', case=True, na=False)]
    month_expense = month_expense.sort_values(by=['Amount'])
    #print(month_expense)
    return(month_expense)

def incomeTable_byMonth(df, month, year):
    # check if month in bounds
    if not (1 <= month <= 12):
        print('Month not in bounds')
        return
    
    month_income = df[(df['Month'] == month)
                      & (df['Year'] == year)
                      & (df['Details'] == 'CREDIT')
                      & ~df['Description'].str.contains('Transfer', case=True, na=False)]
    month_income = month_income.sort_values(by=['Amount'], ascending=False)
    #print(month_income)
    return(month_income)

def deltaAmount_byMonth(df, month, year):
    if not (1 <= month <= 12):
        print('Month not in bounds')
        return
    
    month_expense = expenseTable_byMonth(df, month, year)
    month_income = incomeTable_byMonth(df, month, year)
    
    delta_amount = month_income['Amount'] + month_expense['Amount']
    
    print(delta_amount)

# read csv data into dataframe
df = pd.read_csv('activity-csv-data/Chase2809_Activity_20241216.CSV')

# drop null/nan values
df = df.dropna(axis=1)

# change the posting date type to datetime
df['Posting Date'] = pd.to_datetime(df['Posting Date'])

# get year and month data
df['Year'] = df['Posting Date'].dt.year
df['Month'] = df['Posting Date'].dt.month

#print(df)






monthly_data = df.groupby(['Year' , 'Month']).agg({'Amount': 'sum'}).reset_index()

monthly_data['Year-Month'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str)
#print(monthly_data)

income = df[(df['Details'] == 'CREDIT') &
            df['Description'].str.contains('|'.join(income_keywords))]
income = income.groupby(['Year', 'Month'])['Amount'].sum()


expenses = df[(df['Details'] == 'DEBIT') & 
              (~df['Description'].str.contains('Transfer', case=True, na=False))]
expenses = expenses.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
#print(expenses)



#delta = income + expenses

# print('income: ', income)
# print('expenses: ', expenses)
# print('diff change: ', delta)
expenses_by_month = df[df['Details'] == 'DEBIT'].groupby(['Year', 'Month'])['Amount'].sum().reset_index()

# Create a 'Year-Month' column for better labels
expenses['Year-Month'] = expenses['Year'].astype(str) + '-' + expenses_by_month['Month'].astype(str)


# print(expenses)
# print(income)

#plotExpenses_barGraph(expenses)
# expenseTable_byMonth(df, 9, 2024)
# incomeTable_byMonth(df, 9, 2024)
deltaAmount_byMonth(df, 9, 2024)