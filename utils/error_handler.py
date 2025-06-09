from PyQt5.QtWidgets import QMessageBox
from utils.validators import ValidationError
from models.product import OutOfStockError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMixin:
    """ميكس لمعالجة الأخطاء في واجهة المستخدم"""
    
    def handle_error(self, func, success_callback=None):
        """معالجة الأخطاء بشكل موحد"""
        try:
            result = func()
            if success_callback:
                success_callback(result)
            return result
        except ValidationError as e:
            # عرض رسالة تحذير للمستخدم
            QMessageBox.warning(self, "خطأ في التحقق", str(e))
            logger.warning(f"Validation error: {str(e)}")
        except OutOfStockError as e:
            # عرض رسالة تحذير للمستخدم
            QMessageBox.warning(self, "خطأ في المخزون", str(e))
            logger.warning(f"Stock error: {str(e)}")
        except IntegrityError as e:
            # خطأ في قاعدة البيانات (مثل: تكرار البيانات)
            QMessageBox.critical(self, "خطأ", "حدث خطأ في قاعدة البيانات. تأكد من عدم تكرار البيانات.")
            logger.error(f"Database integrity error: {str(e)}", exc_info=True)
        except SQLAlchemyError as e:
            # خطأ عام في قاعدة البيانات
            QMessageBox.critical(self, "خطأ", "حدث خطأ في قاعدة البيانات. يرجى المحاولة مرة أخرى.")
            logger.error(f"Database error: {str(e)}", exc_info=True)
        except Exception as e:
            # عرض رسالة خطأ للمستخدم
            QMessageBox.critical(self, "خطأ", f"حدث خطأ غير متوقع: {str(e)}")
            logger.error(f"Unexpected error: {str(e)}", exc_info=True) 
