'''
    TOKEN MODULE
    This module is used to create token in the different stages of the game. There are two 
    tokens large and regular and each have a different value. This module facilitates the 
    creation of these tokens.
    Author: Carlos M. Galdamez
'''

from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import XUp

from panda3d.core import BitMask32

class Token():
	
	# Class variables for regular sized token
	R_VALUE = 10
	R_RADIUS = 3
	R_HEIGHT = 6.5
	R_TOKEN_SCALE = (4,4,4)
	
	# Class variables for large token
	L_VALUE = 100
	L_RADIUS = 6
	L_HEIGHT = 15
	L_TOKEN_SCALE = (10,10,10)

	# Model used for token
	MODEL_PATH = 'models/environ/tire/tire.egg'

	'''
	    Constructor creates instance variables for the name and position or the token as well
	    as a reference to the game.
	    @param name - name of the token can either be 'Token' or 'BigToken'
	    @param location - position where the token will be placed
	    @param game - reference to the current game
	'''	
	def __init__(self,name,location,game):
		self.name = name
		(self.x,self.y,self.z) = location
		self.__game = game

		self.collect = base.loader.loadSfx("sfx/coin_collect.wav")
		self.collect.setVolume(.04)	

	
	'''
	    Creates regular token
	'''	
	def create_token(self):
		# Create a cylindrical collision shape
		collisionShape = BulletCylinderShape(Token.R_HEIGHT,Token.R_RADIUS,XUp)

		# Create a ghost node and attach to render
		self.ghostNode = BulletGhostNode(self.name)
		self.ghostNode.addShape(collisionShape)
		self.np = self.__game.render.attachNewNode(self.ghostNode)
			
		self.np.setCollideMask(BitMask32.allOff())
		self.np.setPos(self.x, self.y, self.z)
		self.__game.world.attachGhost(self.ghostNode)

		token = self.__game.loader.loadModel(Token.MODEL_PATH)
		token.setScale((Token.R_TOKEN_SCALE[0],Token.R_TOKEN_SCALE[1],Token.R_TOKEN_SCALE[2]))
                token.setPos(-.5,0,0)

                token.reparentTo(self.np)
		self.__game.e.tokens.append(self)


	'''
	    Create big token for end of stage
	'''
	def create_big_token(self):
		# Create a cylindrical collision shape
		collisionShape = BulletCylinderShape(Token.L_HEIGHT,Token.L_RADIUS,XUp)

		# Create a ghost node and attach to render
		self.ghostNode = BulletGhostNode(self.name)
		self.ghostNode.addShape(collisionShape)
		self.np = self.__game.render.attachNewNode(self.ghostNode)
			
		self.np.setCollideMask(BitMask32.allOff())
		self.np.setPos(self.x, self.y, self.z)
		self.__game.world.attachGhost(self.ghostNode)

		token = self.__game.loader.loadModel(Token.MODEL_PATH)
		token.setScale(Token.L_TOKEN_SCALE[0],Token.L_TOKEN_SCALE[1],Token.L_TOKEN_SCALE[2])
                token.setPos(-.5,0,0)

                token.reparentTo(self.np)
		self.__game.e.tokens.append(self)

    	
	def collected(self):
        	contactResult = self.__game.world.contactTestPair(self.__game.eve.currentControllerNode, self.ghostNode)
        	if len(contactResult.getContacts()) > 0:
			if(self.ghostNode.getName() == 'BigToken'):
				self.__game.levelFinish = True
				self.__game.user.score += Token.L_VALUE
			else:
				self.__game.user.score += Token.L_VALUE
			self.ghostNode.removeChild(0)
			self.__game.world.removeGhost(self.ghostNode)
			self.__game.e.tokens.remove(self)
			self.__game.eve.tiresCollected += 1 
			self.collect.play()

	def spinToken(self):
	        self.np.setH(self.np.getH() + 2)



