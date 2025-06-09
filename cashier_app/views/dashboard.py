"""Dashboard view with simple navigation sidebar."""

from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QWidget,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from cashier_app.main_window import MainWindow
from cashier_app.config.settings import ICONS_PATH
from cashier_app.views.sales_view import SalesView
from cashier_app.views.product_entry_view import ProductEntryView
from cashier_app.views.debt_view import DebtView
from cashier_app.views.reports_view import ReportsView
from cashier_app.views.price_update_view import PriceUpdateView


class Dashboard(MainWindow):
    """Main dashboard window containing a sidebar to switch views."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("لوحة التحكم")

        container = QWidget()
        container_layout = QHBoxLayout(container)

        sidebar = QVBoxLayout()
        container_layout.addLayout(sidebar)

        self.stack = QStackedWidget()
        container_layout.addWidget(self.stack)

        # instantiate views
        self.views = [
            ("المبيعات", "barcode.svg", SalesView()),
            ("المنتجات", "plus.svg", ProductEntryView()),
            ("الدائنون", "check.svg", DebtView()),
            ("التقارير", "print.svg", ReportsView()),
            ("تحديث الأسعار", "cancel.svg", PriceUpdateView()),
        ]

        for index, (label, icon_file, view) in enumerate(self.views):
            button = QPushButton(label)
            icon_path = ICONS_PATH / icon_file
            if icon_path.exists():
                button.setIcon(QIcon(str(icon_path)))
                button.setIconSize(QSize(24, 24))
            button.clicked.connect(lambda _=False, i=index: self.stack.setCurrentIndex(i))
            sidebar.addWidget(button)
            self.stack.addWidget(view)

        sidebar.addStretch()

        welcome = QLabel("مرحباً بك في لوحة التحكم")
        welcome.setStyleSheet("font-size: 18px")
        self.layout.addWidget(welcome)
        self.layout.addWidget(container)
