@echo off
echo ====================================
echo INVENTORY REWIRED - ANALYSIS SCRIPT
echo Business Analytics Bootcamp 2025
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Checking for required packages...

REM Install required packages if not present
echo Installing/updating required packages...
pip install pandas numpy scipy openpyxl xlsxwriter
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)

echo.
echo Packages installed successfully.

REM Check if data file exists
if not exist "InventoryRewired_Dataset.xlsx" (
    echo ERROR: Data file 'InventoryRewired_Dataset.xlsx' not found
    echo Please ensure the Excel file is in the same directory as this script
    pause
    exit /b 1
)

echo Data file found.
echo.
echo Starting inventory analysis...
echo.

REM Run the main analysis
python main_analysis.py

if errorlevel 1 (
    echo.
    echo ERROR: Analysis failed to complete
    echo Check the error messages above for details
) else (
    echo.
    echo ====================================
    echo ANALYSIS COMPLETED SUCCESSFULLY!
    echo ====================================
    echo.
    echo Output files generated:
    echo - inventory_analysis_results.xlsx
    echo - executive_summary.txt
    echo.
    echo You can now open these files to view the results.
)

echo.
pause