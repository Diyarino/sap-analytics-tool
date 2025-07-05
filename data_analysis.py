# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:45:19 2025

@author: Diyar Altinses, M.Sc.
"""

# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%

class SAPDataAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.convert_data_types()
        
    def convert_data_types(self):
        """Convert data types for better analysis"""
        self.df['PostingDate'] = pd.to_datetime(self.df['PostingDate'])
        self.df['FiscalYear'] = self.df['FiscalYear'].astype('category')
        self.df['FiscalPeriod'] = self.df['FiscalPeriod'].astype('category')
        
    def basic_statistics(self):
        """Basic statistics"""
        stats = {
            'total_records': len(self.df),
            'time_period': {
                'start': self.df['PostingDate'].min(),
                'end': self.df['PostingDate'].max()
            },
            'numeric_fields': {
                'Quantity': {
                    'mean': self.df['Quantity'].mean(),
                    'median': self.df['Quantity'].median(),
                    'std': self.df['Quantity'].std(),
                    'min': self.df['Quantity'].min(),
                    'max': self.df['Quantity'].max()
                },
                'Amount': {
                    'mean': self.df['Amount'].mean(),
                    'median': self.df['Amount'].median(),
                    'std': self.df['Amount'].std(),
                    'min': self.df['Amount'].min(),
                    'max': self.df['Amount'].max()
                }
            },
            'categorical_counts': {
                'CompanyCode': self.df['CompanyCode'].value_counts().to_dict(),
                'DocumentType': self.df['DocumentType'].value_counts().to_dict(),
                'Plant': self.df['Plant'].value_counts().to_dict()
            }
        }
        return stats
    
    def time_series_analysis(self):
        """Time series analysis of amounts"""
        ts_df = self.df.set_index('PostingDate').sort_index()
        monthly = ts_df.resample('M')['Amount'].agg(['sum', 'mean', 'count'])
        
        # Trend analysis
        monthly['rolling_avg'] = monthly['sum'].rolling(window=3).mean()
        
        return monthly
    
    def cost_center_analysis(self):
        """Cost center analysis"""
        cc_analysis = self.df.groupby('CostCenter')['Amount'].agg(['sum', 'mean', 'count'])
        cc_analysis['percentage'] = cc_analysis['sum'] / cc_analysis['sum'].sum() * 100
        return cc_analysis.sort_values('sum', ascending=False)
    
    def material_analysis(self):
        """Material valuation (ABC analysis)"""
        material_value = self.df.groupby('Material')['Amount'].sum().reset_index()
        material_value = material_value.sort_values('Amount', ascending=False)
        material_value['cumulative_percentage'] = material_value['Amount'].cumsum() / material_value['Amount'].sum() * 100
        
        # ABC classification
        material_value['ABC_Class'] = np.where(
            material_value['cumulative_percentage'] <= 80, 'A',
            np.where(material_value['cumulative_percentage'] <= 95, 'B', 'C')
        )
        
        return material_value.set_index('Material')
    
    def correlation_analysis(self):
        """Correlation analysis between quantity and amount"""
        return self.df[['Quantity', 'Amount']].corr()
    
    def document_type_analysis(self):
        """Document type analysis"""
        doc_analysis = self.df.groupby('DocumentType')['Amount'].agg(['sum', 'mean', 'count'])
        doc_analysis['percentage'] = doc_analysis['sum'] / doc_analysis['sum'].sum() * 100
        return doc_analysis.sort_values('sum', ascending=False)
    
    def generate_all_reports(self):
        """Generate all analysis reports"""
        reports = {
            'basic_statistics': self.basic_statistics(),
            'time_series': self.time_series_analysis(),
            'cost_centers': self.cost_center_analysis(),
            'material_analysis': self.material_analysis(),
            'correlation': self.correlation_analysis(),
            'document_types': self.document_type_analysis()
        }
        return reports
    
    def plot_time_series(self):
        """Visualize time series data"""
        ts_data = self.time_series_analysis()
        
        plt.figure(figsize=(12, 6))
        plt.plot(ts_data.index, ts_data['sum'], label='Monthly total amount')
        plt.plot(ts_data.index, ts_data['rolling_avg'], label='3-month moving average')
        plt.title('Monthly amounts over time')
        plt.xlabel('Date')
        plt.ylabel('Amount (EUR)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        return plt
    
    def plot_cost_centers(self):
        """Visualize top cost centers"""
        cc_data = self.cost_center_analysis().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=cc_data.index, y=cc_data['sum'])
        plt.title('Top 10 cost centers by total amount')
        plt.xlabel('Cost center')
        plt.ylabel('Total amount (EUR)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
    
    def plot_material_abc(self):
        """Visualize material ABC analysis"""
        mat_data = self.material_analysis()
        
        plt.figure(figsize=(12, 6))
        for abc_class, color in zip(['A', 'B', 'C'], ['green', 'orange', 'red']):
            subset = mat_data[mat_data['ABC_Class'] == abc_class]
            plt.scatter(subset.index, subset['Amount'], label=f'Class {abc_class}', color=color)
        
        plt.title('Material ABC analysis')
        plt.xlabel('Material number')
        plt.ylabel('Total amount (EUR)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        return plt