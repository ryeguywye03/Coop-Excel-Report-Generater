from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QGroupBox

class MainMenuUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        # Layout for main menu using QGridLayout
        self.main_layout = QGridLayout(self)

        # Sidebar with navigation buttons
        sidebar_group = self.setup_sidebar(parent)

        # Main panel with welcome message
        welcome_panel = self.setup_main_panel()

        # Add sidebar and welcome panel to the main layout using grid
        self.main_layout.addWidget(sidebar_group, 0, 0, 1, 1)  # Sidebar on the left
        self.main_layout.addWidget(welcome_panel, 0, 1, 1, 2)  # Welcome panel takes 2 columns

    def setup_sidebar(self, parent):
        """Set up the sidebar for the Main Menu."""
        sidebar_group = QGroupBox("Navigation")
        sidebar_layout = QVBoxLayout()

        # Add buttons for navigation
        sr_counter_button = QPushButton("SR Counter")
        sr_counter_button.clicked.connect(parent.switch_to_sr_counter)
        sidebar_layout.addWidget(sr_counter_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for the welcome message."""
        welcome_panel = QGroupBox("Welcome")
        welcome_layout = QVBoxLayout()

        welcome_message = QLabel("Welcome to the Excel Report Generator!")
        welcome_layout.addWidget(welcome_message)

        welcome_panel.setLayout(welcome_layout)
        return welcome_panel
