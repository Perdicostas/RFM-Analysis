import pandas as pd

#Load your dataset
file_path = "scanner_data.csv"  #Add the name of the CSV file
df = pd.read_csv(file_path)

#Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')  

#Define the latest date in the dataset
latest_date = df['Date'].max()

#Group data by Customer ID to calculate RFM metrics
rfm = df.groupby('Customer_ID').agg({
    'Date': lambda x: (latest_date - x.max()).days,  #Recency: Days since last purchase
    'Transaction_ID': 'nunique',  #Frequency: Number of unique transactions
    'Sales_Amount': 'sum'  #Monetary: Total spend
}).reset_index()

#New columns
rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

#Assign RFM scores (1-5)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

#Combine RFM scores as a single score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

#Define customer segments based on RFM Score
def segment_customer(row):
    if row['Frequency'] == 1:
        if row['Recency'] <= 30:  #If client bought recently, is "New Customer"
            return 'New Customer'
        else:  #If client has only purchased once in the past, is "One-Time Buyer"
            return 'One-Time Buyer'
    
    #Segmentation for other cases
    if row['R_Score'] == 5 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Best Customers'
    elif row['RFM_Score'].startswith('5'):
        return 'Loyal Customers'
    elif row['RFM_Score'].startswith('1'):
        return 'At Risk Customers'
    elif row['RFM_Score'].startswith('2'):
        return 'Churned Customers'
    elif row['RFM_Score'].startswith('4'):
        return 'Potential Loyalists'
    else:
        return 'Average Customers'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

#Save the New CSV
rfm.to_csv("RFM_analysis.csv", index=False)


