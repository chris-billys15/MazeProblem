#initialize
content = []
baris = 0
kolom = 0
curPoint = (0,0)
prevPoint = (0,0)
BFSqueue = [] #queue of tuple point
passedNode = [] #array of tuple point yang sudah di lewati

def mainBFS(): 
    content = readFile("input.txt") #content -> list of string
    printMatrix(content)

    start = 0
    found = False
    while(start < len(content) and not(found)):
        if(content[start][0] == '0'):
            found = True
        else:
            start += 1

    baris = len(content)
    kolom = len(content[0])
    prevPoint = (start,0)
    curPoint = (start,0)


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
    pathChoice = 0 #Banyak jalan yang bisa diambil
    if(curPoint[1] == 0):
        print("Start")
        if(content[curPoint[0]][curPoint[1]+1] == '0' and searchPoint(curPoint[0],curPoint[1]+1,passedNode)):
            BFSqueue.append((curPoint[0],curPoint[1]+1))
    elif(curPoint[1] == baris -1):
        print("Goal")
    elif(curPoint[1] > 0 and curPoint[1] < baris):
        if(content[curPoint[0]][curPoint[1]-1] == '0' and searchPoint(curPoint[0],curPoint[1]-1,passedNode) == -1):
            BFSqueue.append((curPoint[0],curPoint[1]-1))
            pathChoice +=1
        if(content[curPoint[0]][curPoint[1]+1] == '0' and searchPoint(curPoint[0],curPoint[1]+1,passedNode) == -1):
            BFSqueue.append((curPoint[0],curPoint[1]+1))
            pathChoice +=1
        if(content[curPoint[0]-1][curPoint[1]] == '0' and searchPoint(curPoint[0]-1,curPoint[1],passedNode) == -1):
            BFSqueue.append((curPoint[0]-1,curPoint[1]))
            pathChoice +=1
        if(content[curPoint[0]+1][curPoint[1]] == '0' and searchPoint(curPoint[0]+1,curPoint[1],passedNode) == -1 ):
            BFSqueue.append((curPoint[0]+1,curPoint[1]))
            pathChoice +=1
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

# def BFS(startPoint):
#     if()

