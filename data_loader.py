# data_loader.py
# Data Loading and Preparation Module
# Inventory Rewired Project

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_prepare_data():
    """Load and prepare all data from Excel file"""
    try:
        # Load Excel file with all sheets
        excel_file = 'InventoryRewired_Dataset.xlsx'
        
        print("Loading data from Excel file...")
        
        # Load all sheets
        sales_data = pd.read_excel(excel_file, sheet_name='Sales_data')
        inventory_data = pd.read_excel(excel_file, sheet_name='Inventory_data')
        sku_master = pd.read_excel(excel_file, sheet_name='SKU_master')
        purchase_orders = pd.read_excel(excel_file, sheet_name='Purchase_orders')
        supplier_data = pd.read_excel(excel_file, sheet_name='Supplier_data')
        
        # Data preparation and cleaning
        sales_data = prepare_sales_data(sales_data)
        inventory_data = prepare_inventory_data(inventory_data)
        sku_master = prepare_sku_master(sku_master)
        purchase_orders = prepare_purchase_orders(purchase_orders)
        supplier_data = prepare_supplier_data(supplier_data)
        
        print(f"✓ Sales data: {len(sales_data)} records")
        print(f"✓ Inventory data: {len(inventory_data)} records")
        print(f"✓ SKU master: {len(sku_master)} SKUs")
        print(f"✓ Purchase orders: {len(purchase_orders)} orders")
        print(f"✓ Supplier data: {len(supplier_data)} suppliers")
        
        return sales_data, inventory_data, sku_master, purchase_orders, supplier_data
        
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Please ensure 'InventoryRewired_Dataset.xlsx' is in the same directory")
        return None, None, None, None, None

def prepare_sales_data(df):
    """Clean and prepare sales data"""
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove any negative quantities (data quality check)
    df = df[df['quantity_sold'] >= 0]
    
    # Add derived columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['week'] = df['date'].dt.isocalendar().week
    
    return df

def prepare_inventory_data(df):
    """Clean and prepare inventory data"""
    # Ensure non-negative stock levels
    df['current_stock'] = df['current_stock'].clip(lower=0)
    
    return df

def prepare_sku_master(df):
    """Clean and prepare SKU master data"""
    # Ensure positive values for costs and lead times
    df['unit_cost'] = df['unit_cost'].clip(lower=0)
    df['avg_lead_time'] = df['avg_lead_time'].clip(lower=1)
    df['shelf_life_days'] = df['shelf_life_days'].clip(lower=1)
    
    return df

def prepare_purchase_orders(df):
    """Clean and prepare purchase orders data"""
    # Convert date columns
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
    
    # Calculate order lead time
    df['order_lead_time'] = (df['expected_delivery_date'] - df['order_date']).dt.days
    
    # Ensure positive quantities
    df['quantity_ordered'] = df['quantity_ordered'].clip(lower=0)
    
    return df

def prepare_supplier_data(df):
    """Clean and prepare supplier data"""
    # Ensure service levels are between 0 and 1
    df['service_level'] = df['service_level'].clip(lower=0, upper=1)
    df['delay_rate'] = df['delay_rate'].clip(lower=0, upper=1)
    
    return df

def get_data_summary():
    """Generate summary statistics for all datasets"""
    summary = {
        'data_period': '3 months (Mar-May 2024)',
        'stores': 3,
        'skus': 10,
        'total_transactions': 'Dynamic based on data',
        'suppliers': 5
    }
    return summary