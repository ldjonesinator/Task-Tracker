import time
from datetime import datetime
from PyQt5.QtWidgets import QPushButton
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
			self.end = (time.perf_counter() - self.st) + self.start
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
		return time.perf_counter() - self.st - self.pt

	def restart_timer(self):
		self.end_timer()
		self.total_time = 0
		self.end = 0
		self.st = 0
		self.et = 0

	def store_time(self, filename, date):
		if self.isEnd and self.total_time >= STORE_LIMIT:
			try:
				with open(filename, 'x') as file:
					write_line = format_text(self.title, date, self.total_time, self.start,
											 self.end, self.note)
					print(f"Creating file: {filename}")
					file.write(write_line)
			except FileExistsError:

				with open(filename, 'r') as file:
					lines = file.readlines()

				# getting the line to write to if it exists
				found_i = -1;
				for i in range(len(lines)):
					if self.title in lines[i]:
						write_line = lines[i][:-1] # remove \n
						found_i = i;

				# adding new data to specific line in file
				if found_i != -1:
					write_line += format_text("FALSE", date, self.total_time, self.start,
											 self.end, self.note)
					lines[found_i] = write_line

				else:
					write_line = format_text(self.title, date, self.total_time, self.start,
											 self.end, self.note)
					lines.append(write_line)

				with open(filename, 'w') as file:
					file.writelines(lines)

			self.restart_timer()

		else:
			print("Can't store because timer hasn't ended or the length is too short.")
			print(f"Time: {self.total_time:.0f}s")


class TimerButton(QPushButton):
	def __init__(self, timer, type):
		super().__init__()

		self.type = type
		self.timer = timer
		self.setText(self.type)

	def mousePressEvent(self, e):
		if self.type == BUTTON_TYPES["PLAY"]:
			if self.timer.isEnd:
				self.timer.start_timer(get_system_time())
				self.setText("Pause")
			elif self.timer.isPaused:
				self.timer.resume_timer()
				self.setText("Pause")
			else:
				self.timer.pause_timer()
				self.setText("Play")
		elif self.type == BUTTON_TYPES["SAVE"]:
			if self.timer.total_time >= STORE_LIMIT:
				self.timer.end_timer()

				self.timer.store_time(TIMER_FILE, get_system_date())
		elif self.type == BUTTON_TYPES["RESET"]:
			self.timer.restart_timer()



		e.accept()


def format_text(title, date, tt, st, et, note):
	t_time = round(tt/60)
	e_time = round(et/60)
	if title == "FALSE":
		return f"{date},{t_time},{st} - {e_time},{note},,\n"
	return f"{title},{date},{t_time},{st}-{e_time},{note},,\n"


def get_system_time():
	now = datetime.now().time()
	return now.strftime("%H:%M")

def get_system_date():
	now = datetime.now().date()
	return now.strftime("%d/%m/%Y")


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
