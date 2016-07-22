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

from direct.interval.IntervalGlobal import *

from direct.task import Task

from onscreeninterface import OnScreenInterface
from envobject import EnvObject
from platform import Platform
from environ import Environment
from eve import Eve
from kyklops import Kyklops

import time

from direct.showbase.Transitions import Transitions


import math,random

class RollingEve(ShowBase):

	MUSIC_ON = True
	SOUND_EFFECT_ON =True

	def __init__(self):
		ShowBase.__init__(self)
		self.levelFinish = False
		self.gameOver = False
		self.alreadyPlayed= False
		self.current_level = 'L0'
		self.user = None
		self.tasks=[]
		self.enemies=[]

		base.disableMouse()					# Disable use of mouse for camera movement

		base.win.setClearColor(Vec4(0,0.102,0.2,1))	

		self.accept('m',self.toggle_music)
		self.accept('f', self.toggle_sfx)									
	

		self.set_world()
		self.set_debug_mode()
			

		self.create_player()

		self.set_interface()

	def toggle_music(self):
		if RollingEve.MUSIC_ON is True:
			base.enableMusic(False)
			RollingEve.MUSIC_ON = False
		else:
			base.enableMusic(True)
			RollingEve.MUSIC_ON = True

	def toggle_sfx(self):
		if RollingEve.SOUND_EFFECT_ON is True:
			base.enableSoundEffects(False)
			RollingEve.SOUND_EFFECT_ON = False
		else:
			base.enableSoundEffects(True)
			RollingEve.SOUND_EFFECT_ON = True

	def set_interface(self,start=True):
		#	ONSCREEN INTERFACE	#
		self.interface = OnScreenInterface(self)
		if start is True:
			self.interface.load_initial_interface()
		self.interface.load_essentials()

	def set_world(self):
		#	INSTANTIATE BULLET WORLD	#
		self.world = BulletWorld()
		self.world.setGravity(Vec3(0,0,-9.81))

	def set_debug_mode(self):
		#	Create and attach bullet debug node	#
		self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
		self.world.setDebugNode(self.debugNP.node())

	def create_player(self):
		self.eve = Eve(self,self.render,self.world,self.accept)

	def clean_and_set(self,level):
		print '\n\tCLEANING WORLD...\n'
		#self.interface.stage_select_frame.hide()
		self.interface.main_frame.hide()
		self.world = None
		self.interface = None
		self.taskMgr.remove('moving')
		self.taskMgr.remove('Ghost-Collision-Detection') 
		self.taskMgr.remove('TokenSpin')
		self.taskMgr.remove('update') 
		self.taskMgr.remove('Timer')
		self.taskMgr.remove('weapon') 
		self.taskMgr.remove('attacks')
		self.taskMgr.remove('attacked')


		print self.taskMgr.getTasks()

		for node in self.render.getChildren():
			if node != camera:
				node.remove_node()
		self.set_world()
		self.set_debug_mode()
		self.create_player()
		self.set_interface(start = False)
		self.taskMgr.add(self.interface.show_title,'Title')
		self.taskMgr.add(self.interface.update_timer,'Timer')
		self.accept('h', self.do_nothing)
		self.accept('f1', self.do_nothing)
		self.setup(level)
		
	def do_nothing(self):
		pass

	def setup(self,level):
		self.actual_start = globalClock.getRealTime()
		self.current_level = level
		self.interface.set_timer()
		self.interface.create_stage_title(self.current_level)

		self.e = Environment(self)
		if self.current_level == 'L1':
			self.e.loadStage1()
			self.eve.render_eve((1500,1100,1.5))
		elif self.current_level == 'L2':
			self.e.loadStage2()
			#self.eve.render_eve((1500,1100,1005))
			#self.eve.render_eve((1323,876,1091))
			#self.eve.render_eve((1335,760,1101))
			#self.eve.render_eve((1419,844,1111))
			#self.eve.render_eve((1254,917,1180))
			#self.eve.render_eve((1402,878,1213))
			#self.eve.render_eve((1326,875,1250))
			#self.eve.render_eve((1350,760,1260))
			self.eve.render_eve((1363,982,1335))
			#self.eve.render_eve((1345,1690,1335))
			#self.eve.render_eve((1179,1600,1435))
			e1 = Kyklops(self,health = 100, damage=.22)
			e1.render_kyklops(((1363,1150,1335)))
			#e1.scout_area((1363,1200,1335),(1363,1100,1335))
			self.enemies.append(e1)
			self.taskMgr.add(e1.detect_collision,"attacked")

		
		#	TASK FOR ALL GAME STAGES	#
		self.taskMgr.add(self.processContacts,'Ghost-Collision-Detection') 
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
		self.interface.bar['text'] = str(self.eve.health) + ' / 100'
		self.interface.bar['value'] = self.eve.health
		self.world.doPhysics(dt, 400, 1/180.0)		# Update physics world
		if check == False and self.eve.currentControllerNode.isOnGround() is True:
			self.eve.finishJump()
		
		if self.current_level == 'L1':
			death = -26
		elif self.current_level == 'L2':
			death = 900
		if self.eve.currentNP.getZ() < death:
			#results = DirectFrame(frameColor=(0, 0, 0, .1),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
			#textObject = OnscreenText(parent = results,text = 'GAME OVER', pos = (0, 0), scale = .1, fg=(1,0,0,1))
			self.clean_and_set(self.current_level)
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

	
	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.taskMgr.add(self.interface.updateCoord, 'updateCoord') 
			self.interface.coord.show()
			self.debugNP.show()
		else:
			self.taskMgr.remove('updateCoord') 
			self.interface.coord.hide()
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
			self.interface.score['text'] = str(self.eve.tiresCollected)
			#Eve.INITIAL_ROLL_SPEED += 75
			self.collect.play()
	




game = RollingEve()
game.run()
