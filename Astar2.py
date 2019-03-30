from queue import PriorityQueue, Queue
import copy

#initialize
content = []
baris = 0
kolom = 0
AStarqueue = PriorityQueue() # priority queue of tuple point
visitedNode = [] #list of tuple point yang sudah di lewati
curNode = [0,0,0]
goalNode = [0,0,0]

def readFile(filename):
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
                maps[i].append(1)
            elif(contentTemp[i][j] == '0'):
                # maps[i][j] = '0'
                maps[i].append(0)
    return maps
    #
    # matrix = open('myfile.txt').read()
    # matrix = [item.split() for item in matrix.split('\n')[:-1]]


def manhattan(current, goal):
    #Return the heuristic distance from current position to goal.
    # print("manhattan :" ,abs(current[1] - goal[1]) + abs(current[2] - goal[2]))
    return abs(current[1] - goal[1]) + abs(current[2] - goal[2])


def printMatrix(M):
    for i in range(len(M)):
        for j in range (len(M[i])):
            if(j == len(M[i]) -1):
                if(M[i][j] == 1):
                    print("\033[1;36;46m",M[i][j] ,"\033[0m")
                elif(M[i][j] == 0):
                    print("\033[1;37;47m",M[i][j] ,"\033[0m")
                elif(M[i][j] == 4):
                    print("\033[1;37;40m",M[i][j] ,"\033[0m")
            else:
                if(M[i][j] == 1):
                    print("\033[1;36;46m",M[i][j] ,"\033[0m",end ='')
                elif(M[i][j] == 0):
                    print("\033[1;37;47m",M[i][j] ,"\033[0m",end ='')
                elif(M[i][j] == 4):
                    print("\033[1;37;40m",M[i][j] ,"\033[0m",end ='')
                # print(M[i][j],end ='')


def cost(curNode,Direction):
    nodeTemp = copy.deepcopy(curNode)
    gn = nodeTemp[0] - manhattan(nodeTemp,goalNode) + 1
    if(Direction == "Left"):
        nodeTemp[2] -= 1
    elif(Direction == "Right"):
        nodeTemp[2] += 1
    elif(Direction == "Up"):
        nodeTemp[1] -= 1
    elif(Direction == "Down"):
        nodeTemp[1] += 1
    cost = gn + manhattan(nodeTemp,goalNode)
    return cost 

def expand(curNode):
    global baris
    
    
    if(curNode[2] == 0):
        print("Start")
        if(content[curNode[1]][curNode[2]+1] == 0 and searchPoint(curNode[1],curNode[2]+1,visitedNode)):
            
            AStarqueue.put([cost(curNode, "Right"), curNode[1], curNode[2]+1])
    
    elif(curNode[2] == baris -1):
        print("Goal")
    
    elif(curNode[2] > 0 and curNode[2] < baris):
        if(content[curNode[1]][curNode[2]-1] == 0 and searchPoint(curNode[1],curNode[2]-1,visitedNode) == -1):

            AStarqueue.put([cost(curNode, "Left"), curNode[1], curNode[2]-1])

        if(content[curNode[1]][curNode[2]+1] == 0 and searchPoint(curNode[1],curNode[2]+1,visitedNode) == -1):
            
            AStarqueue.put([cost(curNode, "Right"), curNode[1], curNode[2]+1])
        
        if(content[curNode[1]-1][curNode[1]] == 0 and searchPoint(curNode[1]-1,curNode[2],visitedNode) == -1):
            
            AStarqueue.put([cost(curNode, "Up"), curNode[1]-1, curNode[2]])
        
        if(content[curNode[1]+1][curNode[1]] == 0 and searchPoint(curNode[1]+1,curNode[2],visitedNode) == -1 ):
            
            AStarqueue.put([cost(curNode, "Down"), curNode[1]+1, curNode[2]])

# def manyPath(curNode):
#     pathChoice = 0
#     if(curNode[1] == 0):
#         if(content[curNode[0]][curNode[1]+1]):
#             pathChoice += 1
#         if(content[curNode[0]+1][curNode[1]]):
#             pathChoice += 1
#         if(content[curNode[0]-1][curNode[1]]):
#             pathChoice += 1
#     elif(curNode[1] == baris - 1):
#         if(content[curNode[0]][curNode[1]-1]):
#             pathChoice += 1
#         if(content[curNode[0]+1][curNode[1]]):
#             pathChoice += 1
#         if(content[curNode[0]-1][curNode[1]]):
#             pathChoice += 1
#     elif(curNode[1] > 0 and curNode[1] < baris):
#         if(content[curNode[0]][curNode[1]+1]):
#             pathChoice += 1
#         if(content[curNode[0]][curNode[1]-1]):
#             pathChoice += 1
#         if(content[curNode[0]+1][curNode[1]]):
#             pathChoice += 1
#         if(content[curNode[0]-1][curNode[1]]):
#             pathChoice += 1
#     return pathChoice


# def isEmpty(list):
#     if(len(list) == 0):
#         return True
#     else:
#         return False

def searchPoint(pointB, pointK, list1):
    found = False
    i = 0
    while(i < len(list1) and not(found)):
        if(list1[i][1] == pointB and list1[i][2] == pointK):
            found = True
        else:
            i += 1
    if(found):
        return i
    else:
        return -1



def AStar(curNode,goalNode):
    # global distance
    # global h
    # global manhattan_cost

    # distance = 0
    # h = 0
    # manhattan_cost = 0

    while(curNode[1] < len(content)-1):
        expand(curNode)
        content[curNode[1]][curNode[2]] = 4
        visitedNode.append(curNode)
        curNode = AStarqueue.get()
        # print(goalNode)
        # print(curNode)
    content[curNode[1]][curNode[2]] = 4
    visitedNode.append(curNode)



content = readFile("input.txt") #content -> list of string
printMatrix(content)
print (content)
start = 0
found = False
while(start < len(content) and not(found)):
    if(content[start][0] == 0):
        found = True
    else:
        start += 1


goal = 0
found = False
while(goal < len(content) and not(found)):
    if(content[goal][len(content[0])-1] == 0):
        found = True
    else:
        goal += 1

goalNode[0] = 0 #initialize (Later will be updated)
goalNode[1] = copy.deepcopy(goal)
goalNode[2] = copy.deepcopy(len(content)-1) 

curNode[0] = 0 + manhattan(curNode,goalNode) #Cost dari node
curNode[1] = copy.deepcopy(start) #Koordinat Y dari Node (Baris)
curNode[2] = copy.deepcopy(0) #Koordinat X dari Node (Kolom)

print("curNode :", curNode)
print("goalNode : " , goalNode)
baris = len(content)
kolom = len(content[0])


AStar(curNode,goalNode)

# print(AStarqueue)
print(visitedNode)
printMatrix(content)