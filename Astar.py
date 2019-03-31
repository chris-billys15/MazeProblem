# from queue import PriorityQueue, Queue
import copy

content = [] # Matrix of char
visitedPoint = [] # Point yang dilalui atau diexpand
AStarQueue = [] #Queue of Node

class Node:
	def __init__(self, cost, point ,path):
		self.cost = cost
		self.point = point
		self.path = path
	def addPath(self):
		pathTemp = []
		pathTemp = copy.deepcopy(self.path)
		pathTemp.append(self.point)
	
def printMatrix(M):
	for i in range(len(M)):
		for j in range (len(M[i])):
			if(j == len(M[i]) -1):
				if(M[i][j] == '1'):
					print("\033[1;37;47m",M[i][j] ,"\033[0m")
				elif(M[i][j] == '0'):
					print("\033[1;38;48m",M[i][j] ,"\033[0m")
				elif(M[i][j] == '#'):
					print("\033[5;37;46m",M[i][j] ,"\033[0m")
			else:
				if(M[i][j] == '1'):
					print("\033[1;37;47m",M[i][j] ,"\033[0m",end ='')
				elif(M[i][j] == '0'):
					print("\033[1;38;48m",M[i][j] ,"\033[0m",end ='')
				elif(M[i][j] == '#'):
					print("\033[5;37;46m",M[i][j] ,"\033[0m",end ='')
				# print(M[i][j],end ='')


def manhattan(current, goal):
	#Return the heuristic distance from current position to goal.
	# print("manhattan :" ,abs(current[0] - goal[0]) + abs(current[1] - goal[1]))
	return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def cost(curNode,goalNode,costToNode):
	gn = curNode.cost - manhattan(curNode.point,goalNode.point) + costToNode -1
	cost = gn + manhattan(curNode.point,goalNode.point)
	return cost 

def readFile(filename):
	contentTemp = []
	with open(filename) as f:
		contentTemp = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	contentTemp = [x.strip() for x in contentTemp]
	maps = []
	for i in range(len(contentTemp)):
		maps.append([])
		for j in range (len(contentTemp[0])):
			if(contentTemp[i][j] == '1'):
				# maps[i][j] = '1'
				maps[i].append('1')
			elif(contentTemp[i][j] == '0'):
				# maps[i][j] = '0'
				maps[i].append('0')
	return maps

def manyPath(curPos):
	pathChoice = 0
	if(curPos[1] == 0):
		if(content[curPos[0]][curPos[1]+1]):
			pathChoice += 1
		if(content[curPos[0]+1][curPos[1]]):
			pathChoice += 1
		if(content[curPos[0]-1][curPos[1]]):
			pathChoice += 1
	elif(curPos[1] == len(content) - 1):
		if(content[curPos[0]][curPos[1]-1]):
			pathChoice += 1
		if(content[curPos[0]+1][curPos[1]]):
			pathChoice += 1
		if(content[curPos[0]-1][curPos[1]]):
			pathChoice += 1
	elif(curPos[1] > 0 and curPos[1] < len(content)):
		if(content[curPos[0]][curPos[1]+1]):
			pathChoice += 1
		if(content[curPos[0]][curPos[1]-1]):
			pathChoice += 1
		if(content[curPos[0]+1][curPos[1]]):
			pathChoice += 1
		if(content[curPos[0]-1][curPos[1]]):
			pathChoice += 1
	return pathChoice

def searchPoint(pointB, pointK, list1):
	found = False
	i = 0
	while(i < len(list1) and not(found)):
		if(list1[i][0] == pointB and list1[i][1] == pointK):
			found = True
		else:
			i += 1
	if(found):
		return i
	else:
		return -1

def addPrio(Queue,item):
	Queue.append(item)
	idx = 0
	while(Queue[idx].cost < item.cost):
		idx+=1

	j = len(Queue) -1
	while(j > idx):
		Queue[j] = Queue[j-1]
		j -= 1
	Queue[j] = item
	
