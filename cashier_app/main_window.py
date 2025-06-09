"""Main application window."""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """Provides the base window layout."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("نظام نقاط البيع")
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)
