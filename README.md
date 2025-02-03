# RFM Analysis in Marketing Analytics

## Overview

**RFM Analysis** is a technique to segment customers based on:

  - **Recency (R)** – How recently a customer made a purchase.
  - **Frequency (F)** – How often they make purchases.
  - **Monetary (M)** – How much they spend.

This helps businesses identify **high-value customers**, **re-engage at-risk ones**, and **optimize marketing efforts**.

## Implementation in Python

### **1. Load & Preprocess Data**

Load transaction data from a [CSV file](https://www.kaggle.com/datasets/marian447/retail-store-sales-transactions) (For Example a Dataset from Kaggle):

```python
df = pd.read_csv("your_data.csv")
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
```

### **2. Compute RFM Metrics**

```python
rfm = df.groupby('Customer ID').agg({
    'Date': lambda x: (latest_date - x.max()).days,  # Recency
    'Transaction ID': 'nunique',  # Frequency
    'Total Amount of Sales': 'sum'  # Monetary
}).reset_index()
```

### **3. Assign RFM Scores**

```python
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
```

### **4. Segment Customers**

```python
def segment_customer(row):
    if row['Frequency'] == 1:
        if row['Recency'] <= 30:  
            return 'New Customer'
        else:  
            return 'One-Time Buyer'  
    if row['R_Score'] == 5 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Best Customers'
    elif row['R_Score'] == 5:
        return 'Loyal Customers'
    elif row['R_Score'] == 1:
        return 'At Risk Customers'
    elif row['R_Score'] == 2:
        return 'Churned Customers'
    elif row['R_Score'] == 4:
        return 'Potential Loyalists'
    else:
        return 'Average Customers'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)
```

### **5. Save Results**

```python
rfm.to_csv("rfm_analysis.csv", index=False)
```

## Marketing Applications Examples

  - **Best Customers**: Reward with loyalty programs.
  - **Potential Loyalists**: Encourage repeat purchases.
  - **At-Risk Customers**: Offer discounts to re-engage.
  - **New Customers**: Onboard with promotions.
  - **One-Time Buyers**: Incentivize a second purchase.
  - **Churned Customers**: Minimal marketing spend.

## Conclusion

RFM Analysis enables **data-driven customer segmentation** for targeted marketing. Automating it with Python allows businesses to improve **customer retention**, **engagement**, and **revenue**.
