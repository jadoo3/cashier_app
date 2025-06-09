"""Application entry point."""

import locale
import sys

from PyQt5.QtWidgets import QApplication

from cashier_app.config.settings import LOCALE
from cashier_app.database.db_session import init_db
from cashier_app.views.dashboard import Dashboard


def main() -> None:
    """Initialize DB and start Qt application."""
 hl67wh-codex/generate-pyqt-cashier-app-structure
    try:
        locale.setlocale(locale.LC_ALL, LOCALE)
    except locale.Error:
        print(
            f"تحذير: التعريب {LOCALE} غير متوفر على هذا النظام، سيتم استخدام الإعداد الافتراضي."
        )
        locale.setlocale(locale.LC_ALL, "")

    locale.setlocale(locale.LC_ALL, LOCALE)
main
    init_db()

    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
