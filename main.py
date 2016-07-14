from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import ZUp,XUp

from panda3d.core import NodePath, PandaNode, TextNode
from panda3d.core import AmbientLight,DirectionalLight,Spotlight,PerspectiveLens
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
		#self.eve = Eve(self.render,self.world,self.accept, pos=(675,375,10))
		#self.eve = Eve(self.render,self.world,self.accept, pos=(392,1322,133))	###########################################################################################################
		#self.eve = Eve(self.render,self.world,self.accept, pos=(175,1049,48))	###########################################################################################################
		#self.eve = Eve(self.render,self.world,self.accept, pos=(101,29,18))	###########################################################################################################
		self.eve = Eve(self.render,self.world,self.accept)
		#self.eve = Eve(self.render,self.world,self.accept, pos=(0,-5125,-15))
		self.coord = OnscreenText(text='1', style = 1, fg= (1,1,1,1),  pos=(0,-0.95), align=TextNode.A_right, scale=0.08)
		self.taskMgr.add(self.updateCoord, 'updateCoord')
		self.taskMgr.add(self.update,'update')   

		#myFog = Fog("Fog Name")
		#myFog.setColor(.1,.1,.1)
		#myFog.setExpDensity(.001)
		#render.setFog(myFog)

		colour = (0.5,0.8,0.8)
		expfog = Fog("Scene-wide exponential Fog object")
		expfog.setColor(*colour)
		expfog.setExpDensity(0.0005)
		render.setFog(expfog)
		base.setBackgroundColor(*colour)


		#	INSTANTIATE MAIN CHARACTER	#	
		#self.eve = Eve(self.render,self.world,self.accept, pos=(675,375,10))
		#self.eve = Eve(self.render,self.world,self.accept)
		#self.eve = Eve(self.render,self.world,self.accept, pos=(330,1325,130))


		self.create_help_menu()		# Sets up help menu
		self.createHealthBar()		# Sets up health bar	
		self.createTiresCollected()	# Sets up tires collected count

		self.e = Environment(self.render, self.world, self.loader)
		self.set_lights()

		self.model = loader.loadModel('models/environ/sunset/sunset.egg')
		self.model.setPos(90)
		self.model.setScale(20)
		self.model.reparentTo(self.render)

		#	LOWEST LEVEL GROUND		#
		#(self,name,tex_path,b_scale,m_scale,b_pos,m_pos)
		self.createPlat('Ground', 'models/textures/grass.jpg',(165,165,0),(110,110,7), (1500,1200,0),(0,0,-8))
		self.createPlat('Platform', 'models/textures/grass.jpg',(200,200,5),(150,150,7), (0,-5150,-25),(0,0,-8))
		
		self.createPlat('Platform', 'models/textures/rock.jpg',(90,15,3),(60,10,2), (1200,1100,5),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(15,40,3),(10,25,2), (1025,1075,5),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(15,15,3),(10,10,2), (1025,925,10),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(20,40,3),(14,27,2), (1025,775,20),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(20,40,3),(14,27,2), (1025,625,20),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(15,15,3),(10,10,2), (1025,475,10),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(40,15,3),(25,10,2), (975,375,10),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(40,15,3),(25,10,2), (825,375,10),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(15,15,3),(10,10,2), (675,375,10),(0,0,0))

		self.createPlat('Ground', 'models/textures/grass.jpg',(150,935,0),(100,625,7), (0,-1000,0),(0,0,-10))
		
		z = 0
		y = 0
		for x in range(0,1000,100):
			self.createPlat('Platform', 'models/textures/rock.jpg',(15,15,3),(10,10,2), (750 - y,425 + x,30 + z),(0,0,0))
			y += 40
			z += 10

		self.createPlatVRot('Platform', 'models/textures/rock.jpg',(8,115,3),(5,75,2), (250,1200,60),(0,0,0),0,0)
		self.createPlat('Platform', 'models/textures/rock.jpg',(8,50,3),(5,33,2), (175,1025,35),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(20,40,3),(14,27,2), (170,850,30),(0,0,0))
		#self.createPlat('Platform', 'models/textures/rock.jpg',(15,40,3),(10,10,2), (98,675,13),(0,0,0))
		
		self.createPlat('Platform', 'models/textures/rock.jpg',(15,15,3),(10,10,2), (98,700,13),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(10,10,3),(7,7,2), (98,575,13),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(9,9,3),(6,6,2), (98,465,13),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(7,7,3),(5,5,2), (98,350,13),(0,0,0))

		self.createPlat('Platform', 'models/textures/rock.jpg',(20,40,3),(14,27,2), (98,200,5),(0,0,0))
		self.createPlat('Platform', 'models/textures/rock.jpg',(9,9,3),(6,6,2), (98,150,5),(0,0,0))

		self.createPlat('Platform', 'models/textures/rock.jpg',(9,9,3),(6,6,2), (98,35,5),(0,0,0))

		base.camera.setPos(self.eve.characterNP1.getX()+80,self.eve.characterNP1.getY(),50)        	
       		
		# Create a floater object.  We use the "floater" as a temporary
        	# variable in a variety of calculations.
        
        	self.floater = NodePath(PandaNode("floater"))
        	self.floater.reparentTo(render)

		self.setTokens()
		
		self.createToken((1023,1081,18))
		self.createToken((1252,1100,18))
		self.createToken((1200,1100,18))
		self.createToken((1023,922,23))
		self.createToken((1023,775,30))
		self.createToken((1023,740,40))
		self.createToken((1023,720,45))
		self.createToken((1023,700,50))
		self.createToken((1023,680,45))
		self.createToken((1023,660,40))
		self.createToken((1023,620,30))

		self.createToken((831,375,23))
		self.createToken((974,375,23))
		self.createToken((670,375,23))
		self.createToken((750,424,43))
		self.createToken((667,629,63))
		self.createToken((586,827,83))
		self.createToken((515,1028,103))
		self.createToken((423,1238,123))
		self.createToken((267,1255,115))
		self.createToken((256,1222,91))
		self.createToken((248,1200,75))
		self.createToken((334,1152,40))
		self.createToken((171,846,43))
		self.createToken((175,1046,48))
		self.createToken((176,1009,48))
		self.createToken((89,700,26))
		self.createToken((97,575,26))
		self.createToken((97,466,26))
		self.createToken((99,351,26))
		self.createToken((98,158,18))
		self.createToken((98,35,18))
		self.createToken((98,-92,10))
		self.createToken((97,-318,10))
		self.createToken((97,-675,10))
		self.createToken((90,-1053,10))
		self.createToken((-97,-318,10))
		self.createToken((-97,-675,10))
		self.createToken((-13,-500,10))
		self.createToken((-13,-400,10))
		self.createToken((-13,-300,10))
		self.createToken((-13,-200,10))
		self.createBigToken((0,-5150,0))

		self.totalTokens = len(self.tokens)

		

		self.createTree1((1036,801,25))


		#self.e.render_creepy_tree((-1000,-920,2),(1,1,1.5),10,150)
		#self.e.render_creepy_tree((-1100,1290,2),(1,1,1.5),10,150)
		#self.e.render_creepy_tree((-1403,-278,2),(1,1,1.5),10,150)
		#self.e.render_creepy_tree((-230,210,2),(1,1,1.5),10,150)
		#self.e.render_creepy_tree((-10,20,2),(1,1,1.5),10,150)
		#self.e.render_creepy_tree((-900,780,2),(1,1,1.5),10,150)

		#self.e.render_wide_ramp((-10,-1000,2),(.2,1,.75))
		ramp = EnvObject('wide_ramp',(-10,-1000,2),self.render,self.world,self.loader)
		ramp.renderObject((.1,1,.75),collisionOn = True)
		for x in range(0,500,50):
			self.createTree1((-50,-700 + x,2))
			self.createTree1((30,-700 + x,2))
		

		self.plant((1,1,1),(109,-87,10),7,10,'models/environ/plant1/plants1.egg')
		self.plant((1,1,1),(59,-265,10),7,10,'models/environ/plant1/plants1.egg')
		self.plant((1,1,1),(65,-691,10),7,10,'models/environ/plant1/plants1.egg')
		self.plant((1,1,1),(90,-1446,10),7,10,'models/environ/plant1/plants1.egg')
		self.plant((1,1,1),(-115,-1865,10),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(-125,973,10),7,10,'models/environ/plant1/plants1.egg')
		self.plant((1,1,1),(1261,1091,10),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(-123,-985,18),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(234,-789,2),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(1030,-1000,2),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(987,892,2),7,10,'models/environ/plant1/plants1.egg')
		#self.plant((1,1,1),(678,678,2),7,10,'models/environ/plant1/plants1.egg')

		self.mountain((4,2,2),(500,2500,70))
		self.mountain2((4,2,2),(2400,1000,50))
		self.mountain2((1,1,1),(1500,2000,50))
		self.collect = base.loader.loadSfx("sfx/coin_collect.wav")
		self.collect.setVolume(.04)
		self.meadow = base.loader.loadSfx("sfx/meadow_land.wav")
		self.meadow.setLoop(True)
		self.meadow.setVolume(.2)
		self.meadow.play()
		self.music = base.loader.loadMusic("sfx/nerves.mp3")
		self.music.setVolume(.07)
		self.music.setLoop(True)
		self.music.play()
		self.complete = base.loader.loadSfx("sfx/complete.wav")
		self.complete.setLoop(False)
		self.complete.setVolume(.07)

	def createPlat(self,name,tex_path,b_scale,m_scale,b_pos,m_pos):
		p = Platform(name,b_pos,b_scale)
		p.create_bullet_node(self.render, self.world)
		p.add_model(m_scale,m_pos)
		p.add_texture(tex_path)

	def createPlatVRot(self,name,tex_path,b_scale,m_scale,b_pos,m_pos,h,p):
		p = Platform(name,b_pos,b_scale)
		p.create_bullet_node(self.render, self.world)
		p.add_model(m_scale,m_pos)
		p.add_texture(tex_path)
		p.rotateV()
	
	def createTree1(self,pos):
		tree = EnvObject('tree1',pos,self.render,self.world,self.loader)
		tree.renderObject((7,7,5),collisionOn = True)
	
	def set_lights(self):
        	ambientLight = AmbientLight("ambientLight")
        	ambientLight.setColor(Vec4(.3, .3, .3, 1))
        	directionalLight = DirectionalLight("directionalLight")
        	directionalLight.setDirection(Vec3(-5, -5, -5))
        	directionalLight.setColor(Vec4(1, 1, 1, 1))
        	directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        	render.setLight(render.attachNewNode(ambientLight))
        	render.setLight(render.attachNewNode(directionalLight))
	
	
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
			textObject = OnscreenText(parent = results,text = 'Wheels Collected : ' + str(self.eve.tiresCollected) + ' / ' + str(self.totalTokens) , pos = (0, -.2), scale = .1, fg=(1,0,0,1))
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
		#self.statsFrame = DirectFrame(frameColor=(0, 0, 0, .4),frameSize=(-2, 3, -.1, 1),pos=(-.6, 0, .9))
		#self.bar = DirectWaitBar(parent=self.statsFrame,text = "HEALTH", value = 100, range=100, pos = (.15,0,-.02))
		#self.bar['text'] = str(self.eve.health) + ' / 100'
		#self.bar['barColor'] = VBase4(153,0,0,1)
		#self.bar.setScale(self.bar, .6)
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

	def plant(self, scale, position, r, h, path):
		(x_scale,y_scale,z_scale) = scale
		(x_pos,y_pos,z_pos) = position
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
	
	def setTokens(self):
		self.tokens = []
		self.nodes=[]
		#for x in range(0, 200,10):
		#	# create a collision shape
		#	collisionShape = BulletCylinderShape(6.5,3,XUp)
		#	# create a ghost node
		#	ghostNode = BulletGhostNode('Token' + str(x))
		#	# add collision shape to the ghost node
		#	ghostNode.addShape(collisionShape)
		#	# add ghost node to scene graph
		#	np = self.render.attachNewNode(ghostNode)
		#	
		#	# turn off collisions for ghost node
		#	np.setCollideMask(BitMask32.allOff())
		#	# position ghost node in the scene
		#	np.setPos(random.randrange(-1000,1000), random.randrange(-1000,1000), 12)
		#	# add ghost node to bullet world
		#	self.world.attachGhost(ghostNode)
		#	token = self.loader.loadModel('models/environ/tire/tire.egg')
		#	token.setScale(4,4,4)
                #	token.setPos(-.5,0,0)
		#	#mountModel.setHpr(90,0,0)
                #	token.reparentTo(np)
		#	self.tokens.append(ghostNode)
		#	self.nodes.append(np)
		#	#plat_texture = loader.loadTexture('models/textures/gold.jpg')
		#	#plat_texture.setWrapU(Texture.WM_repeat)
		#	#plat_texture.setWrapV(Texture.WM_repeat)
                #	#token.setTexture(plat_texture,1)		
		# add this task to task manager
		self.taskMgr.add(self.processContacts,'Ghost-Collision-Detection')
		self.taskMgr.add(self.spinToken,'TokenSpin')

	def spinToken(self,task):
		for node in self.nodes:
	            node.setH(node.getH() + 2)
		return Task.cont	

   
	def processContacts(self,task):
	        for tokens in self.tokens:
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
			self.tokens.remove(secondNode)
			self.eve.tiresCollected += 1 
			self.score['text'] = str(self.eve.tiresCollected)
			#Eve.INITIAL_ROLL_SPEED += 75
			self.collect.play()
	
	def createToken(self,position):
		(x,y,z) = position
		# create a collision shape
		collisionShape = BulletCylinderShape(6.5,3,XUp)
		# create a ghost node
		ghostNode = BulletGhostNode('Token')
		# add collision shape to the ghost node
		ghostNode.addShape(collisionShape)
		# add ghost node to scene graph
		np = self.render.attachNewNode(ghostNode)
			
		# turn off collisions for ghost node
		np.setCollideMask(BitMask32.allOff())
		# position ghost node in the scene
		np.setPos(x, y, z)
		# add ghost node to bullet world
		self.world.attachGhost(ghostNode)
		token = self.loader.loadModel('models/environ/tire/tire.egg')
		token.setScale(4,4,4)
                token.setPos(-.5,0,0)
		#mountModel.setHpr(90,0,0)
                token.reparentTo(np)
		self.tokens.append(ghostNode)
		self.nodes.append(np)

	def createBigToken(self,position):
		(x,y,z) = position
		# create a collision shape
		collisionShape = BulletCylinderShape(15,6,XUp)
		# create a ghost node
		ghostNode = BulletGhostNode('BigToken')
		# add collision shape to the ghost node
		ghostNode.addShape(collisionShape)
		# add ghost node to scene graph
		np = self.render.attachNewNode(ghostNode)
			
		# turn off collisions for ghost node
		np.setCollideMask(BitMask32.allOff())
		# position ghost node in the scene
		np.setPos(x, y, z)
		# add ghost node to bullet world
		self.world.attachGhost(ghostNode)
		token = self.loader.loadModel('models/environ/tire/tire.egg')
		token.setScale(10,10,10)
                token.setPos(-.5,0,0)
		#mountModel.setHpr(90,0,0)
                token.reparentTo(np)
		self.tokens.append(ghostNode)
		self.nodes.append(np)
		#slight = Spotlight('slight')
		#slight.setColor(VBase4(255, 0, 0, 1))
		#lens = PerspectiveLens()
		#slight.setLens(lens)
		#slnp = render.attachNewNode(slight)
		#slnp.setPos(x, y, z + 100)
		#slnp.lookAt(token)
		#render.setLight(slnp)

	def updateCoord(self, task):
        	x = self.eve.currentNP.getX()
       		y = self.eve.currentNP.getY()
        	z = self.eve.currentNP.getZ()
        	self.coord.setText(str(x) + " , " + (str(y)) + " , "  + str(z))
        	return Task.cont



game = RollingEve()
game.run()
