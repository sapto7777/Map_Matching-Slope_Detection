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

def reduce_date(x):
	'''REDUCES DATE/TIME TO SECONDS SINCE START OF DAY (ignores date)'''
	split_x = x.split()

	y = split_x[1]
	y = y.split(':')

	z = map(lambda x: to_float(x), y)

	if split_x[2] == 'PM':
		z[0] += 12

	hours_in_mins = z[0]*60
	mins_in_secs = (hours_in_mins + z[1])*60
	ret = mins_in_secs + z[2]
	return ret

def shapeInfo_to_lat_long_points(sInfo):
	'''CONVERTS SHAPEINFO INTO TUPLES OF LAT-LONG-ELEV'''
	points = sInfo.split('|')
	points = map(lambda x: x.split('/'), points)
	for i in range(len(points)):
		points[i] = map(lambda x: to_float(x), points[i])
		if points[i][2] == '':
			points[i][2] = None
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


def compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    AUTHOR: Jerome Renard (https://gist.github.com/jeromer)
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def determine_direction(probe_bearing, link_bearing):
	diff = (link_bearing - probe_bearing) % 360
	if diff < 90:
		return 'F'
	else:
		return 'T'


def match_first(point_data):
	'''matches first point of a probe sequence by brute-force'''
	closest = float('inf')
	matched_point = [None for x in range(12)]
	matched_point[:8] = point_data

	for link in link_data:
		link_id = link[0]
		for p in link[14]:
			distance = distance_on_earth(point_data[3], point_data[4], p[0], p[1])
			if distance < closest:
				closest = distance
				matched_point[8] = link_id
				link_bearing = compass_bearing((link[14][0][0], link[14][1][1]), (link[14][-1:][0][0], link[14][-1:][0][1]))
				matched_point[9] = determine_direction(point_data[7], link_bearing)
				matched_point[10] = distance_on_earth(point_data[3], point_data[4], link[14][0][0], link[14][0][1])
				matched_point[11] = closest

	return matched_point

def match_around(point_data, match):
	'''matches a point in a sequence given a previously matched point in the same probe sequence'''
	link_id = match[8]
	link = sDict[link_id][0]
	i = sDict[link_id][1]
	links_around_index = range(21)
	links_around_index = map(lambda x: x+i-10, links_around_index)
	closest = float('inf')
	matched_point = [None for x in range(12)]
	matched_point[:8] = point_data

# ***********************************************
# ********* END OF HELPER FUNCTION DEFS *********
# ***********************************************

probe_file = 'Partition6467ProbePoints.csv'
link_file = 'Partition6467LinkData.csv'

probe_data = []
link_data = []


# Open files and read into lists
with open(probe_file, 'rb') as f:
    reader = csv.reader(f)
    raw_probe_data = list(reader)
with open(link_file, 'rb') as f:
	reader = csv.reader(f)
	raw_link_data = list(reader)

probe_data = raw_probe_data
link_data = raw_link_data

# convert all data to int if possible
# reduce all dates in probe_data
pDict = dict()

for i in range(len(probe_data)):
	probe_data[i][:] = map(lambda x: to_float(x), probe_data[i][:])
	probe_data[i][1] = reduce_date(probe_data[i][1])

sDict = dict()
link_data.sort(key = lambda x: x[0])

for i in range(len(link_data)):
	link_data[i][:] = map(lambda x: to_float(x), link_data[i][:])
	link_data[i][14] = shapeInfo_to_lat_long_points(link_data[i][14])
	sDict[link_data[i][0]] = (link_data[i][:], i)

	for i in links_around_index:
		try:
			link = link_data[i]
		except IndexError:
			continue

		for p in link[14]:
			distance = distance_on_earth(point_data[3], point_data[4], p[0], p[1])
			if distance < closest:
					closest = distance
					matched_point[8] = link_id
					link_bearing = compass_bearing((link[14][0][0], link[14][1][1]), (link[14][-1:][0][0], link[14][-1:][0][1]))
					matched_point[9] = determine_direction(point_data[7], link_bearing)
					matched_point[10] = distance_on_earth(point_data[3], point_data[4], link[14][0][0], link[14][0][1])
					matched_point[11] = closest

	return matched_point

# START OF MAP MATCHING
prev_id = 0
match = []
prev_match = []
matches = []
all_dist = 0
all_match = 0

count = 0
writer = csv.writer(open('Partition6467MatchedPoints.csv', 'wb'))
for i in range(len(probe_data[:])):

	curr_id = probe_data[i][0]

	if prev_id != curr_id:
		prev_match = match_first(probe_data[i])
		print "MATCH\n", count
		all_match += 1
		all_dist += prev_match[11]
	else:
		match = match_around(probe_data[i], prev_match)
		matches.append(prev_match)	
		all_match += 1
		all_dist += match[11]	
		print "MATCH\n", count
		prev_match = match

	count += 1
	prev_id = curr_id

	writer.writerow([prev_match])