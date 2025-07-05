
# %% imports

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QFileDialog, QTabWidget, QTextEdit, 
                              QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
from matplotlib.figure import Figure
import pandas as pd
import io
import data_analysis

from canvas import MplCanvas

# %%

class AnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP Datenanalyse Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        self.analyzer = None
        self.reports = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # data selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Keine Datei ausgewählt")
        file_button = QPushButton("Daten auswählen")
        file_button.clicked.connect(self.load_data)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(file_button)
        
        # Analysis-Button
        analyze_button = QPushButton("Analyse durchführen")
        analyze_button.clicked.connect(self.run_analysis)
        
        # Tabs for diverse Analysen
        self.tabs = QTabWidget()
        
        # Summary Tab
        self.summary_tab = QWidget()
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        summary_layout = QVBoxLayout()
        summary_layout.addWidget(self.summary_text)
        self.summary_tab.setLayout(summary_layout)
        self.tabs.addTab(self.summary_tab, "Zusammenfassung")
        
        # Time-series Tab
        self.time_series_tab = QWidget()
        self.time_series_plot = MplCanvas(self.time_series_tab, width=10, height=6, dpi=100)
        time_series_layout = QVBoxLayout()
        time_series_layout.addWidget(self.time_series_plot)
        self.time_series_tab.setLayout(time_series_layout)
        self.tabs.addTab(self.time_series_tab, "Zeitreihen")
        
        # Cost Tab
        self.cost_center_tab = QWidget()
        self.cost_center_plot = MplCanvas(self.cost_center_tab, width=10, height=6, dpi=100)
        cost_center_layout = QVBoxLayout()
        cost_center_layout.addWidget(self.cost_center_plot)
        self.cost_center_tab.setLayout(cost_center_layout)
        self.tabs.addTab(self.cost_center_tab, "Kostenstellen")
        
        # Materialanalysis Tab
        self.material_tab = QWidget()
        self.material_plot = MplCanvas(self.material_tab, width=10, height=6, dpi=100)
        material_layout = QVBoxLayout()
        material_layout.addWidget(self.material_plot)
        self.material_tab.setLayout(material_layout)
        self.tabs.addTab(self.material_tab, "Materialanalyse")
        
        # Tabular view
        self.table_tab = QWidget()
        self.data_table = QTableWidget()
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.data_table)
        self.table_tab.setLayout(table_layout)
        self.tabs.addTab(self.table_tab, "Tabellenansicht")
        
        # Report-selection
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Zeitreihenanalyse",
            "Kostenstellenanalyse",
            "Materialanalyse",
            "Dokumenttypenanalyse"
        ])
        self.report_combo.currentTextChanged.connect(self.update_report_view)
        
        # Mainlayout 
        main_layout.addLayout(file_layout)
        main_layout.addWidget(analyze_button)
        main_layout.addWidget(QLabel("Bericht auswählen:"))
        main_layout.addWidget(self.report_combo)
        main_layout.addWidget(self.tabs)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def load_data(self):
        """Lädt die Daten aus einer CSV-Datei"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Daten auswählen", "", "CSV Files (*.csv)")
        if file_path:
            self.file_label.setText(file_path)
            try:
                self.analyzer = data_analysis.SAPDataAnalyzer(file_path)
                self.show_data_preview(file_path)
            except Exception as e:
                self.summary_text.setText(f"Fehler beim Laden der Daten: {str(e)}")
    
    def show_data_preview(self, file_path):
        """Zeigt eine Vorschau der geladenen Daten"""
        df = pd.read_csv(file_path)
        self.display_data_table(df.head(20))
        
    def display_data_table(self, data):
        """Zeigt Daten in der Tabellenansicht"""
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
            
        self.data_table.setRowCount(df.shape[0])
        self.data_table.setColumnCount(df.shape[1])
        self.data_table.setHorizontalHeaderLabels(df.columns)
        
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.data_table.setItem(row, col, item)
        
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def run_analysis(self):
        """Führt die Analyse durch und zeigt die Ergebnisse"""
        if self.analyzer is None:
            self.summary_text.setText("Bitte zuerst Daten laden!")
            return
            
        try:
            self.reports = self.analyzer.generate_all_reports()
            self.display_summary()
            self.plot_time_series()
            self.plot_cost_centers()
            self.plot_material_analysis()
        except Exception as e:
            self.summary_text.setText(f"Fehler bei der Analyse: {str(e)}")
    
    def display_summary(self):
        """Zeigt die Analyse-Zusammenfassung"""
        if not self.reports:
            return
            
        basic = self.reports['basic_statistics']
        text = io.StringIO()
        
        text.write("=== GRUNDLEGENDE STATISTIK ===\n")
        text.write(f"Gesamtzahl der Datensätze: {basic['total_records']:,}\n")
        text.write(f"Zeitraum: {basic['time_period']['start']} bis {basic['time_period']['end']}\n\n")
        
        text.write("=== NUMERISCHE FELDER ===\n")
        for field, stats in basic['numeric_fields'].items():
            text.write(f"\n{field}:\n")
            for stat, value in stats.items():
                text.write(f"  {stat}: {value:,.2f}\n")
        
        text.write("\n=== KATEGORISCHE FELDER ===\n")
        for field, counts in basic['categorical_counts'].items():
            text.write(f"\n{field} Verteilung:\n")
            for value, count in counts.items():
                text.write(f"  {value}: {count:,} ({count/basic['total_records']:.1%})\n")
        
        self.summary_text.setText(text.getvalue())
    
    def plot_time_series(self):
        """Zeigt die Zeitreihenanalyse"""
        if not self.reports:
            return
            
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        ts_data = self.reports['time_series']
        ax.plot(ts_data.index, ts_data['sum'], label='Monatlicher Gesamtbetrag')
        if 'rolling_avg' in ts_data.columns:
            ax.plot(ts_data.index, ts_data['rolling_avg'], label='Gleitender Durchschnitt (3 Monate)')
        ax.set_title('Monatliche Beträge über die Zeit')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Betrag (EUR)')
        ax.legend()
        ax.grid(True)
        
        self.time_series_plot.figure = fig
        self.time_series_plot.draw()
    
    def plot_cost_centers(self):
        """Zeigt die Kostenstellenanalyse"""
        if not self.reports:
            return
            
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        cc_data = self.reports['cost_centers'].head(10)
        ax.bar(cc_data.index, cc_data['sum'])
        ax.set_title('Top 10 Kostenstellen nach Gesamtbetrag')
        ax.set_xlabel('Kostenstelle')
        ax.set_ylabel('Gesamtbetrag (EUR)')
        
        self.cost_center_plot.figure = fig
        self.cost_center_plot.draw()
    
    def plot_material_analysis(self):
        """Zeigt die Materialanalyse"""
        if not self.reports:
            return
            
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        mat_data = self.reports['material_analysis']
        colors = {'A': 'green', 'B': 'orange', 'C': 'red'}
        
        for abc_class, color in colors.items():
            subset = mat_data[mat_data['ABC_Class'] == abc_class]
            ax.scatter(subset.index, subset['Amount'], label=f'Klasse {abc_class}', color=color)
        
        ax.set_title('ABC-Analyse der Materialien')
        ax.set_xlabel('Materialnummer')
        ax.set_ylabel('Gesamtbetrag (EUR)')
        ax.legend()
        ax.grid(True)
        
        self.material_plot.figure = fig
        self.material_plot.draw()
    
    def update_report_view(self, report_name):
        """Aktualisiert die Ansicht basierend auf dem ausgewählten Report"""
        if not self.reports:
            return
            
        if report_name == "Zeitreihenanalyse":
            self.tabs.setCurrentWidget(self.time_series_tab)
        elif report_name == "Kostenstellenanalyse":
            self.tabs.setCurrentWidget(self.cost_center_tab)
        elif report_name == "Materialanalyse":
            self.tabs.setCurrentWidget(self.material_tab)
        elif report_name == "Dokumenttypenanalyse":
            self.display_data_table(self.reports['document_types'])

# %%


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalysisApp()
    window.show()
    sys.exit(app.exec())