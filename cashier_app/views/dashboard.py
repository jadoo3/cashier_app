"""Dashboard view."""

from PyQt5.QtWidgets import QLabel, QVBoxLayout

from cashier_app.main_window import MainWindow


class Dashboard(MainWindow):
    """Main dashboard window for navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("لوحة التحكم")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("مرحباً بك في لوحة التحكم"))
        self.layout.addLayout(layout)
