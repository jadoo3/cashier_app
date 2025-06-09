"""Product entry view."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ProductEntryView(QWidget):
    """Interface for adding or editing products."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("إدخال المنتج")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("إضافة أو تعديل المنتجات"))
