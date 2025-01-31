# RFM Analysis in Marketing Analytics

## What is RFM Analysis?

**RFM Analysis** is a marketing technique used to analyze and segment customers based on three key metrics derived from their transaction history:

- **Recency (R)**: *How recently did the customer make a purchase?*  
  This tells you how active and engaged the customer is with your brand. Recent buyers are more likely to respond to offers and promotions.

- **Frequency (F)**: *How often does the customer make a purchase?*  
  Frequent customers are often more loyal and have a higher lifetime value (CLTV). The more frequently they buy, the more engaged they are.

- **Monetary (M)**: *How much does the customer spend?*  
  High-spending customers are typically your most valuable. These customers contribute the most to your revenue and are prime candidates for loyalty programs and upselling.

### Why RFM Analysis?

RFM analysis helps you **identify high-value customers**, segment them into distinct groups, and **target marketing efforts** effectively. It's often used to:

- **Target loyal customers** with rewards or retention campaigns.
- **Re-engage dormant or "at-risk" customers** through special offers.
- **Identify and nurture new or occasional buyers** with promotional strategies.

---

## What We Did in the Python Code

The Python code provided performs the following steps to calculate and segment customers using **RFM analysis**:

### **Step 1: Load and Preprocess Data**
We start by loading transaction data (from a CSV file) into a **pandas DataFrame**. The dataset includes **Transaction Date**, **Customer ID**, **Transaction ID**, **Quantity**, and **Total Amount of Sales**.

```python
file_path = "your_data.csv"  #Add the name of the CSV file
df = pd.read_csv(file_path)
```
The **Date** column is converted to ```datetime``` format to facilitate date-related calculations.
```python
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
```
### **Step 2: Calculate Recency, Frequency, and Monetary (RFM)**

- **Recency** is calculated as the number of days since the **last purchase** of each customer.  
  
- **Frequency** is calculated as the number of **unique transactions** each customer made.

- **Monetary** is calculated as the total **amount spent** by each customer.
```python
rfm = df.groupby('Customer ID').agg({
    'Date': lambda x: (latest_date - x.max()).days,  #Recency
    'Transaction ID': 'nunique',  #Frequency
    'Total Amount of Sales': 'sum'  #Monetary
}).reset_index()
```
The ```groupby()``` function aggregates the data by **Customer ID**, and we calculate the metrics based on the customer’s transaction history.

### **Step 3: Assign RFM Scores**

For each metric (Recency, Frequency, and Monetary), we assign a score between 1 and 5 using **quantiles**:
- **Recency**: Lower values (more recent) get a higher score (5 = most recent).  
  
- **Frequency**: Higher frequency (more transactions) gets a higher score (5 = most frequent).

- **Monetary**: Higher spend gets a higher score (5 = highest spend).
```python
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
```
This gives us a numerical score for each customer across these three dimensions.

### **Step 4: Combine RFM Scores**

The final **RFM score** is created by concatenating the scores for **Recency**, **Frequency**, and **Monetary** into a single string.
```python
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
```
This results in a 3-digit string (e.g., "555", "431") that represents the combined behavior of each customer.

### **Step 5: Segment Customers**

We then segment customers based on their **RFM score** and define groups like:

### **Customer Segments Based on RFM Score**
We classify customers into **eight key segments** based on their RFM scores:

1. **Best Customers**   
   - High Recency (R), High Frequency (F), High Monetary (M) → (e.g., "555")  
   - These customers purchase frequently and spend the most.  
   
2. **Loyal Customers**  
   - High Frequency (F) with decent Recency (R) and Monetary (M) scores.  
   - Regular buyers who engage with the brand frequently.  

3. **At-Risk Customers**  
   - High Frequency (F) & Monetary (M) but low Recency (R).  
   - Previously engaged customers who haven't purchased recently.  

4. **One-Time Buyers**  
   - Customers who have made only **one** purchase (low Frequency).  
   - Some may have bought recently, while others may have purchased long ago.  

5. **New Customers**  
   - Recently made their **first** purchase but have not yet demonstrated loyalty.  

6. **Churned Customers**  
   - Low Recency (R), Frequency (F), and Monetary (M) scores.  
   - These customers have not made a purchase for a long time.  

7. **Potential Loyalists**  
   - Good Recency (R) & Frequency (F) scores but moderate Monetary (M) score.  
   - These customers are engaged and have the potential to become loyal.  

8. **Average Customers**  
   - Moderate Recency, Frequency, and Monetary values across the board.  
   - These customers buy occasionally but are not highly engaged.  

We use the `RFM_Score` to segment customers based on their behavior.

```python
def segment_customer(row):
    if row['Frequency'] == 1:
        if row['Recency'] <= 30:  #Recent first-time purchase.
            return 'New Customer'
        else:  #First-time purchase but inactive.
            return 'One-Time Buyer'

    if row['RFM_Score'] in ['555', '554', '545', '554']:
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
```
Each customer is classified into one of these segments for targeted marketing campaigns.

### **Step 6: Save and Visualize Results**

The results are saved in a CSV file (```rfm_analysis.csv```), which includes the **RFM score** and **customer segment**. You can later use this data for more advanced analysis or visualizations.

```python
rfm.to_csv("rfm_analysis.csv", index=False)
```

## How to Use RFM Analysis in Marketing Analytics

RFM Analysis is a powerful tool for marketing analytics because it provides insights into customer behavior that can drive effective **targeted marketing strategies**. Here are some ways to use RFM analysis:

### **1. Target Best Customers**
-  **Best Customers** (high Recency, Frequency, and Monetary scores) are your most valuable clients. Create **loyalty programs**, special promotions, and     **exclusive offers** to retain them.

### **2. Engage Potential Loyalists**
-  **Potential Loyalists** are customers who have made a few purchases but aren’t fully loyal yet. These customers should be targeted with **engagement campaigns** to increase their **frequency** of purchases and move them towards **loyalty**.

### **3. Re-engage At-Risk Customers**
-  **At-Risk Customers** are those who have made many purchases in the past but haven’t bought recently. Target them with **retargeting ads**, **email campaigns**, or **discounts** to win them back before they churn.

### **4. Develop New Customers**
-  **New Customers** who bought recently should be nurtured with **welcome emails**, promotions, and educational content to increase their **lifetime value**.

### **5. Convert One-Time Buyers**
-  **One-Time Buyers** need to be incentivized to make a second purchase. Offer **discounts**, create **time-limited promotions**, and **upsell** related products.

### **6. Avoid Wasting Resources**
-  Customers who fall into segments like **Churned Customers** or **One-Time Buyers** can be excluded from certain campaigns or have a tailored re-engagement strategy, reducing wasted marketing spend.

## Conclusion

RFM Analysis is an easy-to-implement yet highly effective technique to categorize customers based on their purchase behavior. It enables businesses to **target the right customers with the right message, increase customer retention**, and **maximize lifetime value**. By using Python and pandas, you can automate the process, segment your customer base, and drive more impactful marketing decisions.
