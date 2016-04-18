import csv, shapely, math
from shapely.geometry import *
import numpy

lat_0 = 50.62500
long_0 = 8.43751

def isfloat(x):
	'''CHECKS IF X IS FLOAT'''
	try:
		a = float(x)
	except ValueError:
		return False
	else:
		return True

def to_float(x):
	'''CONVERTS TO FLOAT IF POSSIBLE'''
	if isfloat(x):
		return float(x)
	else:
		return x

def slopeInfo_process(sInfo):
	'''CONVERTS SLOPEINFO'''
	points = sInfo.split('|')
	points = map(lambda x: x.split('/'), points)
	for i in range(len(points)):
		if len(points[i]) > 1:
			points[i] = map(lambda x: to_float(x[1]), points[i])
		else:
			points[i] = None
	return points

def distance_on_earth(lat1, long1, lat2, long2):
	'''http://www.johndcook.com/blog/python_longitude_latitude/'''
	'''AUTHOR: John D. Cook'''

	degrees_to_radians = math.pi/180.0
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians
	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2)+math.cos(phi1)*math.cos(phi2))
	arc = math.acos(cos)

	return arc*6371000.0

def compute_slope(lat1, long1, alt1, lat2, long2, alt2):
	'''Computes slope between two points'''
	try:
		delta_h = alt2-alt1
		d = distance_on_earth(lat1, long1, lat2, long2)
		deg = math.atan(delta_h/d)
		return deg
	except:
		return None

def average_slopes(slopes):
	'''average of a list of slopes'''
	n = len(slopes)
	if n == 0:
		return None
	acc = 0.0
	for s in slopes:
		try:
			acc += s
		except:
			n -= 1
	try:
		return acc/n
	except:
		return None

def process_matched_data(data):
	'''processes matched data into a list'''
	new_data = []
	for i in range(len(data)):
		new_data.append(process_row(data[i][0]))
	return new_data

def process_row(row):
	'''process a row of matched_data'''
	remove_char = ["'", "[", "]", " "]
	new_row = filter(lambda x: x not in remove_char, row)
	new_row = new_row.split(',')
	new_row = map(lambda x: to_float(x), new_row)
	return new_row

# probe_file = 'Partition6467ProbePoints.csv'
link_file = 'Partition6467LinkData.csv'
matched_file = 'Partition6467MatchedPoints.csv'

# probe_data = []
link_data = []
matched_data = []

# Open files and read into lists
# with open(probe_file, 'rb') as f:
#     reader = csv.reader(f)
#     raw_probe_data = list(reader)
with open(link_file, 'rb') as f:
	reader = csv.reader(f)
	raw_link_data = list(reader)
with open(matched_file, 'rb') as f:
    reader = csv.reader(f)
    raw_matched_data = list(reader)

# process data
matched_data = process_matched_data(raw_matched_data)
link_data = raw_link_data

for i in range(len(link_data)):
	link_data[i][:] = map(lambda x: to_float(x), link_data[i][:])
	link_data[i][16] = slopeInfo_process(link_data[i][16])

#sort data by linkPVID
del matched_data[-1:]
matched_data.sort(key = lambda x: x[8])
link_data.sort(key = lambda x: x[0])

matched_slopes = dict()
link_slopes = dict()

prev_id = -1
slopes = []
prev_point = []

print 'a'

for i in range(len(matched_data)):
	curr_id = matched_data[i][8]
	if curr_id != prev_id:
		matched_slopes[prev_id] = average_slopes(slopes)
		slopes = []
	else:
		slope = compute_slope(prev_point[3], prev_point[4], prev_point[5], matched_data[i][3], matched_data[i][4], matched_data[i][5])
		slopes.append(slope)
	prev_id = curr_id
	prev_point = matched_data[i]

slopes = []

print 'b' 

for i in range(len(link_data)):
	link_id = link_data[i][0]
	slopeInfo = link_data[i][16]
	if slopeInfo == None:
		link_slopes = None
	else:
		for s in slopeInfo:
			slopes.append(s)
		link_slopes[link_id] = average_slopes(slopes)

diffs = dict()
all_diffs = 0
count_diffs = 0

for i in range(len(link_data)):
	ID = link_data[i][0]
	print i
	if link_slopes[ID] != None and matched_slopes[ID] != None:
		diffs[ID] = math.fabs(link_slopes[ID] - matched_slopes[ID])
		all_diffs += diffs[ID]
		count_diffs += 1

avg_diff = all_diffs/count_diffs
print avg_diff


