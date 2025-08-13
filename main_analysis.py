# main_analysis.py
# Inventory Rewired - Main Analysis Script
# Business Analytics Bootcamp 2025
# Retail Craft Pvt. Ltd. Inventory Optimization

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_loader import load_and_prepare_data
from demand_analysis import analyze_demand_patterns, abc_classification
from inventory_models import calculate_eoq_and_safety_stock, calculate_current_performance_kpis
from cost_benefit import calculate_cost_benefit_analysis, simulate_inventory_performance
from report_generator import generate_executive_summary, create_dashboard_summary, export_results

def main():
    """Main execution function"""
    print("=" * 60)
    print("INVENTORY REWIRED - COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    # Step 1: Load and prepare data
    print("\n1. LOADING DATA...")
    sales_data, inventory_data, sku_master, purchase_orders, supplier_data = load_and_prepare_data()
    
    # Step 2: Analyze demand patterns
    print("\n2. ANALYZING DEMAND PATTERNS...")
    demand_analysis = analyze_demand_patterns(sales_data, sku_master)
    
    # Step 3: Perform ABC classification
    print("\n3. PERFORMING ABC CLASSIFICATION...")
    abc_results, abc_summary = abc_classification(sales_data, sku_master)
    
    # Step 4: Calculate inventory model parameters
    print("\n4. CALCULATING INVENTORY MODEL...")
    inventory_model = calculate_eoq_and_safety_stock(demand_analysis, abc_results)
    
    # Step 5: Calculate current performance KPIs
    print("\n5. CALCULATING CURRENT KPIS...")
    current_kpis = calculate_current_performance_kpis(sales_data, inventory_data, sku_master)
    
    # Step 6: Perform cost-benefit analysis
    print("\n6. COST-BENEFIT ANALYSIS...")
    cost_benefit = calculate_cost_benefit_analysis(inventory_model, current_kpis)
    
    # Step 7: Run simulation
    print("\n7. RUNNING SIMULATION...")
    simulation_results, simulation_summary = simulate_inventory_performance(inventory_model, sales_data)
    
    # Step 8: Generate reports
    print("\n8. GENERATING REPORTS...")
    executive_summary = generate_executive_summary()
    dashboard_data = create_dashboard_summary()
    
    # Step 9: Export results
    print("\n9. EXPORTING RESULTS...")
    export_results(
        demand_analysis, abc_results, inventory_model, 
        simulation_results, cost_benefit, dashboard_data
    )
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    # Display key results
    print(f"\nKEY RESULTS:")
    print(f"- Current Fill Rate: {current_kpis['fill_rate']}%")
    print(f"- Target Fill Rate: 98.0%")
    print(f"- Annual Savings: ₹{cost_benefit['total_annual_savings']:,.0f}")
    print(f"- ROI: {cost_benefit['roi_percentage']}%")
    print(f"- Payback Period: {cost_benefit['payback_months']} months")
    print(f"\nFiles exported: inventory_analysis_results.xlsx, executive_summary.txt")

if __name__ == "__main__":
    main()