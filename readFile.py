def readFile(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content
#
# matrix = open('myfile.txt').read()
# matrix = [item.split() for item in matrix.split('\n')[:-1]]

content = readFile("input.txt")
print(content)
