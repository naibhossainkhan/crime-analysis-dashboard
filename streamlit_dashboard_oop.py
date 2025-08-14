#!/usr/bin/env python3
"""
🚔 Crime Analysis Dashboard - OOP Version
========================================

A comprehensive crime analysis and prediction dashboard built with Object-Oriented Programming principles.

This version follows OOP best practices with:
- Modular class-based architecture
- Separation of concerns
- Reusable components
- Clean code structure
- Easy maintenance and extension

Author: Data Science Team
Date: 2024
"""

from dashboard_main import CrimeAnalysisDashboard

def main():
    """
    Main entry point for the Crime Analysis Dashboard
    
    This function initializes and runs the dashboard using the OOP architecture.
    The dashboard is organized into:
    
    - DashboardComponents: UI components and styling
    - DataProcessor: Data manipulation and processing
    - ChartGenerator: Visualization creation
    - PredictionEngine: Crime prediction algorithms
    - PreventionStrategies: Prevention recommendations
    - AlgorithmMetrics: Performance metrics
    - Page Classes: Individual page functionality
    
    Each page is a separate class with its own render() method,
    making the code modular and easy to maintain.
    """
    
    try:
        # Initialize the dashboard
        dashboard = CrimeAnalysisDashboard()
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        print("Please check that all required files are present:")
        print("- crime_data_processed.csv")
        print("- dashboard_components.py")
        print("- dashboard_pages.py")
        print("- dashboard_main.py")

if __name__ == "__main__":
    main()
