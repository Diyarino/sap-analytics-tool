# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:43:51 2025

@author: Diyar Altinses, M.Sc.
"""

# %%

import pandas as pd
from datetime import datetime, timedelta
import random

# %%

def generate_sap_like_data(num_records=1000, days = 730):

    companies = ['COMP_A', 'COMP_B', 'COMP_C', 'COMP_D']
    plants = ['PLANT_{}'.format(i) for i in range(1, 6)]
    materials = ['MAT_{:05d}'.format(i) for i in range(1, 101)]
    cost_centers = ['CC_{:04d}'.format(i) for i in range(1001, 1021)]
    profit_centers = ['PC_{:03d}'.format(i) for i in range(101, 111)]
    gl_accounts = ['G/L_{:05d}'.format(i) for i in range(40000, 40100)]
    vendors = ['VEND_{:05d}'.format(i) for i in range(10001, 10101)]
    customers = ['CUST_{:05d}'.format(i) for i in range(50001, 50101)]
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days)
    date_range = [start_date + timedelta(days=x) for x in range(0, days)]
    
    data = []
    for _ in range(num_records):
        record_date = random.choice(date_range)
        quantity = round(random.uniform(1, 1000), 2)
        amount = round(random.uniform(10, 10000), 2)
        currency = 'EUR'
        doc_type = random.choice(['INV', 'PO', 'SO', 'GR', 'GI'])
        
        record = {
            'CompanyCode': random.choice(companies),
            'Plant': random.choice(plants),
            'Material': random.choice(materials),
            'Quantity': quantity,
            'Amount': amount,
            'Currency': currency,
            'DocumentType': doc_type,
            'PostingDate': record_date.strftime('%Y-%m-%d'),
            'CostCenter': random.choice(cost_centers),
            'ProfitCenter': random.choice(profit_centers),
            'GLAccount': random.choice(gl_accounts),
            'Vendor': random.choice(vendors) if doc_type in ['INV', 'PO', 'GR'] else '',
            'Customer': random.choice(customers) if doc_type in ['INV', 'SO', 'GI'] else '',
            'FiscalYear': record_date.year,
            'FiscalPeriod': record_date.month,
            'DocumentNumber': 'DOC_{:08d}'.format(random.randint(1, 99999999))
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

def save_data(df, filename='sap_data.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved in {filename}")

# %%

if __name__ == "__main__":
    df = generate_sap_like_data(5000)
    save_data(df)