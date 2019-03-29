import heapq
import collections

global curPoint

DIRECTIONS = [(0, -1, 'B'), (0, 1, 'T'), (-1, 0, 'U'), (1, 0, 'S'),]

Node = collections.namedtuple('Node', ['heuristic_distance', 'n', 'distance', 'current_position', 'visitedNode', 'direction'])
curPoint = ()
def manhattan(current, goal):
    """
    Return the heuristic distance from current position to goal.
    """
    print("manhattan :" ,abs(current[0] - goal[0]) + abs(current[1] - goal[1]))
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def readFile(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def printMatrix(M):
    for i in range(len(M)):
        for j in range (len(M[i])):
            if(j == len(M[i]) -1):
                print(M[i][j])
            else:
                print(M[i][j],end ='')

def main():
    global curPoint
    """
    content: A list of lists.  '0' indicates a passable cell.
    """
    content = readFile("input.txt") #content -> list of string
    # printMatrix(content)

    baris = len(content)
    kolom = len(content[0])

    start = 0
    found = False
    while(start < baris and not(found)):
        if(content[start][0] == '0'):
            found = True
        else:
            start += 1
        
    goal = 0
    found = False
    while(goal < baris and not(found)):
        if(content[goal][len(content)-1] == '0'):
            found = True
        else:
            goal += 1

    curPoint = (start,0)
    goalPoint = (goal,len(content)-1)

    # A list of all visited coordinates.
    visitedNode = []
    
    # Each node consists of (estimated path distance, n, distance, (x, y), visitedNode, direction)
    open = [Node(manhattan(curPoint, goalPoint), 0, 0, curPoint, [], "")]
    
    
    
    n = 0
    while open:
        print(curPoint)
        print("OPEN")
        node = heapq.heappop(open)
        print("heapq")
        _, _, distance, curPoint, visitedNode, direction = node
        print("node")
        if curPoint in visitedNode:
            print("visitedNode")
            continue
        if curPoint == goalPoint:
            print("goal")
            break
        print('curPoint :', curPoint)
        print('visitedNode :', visitedNode)
        visitedNode.append(curPoint)
        print("appended")
        print("current point : " , curPoint)
        print("visitedNode : " , visitedNode)
        
        # Now consider moves in each direction.
        for dx, dy, d in DIRECTIONS:
            new_point = (curPoint[0] + dx, curPoint[1] + dy)
            print("new point :" , new_point)
            if new_point not in visitedNode and (content[new_point[0]][new_point[1]] != '1'):
                print("ok")
                if new_point[curPoint[1]] >= 0 and new_point[curPoint[1]] <= len(content[0]):
                    h = distance + 1 + manhattan(new_point, goalPoint)
                    print("h" , h)
                    tie_break = 4 if direction != d else 0 # Prefer moving straight
                    new_node = Node(h, n + tie_break, distance + 1, new_point, node, d)
                    heapq.heappush(open, new_node)
                    # print(new_node)
                    n = n + 1
                    print("masuk")
                    curPoint = new_point
            print("n", n)
            print('curPoint :', curPoint)
            print('visitedNode :', visitedNode)
            print('node :', node)
            
            

    # Return a path to node
    result = ""
    if (curPoint == goalPoint):
        result = node.direction + result
        node = node.visitedNode
    print(result)
    return result

main()