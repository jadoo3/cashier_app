"""Debt management view."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class DebtView(QWidget):
    """Interface for managing creditors."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("إدارة الديون")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("واجهة الدائنين"))
