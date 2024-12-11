from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt  # Ensure Qt namespace for enums and flags in PyQt6
from modules.utils import LoggerManager
from modules.utils import AppSettings
from .settings_handler import SettingsHandler

class MainMenuUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent  # Reference to the main window

        # Initialize logger
        self.logger = LoggerManager()
        
        # Initialize AppSettings for shared settings access
        self.settings = AppSettings()
        
        # Setup UI and other components
        self.setup_ui()
        print("MainMenuUI initialized")

    def setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("mainPanel")  # Set object name for the main panel
        self.main_layout = QGridLayout(self)
        
        # Set up the sidebar and main panel
        sidebar = self.setup_sidebar()  # Ensure sidebar is created only once
        main_panel = self.setup_main_panel()

        # Add sidebar and main panel to the main layout
        self.main_layout.addWidget(sidebar, 0, 0, 1, 1)
        self.main_layout.addWidget(main_panel, 0, 1, 1, 2)

    def setup_sidebar(self):
        """Set up the sidebar for the Main Menu."""
        sidebar_group = QGroupBox("Navigation")
        sidebar_group.setObjectName("sidebarGroup")  # Assign QSS ID
        sidebar_layout = QVBoxLayout()

        # Button to go to SR Counter page
        sr_counter_button = QPushButton("SR Counter")
        sr_counter_button.setProperty("class", "sidebar-button")  # Assign QSS class
        sr_counter_button.clicked.connect(self.main_window.switch_to_sr_counter)

        # Button to go to SR Formatter page
        sr_formatter_button = QPushButton("SR Formatter")
        sr_formatter_button.setProperty("class", "sidebar-button")  # Assign QSS class
        sr_formatter_button.clicked.connect(self.main_window.switch_to_sr_formatter)

        # Settings Button
        settings_button = QPushButton("Settings")
        settings_button.setProperty("class", "sidebar-button")  # Assign QSS class
        settings_button.clicked.connect(self.open_settings_dialog)

        # Add buttons to the layout
        sidebar_layout.addWidget(sr_counter_button)
        sidebar_layout.addWidget(sr_formatter_button)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(settings_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for the welcome screen."""
        main_panel_group = QGroupBox("Welcome")
        main_panel_group.setObjectName("mainPanelGroup")  # Assign QSS ID
        main_panel_layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to the Excel Report Generator!")
        welcome_label.setProperty("class", "welcome-label")  # Assign QSS class
        main_panel_layout.addWidget(welcome_label)

        main_panel_group.setLayout(main_panel_layout)
        return main_panel_group
    
    def open_settings_dialog(self):
        """Open the settings dialog for the main menu."""
        dialog = SettingsHandler(main_app=self.main_window)
        dialog.exec()  # In PyQt6, use exec() instead of exec_()
