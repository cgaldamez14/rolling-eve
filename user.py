class User():
	
	def __init__(self,name):
		self.score = 0
		self.name = name

	def add_to_leaderboard(self,level):
		leaderboard_file = open('.leaderboard.txt','r')
		contents = leaderboard_file.readlines()
		leaderboard_file.close()	
		
		index = -1
		for entry in contents:
			index += 1
			if entry[0] == '#': continue
			elif entry[0] == '@' and entry.split()[1] == level and entry.split()[2] == 'END':		
				contents.insert(index,self.name + ',' + str(self.score) + '\n')
				break;
		
		leaderboard_file = open('.leaderboard.txt','w')
		leaderboard_file.writelines(contents)
		leaderboard_file.close()
