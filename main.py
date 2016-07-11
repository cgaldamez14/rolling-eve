from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import ZUp

from panda3d.core import NodePath, PandaNode, TextNode
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import Vec3,Vec4,VBase4
from panda3d.core import BitMask32
from panda3d.core import TransparencyAttrib

from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectFrame
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

from environ import Environment
from eve import Eve

import math,random

class RollingEve(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)		
		
		base.disableMouse()				# Disable use of mouse for camera movement
	
		# Non-Player related user input	
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
		self.createHealthBar()
		#b = OnscreenImage(parent=render2d,image = 'models/textures/sky.jpg')
		#base.cam.node().getDisplayRegion(0).setSort(20)

	def setup(self):
		#	WORLD	#
		self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))

		self.world = BulletWorld()
		#self.world.setGravity(Vec3(0,0,-9.81))
		self.world.setDebugNode(self.debugNP.node())	
		self.e = Environment(self.render, self.world, self.loader)
		

		#	FLOOR	#
		shape = BulletPlaneShape(Vec3(0,0,1),0)
		floorNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
		floorNP.node().addShape(shape)
		floorNP.setPos(0,0,0)
		floorNP.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(floorNP.node())
		floorModel = self.loader.loadModel('models/square')
		floorModel.setScale(3000,3000,1)
		floorModel.setPos(0,0,0)
		floorModel.reparentTo(self.render)
        	self.rock_texture = loader.loadTexture('models/textures/grass.jpg')
		floorModel.setTexture(self.rock_texture,0)

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

		#	INSTANTIATE MAIN CHARACTER	#	
		self.eve = Eve(self.render,self.world)

		base.camera.setPos(self.eve.characterNP.getX(),self.eve.characterNP.getY()-80,50)        	
       		
		# Create a floater object.  We use the "floater" as a temporary
        	# variable in a variety of calculations.
        
        	self.floater = NodePath(PandaNode("floater"))
        	self.floater.reparentTo(render)

		self.setTokens()

		self.e.render_tree_wo_leaves((50,30,2),(7,7,5),7,100)
		self.e.render_tree_wo_leaves((-50,-30,2),(7,7,7),7,200)

		self.e.render_creepy_tree((-100,220,2),(1,1,1.5),10,150)

		self.e.render_wide_ramp((-10,1000,0),(.2,1,.75))

		#self.plant((1,1,1),(30,-20,2),7,10,'models/environ/plant1/plants1.egg')
		self.mountain((4,2,2),(500,2500,70))
		self.mountain2((4,2,2),(2400,1000,50))
		self.mountain2((1,1,1),(1500,2000,50))
		
    	def processInput(self):
		return
	
	#	WORLD UPDATE TASK	#
	def update(self,task):			# Task that updates physics world every frame
        	dt = globalClock.getDt()
       		self.eve.updateEveAnim()
		self.updateCamera(self.eve.omega)

		# Update info on stats frame		
		self.bar['text'] = str(self.eve.health) + ' / 100'
		self.bar['value'] = self.eve.health
		self.world.doPhysics(dt, 10, 1/180.0)		# Update physics world
		return Task.cont				# Continue task
	
	def updateCamera(self,omega):
		base.camera.lookAt(self.eve.characterNP)
        	if (omega < 0):
            		base.camera.setX(base.camera, -300 * globalClock.getDt())
        	if (omega > 0):
            		base.camera.setX(base.camera, +300 * globalClock.getDt())


		# If the camera is too far from eve, move it closer.
        	# If the camera is too close to eve, move it farther.
        	camvec = self.eve.characterNP.getPos() - base.camera.getPos()
        	camvec.setZ(0)
        	camdist = camvec.length()
        	camvec.normalize()
        	if (camdist > 200.0):
            		base.camera.setPos(base.camera.getPos() + camvec*(camdist-200))
            		camdist = 200.0
        	if (camdist <= 200.0):
            		base.camera.setPos(base.camera.getPos() - camvec*(200-camdist))
            		camdist = 100.0
        	
        	self.floater.setPos(self.eve.characterNP.getPos())
        	self.floater.setZ(self.eve.characterNP.getZ() + 30.0)

		base.camera.lookAt(self.floater)

	def createHealthBar(self):
		self.statsFrame = DirectFrame(frameColor=(0, 0, 0, .4),frameSize=(-2, 3, -.1, 1),pos=(-.6, 0, .9))
		self.bar = DirectWaitBar(parent=self.statsFrame,text = "HEALTH", value = 100, range=100, pos = (.15,0,-.02))
		self.bar['text'] = str(self.eve.health) + ' / 100'
		self.bar['barColor'] = VBase4(153,0,0,1)
		self.bar.setScale(self.bar, .6)
		self.eveIcon = OnscreenImage(parent=self.bar,image = 'eve_face.png', pos = (-1.15, 0, -.075), scale = (.25,0,.25))
		self.eveIcon.setTransparency(TransparencyAttrib.MAlpha)
		
	
	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()

	def plant(self, scale, position, r, h, path):
		(x_scale,y_scale,z_scale) = scale
		(x_pos,y_pos,z_pos) = position
		radius = r
		height = h
		shape = BulletCylinderShape(radius,height,ZUp)
            	node = BulletRigidBodyNode('Plant')
            	node.setMass(0)
            	node.addShape(shape)
            	np = self.render.attachNewNode(node)
            	np.setPos(x_pos, y_pos, z_pos + z_pos * 6)
            	self.world.attachRigidBody(node)
		platformModel = self.loader.loadModel(path)
		platformModel.setScale(x_scale,y_scale,z_scale)
                platformModel.setPos(x_pos, y_pos, z_pos)
                platformModel.reparentTo(self.render)

	def mountain(self,scale,position):
		(x_scale,y_scale,z_scale) = scale
		(x_pos,y_pos,z_pos) = position
		mountModel = self.loader.loadModel('models/environ/mountain/mountainegg.egg')
		mountModel.setScale(x_scale,y_scale,z_scale)
                mountModel.setPos(x_pos, y_pos, z_pos)
                mountModel.reparentTo(self.render)

	def mountain2(self,scale,position):
		(x_scale,y_scale,z_scale) = scale
		(x_pos,y_pos,z_pos) = position
		mountModel = self.loader.loadModel('models/environ/mountain/mountainegg.egg')
		mountModel.setScale(x_scale,y_scale,z_scale)
                mountModel.setPos(x_pos, y_pos, z_pos)
		mountModel.setHpr(90,0,0)
                mountModel.reparentTo(self.render)
		
	def setTokens(self):
		for x in range(0, 200,10):
			token = self.loader.loadModel('models/environ/tire/tire.egg')
			token.setScale(4,4,4)
                	token.setPos(random.randrange(-1000,1000), random.randrange(-1000,1000), 12)
			#mountModel.setHpr(90,0,0)
                	token.reparentTo(self.render)		


game = RollingEve()
game.run()
