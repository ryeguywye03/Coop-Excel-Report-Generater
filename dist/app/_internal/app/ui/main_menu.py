from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout, QSizePolicy

class MainMenuUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent  # Store the reference to the main window
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("mainpanel")  # Set object name for the main panel

        self.main_layout = QGridLayout(self)

        # Sidebar with buttons
        # sidebar_group = self.setup_sidebar()
        # sidebar_group.setObjectName("sidebar")  # Set object name for sidebar

        # Main panel with welcome text
        welcome_panel = self.setup_main_panel()

        # Add sidebar and welcome panel to the main layout using grid
        # self.main_layout.addWidget(sidebar_group, 0, 0, 1, 1)  # Sidebar on the left
        self.main_layout.addWidget(welcome_panel, 0, 1, 1, 2)  # Main panel on the right

        # Set stretch factors for columns
        self.main_layout.setColumnStretch(0, 0)  # Sidebar has fixed width
        self.main_layout.setColumnStretch(1, 1)  # Main content area expands

        # Set sidebar size policy to fixed width
        # sidebar_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Set main panel size policy to expanding
        welcome_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setup_sidebar(self):
        """Set up the sidebar for the Main Menu."""
        sidebar_group = QGroupBox("Navigation")
        sidebar_layout = QVBoxLayout()

        # Button to go to SR Counter page
        sr_counter_button = QPushButton("SR Counter")
        sr_counter_button.clicked.connect(self.main_window.switch_to_sr_counter)  # Use main_window to switch

        sidebar_layout.addWidget(sr_counter_button)
        sidebar_group.setLayout(sidebar_layout)

        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for the welcome screen."""
        main_panel_group = QGroupBox("Welcome")
        main_panel_layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to the Excel Report Generator!")
        main_panel_layout.addWidget(welcome_label)

        main_panel_group.setLayout(main_panel_layout)
        return main_panel_group
