import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../data/master_orders_clean.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['month'] = df['order_purchase_timestamp'].dt.to_period('M')
df['year'] = df['order_purchase_timestamp'].dt.year
df['year_month'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')

# ========================
# 1. OVERALL KPI
# ========================
print('=== 1. OVERALL KPI ===')
total_gmv = df['price'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['customer_unique_id'].nunique()
avg_aov = df.groupby('order_id')['total_payment'].first().mean()
print(f'Total GMV: R${total_gmv:,.0f}')
print(f'Total Orders: {total_orders:,}')
print(f'Total Customers: {total_customers:,}')
print(f'Avg AOV: R${avg_aov:.2f}')

# ========================
# 2. MONTHLY TRENDS
# ========================
print()
print('=== 2. MONTHLY TRENDS ===')
monthly = df.groupby('year_month').agg(
    revenue=('price','sum'),
    orders=('order_id','nunique'),
    customers=('customer_unique_id','nunique'),
    avg_score=('review_score','mean')
).reset_index()
monthly = monthly.sort_values('year_month')
first3 = monthly.head(3)
last3 = monthly.tail(3)
rev_growth = (last3['revenue'].mean() - first3['revenue'].mean()) / first3['revenue'].mean() * 100
cust_growth = (last3['customers'].mean() - first3['customers'].mean()) / first3['customers'].mean() * 100
print(f'First 3 months avg revenue: R${first3["revenue"].mean():,.0f}')
print(f'Last 3 months avg revenue: R${last3["revenue"].mean():,.0f}')
print(f'Revenue growth: {rev_growth:.1f}%')
print(f'Customer growth: {cust_growth:.1f}%')
peak_month = monthly.loc[monthly['revenue'].idxmax()]
print(f'Peak month: {peak_month["year_month"]} (R${peak_month["revenue"]:,.0f})')

# ========================
# 3. CATEGORY ABC
# ========================
print()
print('=== 3. CATEGORY ABC ===')
cat = df.groupby('category_english').agg(
    revenue=('price','sum'),
    orders=('order_id','nunique'),
    avg_score=('review_score','mean')
).sort_values('revenue', ascending=False)
cat['pct'] = cat['revenue'] / cat['revenue'].sum() * 100
cat['cum_pct'] = cat['pct'].cumsum()
a_cats = cat[cat['cum_pct'] <= 50]
b_cats = cat[(cat['cum_pct'] > 50) & (cat['cum_pct'] <= 80)]
c_cats = cat[cat['cum_pct'] > 80]
print(f'A-class (Top 50% rev): {len(a_cats)} cats, {a_cats["pct"].sum():.1f}% revenue')
print(f'  Top 5: {", ".join(a_cats.head(5).index.tolist())}')
print(f'B-class (50-80%): {len(b_cats)} cats, {b_cats["pct"].sum():.1f}% revenue')
print(f'C-class (80-100%): {len(c_cats)} cats, {c_cats["pct"].sum():.1f}% revenue')

# ========================
# 4. DELIVERY & SCORE
# ========================
print()
print('=== 4. DELIVERY & REVIEW SCORE ===')
df['delivery_bucket'] = pd.cut(df['delivery_days'], bins=[0,5,10,15,20,30,100],
                               labels=['0-5d','6-10d','11-15d','16-20d','21-30d','30d+'])
del_score = df.groupby('delivery_bucket', observed=False)['review_score'].agg(['mean','count'])
print('Score by Delivery Time:')
for bucket, row in del_score.iterrows():
    print(f'  {bucket}: {row["mean"]:.2f} (n={row["count"]:,})')

on_time = (df['delivery_days'] <= 10).mean() * 100
print(f'Orders delivered within 10 days: {on_time:.1f}%')

df['price_bucket'] = pd.qcut(df['price'], q=5, labels=['Q1 (Low)','Q2','Q3','Q4','Q5 (High)'])
price_score = df.groupby('price_bucket', observed=False)['review_score'].mean()
print('Score by Price Quintile:')
for bucket, score in price_score.items():
    print(f'  {bucket}: {score:.2f}')

# ========================
# 5. GEOGRAPHIC
# ========================
print()
print('=== 5. GEOGRAPHIC CONCENTRATION ===')
state = df.groupby('customer_state').agg(
    revenue=('price','sum'),
    customers=('customer_unique_id','nunique')
).sort_values('revenue', ascending=False)
state['pct'] = state['revenue'] / state['revenue'].sum() * 100
top3 = state.head(3)
print(f'SP (Sao Paulo): {state.loc["SP","pct"]:.1f}%')
print(f'Top 3 states: {top3["pct"].sum():.1f}%')
hhi = (state['pct']**2).sum()
print(f'HHI index: {hhi:.0f}')

# ========================
# 6. PAYMENT
# ========================
print()
print('=== 6. PAYMENT BEHAVIOR ===')
pay = df.groupby('payment_type').agg(
    orders=('order_id','nunique'),
    avg_value=('total_payment','mean')
).sort_values('orders', ascending=False)
for ptype, row in pay.iterrows():
    print(f'  {ptype}: {row["orders"]:,} orders, avg R${row["avg_value"]:.2f}')
install_pct = (df['max_installments'] > 1).mean() * 100
print(f'Orders with installments: {install_pct:.1f}%')
print(f'Avg installments (when used): {df[df["max_installments"]>1]["max_installments"].mean():.1f}')

# ========================
# 7. SELLER CONCENTRATION
# ========================
print()
print('=== 7. SELLER CONCENTRATION ===')
seller = df.groupby('seller_id')['price'].sum().sort_values(ascending=False)
seller_pct = seller / seller.sum() * 100
top1 = seller_pct.head(int(len(seller)*0.01)).sum()
top5 = seller_pct.head(int(len(seller)*0.05)).sum()
top20 = seller_pct.head(int(len(seller)*0.20)).sum()
print(f'Top 1% sellers: {top1:.1f}% of revenue')
print(f'Top 5% sellers: {top5:.1f}% of revenue')
print(f'Top 20% sellers: {top20:.1f}% of revenue')

# ========================
# 8. RETENTION
# ========================
print()
print('=== 8. RETENTION STATS ===')
user_orders = df.groupby(['customer_unique_id','order_id']).agg(
    purchase_date=('order_purchase_timestamp','min')
).reset_index()
user_orders['purchase_month'] = user_orders['purchase_date'].dt.to_period('M')

first_purchase = user_orders.groupby('customer_unique_id')['purchase_month'].min().reset_index()
first_purchase.columns = ['customer_unique_id','cohort_month']
user_orders = user_orders.merge(first_purchase, on='customer_unique_id')
user_orders['month_offset'] = (
    user_orders['purchase_month'].dt.year * 12 + user_orders['purchase_month'].dt.month
    - (user_orders['cohort_month'].dt.year * 12 + user_orders['cohort_month'].dt.month)
)

cohort_size = user_orders.groupby('cohort_month')['customer_unique_id'].nunique()
cohort_data = user_orders.groupby(['cohort_month','month_offset'])['customer_unique_id'].nunique().reset_index()
cohort_data = cohort_data.merge(cohort_size.reset_index(name='cohort_size'), on='cohort_month')
cohort_data['retention'] = cohort_data['customer_unique_id'] / cohort_data['cohort_size'] * 100
avg_ret = cohort_data.groupby('month_offset')['retention'].mean()
for m in [1,2,3,6,12]:
    if m in avg_ret.index:
        print(f'Month {m} retention: {avg_ret[m]:.1f}%')

orders_per_user = user_orders.groupby('customer_unique_id')['order_id'].nunique()
repeat_rate = (orders_per_user > 1).mean() * 100
print(f'Repeat purchase rate: {repeat_rate:.1f}%')

user_order_dates = user_orders.groupby('customer_unique_id')['purchase_date'].apply(list).reset_index()
user_order_dates['n_orders'] = user_order_dates['purchase_date'].apply(len)
repeat_buyers = user_order_dates[user_order_dates['n_orders'] > 1].copy()
def days_to_2nd(dates):
    s = sorted(dates)
    return (s[1] - s[0]).days
repeat_buyers['d2'] = repeat_buyers['purchase_date'].apply(days_to_2nd)
print(f'Median days to 2nd purchase: {repeat_buyers["d2"].median():.0f}')
print(f'Avg days to 2nd purchase: {repeat_buyers["d2"].mean():.0f}')

# ========================
# 9. CORRELATION
# ========================
print()
print('=== 9. KEY CORRELATIONS ===')
from scipy.stats import pearsonr
valid = df.dropna(subset=['delivery_days','review_score','price','freight_value'])
for var in ['delivery_days','price','freight_value']:
    r, p = pearsonr(valid[var], valid['review_score'])
    print(f'  review_score ~ {var}: r={r:.3f}, p={p:.6f}')

print()
print('Analysis complete!')
