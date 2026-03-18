import math
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


DATA_TYPE = {"DATE": 0, "TOTAL": 1, "TOTAL_M": 1, "TOTAL_W": 1, "TIMES": 2, "NOTE": 3}
DAYS = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7}
TIMER_FILE = "times.csv"
DELIM = ','


def get_system_time():
	now = datetime.now().time()
	return now.strftime("%H:%M")

def get_system_date():
	now = datetime.now().date()
	return now.strftime("%d/%m/%Y")

def format_text(title, date, tt, st, et, note):
	t_time = math.floor(tt / 60) # convert to minutes
	if title == "FALSE":
		return f"{date},{t_time},{st}-{et},{note},,\n"
	return f"{title},{date},{t_time},{st}-{et},{note},,\n"

def format_time(seconds, text_format=False):
	left_over = round(seconds)
	hours = left_over // 60 // 60
	left_over -= hours * 60 * 60
	minutes = left_over // 60
	left_over -= minutes * 60
	secs = left_over
	if text_format:
		return f"{hours} hrs, {minutes} mins"
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


def get_filter_times(times, dates, date, format="%Y"):
	new_times = []

	ref_format = date.strftime(format)

	for i in range(len(dates)):
		d = datetime.strptime(dates[i], "%d/%m/%Y")
		# print(d.strftime(format), ref_format)
		if d.strftime(format) == ref_format:
			new_times.append(times[i])

	return new_times

def get_week_times(times, dates):
	ref_day = datetime.now().strftime("%a")
	all_times = []
	for i in range(DAYS[ref_day]):
		sub_t = datetime.now() - timedelta(days=DAYS[ref_day]-i - 1)
		temp_times = get_filter_times(times, dates, sub_t, "%d")
		for time in temp_times:
			all_times.append(time)

	return all_times


def find_statistic(task, t_type):
	data = get_time_data(TIMER_FILE, DELIM, task, DATA_TYPE[t_type])
	if DATA_TYPE[t_type] == DATA_TYPE["TOTAL"]:
		if t_type == "TOTAL_M":
			dates = get_time_data(TIMER_FILE, DELIM, task, DATA_TYPE["DATE"])
			data = get_filter_times(data, dates, datetime.now(), "%m")

		elif t_type == "TOTAL_W":
			dates = get_time_data(TIMER_FILE, DELIM, task, DATA_TYPE["DATE"])
			data = get_week_times(data, dates)

		total_spent = 0
		for time in data:
			total_spent += int(time)

		return total_spent

	elif DATA_TYPE[t_type] == DATA_TYPE["NOTE"]:
		time = get_time_data(TIMER_FILE, DELIM, task, DATA_TYPE["TOTAL"])
		note_count = {}
		for i in range(len(data)):
			note_edit = data[i].strip().lower()
			if note_edit in note_count:
				note_count[note_edit] += int(time[i])
			else:
				note_count[note_edit] = int(time[i])

		return note_count

	return -1



def graph_time(filename, task):
	xs = get_time_data(filename, DELIM, task, DATA_TYPE["DATE"])
	ys = get_time_data(filename, DELIM, task, DATA_TYPE["TOTAL"])

	zip_data = zip(xs, ys)
	sorted_data = sorted(zip_data, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))

	x_axis = []
	y_axis = []
	for i, j in sorted_data:
		x_axis.append(i)
		y_axis.append(int(j))

	plt.bar(x_axis, y_axis)
	plt.title(task)
	plt.xlabel("Date")
	plt.xticks(rotation=45)
	plt.yticks(y_axis.sort())
	plt.ylabel("Duration")

	plt.show()

def statistic_pie_chart(task, t_type, title):
	stat_dict = find_statistic(task, t_type)
	plt.pie(stat_dict.values(), labels = stat_dict.keys(), autopct='%1.0f%%')
	plt.title(title)
	plt.show()



if __name__ == "__main__":
	print("Total: ", find_statistic("Uni", "TOTAL"))
	print("Month: ", find_statistic("Uni", "TOTAL_M"))
	print("Week: ", find_statistic("Uni", "TOTAL_W"))
	statistic_pie_chart("Uni", "NOTE", "Time Spent Per Uni Activity")
	graph_time("times.csv", "Uni")
