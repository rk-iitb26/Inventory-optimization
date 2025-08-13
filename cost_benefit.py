# cost_benefit.py
# Cost-Benefit Analysis and Simulation Module
# Inventory Rewired Project

import pandas as pd
import numpy as np
import random

def calculate_cost_benefit_analysis(inventory_model, current_kpis):
    """Calculate cost-benefit analysis of proposed inventory model"""
    print("Calculating cost-benefit analysis...")
    
    # Current state costs
    current_total_inventory_value = current_kpis['total_inventory_value']
    current_fill_rate = current_kpis['fill_rate'] / 100
    
    # Proposed state calculations
    proposed_inventory = inventory_model.groupby('sku_id').agg({
        'max_inventory': 'mean',
        'unit_cost': 'first',
        'total_annual_cost': 'sum',
        'abc_class': 'first'
    })
    
    proposed_total_inventory_value = (
        proposed_inventory['max_inventory'] * proposed_inventory['unit_cost']
    ).sum()
    
    # Cost comparison
    inventory_reduction = current_total_inventory_value - proposed_total_inventory_value
    holding_cost_savings = inventory_reduction * 0.25  # 25% holding cost
    
    # Revenue impact from improved fill rate
    target_fill_rate = 0.98  # 98% target
    fill_rate_improvement = target_fill_rate - current_fill_rate
    
    # Estimate current annual revenue
    avg_daily_revenue = inventory_model['annual_revenue'].sum() / 365
    current_annual_revenue = avg_daily_revenue * 365
    
    # Additional revenue from reduced stockouts
    revenue_from_improved_service = current_annual_revenue * fill_rate_improvement
    
    # Calculate total annual benefits
    total_annual_savings = holding_cost_savings + revenue_from_improved_service
    
    # Implementation costs (one-time)
    implementation_cost = 100000  # ₹1 lakh for system setup and training
    
    # ROI calculations
    roi_percentage = (total_annual_savings / implementation_cost) * 100
    payback_months = (implementation_cost / total_annual_savings) * 12
    
    cost_benefit = {
        'current_inventory_value': current_total_inventory_value,
        'proposed_inventory_value': proposed_total_inventory_value,
        'inventory_reduction': inventory_reduction,
        'holding_cost_savings': holding_cost_savings,
        'revenue_from_improved_service': revenue_from_improved_service,
        'total_annual_savings': total_annual_savings,
        'implementation_cost': implementation_cost,
        'roi_percentage': roi_percentage,
        'payback_months': payback_months,
        'current_fill_rate': current_fill_rate * 100,
        'target_fill_rate': target_fill_rate * 100
    }
    
    print(f"✓ Annual savings: ₹{total_annual_savings:,.0f}")
    print(f"✓ ROI: {roi_percentage:.1f}%")
    print(f"✓ Payback period: {payback_months:.1f} months")
    
    return cost_benefit

def simulate_inventory_performance(inventory_model, sales_data, simulation_days=21):
    """Simulate inventory performance over 3 weeks"""
    print(f"Running {simulation_days}-day simulation...")
    
    # Initialize simulation data
    sim_results = []
    
    # Get unique store-SKU combinations
    store_sku_combinations = inventory_model[['store_id', 'sku_id', 'reorder_point', 
                                           'eoq', 'safety_stock', 'avg_daily_demand']].copy()
    
    for idx, row in store_sku_combinations.iterrows():
        store_id = row['store_id']
        sku_id = row['sku_id']
        rop = row['reorder_point']
        eoq = row['eoq']
        safety_stock = row['safety_stock']
        avg_demand = row['avg_daily_demand']
        
        # Get current stock (simulate starting inventory)
        current_stock = rop + (eoq * 0.5)  # Start at mid-cycle
        
        # Daily simulation
        stockouts = 0
        total_demand = 0
        total_sales = 0
        orders_placed = 0
        
        for day in range(simulation_days):
            # Generate daily demand (with variability)
            daily_demand = max(0, np.random.poisson(avg_demand))
            total_demand += daily_demand
            
            # Check if we can fulfill demand
            if current_stock >= daily_demand:
                total_sales += daily_demand
                current_stock -= daily_demand
            else:
                total_sales += current_stock
                stockouts += 1
                current_stock = 0
            
            # Check if reorder is needed
            if current_stock <= rop:
                current_stock += eoq  # Immediate delivery for simulation
                orders_placed += 1
        
        # Calculate performance metrics
        fill_rate = (total_sales / total_demand * 100) if total_demand > 0 else 100
        
        sim_results.append({
            'store_id': store_id,
            'sku_id': sku_id,
            'total_demand': total_demand,
            'total_sales': total_sales,
            'stockout_days': stockouts,
            'fill_rate': fill_rate,
            'orders_placed': orders_placed,
            'final_stock': current_stock
        })
    
    simulation_df = pd.DataFrame(sim_results)
    
    # Summary statistics
    simulation_summary = {
        'avg_fill_rate': simulation_df['fill_rate'].mean(),
        'total_stockout_days': simulation_df['stockout_days'].sum(),
        'total_orders_placed': simulation_df['orders_placed'].sum(),
        'skus_with_stockouts': len(simulation_df[simulation_df['stockout_days'] > 0]),
        'perfect_fill_rate_skus': len(simulation_df[simulation_df['fill_rate'] == 100])
    }
    
    print(f"✓ Simulation completed:")
    print(f"  - Average fill rate: {simulation_summary['avg_fill_rate']:.1f}%")
    print(f"  - Total stockout days: {simulation_summary['total_stockout_days']}")
    print(f"  - SKUs achieving 100% fill rate: {simulation_summary['perfect_fill_rate_skus']}")
    
    return simulation_df, simulation_summary

def calculate_working_capital_impact(inventory_model, current_kpis):
    """Calculate working capital impact"""
    
    # Current working capital
    current_wc = current_kpis['total_inventory_value']
    
    # Proposed working capital
    proposed_wc = inventory_model.groupby('sku_id').apply(
        lambda x: (x['max_inventory'].mean() * x['unit_cost'].iloc[0])
    ).sum()
    
    # Working capital reduction
    wc_reduction = current_wc - proposed_wc
    wc_reduction_percentage = (wc_reduction / current_wc) * 100
    
    # Free up cash for other investments
    opportunity_cost_savings = wc_reduction * 0.12  # 12% cost of capital
    
    return {
        'current_working_capital': current_wc,
        'proposed_working_capital': proposed_wc,
        'working_capital_reduction': wc_reduction,
        'wc_reduction_percentage': wc_reduction_percentage,
        'opportunity_cost_savings': opportunity_cost_savings
    }