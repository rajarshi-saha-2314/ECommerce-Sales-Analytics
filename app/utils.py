# utils.py

import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

def filter_data(df, region=None, segment=None):
    if region:
        df = df[df['state'] == region]
    if segment:
        df = df[df['segment'] == segment]
    return df

def calculate_kpis(df):
    total_revenue = df['sales'].sum()
    total_orders = df.shape[0]
    avg_order_value = df['sales'].mean()

    return total_revenue, total_orders, avg_order_value

def revenue_trend(df):
    return df.groupby('order_date')['sales'].sum()

def category_sales(df):
    return df.groupby('segment')['sales'].sum()