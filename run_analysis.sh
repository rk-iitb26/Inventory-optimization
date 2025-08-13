#!/bin/bash

echo "======================================"
echo "INVENTORY REWIRED - ANALYSIS SCRIPT"
echo "Business Analytics Bootcamp 2025"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "Python found. Checking for required packages..."

# Install required packages if not present
echo "Installing/updating required packages..."
pip3 install pandas numpy scipy openpyxl xlsxwriter

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install required packages"
    exit 1
fi

echo ""
echo "Packages installed successfully."

# Check if data file exists
if [ ! -f "InventoryRewired_Dataset.xlsx" ]; then
    echo "ERROR: Data file 'InventoryRewired_Dataset.xlsx' not found"
    echo "Please ensure the Excel file is in the same directory as this script"
    exit 1
fi

echo "Data file found."
echo ""
echo "Starting inventory analysis..."
echo ""

# Run the main analysis
python3 main_analysis.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Analysis failed to complete"
    echo "Check the error messages above for details"
    exit 1
else
    echo ""
    echo "======================================"
    echo "ANALYSIS COMPLETED SUCCESSFULLY!"
    echo "======================================"
    echo ""
    echo "Output files generated:"
    echo "- inventory_analysis_results.xlsx"
    echo "- executive_summary.txt"
    echo ""
    echo "You can now open these files to view the results."
fi

echo ""
echo "Press Enter to continue..."
read