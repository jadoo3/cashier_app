# views/report_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QDateEdit, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QDate
from controllers.report_controller import ReportController
import pandas as pd

class ReportView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ReportController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Date range selection
        date_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        
        date_layout.addWidget(QLabel("من:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("إلى:"))
        date_layout.addWidget(self.end_date)
        layout.addLayout(date_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.sales_report_btn = QPushButton("تقرير المبيعات")
        self.low_stock_btn = QPushButton("تقرير المخزون المنخفض")
        
        self.sales_report_btn.clicked.connect(self.show_sales_report)
        self.low_stock_btn.clicked.connect(self.show_low_stock)
        
        button_layout.addWidget(self.sales_report_btn)
        button_layout.addWidget(self.low_stock_btn)
        layout.addLayout(button_layout)

        # Results table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def show_sales_report(self):
        df = self.controller.sales_report(
            self.start_date.date().toPyDate(),
            self.end_date.date().toPyDate()
        )
        self.display_dataframe(df)

    def show_low_stock(self):
        df = self.controller.low_stock()
        self.display_dataframe(df)

    def display_dataframe(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()
