import time

class Timer():
	def __init__(self, title):
		self.title = title

		self.start_time = 0
		self.end_time = 0

		self.pause_time = 0
		self.isPaused = False
		self.pause_log = 0

	def start_timer(self):
		self.start_time = time.perf_counter()

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
		self.check_pause_time()
		return time.perf_counter() - self.start_time - self.pause_time

	def store_time(self, filename, format):
		pass



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


if __name__ == "__main__":
	timer = Timer("Work")
	prompt = input("Start Timer?\n> ")
	while prompt.strip().lower() != 'y':
		prompt = input("Start Timer?\n> ")
	timer.start_timer()
	while prompt.strip().lower() != 'q':
		prompt = input("> ")
		run_commands(prompt)

	print("Quitting...")
