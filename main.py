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


from direct.showbase.InputStateGlobal import inputState

from math import cos,sin,pi

class RollingEve(ShowBase):

	MUSIC_ON = True
	SOUND_EFFECT_ON =True

	def __init__(self):

		ShowBase.__init__(self)
		base.disableMouse()			

		self.camera_views = {'normal' : True, 'top' : False, 'right' : False, 'left' : False, 'first_person' : False}
		self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)

		self.levelFinish = False
		self.game_over = False
		self.alreadyPlayed= False
		self.current_level = 'L0'
		self.user = None
		self.tasks=[]

		self.accept('q',self.toggle_music)
		self.accept('x', self.toggle_sfx)


		self.complete = base.loader.loadSfx("sfx/complete.wav")
		self.complete.setLoop(False)
		self.complete.setVolume(.07)

		self.night = base.loader.loadSfx("sfx/night_time.wav")
		self.night.setLoop(True)
		self.night.setVolume(1)

		self.meadow = base.loader.loadSfx("sfx/meadow_land.wav")
		self.meadow.setLoop(True)
		self.meadow.setVolume(.2)

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

	def toggle_camera(self):
		if self.camera_views['normal'] is True:
			self.camera_views['normal'] = False
			self.camera_views['top'] = True
		elif self.camera_views['top'] is True:
			self.camera_views['top'] = False
			self.camera_views['right'] = True
		elif self.camera_views['right'] is True:
			self.camera_views['right'] = False
			self.camera_views['left'] = True
		elif self.camera_views['left'] is True:
			self.camera_views['left'] = False
			self.camera_views['first_person'] = True
		elif self.camera_views['first_person'] is True:
			self.camera_views['first_person'] = False
			self.camera_views['normal'] = True

	def set_interface(self,start=True):
		#	ONSCREEN INTERFACE	#
		self.interface = OnScreenInterface(self)
		if start is True:
			self.interface.load_initial_interface()


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
		self.camera_views = {'normal' : True, 'top' : False, 'right' : False, 'left' : False, 'first_person' : False}
		self.levelFinish = False
		self.game_over = False
		self.alreadyPlayed= False
		self.user.score = 0

		if self.eve.running.status() == self.eve.running.PLAYING: self.eve.running.stop()
		if self.meadow.status() == self.meadow.PLAYING:
			self.meadow.stop()

		if self.night.status() == self.night.PLAYING:
			self.night.stop()

		print '\n\tCLEANING WORLD...\n'
		#self.interface.stage_select_frame.hide()
		self.interface.main_frame.destroy()
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
		self.taskMgr.remove('moving')
		self.taskMgr.remove('tokens')
		self.taskMgr.remove('cam_update')

		for node in self.render.getChildren():
			if node != camera:
				node.remove_node()
		self.set_world()
		self.set_debug_mode()
		self.create_player()
		self.set_interface(start = False)
		self.interface.set_timer(level)
		#print self.interface.level_time
		self.interface.load_essentials()
		self.accept('h', self.do_nothing)
		self.accept('f1', self.do_nothing)
		self.setup(level)
		self.taskMgr.add(self.interface.show_title,'Title')
		self.taskMgr.add(self.interface.update_timer,'Timer')

		
	def do_nothing(self):
		pass

	def setup(self,level):
		self.actual_start = globalClock.getRealTime()
		self.current_level = level
		#self.interface.set_timer()
		self.interface.create_stage_title(self.current_level)


		self.e = Environment(self)
		if self.current_level == 'L1':
			self.eve.render_eve((1500,1100,1.5))
			#self.eve.render_eve((0,-5250,-15))
			self.e.loadStage1()
			#self.eve.render_eve((1500,1100,1.5))
		elif self.current_level == 'L2':
			self.eve.render_eve((1500,1100,1005))
			#self.eve.render_eve((1363,982,1335))
			#self.eve.render_eve((1345,1690,1335))
			#self.eve.render_eve((179,1594,1435))
			self.e.loadStage2()
		
		self.accept('c', self.toggle_camera)

        	inputState.watchWithModifiers('camera_up', 'arrow_up')
        	inputState.watchWithModifiers('camera_down', 'arrow_down')																
		
		#	TASK FOR ALL GAME STAGES	#
		self.taskMgr.add(self.update_world,'update')
		self.taskMgr.add(self.update_camera,'cam-update')  
      	
	def update_camera(self,task):
		if self.camera_views['normal'] is True:
			self.normal_view()
		elif self.camera_views['top'] is True:
			self.top_view()
		elif self.camera_views['right'] is True:
			self.right_view()
		elif self.camera_views['left'] is True:
			self.left_view()
		elif self.camera_views['first_person'] is True:
			self.first_person()
			if inputState.isSet('camera_up'):
				if base.camera.getP() < 45:
					base.camera.setP(base.camera.getP() + 1)
			if inputState.isSet('camera_down'):
				if base.camera.getP() > -90:
					base.camera.setP(base.camera.getP() - 1)
		return task.cont
		

	#	WORLD UPDATE TASK	#
	def update_world(self,task):
		check = self.eve.currentControllerNode.isOnGround()				# Task that updates physics world every frame
        	dt = globalClock.getDt()
       		self.eve.updateEveAnim()
		

		# Update info on stats frame		
		self.interface.bar['text'] = str(int(self.eve.health)) + ' / 100'
		self.interface.bar['value'] = int(self.eve.health)
		self.world.doPhysics(dt, 10, 1/180.0)		# Update physics world
		if check == False and self.eve.currentControllerNode.isOnGround() is True:
			self.eve.finishJump()
			self.eve.state['jumping'] = False
		
		if self.current_level == 'L1':
			death = -26
		elif self.current_level == 'L2':
			death = 900


		if self.eve.currentNP.getZ() < death:
			self.eve.health -= 10	# Damage taken for falling off the map
			if self.eve.health > 0:
				self.eve.reset()
				self.eve.currentNP.setH(90)
			else:
				self.interface.hide_game_interface()
				self.interface.game_over()
				self.user.add_to_leaderboard(self.current_level)
				return task.done
		if self.levelFinish is True:
			if self.complete.status() is not self.complete.PLAYING and self.alreadyPlayed is False:
				self.interface.hide_game_interface()
				self.alreadyPlayed = True
				self.complete.play()
			self.interface.level_passed()
			self.user.add_to_leaderboard(self.current_level)
			return task.done

		if self.eve.health <= 0 or self.game_over is True:		
			self.interface.hide_game_interface()
			self.interface.game_over()
			self.user.add_to_leaderboard(self.current_level)
			return task.done
			
		return task.cont
	


	def top_view(self):
		base.camera.setPos(self.eve.currentNP.getX(),self.eve.currentNP.getY(),self.eve.currentNP.getZ()+400)
		base.camera.setHpr(self.eve.currentNP.getH(),-90,0)

	def right_view(self):
		xpos = 200 * cos((180 - self.eve.currentNP.getH()) * (pi / 180.0))
		ypos = -200 * sin((180 - self.eve.currentNP.getH()) * (pi / 180.0))
		base.camera.setPos(self.eve.currentNP.getX() - xpos,self.eve.currentNP.getY() - ypos, self.eve.currentNP.getZ() + 20)
		base.camera.lookAt(self.eve.currentNP)

	def normal_view(self):
		xpos = 200 * cos((270 - self.eve.currentNP.getH()) * (pi / 180.0))
		ypos = -200 * sin((270 - self.eve.currentNP.getH()) * (pi / 180.0))
		base.camera.setPos(self.eve.currentNP.getX() - xpos,self.eve.currentNP.getY() - ypos, self.eve.currentNP.getZ() + 60)
		base.camera.setHpr(self.eve.currentNP.getH(),-15,0)

	def left_view(self):
		xpos = -200 * cos((180 - self.eve.currentNP.getH()) * (pi / 180.0))
		ypos = 200 * sin((180 - self.eve.currentNP.getH()) * (pi / 180.0))
		base.camera.setPos(self.eve.currentNP.getX() - xpos,self.eve.currentNP.getY() - ypos, self.eve.currentNP.getZ() + 20)
		base.camera.lookAt(self.eve.currentNP)

	def first_person(self):
		xpos = 5 * cos((90 - self.eve.currentNP.getH()) * (pi / 180.0))
		ypos = -5 * sin((90 - self.eve.currentNP.getH()) * (pi / 180.0))
		base.camera.setPos(self.eve.currentNP.getX() - xpos,self.eve.currentNP.getY() - ypos, self.eve.currentNP.getZ() + 15)
		base.camera.setH(self.eve.currentNP.getH())


	
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
