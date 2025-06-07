# views/dashboard.py
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QLineEdit, QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer
from config.settings import ICONS_PATH

# استخدم واردات مطلقة
from views.sales_view       import SalesView
from views.product_view     import ProductView
from views.creditor_view    import CreditorView
from views.report_view      import ReportView
from views.db_explorer_view import DBExplorerView

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("كاشير البقالة")
        self.resize(1280, 800)
        self.current_button = None  # تعريف المتغير قبل استخدامه
        self._setup_ui()
        self._setup_timer()

    def _setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # تحديث كل ثانية

    def update_datetime(self):
        current = datetime.now()
        self.lbl_datetime.setText(current.strftime("%d %B %Y، %I:%M %p"))

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #f0f0f0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        # Logo
        logo = QLabel()
        logo.setPixmap(QIcon(os.path.join(ICONS_PATH, 'logo.svg')).pixmap(40, 40))
        header_layout.addWidget(logo)

        # Title
        title = QLabel("كاشير البقالة")
        title.setFont(QFont("Tajawal", 16))
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Exchange rates
        rates_widget = QWidget()
        rates_layout = QHBoxLayout(rates_widget)
        rates_layout.setSpacing(10)

        self.lbl_sy = QLabel("1$ =")
        self.txt_sy = QLineEdit("15000")
        self.txt_sy.setFixedWidth(80)
        self.lbl_sy_currency = QLabel("ليرة سورية")

        self.lbl_tr = QLabel("1$ =")
        self.txt_tr = QLineEdit("20")
        self.txt_tr.setFixedWidth(80)
        self.lbl_tr_currency = QLabel("ليرة تركية")

        btn_update = QPushButton()
        btn_update.setIcon(QIcon(os.path.join(ICONS_PATH, 'refresh.svg')))
        btn_update.setFixedSize(30, 30)

        rates_layout.addWidget(self.lbl_sy)
        rates_layout.addWidget(self.txt_sy)
        rates_layout.addWidget(self.lbl_sy_currency)
        rates_layout.addWidget(self.lbl_tr)
        rates_layout.addWidget(self.txt_tr)
        rates_layout.addWidget(self.lbl_tr_currency)
        rates_layout.addWidget(btn_update)

        header_layout.addWidget(rates_widget)

        # DateTime
        self.lbl_datetime = QLabel()
        self.lbl_datetime.setFont(QFont("Tajawal", 10))
        header_layout.addWidget(self.lbl_datetime)

        main_layout.addWidget(header)

        # Main content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f8f9fa;")
        vbox = QVBoxLayout(sidebar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(2)

        # Sidebar buttons
        self.btn_sales = self._create_sidebar_button("المبيعات", "sales.svg")
        self.btn_products = self._create_sidebar_button("إدخال المنتجات", "products.svg")
        self.btn_invoices = self._create_sidebar_button("إدخال الفواتير", "invoices.svg")
        self.btn_creditors = self._create_sidebar_button("إدارة الدائنين", "creditors.svg")
        self.btn_reports = self._create_sidebar_button("التقارير", "reports.svg")
        self.btn_price = self._create_sidebar_button("تحديث الأسعار", "price.svg")

        for btn in [self.btn_sales, self.btn_products, self.btn_invoices,
                   self.btn_creditors, self.btn_reports, self.btn_price]:
            vbox.addWidget(btn)

        vbox.addStretch()
        content_layout.addWidget(sidebar)

        # Stacked pages
        self.stack = QStackedWidget()
        self.page_sales = SalesView()
        self.page_products = ProductView()
        self.page_creditors = CreditorView()
        self.page_reports = ReportView()
        self.page_explorer = DBExplorerView()

        self.stack.addWidget(self.page_sales)         # index 0
        self.stack.addWidget(self.page_products)      # index 1
        self.stack.addWidget(self.page_creditors)     # index 2
        self.stack.addWidget(self.page_reports)       # index 3
        self.stack.addWidget(self.page_explorer)      # index 4

        content_layout.addWidget(self.stack, 1)
        main_layout.addWidget(content)

        # Connect buttons
        self.btn_sales.clicked.connect(lambda: self.switch_page(0, self.btn_sales))
        self.btn_products.clicked.connect(lambda: self.switch_page(1, self.btn_products))
        self.btn_creditors.clicked.connect(lambda: self.switch_page(2, self.btn_creditors))
        self.btn_reports.clicked.connect(lambda: self.switch_page(3, self.btn_reports))
        self.btn_price.clicked.connect(lambda: self.switch_page(1, self.btn_price))  # reuse products page

        # Set initial page
        self.switch_page(0, self.btn_sales)

    def switch_page(self, index, button):
        # Uncheck previous button
        if self.current_button:
            self.current_button.setChecked(False)
        
        # Set new button as checked
        button.setChecked(True)
        self.current_button = button
        
        # Switch page
        self.stack.setCurrentIndex(index)

    def _create_sidebar_button(self, text, icon_name):
        btn = QPushButton(text)
        btn.setIcon(QIcon(os.path.join(ICONS_PATH, icon_name)))
        btn.setFixedHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                text-align: right;
                padding: 5px 10px;
                border: none;
                border-radius: 0;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QPushButton:checked {
                background-color: #e9ecef;
                border-right: 3px solid #007bff;
            }
        """)
        btn.setCheckable(True)
        return btn