def expand(curNode,goalNode):
	curPos = copy.deepcopy(curNode.point)
	# print(curPos)
	visitedPointFromNode = [] # Point yang di lalui dari Node A ke B
	visitedPoint.append(curPos)
	visitedPointFromNode.append(curPos)

	#expand ke kanan
	if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
		curPosRight = copy.deepcopy(curPos)
		curPosRight[1] += 1
		addPrio(AStarQueue,buildNode(curNode,goalNode,curPosRight))

	#expand ke kiri
	if(content[curPos[0]][curPos[1]-1] == '0' and searchPoint(curPos[0], curPos[1]-1, visitedPoint) == -1):
		curPosLeft = copy.deepcopy(curPos)
		curPosLeft[1] -= 1
		addPrio(AStarQueue,buildNode(curNode,goalNode,curPosLeft))

	#expand ke bawah
	if(content[curPos[0]+1][curPos[1]] == '0' and searchPoint(curPos[0]+1, curPos[1], visitedPoint) == -1):
		curPosDown = copy.deepcopy(curPos)
		curPosDown[0] += 1
		addPrio(AStarQueue,buildNode(curNode,goalNode,curPosDown))

	#expand ke atas
	if(content[curPos[0]-1][curPos[1]] == '0' and searchPoint(curPos[0]-1, curPos[1], visitedPoint) == -1):
		curPosUp = copy.deepcopy(curPos)
		curPosUp[0] -= 1
		addPrio(AStarQueue,buildNode(curNode,goalNode,curPosUp))

def buildNode(curNode,goalNode,curPos):
	visitedPointFromNode = []
	visitedPointFromNode.append(curPos)
	visitedPoint.append(curPos)
	if(curPos[1] == 0):
		if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
			curPos[1] += 1
			visitedPoint.append(curPos)
			visitedPointFromNode.append(curPos)
	while(manyPath(curPos) < 3 and manyPath(curPos) != 1):
		if(curPos[1] == 0):
			if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
				curPos[1] += 1
				visitedPoint.append(curPos)
				visitedPointFromNode.append(curPos)

		elif(curPos[1] > 0 and curPos[1] < len(content)):
			if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
				curPos[1] += 1
				visitedPoint.append(curPos)
				visitedPointFromNode.append(curPos)

			if(content[curPos[0]][curPos[1]-1] == '0' and searchPoint(curPos[0], curPos[1]-1, visitedPoint) == -1):
				curPos[1] -= 1
				visitedPoint.append(curPos)
				visitedPointFromNode.append(curPos)

			if(content[curPos[0]+1][curPos[1]] == '0' and searchPoint(curPos[0]+1, curPos[1], visitedPoint) == -1):
				curPos[0] += 1
				visitedPoint.append(curPos)
				visitedPointFromNode.append(curPos)

			if(content[curPos[0]-1][curPos[1]] == '0' and searchPoint(curPos[0]-1, curPos[1], visitedPoint) == -1):
				curPos[0] -= 1
				visitedPoint.append(curPos)
				visitedPointFromNode.append(curPos)

	return Node(cost(curNode, goalNode, len(visitedPointFromNode)),curPos, curNode.path + visitedPointFromNode)

def AStar(curNode, goalNode):
	curTemp = copy.deepcopy(curNode)
	goalTemp = copy.deepcopy(goalNode)
	while(curTemp.point[1] < len(content)-1):
		expand(curTemp,goalTemp)
		curTemp = AStarQueue.pop(0)
	goalNode = copy.deepcopy(curTemp)
	# print(goalNode.path)
	return goalNode

# def init():
# 	content = [] # Matrix of char
# 	visitedPoint = [] # Point yang dilalui atau diexpand
# 	AStarQueue = [] #Queue of Node

def mainAStar(filename):
	global content, visitedPoint, AStarQueue
	content = readFile(filename)
	# print(content)

	goal = 0
	found = False
	while(goal < len(content) and not(found)):
		if(content[goal][len(content)-1] == '0'):
			found = True
		else:
			goal += 1

	goalNode = Node(0,[goal,len(content)-1],[])

	start = 0
	found = False
	while(start < len(content) and not(found)):
		if(content[start][0] == '0'):
			found = True
		else:
			start += 1
	curNode = Node(0 + manhattan([start,0],[goal,len(content)-1]),[start,0],[[start,0]])
	curNode = AStar(curNode, goalNode)

	i = 0
	while(i < len(curNode.path)):
		content[curNode.path[i][0]][curNode.path[i][1]] = '#'
		i += 1
	printMatrix(content)
	print("Total Biaya : ", curNode.cost)