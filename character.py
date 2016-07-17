'''
    CHARACTER MODULE
    Any character created of this game will inherit from this character class
    Author: Carlos M Galdamez
'''
class Character(object):
	
	'''
	    Constructor creates three instance variables for Character.
	    @param name - name of the character
	    @param health - total health of the character
	    @param damage - damage that the character causes if it were to attack other characters
	'''
	def __init__(self, name,health, damage):
		self.name = name		
		self.health = health
		self.damage = damage 
