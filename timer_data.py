from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


def get_system_time():
	now = datetime.now().time()
	return now.strftime("%H:%M")

def get_system_date():
	now = datetime.now().date()
	return now.strftime("%d/%m/%Y")

def format_text(title, date, tt, st, et, note):
	t_time = round(tt / 60) # in seconds
	if title == "FALSE":
		return f"{date},{t_time},{st}-{et},{note},,\n"
	return f"{title},{date},{t_time},{st}-{et},{note},,\n"

def format_time(seconds):
	left_over = round(seconds)
	hours = left_over // 60 // 60
	left_over -= hours * 60 * 60
	minutes = left_over // 60
	left_over -= minutes * 60
	secs = left_over
	return f"{hours:02d}:{minutes:02d}"

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


def graph_time():
	pass

def update_statistics():
	pass