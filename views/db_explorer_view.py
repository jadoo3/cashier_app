# views/db_explorer_view.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem
)
from controllers.db_explorer_controller import DBExplorerController
import pandas as pd

class DBExplorerView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = DBExplorerController()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.combo = QComboBox()
        self.combo.addItems(self.controller.list_tables())
        self.btn_load = QPushButton("تحميل الجدول")
        layout.addWidget(self.combo)
        layout.addWidget(self.btn_load)
        self.table = QTableWidget(0, 0)
        layout.addWidget(self.table)

        self.btn_load.clicked.connect(self.load_table)

    def load_table(self):
        name = self.combo.currentText()
        data = self.controller.fetch_all(name, limit=1000)
        cols = [col['name'] for col in self.controller.get_columns(name)]
        df = pd.DataFrame(data, columns=cols)
        self.table.clear()
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(list(df.columns))
        for i, row in df.iterrows():
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
