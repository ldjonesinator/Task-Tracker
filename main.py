import sys
import math

from PyQt5.QtCore import QSize, Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
							 QSizePolicy, QPushButton, QLineEdit, QComboBox, QDateTimeEdit, QSpinBox,
							 QSystemTrayIcon, QStyle)
from PyQt5.QtGui import QFont, QPalette, QColor

from datetime import time as dtime
from datetime import datetime


from layout_colour import Color

from timer import Timer, BUTTON_TYPES, STORE_LIMIT
import timer_data as td


MIN_SIZE = 0.55
SPACING = 10
LAYOUT_COLOUR = QColor(48, 48, 48)

TIMER_FONT_SIZE = 120
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

DESCRIPTION_LENGTH = 100

NOTIFICATION_CHECK_TIME = 15 # minutes

class MainWindow(QMainWindow):

	def __init__(self, width, height):
		super().__init__()

		self.setWindowTitle("Task Tracker")
		self.setFixedSize(QSize(int(width), int(height)))
		# self.setMinimumSize(QSize(int(width), int(height)))

		palette = QPalette()
		palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))
		palette.setColor(QPalette.ColorRole.WindowText, QColor(210, 210, 210))
		palette.setColor(QPalette.ColorRole.Text, QColor(210, 210, 210))
		palette.setColor(QPalette.ColorRole.Base, QColor(90, 90, 90))
		palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(50, 50, 50))
		palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
		palette.setColor(QPalette.ColorRole.ButtonText, QColor('white'))
		self.setPalette(palette)


		self.tasks = ["Uni", "Projects", "Work", "Uni Campus"]

		self.base_layout = QHBoxLayout()
		self.left_layout = QVBoxLayout()
		self.right_layout = QVBoxLayout()

		self.base_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
		self.base_layout.setSpacing(SPACING*4)

		self.setup_left_layout()
		self.timer_widget = TimerWidget(self.tasks, "fail", "failed to add note")
		self.base_layout.addWidget(self.timer_widget, alignment=Qt.AlignVCenter)
		self.setup_right_layout()


		widget = QWidget()
		widget.setLayout(self.base_layout)
		self.setCentralWidget(widget)

		self.notifictn_count = 1
		self.notification_check = QTimer(self)
		self.notification_check.timeout.connect(lambda: self.check_send_notification("Timer Running", "Don't forget to stop the timer!",
																				self.timer_widget.get_time()))
		self.notification_check.start(10000)


	def setup_left_layout(self):

		self.add_time_layout = QVBoxLayout()
		self.add_time = create_button("Add a Task Time", self.toggle_manual_time_widg)
		self.add_time_layout.addWidget(self.add_time, alignment=Qt.AlignVCenter)

		self.make_manual_time_widgets()
		self.add_time_widg = Color(LAYOUT_COLOUR)
		self.add_time_widg.setLayout( self.add_time_layout )


		self.left_layout.addWidget(self.add_time_widg, alignment=Qt.AlignTop)

		self.left_layout.addWidget(Color(LAYOUT_COLOUR))

		self.stats_layout = QVBoxLayout()
		self.make_stat_widgets()

		self.stats_widg = Color(LAYOUT_COLOUR)
		self.stats_widg.setLayout( self.stats_layout )
		self.left_layout.addWidget(self.stats_widg, alignment=Qt.AlignBottom)


		self.base_layout.addLayout( self.left_layout )


	def setup_right_layout(self):
		self.right_layout.addWidget(Color(LAYOUT_COLOUR))
		self.right_layout.addWidget(Color(LAYOUT_COLOUR))

		self.base_layout.addLayout( self.right_layout )


	def make_manual_time_widgets(self):

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

	def make_stat_widgets(self):
		self.stat_widgets = {
			"total": [QLabel(), ""]
		}

		for task in self.tasks:
			self.stat_widgets[task] = [QLabel(), ""]
			self.stats_layout.addWidget(self.stat_widgets[task][0])

		self.stats_layout.addLayout(h_layout(self.stat_widgets["total"][0]))

		self.update_stat_times()






	def toggle_manual_time_widg(self):
		hide_widgets(self.manual_widgets.values(), self.m_widg_hide)


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
		td.time_store_in_file(td.TIMER_FILE, title, date.strftime("%d/%m/%Y"), duration * 60, start.strftime("%H:%M"), end.strftime("%H:%M"), note)
		self.toggle_manual_time_widg()
		self.update_stat_times()


	def update_stat_times(self):
		total = 0
		total_time_m = 0
		total_time_d = 0
		for task in self.tasks:
			time = td.find_statistic(task, "TOTAL") * 60
			time_w = td.find_statistic(task, "TOTAL_W") * 60
			self.stat_widgets[task][1] = f"{task} Total Time: {td.format_time(time, True)} | This Week: {math.ceil(time_w/60/60)} hrs"

			total += time
			total_time_m += td.find_statistic(task, "TOTAL_M") * 60
			total_time_d += td.find_statistic(task, "TOTAL_D") * 60

		tty = f"Time Spent This Year: {math.ceil(total/60/60)} hrs"
		ttm = " | " + f"This Month: {math.ceil(total_time_m/60/60)} hrs"
		ttw = " | " + f"Today: {math.ceil(total_time_d/60/60)} hrs"

		self.stat_widgets["total"][1] = tty + ttm + ttw

		for key in self.stat_widgets.keys():
			self.stat_widgets[key][0].setText(self.stat_widgets[key][1])




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


