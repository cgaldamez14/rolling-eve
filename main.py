from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletWorld

from panda3d.core import NodePath, PandaNode, TextNode
from panda3d.core import Vec3

from direct.showbase.ShowBase import ShowBase

from direct.task import Task

from direct.showbase import Audio3DManager

from onscreeninterface import OnScreenInterface
from environ import Environment
from eve import Eve

class RollingEve(ShowBase):

	MUSIC_ON = True
	SOUND_EFFECT_ON =True

	def __init__(self):

		ShowBase.__init__(self)

		self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)

		self.levelFinish = False
		self.gameOver = False
		self.alreadyPlayed= False
		self.current_level = 'L0'
		self.user = None
		self.tasks=[]

		base.disableMouse()					# Disable use of mouse for camera movement

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
		self.eve = Eve(self,self.render,self.world,self.accept,damage=12.5)

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
		self.taskMgr.remove('enemies')


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
			self.eve.render_eve((1500,1100,1.5))
			self.e.loadStage1()
			#self.eve.render_eve((1500,1100,1.5))
		elif self.current_level == 'L2':
			#self.eve.render_eve((1500,1100,1005))
			#self.eve.render_eve((1363,982,1335))
			self.eve.render_eve((1345,1690,1335))
			self.e.loadStage2()

		
		#	TASK FOR ALL GAME STAGES	#
		self.taskMgr.add(self.update,'update') 

		base.camera.setPos(self.eve.characterNP1.getX()+80,self.eve.characterNP1.getY(),50)        	
       		
		# Create a floater object.  We use the "floater" as a temporary
        	# variable in a variety of calculations.
        
        	self.floater = NodePath(PandaNode("floater"))
        	self.floater.reparentTo(render)

	#	WORLD UPDATE TASK	#
	def update(self,task):
		check = self.eve.currentControllerNode.isOnGround()				# Task that updates physics world every frame
        	dt = globalClock.getDt()
       		self.eve.updateEveAnim()
		self.updateCamera(self.eve.omega)

		# Update info on stats frame		
		self.interface.bar['text'] = str(int(self.eve.health)) + ' / 100'
		self.interface.bar['value'] = int(self.eve.health)
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
			self.eve.reset()
			self.eve.currentNP.setH(90)
			#self.clean_and_set(self.current_level)
		if self.levelFinish is True:
			results = DirectFrame(frameColor=(0, 0, 0, .1),frameSize=(-2, 2, 1, -1),pos=(0, 0, 0))
			textObject = OnscreenText(parent = results,text = 'STAGE 1 COMPLETE', pos = (0, 0), scale = .1, fg=(1,0,0,1))
			textObject = OnscreenText(parent = results,text = 'Wheels Collected : ' + str(self.eve.tiresCollected) + ' / ' + str(len(self.e.tokens)) , pos = (0, -.2), scale = .1, fg=(1,0,0,1))
			if self.complete.status() is not self.complete.PLAYING and self.alreadyPlayed is False:
				self.alreadyPLayed = True
				self.complete.play()
			

		return task.cont				# Continue task
	

	def updateCamera(self,omega):

		base.camera.lookAt(self.eve.currentNP)
        	if (omega < 0):
            		base.camera.setX(base.camera, -200 * globalClock.getDt())
        	if (omega > 0):
            		base.camera.setX(base.camera, +200 * globalClock.getDt())

		pos =self.eve.currentNP.getPos()
		z=self.eve.currentNP.getZ()	
        	
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


game = RollingEve()
game.run()
