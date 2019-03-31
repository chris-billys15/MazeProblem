import BFS
import Astar

print(".-. .-')                .-') _    ('-.     _  .-')                             ('-.    .-. .-')           _  .-')               .-') _  .-') _    ('-. .-.")
print("\  ( OO )              ( OO ) )  ( OO ).-.( \( -O )                           ( OO ).-.\  ( OO )         ( \( -O )             ( OO ) )(  OO) )  ( OO )  /")
print(" ;-----.\   ,-.-') ,--./ ,--,'   / . --. / ,------.   ,--.   ,--.  ,--.       / . --. / ;-----.\   ,-.-') ,------.  ,-.-') ,--./ ,--,' /     '._ ,--. ,--.")
print(" | .-.  |   |  |OO)|   \ |  |\   | \-.  \  |   /`. '   \  `.'  /   |  |.-')   | \-.  \  | .-.  |   |  |OO)|   /`. ' |  |OO)|   \ |  |\ |'--...__)|  | |  |")
print(" | '-' /_)  |  |  \|    \|  | ).-'-'  |  | |  /  | | .-')     /    |  | OO ).-'-'  |  | | '-' /_)  |  |  \|  /  | | |  |  \|    \|  | )'--.  .--'|   .|  |")
print(" | .-. `.   |  |(_/|  .     |/  \| |_.'  | |  |_.' |(OO  \   /     |  |`-' | \| |_.'  | | .-. `.   |  |(_/|  |_.' | |  |(_/|  .     |/    |  |   |       |")
print(" | |  \  | ,|  |_.'|  |\    |    |  .-.  | |  .  '.' |   /  /\_   (|  '---.'  |  .-.  | | |  \  | ,|  |_.'|  .  '.',|  |_.'|  |\    |     |  |   |  .-.  |")
print(" | '--'  /(_|  |   |  | \   |    |  | |  | |  |\  \  `-./  /.__)   |      |   |  | |  | | '--'  /(_|  |   |  |\  \(_|  |   |  | \   |     |  |   |  | |  |")
print(" `------'   `--'   `--'  `--'    `--' `--' `--' '--'   `--'        `------'   `--' `--' `------'   `--'   `--' '--' `--'   `--'  `--'     `--'   `--' `--'")

print("WELCOME TO BINARY LABIRINTH!")
print("Choose your Path!")
valid  = True
while (valid):
	print("List of Choices :")
	print("1. BFS")
	print("2. A Star \n")
	choice = input(">> ")
	
	if (choice == "BFS" or choice == "1"):
		filename = input("FileName : ")
		BFS.mainBFS(filename)
	elif (choice == "A Star" or choice == "2"):
		filename = input("FileName : ")
		Astar.mainAStar(filename)
	elif(choice == "exit" or choice == "Exit"):
		valid = False
	else:
		print("Input is not Valid\n")
		valid = False


