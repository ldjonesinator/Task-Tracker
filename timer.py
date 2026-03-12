import time
from datetime import datetime

from random import randint, choice

from timer_data import time_store_in_file, get_system_time

STORE_LIMIT = 1
BUTTON_TYPES = {"PLAY": "Start", "SAVE": "Save", "RESET": "Reset"}
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
