import sys

from PyQt5.QtCore import QSize, Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
							 QSizePolicy, QPushButton, QLineEdit, QComboBox, QDateTimeEdit, QSpinBox)
from PyQt5.QtGui import QFont, QPalette, QColor

from datetime import time as dtime
from datetime import datetime


from layout_colour import Color

from timer import Timer, BUTTON_TYPES, STORE_LIMIT, TIMER_FILE
from timer_data import time_store_in_file, format_time, get_system_time, get_system_date


MIN_SIZE = 0.5
SPACING = 10
LAYOUT_COLOUR = "lightGray"
TIMER_FONT_SIZE = 90

class MainWindow(QMainWindow):

	def __init__(self, width, height):
		super().__init__()

		self.setWindowTitle("Task Tracker")
		self.setMinimumSize(QSize(int(width), int(height)))

		self.tasks = ["Work", "Uni", "Projects"]

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
		self.m_widg_hide = False

		self.add_time_layout = QVBoxLayout()
		self.add_time = QPushButton("Add a Task Time")
		self.add_time.clicked.connect(self.toggle_manual_time_widg)

		self.add_time_layout.addWidget(self.add_time, alignment=Qt.AlignVCenter)

		self.add_time_widg = Color(LAYOUT_COLOUR)
		self.manual_time_widgets()

		self.add_time_widg.setLayout( self.add_time_layout )
		self.left_layout.addWidget(self.add_time_widg, alignment=Qt.AlignVCenter)

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

		self.btn_text = []
		self.play_btn = QPushButton(BUTTON_TYPES["PLAY"])
		self.play_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.play_btn.clicked.connect(lambda: self.timer_btn_events(BUTTON_TYPES["PLAY"]))
		self.timer_layout.addWidget(self.play_btn, Qt.AlignHCenter | Qt.AlignVCenter)

		self.save_btn = QPushButton(BUTTON_TYPES["SAVE"])
		self.save_btn.clicked.connect(lambda: self.timer_btn_events(BUTTON_TYPES["SAVE"]))
		self.save_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

		self.reset_btn = QPushButton(BUTTON_TYPES["RESET"])
		self.reset_btn.clicked.connect(lambda: self.timer_btn_events(BUTTON_TYPES["RESET"]))
		self.reset_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

		self.t_btn_layout = QHBoxLayout()
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

	def timer_btn_events(self, b_type):
		if b_type == BUTTON_TYPES["PLAY"]:
			if self.timer.isEnd:
				self.timer.start_timer(get_system_time())
				self.play_btn.setText("Pause")
			elif self.timer.isPaused:
				self.timer.resume_timer()
				self.play_btn.setText("Pause")
			else:
				self.timer.pause_timer()
				self.play_btn.setText("Play")
		elif b_type == BUTTON_TYPES["SAVE"]:
			if self.timer.end_timer() >= STORE_LIMIT:
				self.timer.store_time(TIMER_FILE, get_system_date())
				self.timer_label.setText("00:00")
				self.play_btn.setText("Start")

		elif b_type == BUTTON_TYPES["RESET"]:
			self.timer.restart_timer()
			self.timer_label.setText("00:00")
			self.play_btn.setText("Start")

	def manual_time_widgets(self):

		self.task_box = QComboBox()
		self.task_box.setMinimumWidth(200)
		self.task_box.addItems(self.tasks)
		self.task_box.setHidden(True)


		self.time_box = QDateTimeEdit()
		self.time_box.setDateTime(QDateTime.currentDateTime())
		self.time_box.setDisplayFormat("dd/MM/yyyy hh:mm")
		self.time_box.setHidden(True)

		self.duration_box = QSpinBox()
		self.duration_box.setRange(0, 5940)
		self.duration_box.setSingleStep(15)
		self.duration_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.duration_box.setHidden(True)

		self.text_box = QLineEdit()
		self.text_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.text_box.setMaxLength(100)
		self.text_box.setPlaceholderText("Short Description")
		self.text_box.setHidden(True)

		self.confirm_btn = QPushButton("Store Time")
		self.confirm_btn.clicked.connect(self.store_manual)
		self.confirm_btn.setHidden(True)

		self.selection_layout = QHBoxLayout()

		self.selection_layout.addWidget(self.task_box, alignment=Qt.AlignVCenter)
		self.selection_layout.addWidget(self.time_box, alignment=Qt.AlignVCenter)
		self.selection_layout.addWidget(self.duration_box, alignment=Qt.AlignVCenter)
		self.add_time_layout.addLayout(self.selection_layout)
		self.add_time_layout.addWidget(self.text_box, alignment=Qt.AlignVCenter)
		self.add_time_layout.addWidget(self.confirm_btn, alignment=Qt.AlignVCenter)

	def toggle_manual_time_widg(self):
		self.task_box.setHidden(self.m_widg_hide)
		self.time_box.setHidden(self.m_widg_hide)
		self.duration_box.setHidden(self.m_widg_hide)
		self.text_box.setHidden(self.m_widg_hide)
		self.confirm_btn.setHidden(self.m_widg_hide)

		if self.m_widg_hide:
			self.add_time.setText("Add a Task Time")
		else:
			self.add_time.setText("Hide")

		self.m_widg_hide = not self.m_widg_hide

	def store_manual(self):
		title = self.task_box.currentText()
		duration = self.duration_box.value()
		d_hours = duration // 60
		d_mins = duration - d_hours * 60


		note = self.text_box.text()

		dt = self.time_box.dateTime()

		year = dt.date().year()
		month = dt.date().month()
		day = dt.date().day()
		date = datetime(year, month, day)

		s_hours = dt.time().hour()
		s_mins = dt.time().minute()
		start = dtime(s_hours, s_mins)

		e_hours = s_hours + d_hours + (s_mins + d_mins) // 60
		e_mins = s_mins + d_mins - 60 * ((s_mins + d_mins) // 60)
		end = dtime(e_hours % 24, e_mins)

		print(date.strftime("%d/%m/%Y"), " : ", end.strftime("%H:%M"), duration)
		time_store_in_file(TIMER_FILE, title, date.strftime("%d/%m/%Y"), duration * 60, start.strftime("%H:%M"), end.strftime("%H:%M"), note)
		self.toggle_manual_time_widg()










app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
print(f"Screen size (resolution): {size.width()} x {size.height()} pixels")

window = MainWindow(size.width()*MIN_SIZE, size.height()*MIN_SIZE)
window.show()

app.exec()