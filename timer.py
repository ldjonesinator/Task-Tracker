import time
from random import randint, choice

STORE_LIMIT = 1

class Timer():
	def __init__(self, title, date, start, note):
		self.title = title
		self.date = date
		self.start = start
		self.end = 0
		self.note = note

		self.st = 0
		self.et = 0
		self.isEnd = True
		self.total_time = 0

		self.pt = 0
		self.isPaused = False
		self.pause_log = 0

	def start_timer(self):
		if self.isEnd:
			self.st = time.perf_counter()
			self.isEnd = False

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

	def store_time(self, filename):
		if self.isEnd and self.total_time >= STORE_LIMIT:
			try:
				with open(filename, 'x') as file:
					write_line = format_text(self.title, self.date, self.total_time, self.start,
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
					write_line += format_text("FALSE", self.date, self.total_time, self.start,
											 self.end, self.note)
					lines[found_i] = write_line

				else:
					write_line = format_text(self.title, self.date, self.total_time, self.start,
											 self.end, self.note)
					lines.append(write_line)

				with open(filename, 'w') as file:
					file.writelines(lines)

			self.total_time = 0
			self.end = 0
			self.st = 0
			self.et = 0

		else:
			print("Can't store because timer hasn't ended or the length is too short.")
			print(f"Time: {self.total_time:.0f}s")



def format_text(title, date, tt, st, et, note):
	t_time = round(tt)
	e_time = round(et)
	if title == "FALSE":
		return f"{date},{t_time},{st} - {e_time},{note},,\n"
	return f"{title},{date},{t_time},{st}-{e_time},{note},,\n"


def run_commands(command):
	cmnd = command.strip().lower()
	if cmnd == "start" or cmnd == 's':
		print("Starting Timer")
		timer.start_timer()
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
		timer.store_time("times.csv")


if __name__ == "__main__":
	tasks = ("Work", "Homework", "Projects")

	timer = Timer(choice(tasks), f"{randint(1,28)}/{randint(1,12)}/2026", randint(60,6000), "idk")
	prompt = ""
	while prompt.strip().lower() != 'q':
		prompt = input("> ")
		run_commands(prompt)

	print("Quitting...")
