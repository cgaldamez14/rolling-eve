'''
    Eve Module
    Author: Carlos Galdamez
    CS 594 3D Game Programming
'''

from character import Character

from panda3d.core import BitMask32
from panda3d.core import Vec3

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp,XUp

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
	INITIAL_ROLL_SPEED = 800.0
	ROLL_ANIM_RATE = 15
	OMEGA = 120.0
	
	#----- CONSTRUCTOR -----#
	def __init__(self,render,world,accept,health=100,damage=0):
		super(Eve,self).__init__('Eve',health,damage)
		#----- INSTANCE VARIABLES -----#
		self.state = {'running': False, 'jumping' : False, 'rolling' : False}
		self.previousState = 'None'
		self.speed = Vec3(0, 0, 0)
        	self.omega = 0.0
		self.tiresCollected = 0

		#----- PRIVATE INSTANCE VARIABLES -----#		
		self.__render = render
		self.__world = world
		#self.accept('space', self.doJump)

		accept('1', self.toggle_modes)

		#----- ACTOR SETUP -----#
        	self.actorNP1 = Actor('models/eve/eve.egg', {
                         				    'run' : 'models/eve/eve-run.egg',
                         				    'walk' : 'models/eve/eve-walk.egg',
                         				    'jump' : 'models/eve/eve-jump.egg',
			 				    'roll' : 'models/eve/eve-tireroll.egg'})
        	self.actorNP2 = Actor('models/eve/eve-tireroll.egg', {'roll' : 'models/eve/eve-tireroll.egg'})
		self.current = self.actorNP1

		self.render_eve((10,-150,5))

		#self.previousZ = self.characterNP.getZ()
		
		#----- SETUP CONTROL FOR EVE -----#
        	inputState.watchWithModifiers('forward', 'w')
        	inputState.watchWithModifiers('turnLeft', 'a')
        	inputState.watchWithModifiers('turnRight', 'd')
		inputState.watchWithModifiers('jump', 'space')

	def searchMode(self,location,heading):
		(init_x,init_y,init_z) = location

		self.__capsule_shape = BulletCapsuleShape(Eve.WIDTH, Eve.HEIGHT - 2 * Eve.WIDTH, ZUp)
		
		# Create bullet character controller
		self.character1= BulletCharacterControllerNode(self.__capsule_shape,0.4,self.name)		
		#self.character1.setMaxJumpHeight(Eve.MAX_JUMP_HEIGHT)
        	self.character1.setJumpSpeed(Eve.JUMP_SPEED)

		self.characterNP1 = self.__render.attachNewNode(self.character1)
		self.characterNP1.setPos(init_x,init_y,init_z)
		self.characterNP1.setH(Eve.INITIAL_HEADING)
		self.characterNP1.setCollideMask(BitMask32.allOn())
		self.__world.attachCharacter(self.character1)

        	self.actorNP1.reparentTo(self.characterNP1)
        	self.actorNP1.setScale(4.0)
        	self.actorNP1.setH(180)
        	self.actorNP1.setPos(0,0,-9)

	def attackMode(self,location,heading):
		(init_x,init_y,init_z) = location

		self.__cylinder_shape = BulletCylinderShape(Eve.WIDTH + 2, Eve.HEIGHT - 4, XUp)
		
		# Create bullet character controller
		self.character2= BulletCharacterControllerNode(self.__cylinder_shape,0.4,self.name)		
		#self.character1.setMaxJumpHeight(Eve.MAX_JUMP_HEIGHT)
        	#self.character1.setJumpSpeed(Eve.JUMP_SPEED)

		self.characterNP2 = self.__render.attachNewNode(self.character2)
		self.characterNP2.setPos(init_x,init_y,init_z-3)
		self.characterNP2.setH(Eve.INITIAL_HEADING)
		self.characterNP2.setCollideMask(BitMask32.allOn())
		self.__world.attachCharacter(self.character2)

        	self.actorNP2.reparentTo(self.characterNP2)
        	self.actorNP2.setScale(4.0)
        	self.actorNP2.setH(180)
        	self.actorNP2.setPos(0,0,0)

	def is_attack_mode(self):
		return self.state['rolling']

	
	def toggle_modes(self):
		if self.is_attack_mode() is False:
			loc = (self.characterNP1.getX(),self.characterNP1.getY(),self.characterNP1.getZ())
			heading = self.characterNP1.getH()
			self.__world.removeCharacter(self.character1)
			self.character1.removeChild(0)
			self.attackMode(loc,heading)
			self.state['rolling'] = True
			self.current = self.actorNP2
		else:
			loc = (self.characterNP2.getX(),self.characterNP2.getY(),self.characterNP2.getZ())
			heading = self.characterNP2.getH()
			self.__world.removeCharacter(self.character2)
			self.character2.removeChild(0)
			self.searchMode(loc,heading)
			self.state['rolling'] = False	
			self.current = self.actorNP1		

	def render_eve(self, location):
		self.searchMode(location,0)
		#self.running = base.loader.loadSfx("sfx/grass_running.ogg")
		#self.running.setPlayRate(2.5)
		#self.running.setVolume(.6)		
		#self.running.setLoop(True)
		#self.running.play()

		# Changing jump animation play rate
		self.current.setPlayRate(.30,'jump')

	def doJump(self):
		return
		

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
				self.current.setP(15)
			self.state['running'] = True
        	if inputState.isSet('turnLeft'):  
			self.omega = Eve.OMEGA
			self.state['running'] = True
			self.current.setR(15)
        	if inputState.isSet('turnRight'): 
			self.omega = Eve.OMEGA * -1 
			self.state['running'] = True
			self.current.setR(-15)
		if inputState.isSet('throttle'):
			if self.previousState == 'roll':
        			self.current.setPos(0,0,-9)
				self.state['rolling'] = False
			else:
        			self.current.setPos(0,0,0)
				self.state['rolling'] = True

		if self.state['rolling'] is False:
			n = self.character1
		else:
			n = self.character2
		# Set angular and linear movement for eve

		if n.isOnGround() is True:
			self.state['jumping'] = False

        	n.setAngularMovement(self.omega)
        	n.setLinearMovement(self.speed, True)

        	if inputState.isSet('jump'):
			n.doJump()
			self.current.play('jump')
			self.state['jumping'] = True

	def updateEveAnim(self):
		self.processEveInput()
		if self.state['rolling'] is False:
			n = self.character1
		else:
			n = self.character2
		if n.isOnGround() is True:	
			if self.state['running'] is True:
				if self.state['rolling'] is True:
					if self.omega == 0.0:
						self.current.setR(0)
					self.current.setPlayRate(15,'roll')
					if self.current.getCurrentFrame('roll') == (self.current.getNumFrames('roll') - 1):
						self.current.loop('roll',fromFrame=0)
					else:
						self.current.loop('roll',restart=0)
				else:	
					if self.omega == 0.0:
						self.current.setR(0)
					#if self.previousState is not 'running':
						#self.running.setLoop(True)
						#self.running.play()		
					if self.current.getCurrentFrame('run') == (self.current.getNumFrames('run') - 1):
						self.current.loop('run',fromFrame=0)
					else:
						self.current.loop('run',restart=0)
			elif self.state['jumping'] is True:
				if self.previousState is not 'jump':
					self.current.play('jump')
			else:	
				self.current.stop(self.current.getCurrentAnim())
				#self.running.setLoop(False)
				#self.running.stop()
				self.current.setP(0)
				self.current.setR(0)				
				if self.state['rolling'] is True:
					self.current.pose('roll',5) 			
				else:	
					self.current.pose('walk',5) 
			
			self.previousState = self.current.getCurrentAnim()	# Record previous state




	
