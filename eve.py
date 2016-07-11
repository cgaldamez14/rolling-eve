'''
    Eve Module
    Author: Carlos Galdamez
    CS 594 3D Game Programming
'''

from character import Character

from panda3d.core import BitMask32
from panda3d.core import Vec3

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

from direct.showbase.InputStateGlobal import inputState
from direct.actor.Actor import Actor



class Eve(Character):
	
	#----- CLASS VARIABLES -----#	
	HEIGHT = 21.00
	WIDTH = 5.0
	INITIAL_HEADING = 45

	MAX_JUMP_HEIGHT = 200.0
	JUMP_SPEED = 11.0	
	RUNNING_SPEED = 60.0
	#INITIAL_ROLL_SPEED = 100.0
	INITIAL_ROLL_SPEED = 500.0
	ROLL_ANIM_RATE = 15
	OMEGA = 120.0
	
	#----- CONSTRUCTOR -----#
	def __init__(self,render,world,health=100,damage=0):
		super(Eve,self).__init__('Eve',health,damage)
		#----- INSTANCE VARIABLES -----#
		self.state = {'running': False, 'jumping' : False, 'rolling' : False}
		self.previousState = 'None'
		self.speed = Vec3(0, 0, 0)
        	self.omega = 0.0

		#----- PRIVATE INSTANCE VARIABLES -----#		
		self.__render = render
		self.__world = world		

		self.render_eve((10,-150,5))

		self.previousZ = self.characterNP.getZ()
		
		#----- SETUP CONTROL FOR EVE -----#
        	inputState.watchWithModifiers('forward', 'w')
        	inputState.watchWithModifiers('turnLeft', 'a')
        	inputState.watchWithModifiers('turnRight', 'd')
		inputState.watchWithModifiers('throttle', '1')
		inputState.watchWithModifiers('jump', 'space')

	def render_eve(self, location):
		
		(init_x,init_y,init_z) = location

		self.__capsule_shape = BulletCapsuleShape(Eve.WIDTH, Eve.HEIGHT - 2 * Eve.WIDTH, ZUp)
		
		# Create bullet character controller
		self.character = BulletCharacterControllerNode(self.__capsule_shape,0.4,self.name)		
		self.character.setMaxJumpHeight(Eve.MAX_JUMP_HEIGHT)
        	self.character.setJumpSpeed(Eve.JUMP_SPEED)

		self.characterNP = self.__render.attachNewNode(self.character)
		self.characterNP.setPos(init_x,init_y,init_z)
		self.characterNP.setH(Eve.INITIAL_HEADING)
		self.characterNP.setCollideMask(BitMask32.allOn())
		self.__world.attachCharacter(self.character)
		
		#----- ACTOR SETUP -----#
        	self.actorNP = Actor('models/eve/eve.egg', {
                         				    'run' : 'models/eve/eve-run.egg',
                         				    'walk' : 'models/eve/eve-walk.egg',
                         				    'jump' : 'models/eve/eve-jump.egg',
			 				    'roll' : 'models/eve/eve-tireroll.egg'})

		self.running = base.loader.loadSfx("sfx/grass_running.ogg")
		self.running.setPlayRate(2.5)
		self.running.setVolume(.6)		
		#self.running.setLoop(True)
		#self.running.play()

        	self.actorNP.reparentTo(self.characterNP)
        	self.actorNP.setScale(4.0)
        	self.actorNP.setH(180)
        	self.actorNP.setPos(0,0,-9)

		# Changing jump animation play rate
		self.actorNP.setPlayRate(.30,'jump')

	def processEveInput(self):
		self.state['jumping'] = False
		self.state['running'] = False
		self.speed = Vec3(0, 0, 0)
        	self.omega = 0.0

		# This first if statement causes problems need to fix this		
		#if self.characterNP.getZ() >= 10.50:
			#self.state['jumping'] = True
			#return self.omega

        	if inputState.isSet('forward'):
			if self.state['rolling'] == True:
				self.speed.setY( Eve.INITIAL_ROLL_SPEED)
			else:
				self.speed.setY( Eve.RUNNING_SPEED)
				self.actorNP.setP(15)
			self.state['running'] = True
        	if inputState.isSet('turnLeft'):  
			self.omega = Eve.OMEGA
			self.state['running'] = True
			self.actorNP.setR(15)
        	if inputState.isSet('turnRight'): 
			self.omega = Eve.OMEGA * -1 
			self.state['running'] = True
			self.actorNP.setR(-15)
        	if inputState.isSet('jump'):
			self.character.doJump()
			self.state['jumping'] = True
		if inputState.isSet('throttle'):
			if self.previousState == 'roll':
				self.state['rolling'] = False
			else:
				self.state['rolling'] = True
		# Set angular and linear movement for eve
        	self.character.setAngularMovement(self.omega)
        	self.character.setLinearMovement(self.speed, True)

	def updateEveAnim(self):
		self.processEveInput()
			
		if self.state['running'] is True:
			if self.state['rolling'] is True:
				self.actorNP.setPlayRate(15,'roll')
				if self.actorNP.getCurrentFrame('roll') == (self.actorNP.getNumFrames('roll') - 1):
					self.actorNP.loop('roll',fromFrame=0)
				else:
					self.actorNP.loop('roll',restart=0)
			else:	
				if self.omega == 0.0:
					self.actorNP.setR(0)
				if self.previousState is not 'running':
					self.running.setLoop(True)
					self.running.play()		
				if self.actorNP.getCurrentFrame('run') == (self.actorNP.getNumFrames('run') - 1):
					self.actorNP.loop('run',fromFrame=0)
				else:
					self.actorNP.loop('run',restart=0)
		elif self.state['jumping'] is True:
			if self.previousState is not 'jump':
				self.actorNP.play('jump')
		else:	
			self.actorNP.stop(self.actorNP.getCurrentAnim())
			self.running.setLoop(False)
			self.running.stop()
			self.actorNP.setP(0)
			self.actorNP.setR(0)				
			if self.state['rolling'] is True:
				self.actorNP.pose('roll',5) 			
			else:	
				self.actorNP.pose('walk',5) 
		
		self.previousState = self.actorNP.getCurrentAnim()	# Record previous state



	
