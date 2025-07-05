
# SAP Data Analytics Tool (Python/PySide6)

SAP Data Analytics Tool is a comprehensive desktop application designed to simulate, process, and visualize enterprise-grade SAP transaction data for managerial decision-making. Built with Python and PySide6, this tool generates synthetic datasets that mirror real-world SAP ERP structures – including purchase orders, material movements, invoices, and cost center transactions – while providing robust analytical capabilities tailored for business intelligence.

Key functionalities include dynamic data generation with customizable parameters (time ranges, company hierarchies, and transaction volumes), enabling users to create scenario-specific datasets without compromising real SAP system integrity. The analytics engine performs multi-dimensional examinations across fiscal periods, including:  
- **Trend Analysis**: Rolling averages and period-over-period comparisons  
- **Cost Center Performance**: Spend allocation and variance detection  
- **Material Criticality**: ABC classification based on monetary impact  
- **Process Efficiency**: Document type throughput and bottlenecks  

The intuitive Qt-based interface allows non-technical users to:  
1) Import/export CSV datasets  
2) Filter records by date ranges, document types, or organizational units  
3) Generate presentation-ready visualizations (line charts, bar graphs, scatter plots)  
4) Export statistical summaries in tabular formats  

For technical users, the modular architecture supports extensions like:  
- Integration with real SAP systems via RFC connections  
- Custom KPI calculations in the analysis module  
- Advanced forecasting using ARIMA or Prophet models  

Ideal for SAP consultants, business analysts, and educators, this tool bridges the gap between raw transactional data and actionable business insights while eliminating the need for production system access during training or prototyping phases. The included PyInstaller configuration enables seamless Windows executable deployment for enterprise environments with strict Python runtime restrictions. 

<p align="center">
  <img src="animation.gif" width="600" height="300" alt="Decision Boundary Evolution">
</p>

---

## 📂 Repository Structure
```
.
├── data_generator.py   # Synthetic data creation
├── data_analysis.py    # Statistical calculations
├── sap_analytics_app.py # GUI implementation
├── main.py             # Entry point
├── sap_data.csv        # Sample dataset
└── requirements.txt    # Dependencies

```

---

## 🧩 Installation

1. Clone the repository:

```bash
git clone https://github.com/Diyarino/sap-analytics-tool.git
cd sap-analytics-tool
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Usage

Run the main script to train both models and generate evaluation plots:

```bash
python main.py
```

---

## 📦 Dependencies

* Python 3.8+
* pyside6
* pandas
* matplotlib
* numpy
* scipy
* pyinstaller

You can install all with:

```bash
pip install pyside6 pandas matplotlib seaborn numpy scipy pyinstaller
```

---

## 📚 Related Projects 

Below are selected related works and projects that inspired or complement this research:








