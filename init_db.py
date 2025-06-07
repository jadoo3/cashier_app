from database.db_session import Base, engine
from models.sale import Sale
from models.sale_item import SaleItem
from models.product import Product
from models.creditor import Creditor

def init_db():
    # حذف جميع الجداول الموجودة
    Base.metadata.drop_all(bind=engine)
    
    # إنشاء الجداول من جديد
    Base.metadata.create_all(bind=engine)
    
    print("تم إعادة إنشاء قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    init_db() 