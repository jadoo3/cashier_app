from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام نقاط البيع")
        self.setMinimumSize(1200, 800)
        
        # Set RTL layout
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Create side menu
        self.create_side_menu()
        
        # Create content area
        self.create_content_area()
        
        # Create top bar
        self.create_top_bar()
        
        # Update clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        # Set Arabic font
        self.set_arabic_font()
    
    def create_side_menu(self):
        """Create the side menu with navigation buttons"""
        side_menu = QWidget()
        side_menu.setMaximumWidth(200)
        side_menu_layout = QVBoxLayout(side_menu)
        
        # Menu buttons
        buttons = [
            ("المبيعات", "sales"),
            ("المنتجات", "products"),
            ("الدائنين", "creditors"),
            ("التقارير", "reports"),
            ("تحديث الأسعار", "price_update"),
            ("استكشاف قاعدة البيانات", "db_explorer")
        ]
        
        for text, name in buttons:
            btn = QPushButton(text)
            btn.setObjectName(name)
            btn.setMinimumHeight(50)
            side_menu_layout.addWidget(btn)
        
        side_menu_layout.addStretch()
        self.main_layout.addWidget(side_menu)
    
    def create_content_area(self):
        """Create the main content area"""
        self.content_area = QStackedWidget()
        self.main_layout.addWidget(self.content_area)
    
    def create_top_bar(self):
        """Create the top bar with clock and user info"""
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        
        # Clock
        self.clock_label = QLabel()
        self.update_clock()
        top_bar_layout.addWidget(self.clock_label)
        
        # User info
        user_label = QLabel("المستخدم: admin")
        top_bar_layout.addWidget(user_label)
        
        # Add top bar to main layout
        self.main_layout.insertWidget(0, top_bar)
    
    def update_clock(self):
        """Update the clock display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arabic_time = get_display(arabic_reshaper.reshape(current_time))
        self.clock_label.setText(arabic_time)
    
    def set_arabic_font(self):
        """Set Arabic font for the application"""
        font = QFont("Cairo", 10)
        self.setFont(font) 