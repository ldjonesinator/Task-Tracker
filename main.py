import sys

from PyQt5.QtCore import QSize, Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
							 QSizePolicy, QPushButton, QLineEdit, QComboBox, QDateTimeEdit, QSpinBox,
							 QSystemTrayIcon, QStyle)
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
DESCRIPTION_LENGTH = 100
NOTIFICATION_CHECK_TIME = 15 # minutes

class MainWindow(QMainWindow):

	def __init__(self, width, height):
		super().__init__()

		self.setWindowTitle("Task Tracker")
		self.setMinimumSize(QSize(int(width), int(height)))

		self.tasks = ["Uni", "Projects", "Work"]

		self.base_layout = QHBoxLayout()
		self.left_layout = QVBoxLayout()
		self.right_layout = QVBoxLayout()

		self.base_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
		self.base_layout.setSpacing(SPACING)

		self.setup_left_layout()
		self.setup_timer("fail", "failed to add note")
		self.setup_right_layout()


		widget = QWidget()
		widget.setLayout(self.base_layout)
		self.setCentralWidget(widget)

		self.timer_refresh = QTimer(self)
		self.timer_refresh.timeout.connect(self.update_time)
		self.timer_refresh.start(1000)

		self.notifictn_count = 1
		self.notification_check = QTimer(self)
		self.timer_refresh.timeout.connect(lambda: self.check_send_notification("Timer Running", "Don't forget to stop the timer!",
																				self.timer.get_elapsed_time()))
		self.timer_refresh.start(10000)


	def setup_left_layout(self):

		self.add_time_layout = QVBoxLayout()
		self.add_time = QPushButton("Add a Task Time")
		self.add_time.clicked.connect(self.toggle_manual_time_widg)

		self.add_time_layout.addWidget(self.add_time, alignment=Qt.AlignVCenter)

		self.add_time_widg = Color(LAYOUT_COLOUR)
		self.manual_time_widgets()

		self.add_time_widg.setLayout(
			 self.add_time_layout )
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

		self.play_btn = create_button(BUTTON_TYPES["PLAY"],
			lambda: self.timer_btn_events(BUTTON_TYPES["PLAY"])
		)

		self.save_btn = create_button(BUTTON_TYPES["SAVE"],
			lambda: self.timer_btn_events(BUTTON_TYPES["SAVE"]), False
		)

		self.reset_btn = create_button(BUTTON_TYPES["RESET"],
			lambda: self.timer_btn_events(BUTTON_TYPES["RESET"])
		)


		self.t_task_box = QComboBox()
		self.t_task_box.setMinimumWidth(100)
		self.t_task_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.t_task_box.addItems(self.tasks)

		self.t_text_box = QLineEdit()
		self.t_text_box.setMaxLength(DESCRIPTION_LENGTH)
		self.t_text_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.t_text_box.setPlaceholderText("Short Description")


		self.t_btn_layout = QHBoxLayout()
		self.timer_layout.addWidget(self.play_btn, Qt.AlignHCenter | Qt.AlignVCenter)
		self.timer_layout.addLayout(
			h_layout(self.save_btn, self.reset_btn)
		)

		self.timer_layout.addLayout(
			h_layout(self.t_text_box, self.t_task_box)
		)

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
			if self.timer.isEnd: # clicked start
				self.timer.start_timer(get_system_time())
				self.play_btn.setText("Pause")
				self.save_btn.setEnabled(True)
				# self.save_btn.setStyleSheet("background-color: lightblue;")
				self.play_btn.setStyleSheet("background-color: red;")

			elif self.timer.isPaused:
				self.timer.resume_timer()
				self.play_btn.setText("Pause")
				self.play_btn.setStyleSheet("background-color: red;")
			else:
				self.timer.pause_timer()
				self.play_btn.setText("Play")
				self.play_btn.setStyleSheet("background-color: lightblue;")

		elif b_type == BUTTON_TYPES["SAVE"]:
			if self.timer.end_timer() >= STORE_LIMIT:
				self.timer.title = self.t_task_box.currentText()
				self.timer.note = self.t_text_box.text()
				self.timer.store_time(TIMER_FILE, get_system_date())
				self.timer_label.setText("00:00")
				self.play_btn.setText("Start")

				self.play_btn.setStyleSheet("")
				self.save_btn.setEnabled(False)
				self.notifictn_count = 1

		elif b_type == BUTTON_TYPES["RESET"]:
			self.timer.restart_timer()
			self.timer_label.setText("00:00")
			self.play_btn.setText("Start")

			self.play_btn.setStyleSheet("")
			self.notifictn_count = 1

	def manual_time_widgets(self):

		self.manual_widgets = {
			"task": QComboBox(),
			"time": QDateTimeEdit(),
			"duration": QSpinBox(),
			"text": QLineEdit(),
			"confirm": create_button("Store Time", self.store_manual)
		}

		self.manual_widgets["task"].setMinimumWidth(200)
		self.manual_widgets["task"].addItems(self.tasks)

		self.manual_widgets["time"].setDateTime(QDateTime.currentDateTime())
		self.manual_widgets["time"].setDisplayFormat("dd/MM/yyyy hh:mm")

		self.manual_widgets["duration"].setRange(0, 5940)
		self.manual_widgets["duration"].setSingleStep(15)
		self.manual_widgets["duration"].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

		self.manual_widgets["text"].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.manual_widgets["text"].setMaxLength(DESCRIPTION_LENGTH)
		self.manual_widgets["text"].setPlaceholderText("Short Description")

		self.m_widg_hide = True
		self.toggle_manual_time_widg()


		self.add_time_layout.addLayout(
			h_layout(self.manual_widgets["task"], self.manual_widgets["time"], self.manual_widgets["duration"])
		)
		self.add_time_layout.addWidget(self.manual_widgets["text"], alignment=Qt.AlignVCenter)
		self.add_time_layout.addWidget(self.manual_widgets["confirm"], alignment=Qt.AlignVCenter)

	def toggle_manual_time_widg(self):
		for w in self.manual_widgets.values():
			w.setHidden(self.m_widg_hide)

		if self.m_widg_hide:
			self.add_time.setText("Add a Task Time")
		else:
			self.add_time.setText("Hide")

		self.m_widg_hide = not self.m_widg_hide

	def store_manual(self):
		title = self.manual_widgets["task"].currentText()
		duration = self.manual_widgets["duration"].value()
		d_hours = duration // 60
		d_mins = duration - d_hours * 60


		note = self.manual_widgets["text"].text()

		dt = self.manual_widgets["time"].dateTime()

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

