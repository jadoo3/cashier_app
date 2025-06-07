import os

# مسار جذر المشروع
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# رابط قاعدة البيانات (SQLite file-based)
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f"sqlite:///{os.path.join(BASE_DIR, 'cashier.db')}"
)

# لغة الواجهة (حالياً عربية)
LANGUAGE = 'ar'

# مسار الأيقونات (يُستخدم لاحقاً في الواجهة)
ICONS_PATH = os.path.join(BASE_DIR, 'resources', 'icons', 'svg')
