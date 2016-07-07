from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape

from panda3d.core import BitMask32
from panda3d.core import Vec3

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

class RollingEve(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		
		#	USER INPUT	#	
		self.accept('3', self.toggleDebug)	

		self.taskMgr.add(self.update,'update')            # Add task to task manager
		self.setup()

	def setup(self):
		#	WORLD	#
		self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
		self.debugNP.show()

		self.world = BulletWorld()
		self.world.setGravity(Vec3(0,0,-9.81))
		self.world.setDebugNode(self.debugNP.node())	
		
		#	FLOOR	#
		shape = BulletPlaneShape(Vec3(0,0,1),0)
		floorNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
		floorNP.node().addShape(shape)
		floorNP.setPos(0,0,0)
		floorNP.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(floorNP.node())	
	
	def update(self,task):			# Task that updates physics world every frame
		dt = globalClock.getDt()	# Get time elapsed since last render frame
		self.world.doPhysics(dt)	# Update physics world
		return Task.cont		# continue task

	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()
game = RollingEve()
game.run()
