import sys

from PyQt5.QtCore import QSize, Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
							 QSizePolicy)
from PyQt5.QtGui import QFont, QPalette, QColor

from layout_colour import Color

from timer import Timer, TimerButton, BUTTON_TYPES, format_time

MIN_SIZE = 0.5
SPACING = 10
LAYOUT_COLOUR = "lightGray"
TIMER_FONT_SIZE = 90

class MainWindow(QMainWindow):

	def __init__(self, width, height):
		super().__init__()

		self.setWindowTitle("Task Tracker")
		self.setMinimumSize(QSize(int(width), int(height)))

		self.base_layout = QHBoxLayout()
		self.left_layout = QVBoxLayout()
		self.right_layout = QVBoxLayout()

		self.base_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
		self.base_layout.setSpacing(SPACING)

		self.setup_left_layout()
		self.setup_timer("Work", "idk")
		self.setup_right_layout()


		widget = QWidget()
		widget.setLayout(self.base_layout)
		self.setCentralWidget(widget)

		self.qtimer = QTimer(self)
		self.qtimer.timeout.connect(self.update_time)
		self.qtimer.start(1000)

	def setup_left_layout(self):
		self.left_layout.addWidget(Color(LAYOUT_COLOUR))
		self.left_layout.addWidget(Color(LAYOUT_COLOUR))
		self.left_layout.addWidget(Color(LAYOUT_COLOUR))
		self.base_layout.addLayout( self.left_layout )

	def setup_timer(self, title, note):
		self.timer = Timer(title, note)
		self.timer_layout = QVBoxLayout()

		self.timer_label = QLabel("00:00")
		self.timer_label.setFont(QFont("Arial", TIMER_FONT_SIZE))
		self.timer_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.timer_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.timer_layout.addWidget(self.timer_label, alignment=Qt.AlignVCenter)

		self.play_btn = TimerButton(self.timer, BUTTON_TYPES["PLAY"])
		self.play_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.timer_layout.addWidget(self.play_btn, Qt.AlignHCenter | Qt.AlignVCenter)

		self.t_btn_layout = QHBoxLayout()
		self.save_btn = TimerButton(self.timer, BUTTON_TYPES["SAVE"])
		self.save_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

		self.reset_btn = TimerButton(self.timer, BUTTON_TYPES["RESET"])
		self.reset_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

		self.t_btn_layout.addWidget(self.save_btn, alignment=Qt.AlignTop)
		self.t_btn_layout.addWidget(self.reset_btn, alignment=Qt.AlignTop)

		self.timer_layout.addLayout(self.t_btn_layout)
		self.timer_widg = Color(LAYOUT_COLOUR)
		self.timer_widg.setLayout( self.timer_layout )
		self.base_layout.addWidget(self.timer_widg, alignment=Qt.AlignVCenter)


	def setup_right_layout(self):
		self.right_layout.addWidget(Color(LAYOUT_COLOUR))
		self.right_layout.addWidget(Color(LAYOUT_COLOUR))

		self.base_layout.addLayout( self.right_layout )

	def update_time(self):
		if not self.timer.isEnd:
			self.timer_label.setText(format_time(self.timer.get_elapsed_time()))






app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
print(f"Screen size (resolution): {size.width()} x {size.height()} pixels")

window = MainWindow(size.width()*MIN_SIZE, size.height()*MIN_SIZE)
window.show()

app.exec()