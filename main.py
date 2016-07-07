from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import BitMask32
from panda3d.core import Vec3,Vec4

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.actor.Actor import Actor
from direct.task import Task

class RollingEve(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		
		# base.disableMouse()
		base.camera.setPos(0,-500,100)
	
		b = OnscreenImage(parent=render2d,image = 'models/textures/sky.jpg')
		base.cam.node().getDisplayRegion(0).setSort(20)
	
		#	USER INPUT	#	
		self.accept('3', self.toggleDebug)	

		self.taskMgr.add(self.update,'update')            # Add task to task manager
		self.setup()

        	# Create some lighting
        	ambientLight = AmbientLight("ambientLight")
        	ambientLight.setColor(Vec4(.3, .3, .3, 1))
        	directionalLight = DirectionalLight("directionalLight")
        	directionalLight.setDirection(Vec3(-5, -5, -5))
        	directionalLight.setColor(Vec4(1, 1, 1, 1))
        	directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        	render.setLight(render.attachNewNode(ambientLight))
        	render.setLight(render.attachNewNode(directionalLight))

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
		floorModel = self.loader.loadModel('models/square')
		floorModel.setScale(1000,1000,1)
		floorModel.setPos(0,0,0)
		floorModel.reparentTo(self.render)
        	self.rock_texture = loader.loadTexture('models/textures/rock.jpg')
		floorModel.setTexture(self.rock_texture,0)

		#	FLOATING PLATFORM	#
		#shape = BulletPlaneShape(Vec3(0,0,1),1)
		#platformNP = self.render.attachNewNode(BulletRigidBodyNode('Plaform'))
		#platformNP.node().addShape(shape)
		#platformNP.setPos(0,0,5)
		#self.world.attachRigidBody(platformNP.node())
		#pModel = self.loader.loadModel('models/cube.egg')
                #pModel.setScale(10,10,1)
                #pModel.setPos(0,0,5)
                #pModel.reparentTo(self.render)

                #       FLOATING PLATFORM       #
                #shape = BulletPlaneShape(Vec3(0,0,1),1)
                #platformNP = self.render.attachNewNode(BulletRigidBodyNode('Plaform'))
                #platformNP.node().addShape(shape)
                #platformNP.setPos(10,0,10)
                #self.world.attachRigidBody(platformNP.node())
                #pModel = self.loader.loadModel('models/cube.egg')
                #pModel.setScale(10,10,1)
                #pModel.setPos(10,0,10)
                #pModel.reparentTo(self.render)

            	shape = BulletBoxShape(Vec3(20, 20, 1))
            	node = BulletRigidBodyNode('Box')
            	node.setMass(0)
           	node.addShape(shape)
            	np = self.render.attachNewNode(node)
            	np.setPos(10, 0, 10)
            	self.world.attachRigidBody(node)
		platformModel = self.loader.loadModel('models/cube.egg')
		platformModel.setScale(12,12,.50)
                platformModel.setPos(0,0,0)
                platformModel.reparentTo(np)
                self.plat_texture = loader.loadTexture('models/textures/platform.jpg')
                platformModel.setTexture(self.plat_texture,1)
		

            	shape2 = BulletBoxShape(Vec3(20, 20, 1))
            	node2 = BulletRigidBodyNode('Box')
            	node2.setMass(0)
            	node2.addShape(shape2)
            	np2 = self.render.attachNewNode(node2)
            	np2.setPos(0, 0, 5)
            	self.world.attachRigidBody(node2)

        	# Character
       		h = 21.00
        	w = 5.0
        	shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        	self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        	#    self.character.setMass(1.0)
        	self.characterNP = self.render.attachNewNode(self.character)
        	self.characterNP.setPos(10,-150,200)
        	self.characterNP.setH(45)
        	self.characterNP.setCollideMask(BitMask32.allOn())
        	self.world.attachCharacter(self.character)

        	self.actorNP = Actor('models/eve/eve.egg', {
                         'run' : 'models/eve/eve-run.egg',
                         'walk' : 'models/eve/eve-walk.egg',
                         'jump' : 'models/eve/eve-jump.egg'})

        	self.actorNP.reparentTo(self.characterNP)
        	self.actorNP.setScale(4.0)
        	self.actorNP.setH(90)
        	self.actorNP.setPos(0,0,-9)
		
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
