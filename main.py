# main.py
import sys
from PyQt5.QtWidgets import QApplication
from database.db_session import init_db
from views.dashboard import Dashboard

def main():
    # تهيئة قاعدة البيانات (ينشئ الجداول إذا لم تكن موجودة)
    init_db()
    # تشغيل الواجهة
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
