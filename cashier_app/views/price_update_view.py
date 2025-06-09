"""Price update view."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class PriceUpdateView(QWidget):
    """Interface for bulk price updates."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("تحديث الأسعار")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("واجهة تحديث الأسعار"))
