# inventory_models.py
# EOQ and Safety Stock Calculation Module
# Inventory Rewired Project

import pandas as pd
import numpy as np
from scipy import stats

def calculate_eoq_and_safety_stock(demand_analysis, abc_results):
    """Calculate EOQ and safety stock for all SKUs"""
    print("Calculating EOQ and safety stock...")
    
    # Merge demand analysis with ABC classification
    inventory_model = demand_analysis.merge(
        abc_results[['sku_id', 'abc_class', 'target_service_level']], 
        on='sku_id', how='left'
    )
    
    # EOQ calculation parameters
    holding_cost_rate = 0.25  # 25% annual holding cost
    ordering_cost = 50  # ₹50 per order
    
    # Calculate EOQ
    inventory_model['annual_holding_cost'] = inventory_model['unit_cost'] * holding_cost_rate
    inventory_model['eoq'] = np.sqrt(
        (2 * inventory_model['annual_demand'] * ordering_cost) / 
        inventory_model['annual_holding_cost']
    ).round(0)
    
    # Safety stock calculation
    inventory_model['z_score'] = inventory_model['target_service_level'].apply(
        lambda x: stats.norm.ppf(x) if x < 1 else 2.33
    )
    
    # Lead time demand standard deviation
    inventory_model['lead_time_demand_std'] = (
        inventory_model['demand_std'] * np.sqrt(inventory_model['avg_lead_time'])
    )
    
    inventory_model['safety_stock'] = (
        inventory_model['z_score'] * inventory_model['lead_time_demand_std']
    ).round(0).clip(lower=0)
    
    # Reorder point calculation
    inventory_model['lead_time_demand'] = (
        inventory_model['avg_daily_demand'] * inventory_model['avg_lead_time']
    )
    inventory_model['reorder_point'] = (
        inventory_model['lead_time_demand'] + inventory_model['safety_stock']
    ).round(0)
    
    # Maximum inventory level
    inventory_model['max_inventory'] = (
        inventory_model['eoq'] + inventory_model['safety_stock']
    )
    
    # Calculate total annual costs
    inventory_model['annual_ordering_cost'] = (
        inventory_model['annual_demand'] / inventory_model['eoq'] * ordering_cost
    )
    inventory_model['annual_holding_cost_total'] = (
        (inventory_model['eoq'] / 2 + inventory_model['safety_stock']) * 
        inventory_model['annual_holding_cost']
    )
    inventory_model['total_annual_cost'] = (
        inventory_model['annual_ordering_cost'] + 
        inventory_model['annual_holding_cost_total']
    )
    
    print(f"✓ EOQ calculations completed for {len(inventory_model)} combinations")
    
    return inventory_model

def calculate_current_performance_kpis(sales_data, inventory_data, sku_master):
    """Calculate current inventory performance KPIs"""
    print("Calculating current performance KPIs...")
    
    # Merge sales with inventory data
    current_performance = sales_data.merge(sku_master, on='sku_id')
    current_performance = current_performance.merge(inventory_data, on=['store_id', 'sku_id'])
    
    # Calculate revenue
    current_performance['revenue'] = current_performance['quantity_sold'] * current_performance['unit_cost']
    
    # Aggregate by store and SKU
    kpi_data = current_performance.groupby(['store_id', 'sku_id']).agg({
        'quantity_sold': ['sum', 'mean'],
        'revenue': 'sum',
        'current_stock': 'first',
        'unit_cost': 'first'
    }).reset_index()
    
    kpi_data.columns = ['store_id', 'sku_id', 'total_sold', 'avg_daily_sales', 
                       'total_revenue', 'current_stock', 'unit_cost']
    
    # Calculate KPIs
    kpi_data['inventory_value'] = kpi_data['current_stock'] * kpi_data['unit_cost']
    kpi_data['days_of_supply'] = kpi_data['current_stock'] / kpi_data['avg_daily_sales']
    kpi_data['inventory_turnover'] = (kpi_data['total_sold'] * 4) / kpi_data['current_stock']  # Annualized
    
    # Stock out analysis (assuming 0 sales = stock out)
    stockout_analysis = sales_data[sales_data['quantity_sold'] == 0]
    stockout_rate = len(stockout_analysis) / len(sales_data) * 100
    
    # Overall KPIs
    overall_kpis = {
        'fill_rate': 100 - stockout_rate,
        'avg_inventory_turnover': kpi_data['inventory_turnover'].mean(),
        'total_inventory_value': kpi_data['inventory_value'].sum(),
        'avg_days_supply': kpi_data['days_of_supply'].mean(),
        'stockout_events': len(stockout_analysis)
    }
    
    print(f"✓ Current fill rate: {overall_kpis['fill_rate']:.1f}%")
    print(f"✓ Average inventory turnover: {overall_kpis['avg_inventory_turnover']:.1f}x")
    
    return overall_kpis

def calculate_optimal_inventory_levels(inventory_model):
    """Calculate optimal inventory levels for implementation"""
    
    # Group by SKU for aggregated recommendations
    optimal_levels = inventory_model.groupby('sku_id').agg({
        'eoq': 'mean',
        'safety_stock': 'mean',
        'reorder_point': 'mean',
        'max_inventory': 'mean',
        'abc_class': 'first',
        'target_service_level': 'first',
        'unit_cost': 'first'
    }).round(0)
    
    # Calculate total investment required
    optimal_levels['investment_per_sku'] = (
        optimal_levels['max_inventory'] * optimal_levels['unit_cost']
    )
    
    return optimal_levels