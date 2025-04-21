class DialogBase(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        container = QWidget()
        container.setStyleSheet("""
            background: var(--color-card-bg);
            border-radius: 8px;
            border: 1px solid var(--color-border);
        """)

        shadow = ShadowEffect()
        shadow.set_radius(32)
        shadow.set_offset(0, 12)
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.addWidget(container)
        self.setLayout(layout)
