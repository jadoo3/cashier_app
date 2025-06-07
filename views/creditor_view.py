# views/creditor_view.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem
)
from controllers.creditor_controller import CreditorController

class CreditorView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = CreditorController()
        self._setup_ui()
        self.load_creditors()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        hl = QHBoxLayout()
        self.btn_add = QPushButton("إضافة دائِن")
        self.btn_refresh = QPushButton("تحديث القائمة")
        hl.addWidget(self.btn_add)
        hl.addWidget(self.btn_refresh)
        layout.addLayout(hl)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "اسم", "الرصيد"])
        layout.addWidget(self.table)

        self.btn_add.clicked.connect(self.add_creditor)
        self.btn_refresh.clicked.connect(self.load_creditors)

    def load_creditors(self):
        self.table.setRowCount(0)
        for c in self.controller.list_all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(c.id)))
            self.table.setItem(row, 1, QTableWidgetItem(c.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{c.balance:.2f}"))

    def add_creditor(self):
        # To be implemented: dialog for adding a new creditor
        pass
