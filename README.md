# casheri_desktop
### ملخّص مشروع **Cashier App** (بصياغة مختصرة تصلح كدليل لـ Codex)

> **الغرض**: نظام نقاط بيع موجّه للبقاليات السورية، يعمل بدون إنترنت، ويدعم العملات المتعدّدة والديون، مع تكامل قارئ باركود وطابعة حرارية. اللغة العربية هي الواجهة الافتراضية.

---

#### 1. التقنية والأساس المعماري

| جانب           | اختيار                                                                                              |
| -------------- | --------------------------------------------------------------------------------------------------- |
| لغة البرمجة    | **Python 3.12** (type-hints مفعّلة)                                                                 |
| واجهة المستخدم | **PyQt 5/6** – تصميم بـ Qt Designer ثم تحويل إلى ‎`.py`                                             |
| قاعدة البيانات | **SQLite** عبر **SQLAlchemy ORM** (نمط MVC)                                                         |
| بناء الحزم     | `poetry` أو `pip + venv` مع ‎`requirements.txt`                                                     |
| اختبارات       | `pytest` + `pytest-qt`                                                                              |
| أجهزة داعمة    | قارئ باركود USB (يعمل عبر `pyzbar` أو `python-barcode`)\*<br>\*طابعة حرارية USB/Serial (`pyserial`) |

---

#### 2. هيكل المجلدات (TL;DR)

```
cashier_app/
├─ main.py               # Entry point – loads SalesView by default
├─ config/settings.py    # DB path, locale, currency rates
├─ database/db_session.py
├─ models/               # Product, Sale, SaleItem, Creditor, PriceHistory
├─ controllers/          # ProductController, SalesController, ...
├─ views/                # PyQt windows (SalesView is default)
├─ assets/icons          # SVG icons used in the UI
├─ ui/                   # .ui files generated from Qt Designer
├─ utils/                # excel_export.py, pdf_generator.py, validators.py
└─ tests/                # pytest suites
```

---

#### 3. سلوك افتراضي مهم (بدون تفصيل “آلية” التنفيذ)

| النقطة                     | السلوك المختصر                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------ |
| **الإقلاع**                | يفتح مباشرةً على **صفحة المبيعات** ويُشغِّل مسح الباركود آليًا ما دام البرنامج يعمل. |
| **البحث والإكمال التنبؤي** | الحقول (اسم المنتج، اسم الدائن، …) تدعم Auto-Complete يستمدّ اقتراحاته من الـ DB.    |
| **الكمية الافتراضية**      | `1` لكل منتج؛ يمكن تعديلها بـ `+ / –` أو إدخال يدوي.                                 |
| **إضافة منتج ثانٍ**        | المنتج السابق يُدرج تلقائيًا في جدول الفاتورة ويعاد تهيئة الحقول للمنتج التالي.      |
| **طريقة الدفع**            | Dropdown بقيم: *نقدي (افتراضي)*، *إلكتروني*، *دين*، *دفع جزئي*.                      |
| **الدَين**                 | إمكان إنشاء دائن جديد أو ربط الفاتورة بدائن حالي من نفس الواجهة.                     |
| **إتمام الفاتورة**         | تخفيض المخزون، تحديث جدول `sales` و `creditors` (إن وجد)، وتوليد رقم فاتورة متسلسل.  |
| **تنبيهات**                | لون أحمر للمخزون < 5 وحدات أو لمبالغ الديون > 0.<br>لون أصفر عند تعديل سعر > 20 %.   |
| **إرجاع منتج**             | واجهة “مرتجعات” مستقلة تربط الإرجاع بالفاتورة الأصلية وتعيد الكمية للمخزون.          |

---

#### 4. جداول قاعدة البيانات (موجز)

```text
Product(id PK, barcode UNIQUE, name, buy_price, sell_price, quantity)
Sale(id PK, invoice_no UNIQUE, datetime, payment_type, creditor_id FK NULLABLE, total, paid, remaining)
SaleItem(id PK, sale_id FK, product_id FK, qty, unit_price, subtotal)
Creditor(id PK, name, phone, balance)
PriceHistory(id PK, product_id FK, old_buy, new_buy, old_sell, new_sell, changed_at)
```

> **مفتاح**: جميع الطوابع الزمنية بتوقيت **Asia/Damascus**، وتُحفظ بسلسلة ISO-8601.

---

#### 5. إرشادات ترميز مختصرة لـ Codex

```python
# Example: controllers/sales_controller.py
class SalesController:
    "...high-level façade between SalesView and database layer..."

    def add_item(self, barcode: str, qty: int = 1) -> None: ...
    def finalize_invoice(self,
                         payment_type: PaymentType = PaymentType.CASH,
                         creditor: Creditor | None = None,
                         paid_amount: Decimal | None = None) -> InvoiceDTO: ...
```

* **نمط التسمية**: `snake_case` للمتغيرات والدوال، `PascalCase` للأصناف.
* **المستندات**: docstrings بنمط Google، مع أمثلة استخدام مختصرة.
* **الفصل الصارم** بين **view** (PyQt Widgets فقط) و**controller** (لا يستورد `PyQt` إطلاقًا).
* الوحدات في **utils** يجب أن تبقى بلا اعتمادية على **PyQt** أو **SQLAlchemy**.

---

#### 6. خطوات التطوير المقترحة (Sprint 0)

1. **تهيئة المشروع**: `poetry new cashier_app && cd cashier_app`.
2. **config & db**: إعداد `settings.py` + سكربت `populate_demo_data.py`.
3. **نماذج ORM**: إنشاء `base.py` ثم النماذج الخمسة أعلاه.
4. **Sales MVP**:

   * Build `SalesView` from `sales.ui`.
   * Implement `SalesController` (barcode → autocomplete → table).
   * تفعيل الطابعة عبر `pyserial`.
5. **اختبارات**: وحدة واحدة لكل نموذج + smoke test على `SalesController`.
6. **CI**: إعداد GitHub Actions لـ `pytest` + `flake8`.

---

> هذا الملخّص كافٍ ليبدأ Codex (أو أي مساعد ذكي) استنباط هيكل الكود وإنشاء الملفات الأساسية تلقائيًا. إذا احتجت إلى **قوالب ملفات فعلية** أو **نماذج دوال أكثر تفصيلًا**، فأخبرني لأزوّدك بها.

## كيفية التشغيل

```bash
pip install -r requirements.txt
python -m cashier_app.main
```

 cc04qz-codex/generate-pyqt-cashier-app-structure

        qji01o-codex/generate-pyqt-cashier-app-structure
 main
If you run the application on a headless server without an X display,
`main.py` will automatically fall back to the Qt `offscreen` platform.

### Controllers and Models
- SalesController, CreditorController, ReportController, DBExplorerController
- Sale, SaleItem, Creditor, Payment, PriceHistory, Return models with TimestampMixin
- Dashboard includes sidebar buttons for switching between the main views

 cc04qz-codex/generate-pyqt-cashier-app-structure


### Controllers and Models
- SalesController, CreditorController, ReportController, DBExplorerController
- Sale, SaleItem, Creditor, Payment, PriceHistory, Return models with TimestampMixin
 k5wnzb-codex/generate-pyqt-cashier-app-structure
- Dashboard includes sidebar buttons for switching between the main views


 hl67wh-codex/generate-pyqt-cashier-app-structure
- Dashboard includes sidebar buttons for switching between the main views

 main
 main
       main
 main
