# demand_analysis.py
# Demand Analysis and ABC Classification Module
# Inventory Rewired Project

import pandas as pd
import numpy as np
from scipy import stats

def analyze_demand_patterns(sales_data, sku_master):
    """Analyze demand patterns for all SKUs"""
    print("Analyzing demand patterns...")
    
    # Calculate daily demand statistics by SKU and store
    demand_stats = sales_data.groupby(['store_id', 'sku_id']).agg({
        'quantity_sold': ['mean', 'std', 'sum', 'count', 'min', 'max']
    }).round(2)
    
    demand_stats.columns = ['avg_daily_demand', 'demand_std', 'total_demand', 
                           'days_sold', 'min_demand', 'max_demand']
    demand_stats = demand_stats.reset_index()
    
    # Calculate coefficient of variation for demand variability
    demand_stats['cv'] = (demand_stats['demand_std'] / demand_stats['avg_daily_demand']).fillna(0)
    
    # Merge with SKU master data
    demand_analysis = demand_stats.merge(sku_master, on='sku_id', how='left')
    
    # Calculate annual demand
    demand_analysis['annual_demand'] = demand_analysis['avg_daily_demand'] * 365
    
    # Calculate revenue per SKU-store combination
    demand_analysis['annual_revenue'] = demand_analysis['annual_demand'] * demand_analysis['unit_cost']
    
    # Demand classification based on variability
    demand_analysis['demand_pattern'] = pd.cut(
        demand_analysis['cv'], 
        bins=[0, 0.5, 1.0, float('inf')], 
        labels=['Stable', 'Moderate', 'Highly Variable']
    )
    
    print(f"✓ Analyzed demand for {len(demand_analysis)} SKU-store combinations")
    
    return demand_analysis

def abc_classification(sales_data, sku_master):
    """Perform ABC classification based on revenue contribution"""
    print("Performing ABC classification...")
    
    # Calculate total revenue by SKU across all stores
    sku_revenue = sales_data.merge(sku_master, on='sku_id')
    sku_revenue['revenue'] = sku_revenue['quantity_sold'] * sku_revenue['unit_cost']
    
    abc_data = sku_revenue.groupby('sku_id').agg({
        'quantity_sold': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Sort by revenue (descending)
    abc_data = abc_data.sort_values('revenue', ascending=False)
    
    # Calculate cumulative percentage
    abc_data['cumulative_revenue'] = abc_data['revenue'].cumsum()
    total_revenue = abc_data['revenue'].sum()
    abc_data['revenue_percentage'] = (abc_data['revenue'] / total_revenue * 100).round(2)
    abc_data['cumulative_percentage'] = (abc_data['cumulative_revenue'] / total_revenue * 100).round(2)
    
    # ABC Classification
    abc_data['abc_class'] = 'C'
    abc_data.loc[abc_data['cumulative_percentage'] <= 80, 'abc_class'] = 'A'
    abc_data.loc[(abc_data['cumulative_percentage'] > 80) & 
                 (abc_data['cumulative_percentage'] <= 95), 'abc_class'] = 'B'
    
    # Service level assignment based on ABC class
    service_levels = {'A': 0.98, 'B': 0.95, 'C': 0.90}
    abc_data['target_service_level'] = abc_data['abc_class'].map(service_levels)
    
    # Merge additional SKU data
    abc_results = abc_data.merge(sku_master, on='sku_id', how='left')
    
    # Summary statistics
    abc_summary = abc_results.groupby('abc_class').agg({
        'sku_id': 'count',
        'revenue': 'sum',
        'revenue_percentage': 'sum'
    }).round(2)
    abc_summary.columns = ['sku_count', 'total_revenue', 'revenue_contribution']
    
    print(f"✓ ABC Classification completed:")
    for cls in ['A', 'B', 'C']:
        if cls in abc_summary.index:
            count = abc_summary.loc[cls, 'sku_count']
            contrib = abc_summary.loc[cls, 'revenue_contribution']
            print(f"  Class {cls}: {count} SKUs ({contrib}% revenue)")
    
    return abc_results, abc_summary

def calculate_demand_forecast(sales_data, periods_ahead=30):
    """Calculate demand forecast using moving average"""
    
    # Simple moving average forecast by SKU and store
    forecast_data = []
    
    for (store_id, sku_id), group in sales_data.groupby(['store_id', 'sku_id']):
        group = group.sort_values('date')
        
        # Use last 7 days for moving average
        recent_demand = group['quantity_sold'].tail(7).mean()
        
        forecast_data.append({
            'store_id': store_id,
            'sku_id': sku_id,
            'forecast_daily_demand': recent_demand,
            'forecast_period_demand': recent_demand * periods_ahead
        })
    
    forecast_df = pd.DataFrame(forecast_data)
    
    return forecast_df