from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox

class MainMenuUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        # Layout for main menu
        self.main_layout = QVBoxLayout(self)

        # Sidebar with navigation buttons
        sidebar_group = self.setup_sidebar(parent)

        # Main panel with welcome message
        welcome_panel = self.setup_main_panel()

        # Add sidebar and welcome panel to the main layout
        self.main_layout.addWidget(sidebar_group, 0, 0, 1, 1)
        self.main_layout.addWidget(welcome_panel, 0, 1, 1, 2)

    def setup_sidebar(self, parent):
        """Set up the sidebar for the Main Menu."""
        sidebar_group = QGroupBox("Navigation")
        sidebar_layout = QVBoxLayout()

        # Add buttons for navigation
        sr_counter_button = QPushButton("SR Counter")
        sr_counter_button.clicked.connect(parent.switch_to_sr_counter)

        settings_button = QPushButton("Settings")  # Could be added later

        sidebar_layout.addWidget(sr_counter_button)
        sidebar_layout.addWidget(settings_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main welcome panel."""
        main_panel_group = QGroupBox("Welcome to the Excel Report Generator App")
        main_panel_layout = QVBoxLayout()

        # Add a welcome label
        welcome_label = QLabel("Welcome! Use the sidebar to navigate to different options.")

        main_panel_layout.addWidget(welcome_label)
        main_panel_group.setLayout(main_panel_layout)
        return main_panel_group
