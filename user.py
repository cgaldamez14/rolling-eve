'''
    USER MODULE
    This module will be used to create a new user every time the game start. A new user is created
    for the purposed of recording the users score in the game leaderboard.
    Author: Carlos M. Galdamez
'''

class User():

	'''
	    Constructor creates name and score instance variables.
	    @param name - name of user
	'''	
	def __init__(self,name):
		self.score = 0
		self.name = name

	'''
	    Adds new entry on the leaderboard file
	    @param level - level the entry pertains to
	'''
	def add_to_leaderboard(self,level):
		# Open file as read only
		leaderboard_file = open('files/.leaderboard.txt','r')
		# Store all contents of the file
		contents = leaderboard_file.readlines()
		leaderboard_file.close()	
		
		index = -1
		for entry in contents:
			index += 1
			if entry[0] == '#': continue
			elif entry[0] == '@' and entry.split()[1] == level and entry.split()[2] == 'END': 	# Look for the last entry in the list and place new entry after that
				contents.insert(index,self.name + ',' + str(self.score) + '\n')
				break;
		
		# Open file as writeable
		leaderboard_file = open('files/.leaderboard.txt','w')
		leaderboard_file.writelines(contents)			
		leaderboard_file.close()
