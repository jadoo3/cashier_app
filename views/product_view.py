# views/product_view.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDoubleSpinBox,
    QMessageBox, QFrame, QComboBox, QListWidget, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from controllers.product_controller import ProductController
from utils.error_handler import ErrorHandlerMixin
from utils.validators import validate_product_data, ValidationError

class ProductView(QWidget, ErrorHandlerMixin):
    def __init__(self):
        super().__init__()
        self.controller = ProductController()
        self.current_barcode = ""
        self._setup_ui()
        self.load_products()
        self._setup_barcode_timer()
        # تعيين التركيز على حقل الباركود عند فتح الصفحة
        self.barcode_input.setFocus()

    def _setup_barcode_timer(self):
        """إعداد مؤقت لقراءة الباركود"""
        self.barcode_timer = QTimer()
        self.barcode_timer.setSingleShot(True)
        self.barcode_timer.timeout.connect(self.process_barcode)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Left side - Product Entry Form
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)

        # Form Frame
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QVBoxLayout(form_frame)

        # Barcode
        barcode_layout = QHBoxLayout()
        barcode_label = QLabel("الباركود:")
        self.barcode_input = QLineEdit()
        self.barcode_input.setFont(QFont("Tajawal", 12))
        self.barcode_input.setMinimumHeight(40)
        self.barcode_input.textChanged.connect(self.on_barcode_changed)
        self.barcode_input.setReadOnly(True)  # منع الإدخال اليدوي
        barcode_layout.addWidget(barcode_label)
        barcode_layout.addWidget(self.barcode_input)

        # إضافة زر لتخطي الباركود
        self.skip_barcode_btn = QPushButton("تخطي الباركود")
        self.skip_barcode_btn.setStyleSheet("background-color: #6c757d; color: white;")
        self.skip_barcode_btn.setFont(QFont("Tajawal", 12))
        self.skip_barcode_btn.setMinimumHeight(40)
        self.skip_barcode_btn.clicked.connect(self.skip_barcode)
        barcode_layout.addWidget(self.skip_barcode_btn)

        form_layout.addLayout(barcode_layout)

        # Product Name with Suggestions
        name_layout = QVBoxLayout()
        name_label = QLabel("اسم المنتج:")
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Tajawal", 12))
        self.name_input.setMinimumHeight(40)
        self.name_input.textChanged.connect(self.on_name_changed)
        
        # قائمة الاقتراحات
        self.suggestions_list = QListWidget()
        self.suggestions_list.setFont(QFont("Tajawal", 12))
        self.suggestions_list.setMaximumHeight(100)
        self.suggestions_list.itemClicked.connect(self.on_suggestion_selected)
        self.suggestions_list.hide()
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.suggestions_list)
        form_layout.addLayout(name_layout)

        # Unit
        unit_layout = QHBoxLayout()
        unit_label = QLabel("الوحدة:")
        self.unit_input = QComboBox()
        self.unit_input.setFont(QFont("Tajawal", 12))
        self.unit_input.setMinimumHeight(40)
        # إضافة الوحدات الافتراضية
        units = ["قطعة", "كيلو", "علبة", "كرتون", "زجاجة", "علبة", "صندوق"]
        self.unit_input.addItems(units)
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.unit_input)
        form_layout.addLayout(unit_layout)

        # Stock Quantity
        stock_layout = QHBoxLayout()
        stock_label = QLabel("الكمية:")
        self.stock_input = QDoubleSpinBox()
        self.stock_input.setMinimum(0)
        self.stock_input.setMaximum(999999)
        self.stock_input.setDecimals(2)
        self.stock_input.setFont(QFont("Tajawal", 12))
        self.stock_input.setMinimumHeight(40)
        stock_layout.addWidget(stock_label)
        stock_layout.addWidget(self.stock_input)
        form_layout.addLayout(stock_layout)

        # Buy Price
        buy_price_layout = QHBoxLayout()
        buy_price_label = QLabel("سعر الشراء:")
        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setMinimum(0)
        self.buy_price_input.setMaximum(999999)
        self.buy_price_input.setDecimals(2)
        self.buy_price_input.setFont(QFont("Tajawal", 12))
        self.buy_price_input.setMinimumHeight(40)
        buy_price_layout.addWidget(buy_price_label)
        buy_price_layout.addWidget(self.buy_price_input)
        form_layout.addLayout(buy_price_layout)

        # Sell Price
        sell_price_layout = QHBoxLayout()
        sell_price_label = QLabel("سعر البيع:")
        self.sell_price_input = QDoubleSpinBox()
        self.sell_price_input.setMinimum(0)
        self.sell_price_input.setMaximum(999999)
        self.sell_price_input.setDecimals(2)
        self.sell_price_input.setFont(QFont("Tajawal", 12))
        self.sell_price_input.setMinimumHeight(40)
        sell_price_layout.addWidget(sell_price_label)
        sell_price_layout.addWidget(self.sell_price_input)
        form_layout.addLayout(sell_price_layout)

        # Action Buttons
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("حفظ")
        self.save_btn.setStyleSheet("background-color: #28a745; color: white;")
        self.save_btn.setFont(QFont("Tajawal", 12))
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self.save_product)

        self.clear_btn = QPushButton("مسح")
        self.clear_btn.setStyleSheet("background-color: #dc3545; color: white;")
        self.clear_btn.setFont(QFont("Tajawal", 12))
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_form)

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.clear_btn)
        form_layout.addLayout(buttons_layout)

        left_layout.addWidget(form_frame)
        left_layout.addStretch()

        # Right side - Products Table
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "الباركود", "الاسم", "الوحدة", "الكمية", "سعر البيع", "الإجراءات"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.table)

        layout.addWidget(left_widget, 1)
        layout.addWidget(right_widget, 1)

    def on_name_changed(self, text):
        """معالجة تغيير اسم المنتج وعرض الاقتراحات"""
        if len(text) >= 1:  # عرض الاقتراحات بعد كتابة حرف واحد على الأقل
            suggestions = self.controller.search_by_name(text)
            self.suggestions_list.clear()
            for product in suggestions:
                self.suggestions_list.addItem(f"{product.name} - {product.code}")
            self.suggestions_list.show() if suggestions else self.suggestions_list.hide()
        else:
            self.suggestions_list.hide()

    def on_suggestion_selected(self, item):
        """معالجة اختيار اقتراح"""
        # استخراج اسم المنتج من النص المختار
        product_name = item.text().split(" - ")[0]
        self.name_input.setText(product_name)
        self.suggestions_list.hide()
        
        # البحث عن المنتج في قاعدة البيانات وملء البيانات
        products = self.controller.list_all()
        for product in products:
            if product.name == product_name:
                self.barcode_input.setText(product.code)
                index = self.unit_input.findText(product.unit)
                if index >= 0:
                    self.unit_input.setCurrentIndex(index)
                self.stock_input.setValue(product.stock_qty)
                self.buy_price_input.setValue(product.price_buy)
                self.sell_price_input.setValue(product.price_sell)
                break

    def skip_barcode(self):
        """تخطي الباركود"""
        self.barcode_input.clear()
        self.name_input.setFocus()
        QMessageBox.information(self, "تنبيه", "يمكنك الآن إدخال بيانات المنتج بدون باركود")

    def on_barcode_changed(self, text):
        """معالجة تغيير الباركود"""
        self.current_barcode = text
        self.barcode_timer.start(100)  # انتظر 100 مللي ثانية قبل معالجة الباركود

    def process_barcode(self):
        """معالجة الباركود بعد اكتمال القراءة"""
        if len(self.current_barcode) > 0:
            # البحث عن المنتج في قاعدة البيانات
            products = self.controller.list_all()
            found = False
            for product in products:
                if product.code == self.current_barcode:
                    # إذا وجد المنتج، قم بملء النموذج
                    self.name_input.setText(product.name)
                    # البحث عن الوحدة في القائمة المنسدلة
                    index = self.unit_input.findText(product.unit)
                    if index >= 0:
                        self.unit_input.setCurrentIndex(index)
                    self.stock_input.setValue(product.stock_qty)
                    self.buy_price_input.setValue(product.price_buy)
                    self.sell_price_input.setValue(product.price_sell)
                    found = True
                    break
            
            if not found:
                QMessageBox.information(self, "تنبيه", "لم يتم العثور على المنتج. يمكنك إدخال بياناته الآن.")

    def validate_inputs(self) -> dict:
        """التحقق من صحة المدخلات"""
        try:
            # تحويل القيم إلى الأرقام المناسبة
            qty = float(self.stock_input.text() or 0)
            buy_price = float(self.buy_price_input.text() or 0)
            sell_price = float(self.sell_price_input.text() or 0)
            
            data = {
                'code': self.barcode_input.text().strip(),
                'name': self.name_input.text().strip(),
                'unit': self.unit_input.currentText().strip(),
                'stock_qty': qty,
                'price_buy': buy_price,
                'price_sell': sell_price
            }
            
            # التحقق من صحة البيانات
            validate_product_data(data)
            return data
            
        except ValueError:
            raise ValidationError("يرجى إدخال قيم صحيحة للأرقام")
        except ValidationError as e:
            raise e

    def save_product(self):
        """حفظ المنتج"""
        try:
            data = self.validate_inputs()
            
            # محاولة الحفظ
            self.handle_error(
                lambda: self.controller.create(**data),
                success_callback=self.on_save_success
            )
            
        except ValidationError as e:
            QMessageBox.warning(self, "خطأ في البيانات", str(e))

    def on_save_success(self, product):
        """عند نجاح حفظ المنتج"""
        # تحديث الجدول
        self.load_products()
        
        # عرض رسالة نجاح
        if hasattr(product, 'was_existing') and product.was_existing:
            QMessageBox.information(self, "نجاح", f"تم زيادة الكمية للمنتج {product.name}")
        else:
            QMessageBox.information(self, "نجاح", "تم إضافة المنتج بنجاح")
        
        # تنظيف الحقول
        self.clear_form()

    def clear_form(self):
        """مسح النموذج"""
        self.barcode_input.clear()
        self.name_input.clear()
        self.unit_input.setCurrentIndex(0)  # إعادة الوحدة إلى القيمة الافتراضية
        self.stock_input.setValue(0)
        self.buy_price_input.setValue(0)
        self.sell_price_input.setValue(0)
        self.suggestions_list.hide()
        self.barcode_input.setFocus()

    def load_products(self):
        """تحميل المنتجات في الجدول"""
        self.table.setRowCount(0)
        for p in self.controller.list_all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(row, 1, QTableWidgetItem(p.code))
            self.table.setItem(row, 2, QTableWidgetItem(p.name))
            self.table.setItem(row, 3, QTableWidgetItem(p.unit))
            self.table.setItem(row, 4, QTableWidgetItem(f"{p.stock_qty:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{p.price_sell:.2f}"))
            
            # أزرار الإجراءات
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("تعديل")
            edit_btn.clicked.connect(lambda checked, p=p: self.edit_product(p))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("حذف")
            delete_btn.clicked.connect(lambda checked, p=p: self.delete_product(p))
            actions_layout.addWidget(delete_btn)
            
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row, 6, actions_widget)

    def edit_product(self, product):
        """تعديل منتج"""
        self.barcode_input.setText(product.code)
        self.name_input.setText(product.name)
        self.unit_input.setCurrentText(product.unit)
        self.stock_input.setValue(product.stock_qty)
        self.buy_price_input.setValue(product.price_buy)
        self.sell_price_input.setValue(product.price_sell)

    def delete_product(self, product):
        """حذف منتج"""
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف المنتج {product.name}؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.handle_error(
                    lambda: self.controller.delete(product.id),
                    success_callback=lambda: self.load_products()
                )
                QMessageBox.information(self, "نجاح", "تم حذف المنتج بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حذف المنتج: {str(e)}")
