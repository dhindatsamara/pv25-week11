from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import os

class MealPrepUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def load_stylesheet(self, app):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
            print(f"Attempting to load stylesheet from: {qss_path}")
            with open(qss_path, 'r') as file:
                app.setStyleSheet(file.read())
                print("Stylesheet loaded successfully")
        except FileNotFoundError:
            print(f"Error: styles.qss not found at {qss_path}")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout()
        content_frame.setLayout(content_layout)
        content_frame.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=2, yOffset=2))
        main_layout.addWidget(content_frame)

        header_label = QLabel("🍽️ Meal Prep Planner")
        header_label.setObjectName("headerLabel")
        header_label.setFont(QFont("Poppins", 28, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(header_label)

        main_widget = QWidget()
        main_layout_inner = QHBoxLayout()
        main_widget.setLayout(main_layout_inner)
        content_layout.addWidget(main_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(370)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        form_widget = QFrame()
        form_widget.setObjectName("formWidget")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)
        form_widget.setLayout(form_layout)
        form_widget.setFixedWidth(350)
        form_widget.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=2, yOffset=2))

        form_layout.addWidget(QLabel("🍲 Dish Name:"))
        dish_layout = QHBoxLayout()
        self.dish_input = QLineEdit()
        self.dish_input.setPlaceholderText("Dish Name")
        self.dish_input.setMaximumWidth(320)
        dish_layout.addWidget(self.dish_input)
        self.dish_paste_button = QPushButton("Paste")
        self.dish_paste_button.setObjectName("dishPasteButton")
        self.dish_paste_button.setToolTip("Paste text from clipboard to Dish Name")
        dish_layout.addWidget(self.dish_paste_button)
        form_layout.addLayout(dish_layout)

        self.category_input = QComboBox()
        self.category_input.addItems(["Breakfast", "Lunch", "Dinner", "Snack"])
        self.category_input.setMaximumWidth(380)
        form_layout.addWidget(QLabel("🗂️ Category:"))
        form_layout.addWidget(self.category_input)

        self.prep_date_input = QDateEdit()
        self.prep_date_input.setCalendarPopup(True)
        self.prep_date_input.setDate(QDate.currentDate())
        self.prep_date_input.setMaximumWidth(380)
        form_layout.addWidget(QLabel("📅 Prep Date:"))
        form_layout.addWidget(self.prep_date_input)

        self.portion_input = QSpinBox()
        self.portion_input.setRange(1, 10)
        self.portion_input.setValue(1)
        self.portion_input.setMaximumWidth(380)
        form_layout.addWidget(QLabel("🔢 Portion Size:"))
        form_layout.addWidget(self.portion_input)

        self.storage_input = QComboBox()
        self.storage_input.addItems(["Fridge", "Freezer", "Pantry"])
        self.storage_input.setMaximumWidth(380)
        form_layout.addWidget(QLabel("📦 Storage Location:"))
        form_layout.addWidget(self.storage_input)

        form_layout.addWidget(QLabel("📝 Notes:"))
        notes_layout = QHBoxLayout()
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter ingredients or notes...")
        self.notes_input.setFixedHeight(60)
        self.notes_input.setMaximumWidth(320)
        notes_layout.addWidget(self.notes_input)
        self.notes_paste_button = QPushButton("Paste")
        self.notes_paste_button.setObjectName("notesPasteButton")
        self.notes_paste_button.setToolTip("Paste text from clipboard to Notes")
        notes_layout.addWidget(self.notes_paste_button)
        form_layout.addLayout(notes_layout)

        self.save_button = QPushButton("Add")
        self.save_button.setMaximumWidth(380)
        form_layout.addWidget(self.save_button)

        self.update_button = QPushButton("Update")
        self.update_button.setObjectName("updateButton")
        self.update_button.setEnabled(False)
        self.update_button.setMaximumWidth(380)
        form_layout.addWidget(self.update_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.setObjectName("exportButton")
        self.export_button.setMaximumWidth(380)
        form_layout.addWidget(self.export_button)
        form_layout.addStretch()

        scroll_area.setWidget(form_widget)
        main_layout_inner.addWidget(scroll_area, stretch=0)

        table_widget = QWidget()
        table_layout = QVBoxLayout()
        table_widget.setLayout(table_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Dish Name", "Category", "Prep Date", 
                                             "Days Since Prep", "Portion", "Storage", "Notes", ""])
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        column_widths = [50, 150, 100, 100, 120, 80, 100, 150, 60]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        table_layout.addWidget(self.table)
        main_layout_inner.addWidget(table_widget, stretch=1)

    def setup_dock_widget(self, parent):
        self.search_dock = QDockWidget("Search and Sort", parent)
        self.search_dock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | 
                                        Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.search_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.search_dock.setFont(QFont("Roboto", 14))
        
        search_widget = QWidget()
        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(10, 10, 10, 10)
        search_layout.setSpacing(8)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Newest First", "Oldest First"])
        self.sort_combo.setCurrentText("Newest First")
        search_layout.addWidget(self.sort_combo)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by dish name")
        search_layout.addWidget(self.search_input)
        
        search_widget.setLayout(search_layout)
        search_widget.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=2))
        self.search_dock.setWidget(search_widget)
        parent.addDockWidget(Qt.TopDockWidgetArea, self.search_dock)

    def setup_status_bar(self, status_bar):
        status_bar.showMessage("Created by: Dhinda Tsamara Shalsabilla | NIM: F1D022005")
        status_bar.setMinimumHeight(30)
        status_bar.setFont(QFont("Roboto", 12))

    def clear_inputs(self):
        self.dish_input.clear()
        self.category_input.setCurrentIndex(0)
        self.prep_date_input.setDate(QDate.currentDate())
        self.portion_input.setValue(1)
        self.storage_input.setCurrentIndex(0)
        self.notes_input.clear()
        self.update_button.setEnabled(False)

    def resize_table_columns(self, table_width):
        column_widths = [50, 150, 100, 100, 120, 80, 100, 150, 60]
        total_fixed_width = sum(column_widths)
        if table_width > total_fixed_width:
            stretch_factor = table_width / total_fixed_width
            for i, width in enumerate(column_widths):
                self.table.setColumnWidth(i, int(width * stretch_factor))
        else:
            for i, width in enumerate(column_widths):
                self.table.setColumnWidth(i, width)