class TimerWidget(QWidget):

	def __init__(self, tasks, title, note):
		super().__init__()

		self.timer = Timer(title, note)
		self.layout = QVBoxLayout()

		self.timer_refresh = QTimer(self)
		self.timer_refresh.timeout.connect(self.update_time)
		self.timer_refresh.start(10 * 1000) # every 10 seconds

		self.label = QLabel("00:00")
		self.label.setFont(QFont("Arial", TIMER_FONT_SIZE))
		self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.layout.addWidget(self.label, alignment=Qt.AlignVCenter)

		self.btn_text = []

		self.play_btn = create_button(BUTTON_TYPES["PLAY"],
			lambda: self.timer_btn_events(BUTTON_TYPES["PLAY"]),
			height=int(BUTTON_HEIGHT*1.5)
		)

		self.save_btn = create_button(BUTTON_TYPES["SAVE"],
			lambda: self.timer_btn_events(BUTTON_TYPES["SAVE"]), False
		)

		self.reset_btn = create_button(BUTTON_TYPES["RESET"],
			lambda: self.timer_btn_events(BUTTON_TYPES["RESET"])
		)


		self.task_box = QComboBox()
		self.task_box.setMinimumWidth(100)
		self.task_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.task_box.addItems(tasks)

		self.text_box = QLineEdit()
		self.text_box.setMaxLength(DESCRIPTION_LENGTH)
		self.text_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.text_box.setPlaceholderText("Short Description")


		self.layout.addWidget(self.play_btn)
		self.layout.addLayout(
			h_layout(self.save_btn, self.reset_btn)
		)

		self.layout.addLayout(
			h_layout(self.text_box, self.task_box)
		)

		self.setLayout( self.layout )


	def timer_btn_events(self, b_type):
		if b_type == BUTTON_TYPES["PLAY"]:
			if self.timer.isEnd: # clicked start
				self.timer.start_timer(td.get_system_time())
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
				self.timer.title = self.task_box.currentText()
				self.timer.note = self.text_box.text()
				self.timer.store_time(td.TIMER_FILE, td.get_system_date())
				self.label.setText("00:00")
				self.play_btn.setText("Start")

				self.play_btn.setStyleSheet("")
				self.save_btn.setEnabled(False)
				self.notifictn_count = 1

		elif b_type == BUTTON_TYPES["RESET"]:
			self.timer.restart_timer()
			self.label.setText("00:00")
			self.play_btn.setText("Start")

			self.play_btn.setStyleSheet("")
			self.notifictn_count = 1


	def get_time(self):
		return self.timer.get_elapsed_time()

	def update_time(self):
		if not self.timer.isEnd:
			self.label.setText(td.format_time(self.get_time()))




def create_button(text, callback=None, enabled=True, hidden=False, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
				  size_x=QSizePolicy.Minimum, size_y=QSizePolicy.Fixed):
	btn = QPushButton(text)
	btn.setSizePolicy(size_x, size_y)
	btn.setEnabled(enabled)
	btn.setHidden(hidden)
	btn.setMinimumWidth(width)
	btn.setMinimumHeight(height)

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

def hide_widgets(widgets, hide):
	for w in widgets:
		w.setHidden(hide)





app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
print(f"Screen size (resolution): {size.width()} x {size.height()} pixels")

window = MainWindow(size.width()*MIN_SIZE, size.height()*MIN_SIZE)
window.show()

app.exec()