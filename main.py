from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import ZUp,XUp

from panda3d.core import NodePath, PandaNode, TextNode
from panda3d.core import Vec3,Vec4,VBase4,LVecBase3f
from panda3d.core import BitMask32
from panda3d.core import TransparencyAttrib
from panda3d.core import Fog

from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DGG
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from direct.task import Task

from envobject import EnvObject
from platform import Platform
from environ import Environment
from eve import Eve

import math,random

class RollingEve(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		self.levelFinish = False
		self.gameOver = False
		self.alreadyPlayed= False

		self.start = DirectFrame(frameColor=(.05, 0, .05, 1),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
		self.kyklops1 = OnscreenImage(parent=self.start,image = 'kyklops.png', pos = (.9, 0, .3), scale = (.3,0,.3))
		self.kyklops1.setTransparency(TransparencyAttrib.MAlpha)
		self.title = OnscreenImage(parent=self.start,image = 'title.png', pos = (0, 0, 0), scale = (.8,0,.3))
		self.title.setTransparency(TransparencyAttrib.MAlpha)
		self.rolling_eve = OnscreenImage(parent=self.start,image = 'rolling-eve.png', pos = (-.95, 0, -.1), scale = (.5,0,.5))
		self.rolling_eve.setTransparency(TransparencyAttrib.MAlpha)
		self.start_btn = DirectButton(parent=self.start,text = "START",pos=LVecBase3f(0,0,-.5),scale=.2,command=self.setup,pressEffect=1,relief=DGG.RAISED)
		self.start_btn['text_scale'] = (.45,.45)
		self.start_btn['text_pos'] = (.1,.1)
		self.start_btn['text_fg'] = (.1,.1,.1,1)
		self.start_btn['text_shadow'] = (1,1,1,1)
		self.start_btn['image'] = 'btn.png'
		self.start_btn['image_scale'] = (1.8,0,.6)
		self.start_btn['image_pos'] = (0,0,.25)
		hover = base.loader.loadSfx("sfx/hover.mp3")
		hover.setPlayRate(5)
		hover.setVolume(.05)
		click = base.loader.loadSfx("sfx/click.wav")	
		self.start_btn['rolloverSound'] = hover
		self.start_btn['clickSound'] = click

		self.intro = base.loader.loadMusic("sfx/not_seems.mp3")
		self.intro.setVolume(.5)
		self.intro.setLoop(True)
		self.intro.play()

	def setup(self):

		transition = Transitions(loader)
		transition.setFadeColor(0, 0, 0)
		transition.fadeOut()
		self.start.destroy()
		
		transition.fadeIn(10)	

		base.disableMouse()					# Disable use of mouse for camera movement

		base.win.setClearColor(Vec4(0,0.102,0.2,1))						
	
		# Non-Player related user input	
		self.accept('h', self.toggleHelp)
		self.accept('f1', self.toggleDebug)
        	 # Add task to task manager

		#b = OnscreenImage(parent=render2d,image = 'models/textures/sky.jpg')
		#base.cam.node().getDisplayRegion(0).setSort(20)
		#	INSTANTIATE BULLET WORLD	#
		self.world = BulletWorld()
		self.world.setGravity(Vec3(0,0,-9.81))
		
		#	Create and attach bullet debug node	#
		self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
		self.world.setDebugNode(self.debugNP.node())	

		self.eve = Eve(self.render,self.world,self.accept)
		self.coord = OnscreenText(text='1', style = 1, fg= (1,1,1,1),  pos=(0,-0.95), align=TextNode.A_right, scale=0.08)

		self.create_help_menu()		# Sets up help menu
		self.createHealthBar()		# Sets up health bar	
		self.createTiresCollected()	# Sets up tires collected count

		self.e = Environment(self.render, self.world, self.loader)
		self.e.loadStage1()
		
		
		#	TASK FOR ALL GAME STAGES	#
		self.taskMgr.add(self.processContacts,'Ghost-Collision-Detection')
		self.taskMgr.add(self.updateCoord, 'updateCoord')  
		self.taskMgr.add(self.spinToken,'TokenSpin')
		self.taskMgr.add(self.update,'update') 

		self.model = loader.loadModel('models/environ/sunset/sunset.egg')
		self.model.setPos(90)
		self.model.setScale(20)
		self.model.reparentTo(self.render)


		base.camera.setPos(self.eve.characterNP1.getX()+80,self.eve.characterNP1.getY(),50)        	
       		
		# Create a floater object.  We use the "floater" as a temporary
        	# variable in a variety of calculations.
        
        	self.floater = NodePath(PandaNode("floater"))
        	self.floater.reparentTo(render)

		self.mountain((4,2,2),(500,2500,70))
		self.mountain2((4,2,2),(2400,1000,50))
		self.mountain2((1,1,1),(1500,2000,50))
		self.collect = base.loader.loadSfx("sfx/coin_collect.wav")
		self.collect.setVolume(.04)
		#self.meadow = base.loader.loadSfx("sfx/meadow_land.wav")
		#self.meadow.setLoop(True)
		#self.meadow.setVolume(.2)
		#self.meadow.play()
		#self.music = base.loader.loadMusic("sfx/nerves.mp3")
		#self.music.setVolume(.07)
		#self.music.setLoop(True)
		#self.music.play()
		self.complete = base.loader.loadSfx("sfx/complete.wav")
		self.complete.setLoop(False)
		self.complete.setVolume(.07)
	
	
	#	WORLD UPDATE TASK	#
	def update(self,task):
		check = self.eve.currentControllerNode.isOnGround()				# Task that updates physics world every frame
        	dt = globalClock.getDt()
       		self.eve.updateEveAnim()
		self.updateCamera(self.eve.omega)

		# Update info on stats frame		
		self.bar['text'] = str(self.eve.health) + ' / 100'
		self.bar['value'] = self.eve.health
		self.world.doPhysics(dt, 400, 1/180.0)		# Update physics world
		if check == False and self.eve.currentControllerNode.isOnGround() is True:
			self.eve.finishJump()
		if self.eve.currentNP.getZ() < -26:
			results = DirectFrame(frameColor=(0, 0, 0, .1),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
			textObject = OnscreenText(parent = results,text = 'GAME OVER', pos = (0, 0), scale = .1, fg=(1,0,0,1))
		if self.levelFinish is True:
			results = DirectFrame(frameColor=(0, 0, 0, .1),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
			textObject = OnscreenText(parent = results,text = 'STAGE 1 COMPLETE', pos = (0, 0), scale = .1, fg=(1,0,0,1))
			textObject = OnscreenText(parent = results,text = 'Wheels Collected : ' + str(self.eve.tiresCollected) + ' / ' + str(len(self.e.tokens)) , pos = (0, -.2), scale = .1, fg=(1,0,0,1))
			if self.complete.status() is not self.complete.PLAYING and self.alreadyPlayed is False:
				self.alreadyPLayed = True
				self.complete.play()
			

		return Task.cont				# Continue task
	

	def updateCamera(self,omega):
		if self.eve.state['rolling'] is False:
			n = self.eve.characterNP1
		else:
			n = self.eve.characterNP2

		base.camera.lookAt(n)
        	if (omega < 0):
            		base.camera.setX(base.camera, -200 * globalClock.getDt())
        	if (omega > 0):
            		base.camera.setX(base.camera, +200 * globalClock.getDt())


		# If the camera is too far from eve, move it closer.
        	# If the camera is too close to eve, move it farther.
		pos = 0	
		z=0	
		if self.eve.state['rolling'] is False:
			pos = self.eve.characterNP1.getPos()
			z=self.eve.characterNP1.getZ()
		else:
			pos = self.eve.characterNP2.getPos()
			z=self.eve.characterNP2.getZ()
        	
		camvec = pos - base.camera.getPos()
        	camvec.setZ(0)
        	camdist = camvec.length()
        	camvec.normalize()
        	if (camdist > 200.0):
            		base.camera.setPos(base.camera.getPos() + camvec*(camdist-200))
			base.camera.setZ(z + 50.0)
            		camdist = 200.0
        	if (camdist <= 200.0):
            		base.camera.setPos(base.camera.getPos() - camvec*(200-camdist))
			base.camera.setZ(z + 50.0)
            		camdist = 100.0
        	
        	self.floater.setPos(pos)
        	self.floater.setZ(z + 30.0)

		base.camera.lookAt(self.floater)

	def createHealthBar(self):
		self.statsFrame = DirectFrame(frameColor=(0, 0, 0, .4),frameSize=(-2, 3, -.1, 1),pos=(-.6, 0, .9))
		self.bar = DirectWaitBar(parent=self.statsFrame,text = "HEALTH", value = 100, range=100, pos = (.15,0,-.02))
		self.bar['text'] = str(self.eve.health) + ' / 100'
		self.bar['barColor'] = VBase4(153,0,0,1)
		self.bar.setScale(self.bar, .6)
		self.eveIcon = OnscreenImage(parent=self.bar,image = 'eve_face.png', pos = (-1.15, 0, -.075), scale = (.25,0,.25))
		self.eveIcon.setTransparency(TransparencyAttrib.MAlpha)

	def createTiresCollected(self):
		self.shape = OnscreenImage(image = 'tire_score.png', pos = (1, 0, -.85), scale = (.3,0,.1))
		self.shape.setTransparency(TransparencyAttrib.MAlpha)
		self.tire = OnscreenImage(parent=self.shape,image = 'tire.png', pos = (-1, 0, 0), scale = (.4,1,1))
		self.tire.setTransparency(TransparencyAttrib.MAlpha)
		self.score = OnscreenText(parent=self.shape, text = str(self.eve.tiresCollected), pos = (0, -.1), scale = (.3,.8), fg=(255,255,255,1))
	

	def create_help_menu(self):
		self.helpMenu = DirectFrame(frameColor=(0, 0, 0, .8),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
		textObject1 = OnscreenText(parent=self.helpMenu, text = 'CONTROL KEYS', pos = (0, .2), scale = 0.1, fg=(255,255,255,1))
		textObject1 = OnscreenText(parent=self.helpMenu, text = '[w] - Forward', pos = (0, 0), scale = 0.07, fg=(255,255,255,1))
		textObject2 = OnscreenText(parent=self.helpMenu, text = '[a] - Left', pos = (0, -.1), scale = 0.07,fg=(255,255,255,1))
		textObject3 = OnscreenText(parent=self.helpMenu, text = '[d] - Right', pos = (0, -.2), scale = 0.07,fg=(255,255,255,1))
		textObject4 = OnscreenText(parent=self.helpMenu, text = '[space] - Jump', pos = (0, -.3), scale = 0.07,fg=(255,255,255,1))
		textObject5 = OnscreenText(parent=self.helpMenu, text = '[1] - Change character mode', pos = (0, -.4), scale = 0.07,fg=(255,255,255,1))
		textObject6 = OnscreenText(parent=self.helpMenu, text = '[h] - Help Menu', pos = (0, -.5), scale = 0.07,fg=(255,255,255,1))

		self.helpMenu.hide()

	def toggleHelp(self):
		pause = base.loader.loadSfx("sfx/pause.wav")
		if self.helpMenu.isHidden():
			pause.play()
			self.taskMgr.remove('update')
			self.helpMenu.show()
		else:
			pause.play()
			self.taskMgr.add(self.update,'update')            # Add task to task manager
			self.helpMenu.hide()
	
	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()

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
	
	# create a task function
	def detectCollisionForGhosts(self, task):
		ghostNode = self.eve.characterNP.node()
		# print number of colliding objects
		print ghostNode.getNumOverlappingNodes()
		# print all the colliding objects
		for collidingNode in ghostNode.getOverlappingNodes():
			print node
		# continue the task
		return Task.cont

	def spinToken(self,task):
		for node in self.e.tokens_np:
	            node.setH(node.getH() + 2)
		return Task.cont	

   
	def processContacts(self,task):
	        for tokens in self.e.tokens:
	            self.testWithSingleBody(tokens)
		return Task.cont

    	def testWithSingleBody(self, secondNode):
		if self.eve.state['rolling'] is False:
			n = self.eve.character1
		else:
			n = self.eve.character2
        	# test sphere for contacts with secondNode
        	contactResult = self.world.contactTestPair(n, secondNode) # returns a BulletContactResult object
        	if len(contactResult.getContacts()) > 0:
			if(secondNode.getName() == 'BigToken'):
				self.levelFinish = True
			secondNode.removeChild(0)
			self.world.removeGhost(secondNode)
			self.e.tokens.remove(secondNode)
			self.eve.tiresCollected += 1 
			self.score['text'] = str(self.eve.tiresCollected)
			#Eve.INITIAL_ROLL_SPEED += 75
			self.collect.play()
	

	def updateCoord(self, task):
        	x = self.eve.currentNP.getX()
       		y = self.eve.currentNP.getY()
        	z = self.eve.currentNP.getZ()
        	self.coord.setText(str(x) + " , " + (str(y)) + " , "  + str(z))
        	return Task.cont



game = RollingEve()
game.run()
