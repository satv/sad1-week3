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
	r_x = p_x[middle_index+1:]
	r_y = subset_sorted_by_y(q_x, p_y)

	minimum_pair_q = divide_and_conquer(q_x, q_y)
	minimum_pair_r = divide_and_conquer(r_x, r_y)
	minimum_pair = smallest_pair(minimum_pair_q, minimum_pair_r)
	d = minimum_pair.distance

	L = q_x[len(q_x)-1]
	S = []
	
	for point in q_y:
		if math.fabs(L.x - point.x) < d:
			S.append(point)

	for point in r_y:
		if math.fabs(L.x - point.x) < d:
			S.append(point)

	S = sorted(S, key=attrgetter('y')) 

	for counter, point1 in enumerate(S):
		for i in range(counter, counter + 15):
			try:
				point2 = S[i]
			except IndexError:
				break
			
			distance = point1.distance_to(point2)
			if distance < d:
				minimum_pair = Pair(point1, point2)
				d = minimum_pair.distance

	return minimum_pair

def brute_force(points):
	current_minimum = float('inf') 
	minimum_pair = Pair(Point('init1', float('inf'), float('inf')), Point('init2', 0.0, 0.0))
	for p1 in points:
		for p2 in points:
			if (p1.id != p2.id):
				current_pair = Pair(p1, p2)
				minimum_pair = smallest_pair(current_pair, minimum_pair)
	return minimum_pair


# DOING STUFF!
#points = [Point(0,-2,1), Point(1,-1,2), Point(2,1,2), Point(3,2,1)]
points = parse_data()
px, py = sort_points(points) 
result = divide_and_conquer(px, py)
print result.p1.id, result.p2.id, result.distance


				