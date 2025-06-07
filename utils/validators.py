# utils/validators.py
import re
from typing import Any, Dict

class ValidationError(Exception):
    """يُرفع عند حدوث خطأ في التحقق من البيانات."""
    pass

def is_valid_code(code: str) -> bool:
    """
    يتحقق من أن رمز المنتج لا يحتوي إلا على حروف وأرقام وواصلات
    """
    return bool(re.match(r'^[A-Za-z0-9\-]+$', code))

def is_positive_number(value) -> bool:
    try:
        return float(value) >= 0
    except:
        return False

def validate_product_data(data: Dict[str, Any]) -> None:
    """التحقق من صحة بيانات المنتج قبل الحفظ أو التحديث."""
    if not data.get('name'):
        raise ValidationError("اسم المنتج مطلوب")
    if data.get('stock_qty', 0) < 0:
        raise ValidationError("الكمية يجب أن تكون موجبة")
    if data.get('price_buy', 0) < 0:
        raise ValidationError("سعر الشراء يجب أن يكون موجباً")
    if data.get('price_sell', 0) < 0:
        raise ValidationError("سعر البيع يجب أن يكون موجباً")
    if data.get('price_sell', 0) < data.get('price_buy', 0):
        raise ValidationError("سعر البيع يجب أن يكون أكبر من أو يساوي سعر الشراء")

def validate_sale_data(data: Dict[str, Any]) -> None:
    """التحقق من صحة بيانات البيع قبل إنهاء الفاتورة."""
    items = data.get('items')
    if not items or len(items) == 0:
        raise ValidationError("يجب إضافة منتج واحد على الأقل")
    if data.get('paid_amount', 0) < 0:
        raise ValidationError("المبلغ المدفوع يجب أن يكون موجباً")
    total = sum(item.get('qty', 0) * item.get('price', 0) for item in items)
    if data.get('paid_amount', 0) > total:
        raise ValidationError("المبلغ المدفوع أكبر من إجمالي الفاتورة")

def validate_creditor_data(data: Dict[str, Any]) -> None:
    """التحقق من صحة بيانات الدائن قبل الحفظ أو التحديث."""
    if not data.get('name'):
        raise ValidationError("اسم الدائن مطلوب")
    if data.get('balance', 0) < 0:
        raise ValidationError("الرصيد يجب أن يكون صفراً أو موجباً")
