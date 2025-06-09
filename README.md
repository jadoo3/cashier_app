# نظام نقاط البيع (POS)

نظام نقاط البيع مبني باستخدام Python و PyQt6 و SQLAlchemy.

## المتطلبات

- Python 3.8 أو أحدث
- Poetry (مدير الحزم)

## التثبيت

1. قم بتثبيت Poetry إذا لم يكن مثبتاً:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. قم بتثبيت التبعيات:
```bash
poetry install
```

3. قم بتهيئة قاعدة البيانات:
```bash
poetry run python -m cashier_app.init_db
```

## التشغيل

لتشغيل التطبيق:
```bash
poetry run python -m cashier_app.main
```

## الميزات

- إدارة المبيعات والفواتير
- إدارة المنتجات والمخزون
- طباعة الفواتير
- التقارير والإحصائيات
- دعم اللغة العربية

## الهيكل

```
cashier_app/
├── assets/          # الموارد (الأيقونات، إلخ)
├── config/          # إعدادات التطبيق
├── controllers/     # المتحكمات
├── database/        # إعدادات قاعدة البيانات
├── models/          # نماذج البيانات
├── utils/           # أدوات مساعدة
└── views/           # واجهات المستخدم
    └── pages/       # صفحات التطبيق
```

## المساهمة

1. قم بعمل Fork للمشروع
2. قم بإنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. قم بعمل Commit للتغييرات (`git commit -m 'Add some amazing feature'`)
4. قم بعمل Push للفرع (`git push origin feature/amazing-feature`)
5. قم بفتح طلب Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.
