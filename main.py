from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import ZUp

from panda3d.core import NodePath, PandaNode
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import Vec3,Vec4
from panda3d.core import BitMask32

from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

from environ import Environment
from eve import Eve

class RollingEve(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)		

		base.disableMouse()
		#base.camera.setPos(0,-2000,200)

		b = OnscreenImage(parent=render2d,image = 'models/textures/sky.jpg')
		base.cam.node().getDisplayRegion(0).setSort(20)
	
		#	USER INPUT	#	
		self.accept('3', self.toggleDebug)

        	inputState.watchWithModifiers('forward', 'w')
        	inputState.watchWithModifiers('reverse', 's')
        	inputState.watchWithModifiers('turnLeft', 'a')
        	inputState.watchWithModifiers('turnRight', 'd')
		inputState.watchWithModifiers('jump', 'space')
	

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

		#	INSTANTIATE MAIN CHARACTER	#	
		self.eve = Eve(self.render,self.world)

		base.camera.setPos(self.eve.characterNP.getX(),self.eve.characterNP.getY()-80,60)        	
       		
		# Create a floater object.  We use the "floater" as a temporary
        	# variable in a variety of calculations.
        
        	self.floater = NodePath(PandaNode("floater"))
        	self.floater.reparentTo(render)

		self.e.render_tree_wo_leaves((50,30,2),(7,7,5),7,100)
		self.e.render_tree_wo_leaves((-50,-30,2),(7,7,7),7,200)

		self.e.render_creepy_tree((-100,220,2),(1,1,1.5),10,150)

		#self.plant((1,1,1),(30,-20,2),7,10,'models/environ/plant1/plants1.egg')
		self.mountain((4,2,2),(500,2500,70))
		self.mountain2((4,2,2),(2400,1000,50))
		self.mountain2((1,1,1),(1500,2000,50))
		
    	def processInput(self, dt):
		self.eve.state['jumping'] = False
		self.eve.state['running'] = False
		speed = Vec3(0, 0, 0)
        	omega = 0.0		
		if self.eve.characterNP.getZ() >= 10.50:
			self.eve.state['jumping'] = True
			return (speed,omega)

        	if inputState.isSet('forward'): 
			speed.setY( 30.0)
			self.eve.state['running'] = True
        	if inputState.isSet('reverse'): speed.setY(-30.0)
        	if inputState.isSet('left'):    speed.setX(-30.0)
        	if inputState.isSet('right'):   speed.setX( 30.0)
        	if inputState.isSet('turnLeft'):  omega =  120.0
        	if inputState.isSet('turnRight'): omega = -120.0
        	if inputState.isSet('jump'): 
			self.eve.character.setMaxJumpHeight(7.0)
        		self.eve.character.setJumpSpeed(5.0)
			self.eve.character.doJump()
			self.eve.actorNP.setPlayRate(.75,'jump')	# Slow down jumping anim play rate
			self.eve.state['jumping'] = True
		# self.eve.actorNP.pose('walk',0)
        	self.eve.character.setAngularMovement(omega)
        	self.eve.character.setLinearMovement(speed, True)

		return (speed,omega)

	def update(self,task):			# Task that updates physics world every frame
        	dt = globalClock.getDt()
       		(speed,omega) = self.processInput(dt)
		print self.eve.characterNP.getZ()
		if self.eve.state['running'] is True:
			if self.eve.actorNP.getCurrentFrame('run') == (self.eve.actorNP.getNumFrames('run') - 1):
				self.eve.actorNP.loop('run',fromFrame=0)
			else:
				self.eve.actorNP.loop('run',restart=0)
		elif self.eve.state['jumping'] is True:
			if self.eve.previousState is not 'jump':
				self.eve.actorNP.play('jump')
			
		else:
			self.eve.actorNP.stop(self.eve.actorNP.getCurrentAnim())
			self.eve.actorNP.pose('walk',5) 
		
		self.eve.previousState = self.eve.actorNP.getCurrentAnim()
		
		base.camera.lookAt(self.eve.characterNP)
        	if (omega < 0):
            		base.camera.setX(base.camera, -40 * globalClock.getDt())
        	if (omega > 0):
            		base.camera.setX(base.camera, +40 * globalClock.getDt())


		# If the camera is too far from eve, move it closer.
        	# If the camera is too close to eve, move it farther.
        	camvec = self.eve.characterNP.getPos() - base.camera.getPos()
        	camvec.setZ(0)
        	camdist = camvec.length()
        	camvec.normalize()
        	if (camdist > 300.0):
            		base.camera.setPos(base.camera.getPos() + camvec*(camdist-300))
            		camdist = 300.0
        	if (camdist <= 300.0):
            		base.camera.setPos(base.camera.getPos() - camvec*(300-camdist))
            		camdist = 150.0
        	
        	self.floater.setPos(self.eve.characterNP.getPos())
        	self.floater.setZ(self.eve.characterNP.getZ() + 50.0)
		#base.camera.setPos(self.eve.characterNP.getX(),self.eve.characterNP.getY()-300,100)        

		base.camera.lookAt(self.floater)

		self.world.doPhysics(dt, 10, 1/180.0)	# Update physics world
		return Task.cont		# continue task

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
		
		

game = RollingEve()
game.run()
