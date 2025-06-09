"""Sales entry view with barcode scanning."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class SalesView(QWidget):
    """Interface for recording sales."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("المبيعات")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("واجهة المبيعات"))
