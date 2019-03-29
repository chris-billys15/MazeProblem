from queue import PriorityQueue, Queue
import copy

#initialize
content = []
baris = 0
kolom = 0
BFSqueue = Queue() #queue of tuple point
visitedNode = [] #array of tuple point yang sudah di lewati
curPoint = [0,0]

def readFile(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content
    #
    # matrix = open('myfile.txt').read()
    # matrix = [item.split() for item in matrix.split('\n')[:-1]]



def printMatrix(M):
    for i in range(len(M)):
        for j in range (len(M[i])):
            if(j == len(M[i]) -1):
                print(M[i][j])
            else:
                print(M[i][j],end ='')




def expand(curPoint):
    global baris
    # pathChoice = 0 #Banyak jalan yang bisa diambil
    if(curPoint[1] == 0):
        print("Start")
        if(content[curPoint[0]][curPoint[1]+1] == '0' and searchPoint(curPoint[0],curPoint[1]+1,visitedNode)):
            BFSqueue.put((curPoint[0],curPoint[1]+1))
    elif(curPoint[1] == baris -1):
        print("Goal")
    elif(curPoint[1] > 0 and curPoint[1] < baris):
        if(content[curPoint[0]][curPoint[1]-1] == '0' and searchPoint(curPoint[0],curPoint[1]-1,visitedNode) == -1):
            BFSqueue.put((curPoint[0],curPoint[1]-1))
        if(content[curPoint[0]][curPoint[1]+1] == '0' and searchPoint(curPoint[0],curPoint[1]+1,visitedNode) == -1):
            BFSqueue.put((curPoint[0],curPoint[1]+1))
        if(content[curPoint[0]-1][curPoint[1]] == '0' and searchPoint(curPoint[0]-1,curPoint[1],visitedNode) == -1):
            BFSqueue.put((curPoint[0]-1,curPoint[1]))
        if(content[curPoint[0]+1][curPoint[1]] == '0' and searchPoint(curPoint[0]+1,curPoint[1],visitedNode) == -1 ):
            BFSqueue.put((curPoint[0]+1,curPoint[1]))

# def manyPath(curPoint):
#     pathChoice = 0
#     if(curPoint[1] == 0):
#         if(content[curPoint[0]][curPoint[1]+1]):
#             pathChoice += 1
#         if(content[curPoint[0]+1][curPoint[1]]):
#             pathChoice += 1
#         if(content[curPoint[0]-1][curPoint[1]]):
#             pathChoice += 1
#     elif(curPoint[1] == baris - 1):
#         if(content[curPoint[0]][curPoint[1]-1]):
#             pathChoice += 1
#         if(content[curPoint[0]+1][curPoint[1]]):
#             pathChoice += 1
#         if(content[curPoint[0]-1][curPoint[1]]):
#             pathChoice += 1
#     elif(curPoint[1] > 0 and curPoint[1] < baris):
#         if(content[curPoint[0]][curPoint[1]+1]):
#             pathChoice += 1
#         if(content[curPoint[0]][curPoint[1]-1]):
#             pathChoice += 1
#         if(content[curPoint[0]+1][curPoint[1]]):
#             pathChoice += 1
#         if(content[curPoint[0]-1][curPoint[1]]):
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
        if(list1[i][0] == pointB and list1[i][1] == pointK):
            found = True
        else:
            i += 1
    if(found):
        return i
    else:
        return -1



def BFS(curPoint):
    expand(curPoint)
    visitedNode.append(curPoint)
    curPoint = BFSqueue.get()
    expand(curPoint)
    visitedNode.append(curPoint)
    curPoint = BFSqueue.get()
    while(curPoint[1] < len(content)-1):
        expand(curPoint)
        visitedNode.append(curPoint)
        curPoint = BFSqueue.get()
    visitedNode.append(curPoint)

content = readFile("input.txt") #content -> list of string
print(content)
print()
printMatrix(content)

start = 0
found = False
while(start < len(content) and not(found)):
    if(content[start][0] == '0'):
        found = True
    else:
        start += 1

curPoint[0] = copy.deepcopy(start) 
curPoint[1] = copy.deepcopy(0)
baris = len(content)
kolom = len(content[0])
curPoint = (start,0)
BFS(curPoint)
print(BFSqueue)
print(visitedNode)

