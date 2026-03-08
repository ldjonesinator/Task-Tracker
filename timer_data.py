from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


DATA_TYPE = {"DATE": 0, "DURATION": 1, "TIMES": 2, "NOTE": 3}

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

# gets lists of data from the times file
def get_time_data(filename, delim, task, xi):
	xs = []

	with open(filename, 'r') as file:
		lines = file.readlines()

	success = False
	for line in lines:
		if task in line:
			data_line = line
			success = True

	if not success:
		return -1

	value = ""
	i = -1
	for char in list(data_line):

		if char == delim:
			if (i % 5) == xi:
				xs.append(value)
			i += 1
			value = ""
		else:
			value += char


	return xs

def graph_time(filename, task):
	xs = get_time_data(filename, ',', task, DATA_TYPE["DATE"])
	ys = get_time_data(filename, ',', task, DATA_TYPE["DURATION"])

	zip_data = zip(xs, ys)
	sorted_data = sorted(zip_data, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))

	x_axis = []
	y_axis = []
	for i, j in sorted_data:
		x_axis.append(i)
		y_axis.append(j)

	plt.plot(x_axis, y_axis)
	plt.title(task)
	plt.xlabel("Date")
	plt.xticks(rotation=45)
	plt.ylabel("Duration")

	plt.show()


def find_statistic(filename, task, t_type):
	data = get_time_data(filename, ',', task, DATA_TYPE[t_type])
	if DATA_TYPE[t_type] == DATA_TYPE["DURATION"]:
		total_spent = 0
		for time in data:
			total_spent += int(time)

		return total_spent

	elif DATA_TYPE[t_type] == DATA_TYPE["NOTE"]:
		note_count = {}
		for note in data:
			note_edit = note.strip().lower()
			if note_edit in note_count:
				note_count[note_edit] += 1
			else:
				note_count[note_edit] = 1

		return note_count

	return -1

def statistic_pie_chart(filename, task, t_type, title):
	stat_dict = find_statistic(filename, task, t_type)
	plt.pie(stat_dict.values(), labels = stat_dict.keys(), autopct='%1.0f%%')
	plt.title(title)
	plt.show()


if __name__ == "__main__":
	print(find_statistic("times.csv", "Uni", "DURATION"))
	print(find_statistic("times.csv", "Uni", "NOTE"))
	statistic_pie_chart("times.csv", "Uni", "NOTE", "Activity type for Uni")
	graph_time("times.csv", "Work")
