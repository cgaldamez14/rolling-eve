from character import Character

from panda3d.core import BitMask32

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

from direct.actor.Actor import Actor



class Eve(Character):
	
	#	CONSTRUCTOR	#
	def __init__(self,render,world,health=100,damage=0):
		super(Eve,self).__init__('Eve',health,damage)
		self.render = render
		self.world = world		
		self.__height = 21.00
		self.__width = 5.0
		self.state = {'running': False, 'jumping' : False, 'rolling' : False}
		self.previousState = 'None'

		self.render_eve()

		self.previousZ = self.characterNP.getZ()

	def render_eve(self):
		shape = BulletCapsuleShape(self.__width, self.__height -2 * self.__width, ZUp)
		self.character = BulletCharacterControllerNode(shape,0.4,'Player')
		
		self.characterNP = self.render.attachNewNode(self.character)
		self.characterNP.setPos(10,-150,5)
		self.characterNP.setH(45)
		self.characterNP.setCollideMask(BitMask32.allOn())
		self.world.attachCharacter(self.character)

        	self.actorNP = Actor('models/eve/eve.egg', {
                         'run' : 'models/eve/eve-run.egg',
                         'walk' : 'models/eve/eve-walk.egg',
                         'jump' : 'models/eve/eve-jump.egg'})

        	self.actorNP.reparentTo(self.characterNP)
        	self.actorNP.setScale(4.0)
        	self.actorNP.setH(180)
        	self.actorNP.setPos(0,0,-9)
		


	
