import time

class Timer():
	def __init__(self, title, date, note):
		self.title = title
		self.date = date
		self.note = note

		self.start_time = 0
		self.end_time = 0
		self.isEnd = False
		self.total_time = 0

		self.pause_time = 0
		self.isPaused = False
		self.pause_log = 0

	def start_timer(self):
		self.start_time = time.perf_counter()

	def end_timer(self):
		if not self.isPaused:
			self.end_time = time.perf_counter()

		self.total_time = self.get_elapsed_time()
		self.isEnd = True

	def pause_timer(self):
		if not self.isPaused:
			self.end_time = time.perf_counter()
			self.isPaused = True

	def check_pause_time(self):
		if self.isPaused:
			self.pause_time += time.perf_counter() - self.end_time - (self.pause_time - self.pause_log)

	def resume_timer(self):
		if self.isPaused:
			self.check_pause_time()
			self.pause_log += self.pause_time
			self.isPaused = False

	def get_elapsed_time(self):
		if self.isEnd:
			return -1
		self.check_pause_time()
		return time.perf_counter() - self.start_time - self.pause_time

	def store_time(self, filename):
		if self.isEnd:
			try:
				with open(filename, 'x') as file:
					write_line = format_text(self.title, self.date, self.total_time, self.start_time,
											 self.end_time, self.note)
					print(f"Creating file: {filename}")
					file.write(write_line)
			except FileExistsError:

				with open(filename, 'r') as file:
					lines = file.readlines()

				# getting the line to write to if it exists
				found_i = -1;
				for i in range(len(lines)):
					if self.title in lines[i]:
						write_line = lines[i]
						found_i = i;

				# adding new data to specific line in file

				if found_i != -1:
					write_line.join(format_text("FALSE", self.date, self.total_time, self.start_time,
											 self.end_time, self.note))
					lines[found_i] = write_line
				else:
					write_line = format_text(self.title, self.date, self.total_time, self.start_time,
											 self.end_time, self.note)
					lines.append(write_line)

				with open(filename, 'w') as file:
					file.writelines(lines)

		else:
			print("Can't store because timer hasn't ended")

		self.isEnd = False

def format_text(title, date, tt, st, et, note):
	t_time = f"{tt:.1f}"
	e_time = f"{et:.1f}"
	s_time = f"{st:.1f}"
	if title == "FALSE":
		return f"{date},{t_time},{s_time}-{e_time},{note},,"
	return f"{title},{date},{t_time},{s_time}-{e_time},{note},,"

def run_commands(command):
	cmnd = command.strip().lower()
	if cmnd == "pause" or cmnd == 'p':
		print("Pausing timer")
		timer.pause_timer()
	elif cmnd == "resume" or cmnd == 'r':
		print("Resuming timer")
		timer.resume_timer()
	elif cmnd == "check" or cmnd == 'c':
		print(f"Time Passed: {timer.get_elapsed_time():.2f}")
	elif cmnd == "end" or cmnd == 'e':
		print("Ending timer")
		timer.end_timer()
	elif cmnd == "store" or cmnd == 's':
		print("Storing time")
		timer.store_time("times.csv")


if __name__ == "__main__":
	timer = Timer("Work", "11/02/2026", "idk")
	prompt = input("Start Timer?\n> ")
	while prompt.strip().lower() != 'y':
		prompt = input("Start Timer?\n> ")
	timer.start_timer()
	while prompt.strip().lower() != 'q':
		prompt = input("> ")
		run_commands(prompt)

	print("Quitting...")
