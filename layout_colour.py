from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


# def create_button(text, callback=None, enabled=True, hidden=False, size_x=QSizePolicy.Minimum, size_y=QSizePolicy.Fixed):
# 	btn = QPushButton(text)
# 	btn.setSizePolicy(size_x, size_y)
# 	btn.setEnabled(enabled)
# 	btn.setHidden(hidden)

# 	if callback:
# 		btn.clicked.connect(callback)

# 	return btn

# def h_layout(*widgets):
# 	layout = QHBoxLayout()
# 	for w in widgets:
# 		layout.addWidget(w)
# 	return layout


# def v_layout(*widgets):
# 	layout = QVBoxLayout()
# 	for w in widgets:
# 		layout.addWidget(w)
# 	return layout
