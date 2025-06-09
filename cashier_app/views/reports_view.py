"""Reports view."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReportsView(QWidget):
    """Interface for viewing reports."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("التقارير")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("واجهة التقارير"))
