import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal
from random import randint, choice

STORE_LIMIT = 1
BUTTON_TYPES = {"PLAY": "Start", "SAVE": "Save", "RESET": "reset"}
TIMER_FILE = "times.csv"

class Timer():
	def __init__(self, title, note):
		self.title = title
		self.start = 0
		self.end = 0
		self.note = note

		self.st = 0
		self.et = 0
		self.isEnd = True
		self.total_time = 0

		self.pt = 0
		self.isPaused = False
		self.pause_log = 0

	def start_timer(self, start):
		if self.isEnd:
			self.start = start
			self.st = time.perf_counter()
			self.isEnd = False
			return True
		return False

	def end_timer(self):
		if not self.isEnd:
			if not self.isPaused:
				self.et = time.perf_counter()

			self.total_time = self.get_elapsed_time()
			self.end = get_system_time()
			self.isPaused = False
			self.pt = 0
			self.pause_log = 0
			self.isEnd = True
			return self.total_time
		return -1

	def pause_timer(self):
		if not self.isPaused:
			self.et = time.perf_counter()
			self.isPaused = True

	def check_pause_time(self):
		if self.isPaused:
			self.pt += time.perf_counter() - self.et - (self.pt - self.pause_log)

	def resume_timer(self):
		if self.isPaused:
			self.check_pause_time()
			self.pause_log += self.pt
			self.isPaused = False

	def get_elapsed_time(self):
		if self.isEnd:
			return -1
		self.check_pause_time()
		return round(time.perf_counter() - self.st - self.pt, 2)

	def restart_timer(self):
		self.end_timer()
		self.total_time = 0
		self.end = 0
		self.st = 0
		self.et = 0

	def store_time(self, filename, date):
		if self.isEnd and self.total_time >= STORE_LIMIT:
			time_store_in_file(filename, self.title, date, self.total_time, self.start, self.end, self.note)

			self.restart_timer()

		else:
			print("Can't store because timer hasn't ended or the length is too short.")
			print(f"Time: {self.total_time:.0f}s")


def time_store_in_file(filename, title, date, tt, start, end, note):
	try:
		with open(filename, 'x') as file:
			write_line = format_text(title, date, tt, start,
										end, note)
			print(f"Creating file: {filename}")
			file.write(write_line)
	except FileExistsError:

		with open(filename, 'r') as file:
			lines = file.readlines()

		# getting the line to write to if it exists
		found_i = -1;
		for i in range(len(lines)):
			if title in lines[i]:
				write_line = lines[i][:-1] # remove \n
				found_i = i;

		# adding new data to specific line in file
		if found_i != -1:
			write_line += format_text("FALSE", date, tt, start,
										end, note)
			lines[found_i] = write_line

		else:
			write_line = format_text(title, date, tt, start,
										end, note)
			lines.append(write_line)

		with open(filename, 'w') as file:
			file.writelines(lines)



def format_text(title, date, tt, st, et, note):
	t_time = tt//60
	if title == "FALSE":
		return f"{date},{t_time},{st} - {et},{note},,\n"
	return f"{title},{date},{t_time},{st}-{et},{note},,\n"


def get_system_time():
	now = datetime.now().time()
	return now.strftime("%H:%M")

def get_system_date():
	now = datetime.now().date()
	return now.strftime("%d/%m/%Y")

def format_time(seconds):
	left_over = round(seconds)
	hours = left_over // 60 // 60
	left_over -= hours * 60 * 60
	minutes = left_over // 60
	left_over -= minutes * 60
	secs = left_over
	return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def graph_time():
	pass


def run_commands(command):
	cmnd = command.strip().lower()
	if cmnd == "start" or cmnd == 's':
		print("Starting Timer")
		timer.start_timer(randint(60,6000))
	if cmnd == "pause" or cmnd == 'p':
		print("Pausing timer")
		timer.pause_timer()
	elif cmnd == "resume" or cmnd == 'r':
		print("Resuming timer")
		timer.resume_timer()
	elif cmnd == "check" or cmnd == 'c':
		print(f"Time Passed: {timer.get_elapsed_time():.1f}s")
	elif cmnd == "end" or cmnd == 'e':
		print("Ending timer")
		print(f"Time: {timer.end_timer():.1f}s")
	elif cmnd == "store" or cmnd == 'st':
		print("Storing time")
		timer.store_time("times.csv", f"{randint(1,28)}/{randint(1,12)}/2026")


if __name__ == "__main__":
	tasks = ("Work", "Homework", "Projects")

	timer = Timer(choice(tasks), "idk")
	prompt = ""
	while prompt.strip().lower() != 'q':
		prompt = input("> ")
		run_commands(prompt)

	print("Quitting...")
