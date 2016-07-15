from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import XUp

from panda3d.core import BitMask32

class Token():
	
	R_VALUE = 10
	R_RADIUS = 3
	R_HEIGHT = 6.5
	R_TOKEN_SCALE = (4,4,4)
	
	L_VALUE = 100
	L_RADIUS = 6
	L_HEIGHT = 15
	L_TOKEN_SCALE = (10,10,10)

	MODEL_PATH = 'models/environ/tire/tire.egg'
	
	def __init__(self,name,location,render,world,loader):
		self.name = name
		(self.x,self.y,self.z) = location
		self.__render = render
		self.__world = world
		self.__loader = loader

	
	def create_token(self):
		collisionShape = BulletCylinderShape(Token.R_HEIGHT,Token.R_RADIUS,XUp)
		ghostNode = BulletGhostNode(self.name)
		ghostNode.addShape(collisionShape)
		np = self.__render.attachNewNode(ghostNode)
			
		np.setCollideMask(BitMask32.allOff())
		np.setPos(self.x, self.y, self.z)
		self.__world.attachGhost(ghostNode)

		token = self.__loader.loadModel(Token.MODEL_PATH)
		token.setScale((Token.R_TOKEN_SCALE[0],Token.R_TOKEN_SCALE[1],Token.R_TOKEN_SCALE[2]))
                token.setPos(-.5,0,0)

                token.reparentTo(np)
		return (ghostNode,np)
		#self.tokens.append(ghostNode)
		#self.nodes.append(np)

	def create_big_token(self):
		collisionShape = BulletCylinderShape(Token.L_HEIGHT,Token.L_RADIUS,XUp)
		ghostNode = BulletGhostNode(self.name)
		ghostNode.addShape(collisionShape)
		np = self.__render.attachNewNode(ghostNode)
			
		np.setCollideMask(BitMask32.allOff())
		np.setPos(self.x, self.y, self.z)
		self.__world.attachGhost(ghostNode)

		token = self.__loader.loadModel(Token.MODEL_PATH)
		token.setScale(Token.L_TOKEN_SCALE[0],Token.L_TOKEN_SCALE[1],Token.L_TOKEN_SCALE[2])
                token.setPos(-.5,0,0)

                token.reparentTo(np)
		return (ghostNode,np)
		#self.tokens.append(ghostNode)
		#self.nodes.append(np)

