# views/sales_view.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QSpinBox, QDoubleSpinBox, QFrame, QMessageBox, QListWidget,
    QListWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from datetime import datetime
import os
from config.settings import ICONS_PATH
from controllers.sales_controller import SalesController
from controllers.product_controller import ProductController
from utils.error_handler import ErrorHandlerMixin
from utils.validators import validate_sale_data, ValidationError
from models.product import OutOfStockError
import logging

logger = logging.getLogger(__name__)

class SalesView(QWidget, ErrorHandlerMixin):
    def __init__(self):
        super().__init__()
        self.sales_controller = SalesController()
        self.product_controller = ProductController()
        self.current_invoice_number = self.sales_controller.get_next_invoice_number()
        self.barcode_buffer = ""
        self.barcode_timer = QTimer()
        self.barcode_timer.setSingleShot(True)
        self.barcode_timer.timeout.connect(self.process_barcode)
        self.current_items = []
        self.total_amount = 0.0
        self.paid_amount = 0.0
        self.init_ui()
        self._connect_signals()

    def _setup_barcode_timer(self):
        """إعداد مؤقت لقراءة الباركود"""
        self.barcode_timer = QTimer()
        self.barcode_timer.setSingleShot(True)
        self.barcode_timer.timeout.connect(self.process_barcode)

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Left side - Product Entry
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن المنتج أو امسح الباركود")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        
        # تحسين شكل القائمة المنسدلة
        self.suggestions_combo = QComboBox()
        self.suggestions_combo.setMaximumHeight(30)
        self.suggestions_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(icons/down-arrow.svg);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #e0e0e0;
                selection-color: black;
            }
        """)
        self.suggestions_combo.hide()
        
        self.barcode_btn = QPushButton()
        self.barcode_btn.setIcon(QIcon(os.path.join(ICONS_PATH, 'barcode.svg')))
        self.barcode_btn.setFixedSize(40, 40)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.suggestions_combo)
        search_layout.addWidget(self.barcode_btn)
        left_layout.addLayout(search_layout)

        # Product details
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.StyledPanel)
        details_layout = QVBoxLayout(details_frame)

        # Quantity
        qty_layout = QHBoxLayout()
        qty_label = QLabel("الكمية:")
        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(9999)
        self.qty_spin.setValue(1)
        
        self.qty_minus_btn = QPushButton("-")
        self.qty_plus_btn = QPushButton("+")
        self.qty_minus_btn.setFixedSize(30, 30)
        self.qty_plus_btn.setFixedSize(30, 30)
        
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(self.qty_minus_btn)
        qty_layout.addWidget(self.qty_spin)
        qty_layout.addWidget(self.qty_plus_btn)
        details_layout.addLayout(qty_layout)

        # Price
        price_layout = QHBoxLayout()
        price_label = QLabel("السعر:")
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setMinimum(0)
        self.price_spin.setMaximum(999999)
        self.price_spin.setDecimals(2)
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_spin)
        details_layout.addLayout(price_layout)

        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("الإجمالي:")
        self.total_label = QLabel("0.00")
        self.total_label.setStyleSheet("color: blue; font-weight: bold;")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_label)
        details_layout.addLayout(total_layout)

        # Payment method
        payment_layout = QHBoxLayout()
        payment_label = QLabel("طريقة الدفع:")
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["نقدي", "إلكتروني", "دين", "دفع جزئي"])
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_combo)
        details_layout.addLayout(payment_layout)

        # Creditor section (initially hidden)
        self.creditor_widget = QWidget()
        creditor_layout = QVBoxLayout(self.creditor_widget)
        
        creditor_name_layout = QHBoxLayout()
        creditor_name_label = QLabel("اسم الدائن:")
        self.creditor_name_input = QLineEdit()
        creditor_name_layout.addWidget(creditor_name_label)
        creditor_name_layout.addWidget(self.creditor_name_input)
        
        paid_amount_layout = QHBoxLayout()
        paid_amount_label = QLabel("المبلغ المدفوع:")
        self.paid_amount_spin = QDoubleSpinBox()
        self.paid_amount_spin.setMinimum(0)
        self.paid_amount_spin.setMaximum(999999)
        self.paid_amount_spin.setDecimals(2)
        paid_amount_layout.addWidget(paid_amount_label)
        paid_amount_layout.addWidget(self.paid_amount_spin)
        
        creditor_layout.addLayout(creditor_name_layout)
        creditor_layout.addLayout(paid_amount_layout)
        self.creditor_widget.hide()
        details_layout.addWidget(self.creditor_widget)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.add_item_btn = QPushButton("إضافة منتج")
        self.add_item_btn.setIcon(QIcon(os.path.join(ICONS_PATH, 'plus.svg')))
        self.add_item_btn.setStyleSheet("background-color: #28a745; color: white;")
        
        self.complete_btn = QPushButton("إتمام الفاتورة")
        self.complete_btn.setIcon(QIcon(os.path.join(ICONS_PATH, 'check.svg')))
        self.complete_btn.setStyleSheet("background-color: #007bff; color: white;")
        
        self.cancel_btn = QPushButton("إلغاء")
        self.cancel_btn.setIcon(QIcon(os.path.join(ICONS_PATH, 'cancel.svg')))
        self.cancel_btn.setStyleSheet("background-color: #dc3545; color: white;")
        
        buttons_layout.addWidget(self.add_item_btn)
        buttons_layout.addWidget(self.complete_btn)
        buttons_layout.addWidget(self.cancel_btn)
        details_layout.addLayout(buttons_layout)

        left_layout.addWidget(details_frame)
        left_layout.addStretch()

        # Right side - Invoice Preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Invoice header
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QVBoxLayout(header_frame)

        # Store name
        store_name_layout = QHBoxLayout()
        store_name_label = QLabel("اسم المتجر:")
        self.store_name_input = QLineEdit()
        store_name_layout.addWidget(store_name_label)
        store_name_layout.addWidget(self.store_name_input)
        header_layout.addLayout(store_name_layout)

        # Invoice info
        info_layout = QHBoxLayout()
        self.invoice_number_label = QLabel(f"فاتورة رقم: {self.current_invoice_number}")
        self.invoice_date_label = QLabel(datetime.now().strftime("%d %B %Y، %I:%M %p"))
        info_layout.addWidget(self.invoice_number_label)
        info_layout.addWidget(self.invoice_date_label)
        header_layout.addLayout(info_layout)

        # Customer name
        customer_layout = QHBoxLayout()
        customer_label = QLabel("إلى السيد:")
        self.customer_name_label = QLabel("")
        customer_layout.addWidget(customer_label)
        customer_layout.addWidget(self.customer_name_label)
        header_layout.addLayout(customer_layout)

        right_layout.addWidget(header_frame)

        # Invoice table
        self.invoice_table = QTableWidget()
        self.invoice_table.setColumnCount(4)
        self.invoice_table.setHorizontalHeaderLabels(["المنتج", "الكمية", "السعر", "الإجمالي"])
        self.invoice_table.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.invoice_table)

        # Invoice totals
        totals_frame = QFrame()
        totals_frame.setFrameStyle(QFrame.StyledPanel)
        totals_layout = QVBoxLayout(totals_frame)

        self.total_amount_label = QLabel("إجمالي الفاتورة: 0.00")
        self.paid_amount_label = QLabel("المبلغ المدفوع: 0.00")
        self.remaining_amount_label = QLabel("المتبقي: 0.00")
        self.remaining_amount_label.setStyleSheet("color: red;")

        totals_layout.addWidget(self.total_amount_label)
        totals_layout.addWidget(self.paid_amount_label)
        totals_layout.addWidget(self.remaining_amount_label)

        right_layout.addWidget(totals_frame)

        # Print button
        self.print_btn = QPushButton("طباعة")
        self.print_btn.setIcon(QIcon(os.path.join(ICONS_PATH, 'print.svg')))
        self.print_btn.setStyleSheet("background-color: #6c757d; color: white;")
        right_layout.addWidget(self.print_btn)

        # Add widgets to main layout
        layout.addWidget(left_widget, 1)
        layout.addWidget(right_widget, 1)

        # Connect signals
        self.payment_combo.currentTextChanged.connect(self.on_payment_method_changed)
        self.qty_spin.valueChanged.connect(self.update_total)
        self.price_spin.valueChanged.connect(self.update_total)
        self.qty_minus_btn.clicked.connect(lambda: self.qty_spin.setValue(self.qty_spin.value() - 1))
        self.qty_plus_btn.clicked.connect(lambda: self.qty_spin.setValue(self.qty_spin.value() + 1))
        self.add_item_btn.clicked.connect(self.add_item)
        self.complete_btn.clicked.connect(self.complete_invoice)
        self.cancel_btn.clicked.connect(self.cancel_invoice)
        self.print_btn.clicked.connect(self.print_invoice)
        self.suggestions_combo.currentIndexChanged.connect(self.on_suggestion_selected)
        self.barcode_btn.clicked.connect(self.process_barcode)

        # Set the main layout
        self.setLayout(layout)

    def _connect_signals(self):
        self.search_input.textChanged.connect(self.on_search_changed)
        self.suggestions_combo.currentIndexChanged.connect(self.on_suggestion_selected)
        self.barcode_btn.clicked.connect(self.process_barcode)
        self.qty_spin.valueChanged.connect(self.update_total)
        self.price_spin.valueChanged.connect(self.update_total)
        self.qty_minus_btn.clicked.connect(lambda: self.qty_spin.setValue(self.qty_spin.value() - 1))
        self.qty_plus_btn.clicked.connect(lambda: self.qty_spin.setValue(self.qty_spin.value() + 1))
        self.add_item_btn.clicked.connect(self.add_item)
        self.complete_btn.clicked.connect(self.complete_invoice)
        self.cancel_btn.clicked.connect(self.cancel_invoice)
        self.print_btn.clicked.connect(self.print_invoice)

    def on_payment_method_changed(self, method):
        self.creditor_widget.setVisible(method in ["دين", "دفع جزئي"])
        if method in ["دين", "دفع جزئي"]:
            self.customer_name_label.setText(self.creditor_name_input.text())
        else:
            self.customer_name_label.setText("")

    def update_total(self):
        total = self.qty_spin.value() * self.price_spin.value()
        self.total_label.setText(f"{total:.2f}")

    def add_item(self):
        # Add item to invoice table
        row = self.invoice_table.rowCount()
        self.invoice_table.insertRow(row)
        
        # Get values
        product_name = self.search_input.text()
        quantity = self.qty_spin.value()
        price = self.price_spin.value()
        total = quantity * price

        # Add to table
        self.invoice_table.setItem(row, 0, QTableWidgetItem(product_name))
        self.invoice_table.setItem(row, 1, QTableWidgetItem(str(quantity)))
        self.invoice_table.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
        self.invoice_table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}"))

        # Update totals
        self.total_amount += total
        self.update_invoice_totals()

        # Clear inputs
        self.search_input.clear()
        self.qty_spin.setValue(1)
        self.price_spin.setValue(0)

    def update_invoice_totals(self):
        self.total_amount_label.setText(f"إجمالي الفاتورة: {self.total_amount:.2f}")
        self.paid_amount_label.setText(f"المبلغ المدفوع: {self.paid_amount:.2f}")
        remaining = self.total_amount - self.paid_amount
        self.remaining_amount_label.setText(f"المتبقي: {remaining:.2f}")

    def complete_invoice(self):
        if self.invoice_table.rowCount() == 0:
            QMessageBox.warning(self, "تنبيه", "لا يمكن إتمام فاتورة فارغة")
            return

        def _complete():
            # تجميع بيانات الفاتورة
            items = []
            for row in range(self.invoice_table.rowCount()):
                item = {
                    'name': self.invoice_table.item(row, 0).text(),
                    'qty': int(self.invoice_table.item(row, 1).text()),
                    'price': float(self.invoice_table.item(row, 2).text())
                }
                items.append(item)

            # التحقق من صحة البيانات
            validate_sale_data({
                'items': items,
                'paid_amount': self.paid_amount
            })

            # حفظ الفاتورة
            self.sales_controller.create_invoice(
                items=items,
                total_amount=self.total_amount,
                paid_amount=self.paid_amount,
                payment_method=self.payment_combo.currentText(),
                creditor_name=self.creditor_name_input.text() if self.payment_combo.currentText() in ["دين", "دفع جزئي"] else None
            )

            QMessageBox.information(self, "نجاح", "تم إتمام الفاتورة بنجاح")
            self.cancel_invoice()

        self.handle_error(_complete)

    def cancel_invoice(self):
        self.invoice_table.setRowCount(0)
        self.search_input.clear()
        self.qty_spin.setValue(1)
        self.price_spin.setValue(0)
        self.total_amount = 0
        self.paid_amount = 0
        self.update_invoice_totals()
        self.current_invoice_number += 1
        self.invoice_number_label.setText(f"فاتورة رقم: {self.current_invoice_number}")
        self.invoice_date_label.setText(datetime.now().strftime("%d %B %Y، %I:%M %p"))

    def print_invoice(self):
        if self.invoice_table.rowCount() == 0:
            QMessageBox.warning(self, "تنبيه", "لا يمكن طباعة فاتورة فارغة")
            return

        # TODO: Implement invoice printing
        QMessageBox.information(self, "تنبيه", "جاري تطوير خاصية الطباعة")

    def process_barcode(self):
        if not self.barcode_buffer:
            return
            
        product = self.product_controller.get_by_barcode(self.barcode_buffer)
        if product:
            self.search_input.setText(product.name)
            self.qty_spin.setValue(1)  # تعيين الكمية الافتراضية
        else:
            QMessageBox.information(self, "تنبيه", "لم يتم العثور على المنتج")
        
        self.barcode_buffer = ""
        self.search_input.clear()

    def update_product_price(self, product_name: str):
        """دالة مخصصة لتحديث سعر المنتج"""
        try:
            # البحث عن المنتج بالاسم
            product = self.product_controller.get_by_name(product_name)
            if product:
                # تحديث السعر
                self.price_spin.setValue(product.price_sell)
                # تحديث حقل البحث
                self.search_input.setText(product_name)
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating product price: {str(e)}")
            return False

    def on_search_changed(self, text):
        # لا نبحث إلا بعد حرفين على الأقل
        if len(text) < 2:
            self.suggestions_combo.hide()
            return

        def _search():
            products = self.product_controller.search_by_name(text)
            self.suggestions_combo.clear()
            
            if products:
                for product in products:
                    # تنسيق عرض المنتج
                    display_text = f"{product.name} (المخزون: {product.stock_qty:.0f})"
                    self.suggestions_combo.addItem(display_text, product.name)
                self.suggestions_combo.show()
            else:
                self.suggestions_combo.hide()

        self.handle_error(_search)

    def on_suggestion_selected(self, index):
        if index < 0:
            return
            
        def _select():
            product_name = self.suggestions_combo.currentData()
            if not product_name:
                return
                
            # تحديث السعر
            if self.update_product_price(product_name):
                # نظف الاقتراحات
                self.suggestions_combo.hide()
                self.suggestions_combo.clear()
                logger.info(f"Product selected: {product_name}")
            else:
                raise ValidationError(f"لا يمكن العثور على المنتج «{product_name}»")

        self.handle_error(_select)

    def on_barcode_entered(self):
        code = self.search_input.text().strip()
        if not code:
            return

        def _scan():
            # إذا كان النص فارغاً أو "بدون باركود"، نعرض اقتراحات البحث
            if code in ["NO_BARCODE", "بدون باركود", "NONE", ""]:
                self.on_search_changed("")
                return

            product = self.product_controller.get_by_barcode(code)
            if not product:
                # رسالة ودودة بدل رسالة خطأ نابعة من الـDB
                raise ValidationError(f"المنتج بالرمز «{code}» غير موجود")
                
            # تحديث السعر
            if self.update_product_price(product.name):
                self.suggestions_combo.hide()
                logger.info(f"Product scanned: {product.name} (Code: {product.code})")
            else:
                raise ValidationError(f"لا يمكن العثور على المنتج «{product.name}»")

        self.handle_error(_scan)

    def add_product_to_table(self, product, qty: float):
        """إضافة منتج إلى الجدول"""
        row = self.invoice_table.rowCount()
        self.invoice_table.insertRow(row)
        
        # إضافة بيانات المنتج
        self.invoice_table.setItem(row, 0, QTableWidgetItem(product.name))
        self.invoice_table.setItem(row, 1, QTableWidgetItem(f"{qty:.2f}"))
        self.invoice_table.setItem(row, 2, QTableWidgetItem(f"{product.price_sell:.2f}"))
        self.invoice_table.setItem(row, 3, QTableWidgetItem(f"{qty * product.price_sell:.2f}"))

        # تحديث السعر في حقل السعر
        self.price_spin.setValue(product.price_sell)

        # Update totals
        self.total_amount += qty * product.price_sell
        self.update_invoice_totals()

        # إضافة زر حذف
        delete_btn = QPushButton("حذف")
        delete_btn.clicked.connect(lambda: self.remove_product(row))
        self.invoice_table.setCellWidget(row, 4, delete_btn)

    def remove_product(self, row: int):
        """حذف منتج من الجدول"""
        self.invoice_table.removeRow(row)
        self.update_invoice_totals()