# add setting to turn on/off notifications
	def check_send_notification(self, title, message, timer):
		tray_icon = QSystemTrayIcon()

		icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
		tray_icon.setIcon(icon)

		if timer > (NOTIFICATION_CHECK_TIME * 60 * self.notifictn_count):
			tray_icon.show()

			tray_icon.showMessage(
				title,
				message,
				QSystemTrayIcon.Information,
				2000 # 2 seconds timeout
			)
			self.notifictn_count += 1



def create_button(text, callback=None, enabled=True, hidden=False, size_x=QSizePolicy.Minimum, size_y=QSizePolicy.Fixed):
	btn = QPushButton(text)
	btn.setSizePolicy(size_x, size_y)
	btn.setEnabled(enabled)
	btn.setHidden(hidden)

	if callback:
		btn.clicked.connect(callback)

	return btn

def h_layout(*widgets):
	layout = QHBoxLayout()
	for w in widgets:
		layout.addWidget(w)
	return layout


def v_layout(*widgets):
	layout = QVBoxLayout()
	for w in widgets:
		layout.addWidget(w)
	return layout





app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
print(f"Screen size (resolution): {size.width()} x {size.height()} pixels")

window = MainWindow(size.width()*MIN_SIZE, size.height()*MIN_SIZE)
window.show()

app.exec()