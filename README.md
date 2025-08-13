# README.md
# Inventory Rewired - Business Analytics Club IITB

## Project Overview
**Objective**: Optimize inventory and replenishment decisions for Retail Craft Pvt. Ltd. to reduce out-of-stock events and excess inventory holding costs by 10% over a 3-month horizon.

## Project Structure
```
inventory-rewired/
├── main_analysis.py           # Main execution script
├── data_loader.py            # Data loading and preparation
├── demand_analysis.py        # Demand analysis and ABC classification  
├── inventory_models.py       # EOQ, ROP, and safety stock calculations
├── cost_benefit.py          # Cost-benefit analysis and simulation
├── report_generator.py      # Report generation and export
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── run_analysis.bat        # Windows execution script
├── run_analysis.sh         # Unix/Linux execution script
└── InventoryRewired_Dataset.xlsx  # Input data file
```

## Key Features
- **ABC Classification**: Pareto analysis for SKU prioritization
- **EOQ Optimization**: Economic Order Quantity calculations
- **Safety Stock**: Dynamic safety stock based on demand variability
- **Reorder Points**: Automated reorder point calculations
- **Cost-Benefit Analysis**: Comprehensive financial impact assessment
- **Simulation**: 3-week inventory performance simulation

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Excel file handling capability

### Quick Start
1. **Download all files** to a single directory
2. **Place the Excel data file** (`InventoryRewired_Dataset.xlsx`) in the same directory
3. **Install dependencies**:
   ```bash
   pip install pandas numpy scipy openpyxl xlsxwriter
   ```
4. **Run the analysis**:
   ```bash
   python main_analysis.py
   ```

### Alternative Execution Methods

**Windows (Batch Script)**:
```batch
run_analysis.bat
```

**Linux/Mac (Shell Script)**:
```bash
chmod +x run_analysis.sh
./run_analysis.sh
```

## Data Requirements

### Input File Structure
The analysis requires `InventoryRewired_Dataset.xlsx` with the following sheets:
- **Sales_data**: Daily sales transactions (date, store_id, sku_id, quantity_sold)
- **Inventory_data**: Current stock levels (store_id, sku_id, current_stock)
- **SKU_master**: Product information (sku_id, category, unit_cost, avg_lead_time, shelf_life_days)
- **Purchase_orders**: Historical orders (po_id, sku_id, order_date, expected_delivery_date, quantity_ordered)
- **Supplier_data**: Supplier performance (sku_id, supplier_id, service_level, delay_rate)

## Methodology

### ABC Classification
- **Class A**: Top 70% of revenue → 98% service level
- **Class B**: Next 20% of revenue → 95% service level  
- **Class C**: Remaining 10% of revenue → 90% service level

### Inventory Optimization
- **EOQ Formula**: √((2 × Annual Demand × Ordering Cost) / Holding Cost)
- **Safety Stock**: Z-score × Standard Deviation × √(Lead Time)
- **Reorder Point**: (Average Daily Demand × Lead Time) + Safety Stock

### Performance Metrics
- Fill Rate improvement to 98%
- Inventory Turnover optimization
- Cost reduction through better inventory management

## Output Files

### Generated Reports
1. **inventory_analysis_results.xlsx**: Complete analysis with multiple sheets
   - Demand Analysis
   - ABC Classification  
   - Inventory Model Recommendations
   - Simulation Results
   - Cost-Benefit Analysis
   - Dashboard Summary

2. **executive_summary.txt**: Comprehensive executive summary for leadership

### Key Results Expected
- **Annual Savings**: ₹3,00,000+
- **ROI**: 300%+
- **Payback Period**: 4-6 months
- **Fill Rate Improvement**: From ~87% to 98%

## Module Details

### main_analysis.py
Central execution script that coordinates the entire analysis workflow.

### data_loader.py
- Loads data from Excel sheets
- Performs data quality checks
- Prepares data for analysis

### demand_analysis.py
- Calculates demand patterns and variability
- Performs ABC classification based on revenue contribution
- Generates demand forecasts

### inventory_models.py
- Calculates EOQ for each SKU
- Determines optimal safety stock levels
- Sets reorder points based on service level targets

### cost_benefit.py
- Performs comprehensive cost-benefit analysis
- Runs simulation to validate model performance
- Calculates ROI and payback period

### report_generator.py
- Generates executive summary
- Creates Excel dashboard
- Exports all results for presentation

## Troubleshooting

### Common Issues
1. **File not found error**: Ensure `InventoryRewired_Dataset.xlsx` is in the same directory
2. **Module import errors**: Install required packages using pip
3. **Permission errors**: Ensure write permissions for output files

### Dependencies
```
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
openpyxl>=3.0.7
xlsxwriter>=3.0.3
```

## Business Impact

### Expected Improvements
- **Operational Efficiency**: Reduced manual inventory management
- **Customer Satisfaction**: Higher fill rates and product availability
- **Financial Performance**: Lower holding costs and improved cash flow
- **Strategic Advantage**: Data-driven inventory decisions

### Implementation Timeline
- **Week 1-2**: Data analysis and model validation
- **Week 3-4**: System setup and initial parameters
- **Month 2**: Full implementation and staff training
- **Month 3+**: Monitoring and continuous optimization

## Contact & Support
This project was developed for the Business Analytics Bootcamp 2025. For technical questions or implementation support, refer to the comprehensive documentation and code comments.

---

## License
Educational project for Business Analytics Bootcamp 2025.

**Last Updated**: August 2025
