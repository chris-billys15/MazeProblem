import copy

content = [] # Matrix of char
visitedPoint = [] # Point yang dilalui atau diexpand
BFSQueue = [] #Queue of Node

class Node:
	def __init__(self, point ,path):
		self.point = point
		self.path = path
	
def printMatrix(M):
	for i in range(len(M)):
		for j in range (len(M[i])):
			if(j == len(M[i]) -1):
				if(M[i][j] == '1'):
					print("\033[1;37;47m",M[i][j] ,"\033[0m")
				elif(M[i][j] == '0'):
					print("\033[1;39;48m",M[i][j] ,"\033[0m")
				elif(M[i][j] == '#'):
					print("\033[5;37;46m",M[i][j] ,"\033[0m")
				elif(M[i][j] == 'V'):
					print("\033[2;37;41m",M[i][j] ,"\033[0m")
			else:
				if(M[i][j] == '1'):
					print("\033[1;37;47m",M[i][j] ,"\033[0m",end ='')
				elif(M[i][j] == '0'):
					print("\033[1;39;48m",M[i][j] ,"\033[0m",end ='')
				elif(M[i][j] == '#'):
					print("\033[5;37;46m",M[i][j] ,"\033[0m",end ='')
				elif(M[i][j] == 'V'):
					print("\033[2;37;41m",M[i][j] ,"\033[0m",end ='')

def readFile(filename):
	contentTemp = []
	with open(filename) as f:
		contentTemp = f.readlines()

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

def expand(curNode):
	curPos = copy.deepcopy(curNode.point)
	# print(curPos)
	visitedPointFromNode = [] # Point yang di lalui dari Node A ke B
	visitedPoint.append(curPos)
	visitedPointFromNode.append(curPos)

	#expand ke kanan
	if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
		curPosRight = copy.deepcopy(curPos)
		curPosRight[1] += 1
		BFSQueue.append(findNode(curNode,curPosRight))
		# print(BFSQueue)

	#expand ke kiri
	if(curPos[1] != 0):
		if(content[curPos[0]][curPos[1]-1] == '0' and searchPoint(curPos[0], curPos[1]-1, visitedPoint) == -1):
			curPosLeft = copy.deepcopy(curPos)
			curPosLeft[1] -= 1
			BFSQueue.append(findNode(curNode,curPosLeft))

	#expand ke bawah
	if(content[curPos[0]+1][curPos[1]] == '0' and searchPoint(curPos[0]+1, curPos[1], visitedPoint) == -1):
		curPosDown = copy.deepcopy(curPos)
		curPosDown[0] += 1
		BFSQueue.append(findNode(curNode,curPosDown))

	#expand ke atas
	if(content[curPos[0]-1][curPos[1]] == '0' and searchPoint(curPos[0]-1, curPos[1], visitedPoint) == -1):
		curPosUp = copy.deepcopy(curPos)
		curPosUp[0] -= 1
		BFSQueue.append(findNode(curNode,curPosUp))

def findNode(curNode,curPos):
	visitedPointFromNode = []
	visitedPointFromNode.append(curPos)
	visitedPoint.append(curPos)
	if(curPos[1] == 0):
		if(content[curPos[0]][curPos[1]+1] == '0' and searchPoint(curPos[0], curPos[1]+1, visitedPoint) == -1):
			curPos[1] += 1
			visitedPoint.append(curPos)
			visitedPointFromNode.append(curPos)
	while(manyPath(curPos) < 3 and manyPath(curPos) > 1):
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
	return Node(curPos ,curNode.path + visitedPointFromNode)

def BFS(curNode):
	nodeTemp = curNode
	i = 0
	while(nodeTemp.point[1] < len(content)-1):
		# print(i)
		expand(nodeTemp)
		nodeTemp = BFSQueue.pop(0)
		i += 1
	# print(nodeTemp.path)
	return nodeTemp

def mainBFS(filename):
	global content, visitedPoint, BFSQueue
	content = readFile(filename)
	# print(content)
	start = 0
	found = False
	while(start < len(content) and not(found)):
		if(content[start][0] == '0'):
			found = True
		else:
			start += 1
	curNode = Node([start,0],[[start,0]])
	curNode = BFS(curNode)

	i = 0
	while(i<len(visitedPoint)):
		content[visitedPoint[i][0]][visitedPoint[i][1]] = 'V'
		i+=1
		
	i = 0
	while(i < len(curNode.path)):
		content[curNode.path[i][0]][curNode.path[i][1]] = '#'
		i += 1
	printMatrix(content)