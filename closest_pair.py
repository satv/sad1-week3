import sys, re, math
from operator import attrgetter

class Point:
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y

	def distance_to(self, point):
		distance = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
		return distance

class Pair:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.distance = p1.distance_to(p2)

def parse_data():
	data = sys.stdin.read().splitlines()
	data = [d.strip() for d in data] #remove white space to add support for files with white space after NODE_COORD_SECTION
	try:
		starting_index = data.index("NODE_COORD_SECTION") + 1
	except ValueError:
		pass
	else:
		data = data[starting_index:-1]

	points = []
	for d in data:
		p = d.split()
		if len(p) < 3: continue
		point = Point(p[0], float(p[1]), float(p[2]))
		points.append(point)
	return points

def sort_points(points):
	return sorted(points, key=attrgetter('x')) ,sorted(points, key=attrgetter('y')) #O(Nlog(N))

def subset_sorted_by_y(points_x, points_y):
	dictionary = {} # for constant lookup time
	for point in points_x:
		dictionary[point.id] = point

	result = []
	for point in points_y:
		if point.id in dictionary:
			result.append(point)
	return result

def smallest_pair(pair1, pair2):
	if pair1.distance < pair2.distance:
		return pair1
	else:
		return pair2


def divide_and_conquer(p_x, p_y):
	if len(p_x) < 4:
		return brute_force(p_x)

	middle_index = len(p_x)/2
	q_x = p_x[:middle_index]
	q_y = subset_sorted_by_y(q_x, p_y)
	r_x = p_x[middle_index:]
	r_y = subset_sorted_by_y(r_x, p_y)

	minimum_pair_q = divide_and_conquer(q_x, q_y)
	minimum_pair_r = divide_and_conquer(r_x, r_y)

	minimum_pair = smallest_pair(minimum_pair_q, minimum_pair_r)
	d = minimum_pair.distance
	L_x = (q_x[-1].x + r_x[0].x)/2.0
	
	S = []
	for point in p_y:
		if abs(L_x-point.x) < d:
			S.append(point)

	for i, p1 in enumerate(S):
		for j in range(i+1, min(len(S), i+15)):
			p2 = S[j]
			minimum_pair = smallest_pair(Pair(p1,p2),minimum_pair)
	return minimum_pair

def brute_force(points):
	minimum_pair = Pair(Point('init1', float('inf'), float('inf')), Point('init2', 0.0, 0.0))
	for p1 in points:
		for p2 in points:
			if (p1.id != p2.id):
				current_pair = Pair(p1, p2)
				minimum_pair = smallest_pair(current_pair, minimum_pair)
	return minimum_pair

# DOING STUFF!
points = parse_data()
px, py = sort_points(points) 
result = divide_and_conquer(px, py)

print result.p1.id, result.p2.id, result.distance