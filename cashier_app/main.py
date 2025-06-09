"""Application entry point."""

import locale
import sys

from PyQt5.QtWidgets import QApplication

from cashier_app.config.settings import LOCALE
from cashier_app.database.db_session import init_db
from cashier_app.views.dashboard import Dashboard


def main() -> None:
    """Initialize DB and start Qt application."""
    locale.setlocale(locale.LC_ALL, LOCALE)
    init_db()

    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
