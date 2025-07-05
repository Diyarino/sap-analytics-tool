# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:49:59 2025

@author: Diyar Altinses, M.Sc.
"""

# %%

import data_generator
import data_analysis
from sap_analytics_app import AnalysisApp
from PySide6.QtWidgets import QApplication
import sys

# %%

def main():
    print("Generate SAP-Data...")
    df = data_generator.generate_sap_like_data(5000)
    data_generator.save_data(df, "sap_data.csv")
    
    print("\nAnalysze Data...")
    analyzer = data_analysis.SAPDataAnalyzer("sap_data.csv")
    reports = analyzer.generate_all_reports()
    
    print("\nGeneral Statistics:")
    print(f"Amount of datasets: {reports['basic_statistics']['total_records']}")
    print(f"Average value: {reports['basic_statistics']['numeric_fields']['Amount']['mean']:.2f} EUR")
    
    print("\nStart GUI...")
    app = QApplication(sys.argv)
    window = AnalysisApp()
    window.show()
    sys.exit(app.exec())

# %%


if __name__ == "__main__":
    main()