'''
    Eve Module
    Author: Carlos Galdamez
    CS 594 3D Game Programming
'''

from character import Character

from panda3d.core import BitMask32
from panda3d.core import Vec3,Point3

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp,XUp

from direct.showbase.InputStateGlobal import inputState
from direct.interval.IntervalGlobal import Sequence,Func,Wait,ProjectileInterval
from direct.actor.Actor import Actor

from math import sin,cos,pow, sqrt,pi



class Eve(Character):
	
	#----- CLASS VARIABLES -----#	
	HEIGHT = 21.00
	WIDTH = 5.0
	INITIAL_HEADING = 90

	MAX_JUMP_HEIGHT = 200.0
	JUMP_SPEED = 70	
	RUNNING_SPEED = 40.0
	INITIAL_ROLL_SPEED = 700.0
	ROLL_ANIM_RATE = 15
	OMEGA = 60.0
	
	#----- CONSTRUCTOR -----#
	def __init__(self,game,render,world,accept,health=100,damage=0):
		super(Eve,self).__init__('Eve',health,damage)
		#----- INSTANCE VARIABLES -----#
		self.state = {'normal': True, 'jumping' : False, 'rolling' : False}
		self.speed = Vec3(0, 0, 0)
        	self.omega = 0.0
		self.tiresCollected = 0
		self.accept = accept
		self.ready = True

		#----- PRIVATE INSTANCE VARIABLES -----#		
		self.__render = render
		self.__world = world
		self.__game = game


		#self.accept('1', self.toggle_modes)
		#self.accept('space', self.doJump)

		#----- ACTOR SETUP -----#
        	self.actorNP1 = Actor('models/eve/eve.egg', {
                         				    'run' : 'models/eve/eve-run.egg',
                         				    'walk' : 'models/eve/eve-walk.egg',
                         				    'jump' : 'models/eve/eve-jump.egg',
			 				    'roll' : 'models/eve/eve-tireroll.egg'})
        	self.actorNP2 = Actor('models/eve/eve-tireroll.egg', {'roll' : 'models/eve/eve-tireroll.egg'})
		

		#----- PREPARE SFX -----#
		self.jump = base.loader.loadSfx("sfx/jump.wav")
		self.jump.setVolume(.08)
		self.running = base.loader.loadSfx("sfx/walking.wav")
		self.running.setLoop(True)
		self.running.setPlayRate(1.55)
		self.running.setVolume(.08)
		self.land = base.loader.loadSfx("sfx/land.flac")
		self.land.setLoop(False)
		self.land.setVolume(.015)
		self.roll = base.loader.loadSfx("sfx/rolling.wav")
		self.roll.setLoop(True)
		self.roll.setVolume(.09)
		
		#----- SETUP CONTROL FOR EVE -----#
        	inputState.watchWithModifiers('forward', 'w')
        	inputState.watchWithModifiers('turnLeft', 'a')
        	inputState.watchWithModifiers('turnRight', 'd')	
		
		self.__game.taskMgr.add(self.process_contacts,'attacks')

	def render_eve(self,pos):
		self.searchMode(pos,Eve.INITIAL_HEADING)

		# Changing jump animation play rate
		self.currentNode.setPlayRate(1,'jump')

	def disable_character_controls(self):
		self.accept('1', self.do_nothing)
		self.accept('space', self.do_nothing)
		self.accept('enter',self.do_nothing)

	def enable_character_controls(self):
		self.accept('1', self.toggle_modes)
		self.accept('space', self.doJump)
		self.accept('enter',self.attack)

	def do_nothing(self):
		pass
	
	#------ METHODS USED TO MODIFY JUMP ANIMATION ------#
	def firstPart(self): self.currentNode.play('jump', fromFrame=0)

	def stopInJump(self): self.currentNode.stop()

	def finishJump(self): self.currentNode.play('jump', fromFrame=self.currentNode.getCurrentFrame('jump'))
	
	def doJump(self):
		if self.currentControllerNode.isOnGround() is True:
			if self.currentState() is 'normal':
				if self.speed.getY() > 0: self.running.stop()
				self.state['jumping'] = True
				self.jump.play()
				self.currentControllerNode.doJump()

				#sequence = Sequence(Func(self.firstPart),Wait(.3),Func(self.stopInJump),Wait(2.95),Func(self.finishJump))
				sequence = Sequence(Func(self.firstPart),Wait(.3),Func(self.stopInJump),Wait(2.95))
				sequence.start()			

	def searchMode(self,location,heading):
		self.state['normal'] = True
		self.state['rolling'] = False
		(init_x,init_y,init_z) = location

		self.__capsule_shape = BulletCapsuleShape(Eve.WIDTH, Eve.HEIGHT - 2 * Eve.WIDTH, ZUp)
		
		# Create bullet character controller
		self.character1= BulletCharacterControllerNode(self.__capsule_shape,0.4,self.name)		
		#self.character1.setMaxJumpHeight(Eve.MAX_JUMP_HEIGHT)
        	self.character1.setJumpSpeed(Eve.JUMP_SPEED)
		self.character1.setGravity(70)

		self.characterNP1 = self.__render.attachNewNode(self.character1)
		self.characterNP1.setPos(init_x,init_y,init_z)
		self.characterNP1.setH(heading)
		self.characterNP1.setCollideMask(BitMask32.allOn())
		self.__world.attachCharacter(self.character1)

        	self.actorNP1.reparentTo(self.characterNP1)
        	self.actorNP1.setScale(4.0)
        	self.actorNP1.setH(180)
        	self.actorNP1.setPos(0,0,-9)

		self.currentNode = self.actorNP1
		self.currentNP = self.characterNP1
		self.currentControllerNode = self.character1

		# Create a cylindrical collision shape
		collisionShape = BulletCylinderShape(6.5,3,XUp)

		# Create a ghost node and attach to render
		self.ghostNode = BulletGhostNode('Weapon')
		self.ghostNode.addShape(collisionShape)
		self.weaponNP = self.__game.render.attachNewNode(self.ghostNode)
			
		self.weaponNP.setCollideMask(BitMask32.allOff())
		self.weaponNP.setPos(init_x, init_y, init_z)
		self.__game.world.attachGhost(self.ghostNode)

		self.weapon = self.__game.loader.loadModel('models/environ/tire/tire.egg')
		self.weapon.setScale(4,4,4)
                self.weapon.setPos(-.5,0,0)

                self.weapon.reparentTo(self.weaponNP)

		self.weapon.hide()

		self.__game.taskMgr.add(self.update_weapon_pos,"weapon")

		

	def update_weapon_pos(self,task):
		#r = sqrt(pow(1,2) + pow(1,2))
		#print r
		#xpos = cos(int(self.characterNP1.getH()))
		#ypos = sin(int(self.characterNP1.getH()))

		self.weaponNP.setPos(self.characterNP1.getX(),self.characterNP1.getY(), self.characterNP1.getZ() + 5)
		self.weaponNP.setH(self.characterNP1.getH())

		#print str(self.characterNP1.getH())

		#print xpos , ypos
		return task.cont

	def attack(self):
		if self.ready is True:
			self.weapon.show()

			xpos = 100 * cos((90 - self.characterNP1.getH()) * (pi / 180.0))
			ypos = -100 * sin((90 - self.characterNP1.getH()) * (pi / 180.0))
			#print xpos , ypos
		
			trajectory = ProjectileInterval(self.weaponNP,
                                    	 startPos = self.weaponNP.getPos(),
                                    	 endPos = Point3(self.weaponNP.getX() - xpos,self.weaponNP.getY() - ypos, self.weaponNP.getZ()-10), duration = .5, gravityMult = 15)
		
			Sequence(Func(self.set_weapon_busy),trajectory,Func(self.weapon.hide),Func(self.set_weapon_ready)).start()		
			#attackS.start()		
			#trajectory.start()
			#self.weapon.hide()

	def set_weapon_ready(self):
		self.ready = True
	def set_weapon_busy(self):
		self.ready = False

	def process_contacts(self,task):
		for enemy in self.__game.enemies:
			self.check_impact(enemy)
		return task.cont

	def check_impact(self,enemy):
		result = self.__game.world.contactTestPair(self.ghostNode,enemy.np.node())
		if len(result.getContacts()) > 0:
			if self.weapon.isHidden() is False:
				self.weapon.hide()
			if self.ready is False:			
				enemy.health -= 12.5
			print enemy.health

		
		

	def attackMode(self,location,heading):
		self.state['normal'] = False
		self.state['rolling'] = True
		(init_x,init_y,init_z) = location

		self.__cylinder_shape = BulletCylinderShape(Eve.WIDTH + 2, Eve.HEIGHT - 4, XUp)
		
		# Create bullet character controller
		self.character2= BulletCharacterControllerNode(self.__cylinder_shape,0.4,self.name)		

		self.characterNP2 = self.__render.attachNewNode(self.character2)
		self.characterNP2.setPos(init_x,init_y,init_z-2)
		self.characterNP2.setH(heading)
		self.characterNP2.setCollideMask(BitMask32.allOn())
		self.__world.attachCharacter(self.character2)
		self.character2.setGravity(70)

        	self.actorNP2.reparentTo(self.characterNP2)
        	self.actorNP2.setScale(4.0)
        	self.actorNP2.setH(180)
        	self.actorNP2.setPos(0,0,0)

		self.currentNode = self.actorNP2
		self.currentNP = self.characterNP2
		self.currentControllerNode = self.character2

		# Set play rate of the rolling animation		
		self.currentNode.setPlayRate(15,'roll')

	def is_attack_mode(self):
		return self.state['rolling']

	
	def toggle_modes(self):
		if self.is_attack_mode() is False:
			loc = (self.characterNP1.getX(),self.characterNP1.getY(),self.characterNP1.getZ())
			heading = self.characterNP1.getH()
			self.__world.removeCharacter(self.character1)
			self.character1.removeChild(0)
			self.attackMode(loc,heading)
		else:
			loc = (self.characterNP2.getX(),self.characterNP2.getY(),self.characterNP2.getZ())
			heading = self.characterNP2.getH()
			self.__world.removeCharacter(self.character2)
			self.character2.removeChild(0)
			self.searchMode(loc,heading)
		

	def processEveInput(self):
		if self.currentControllerNode.isOnGround() is True:	
			self.speed = Vec3(0, 0, 0)
        		self.omega = 0.0
		
        		if inputState.isSet('forward'):
				if self.state['rolling'] == True:
					self.speed.setY( Eve.INITIAL_ROLL_SPEED)
				else:
					self.speed.setY( Eve.RUNNING_SPEED)
					self.currentNode.setP(15)
        		if inputState.isSet('turnLeft'):
				self.omega = Eve.OMEGA
				self.currentNode.setR(15)
        		if inputState.isSet('turnRight'): 
				self.omega = Eve.OMEGA * -1 
				self.currentNode.setR(-15)

        	self.currentControllerNode.setAngularMovement(self.omega)
        	self.currentControllerNode.setLinearMovement(self.speed, True)

	def currentState(self):
		if self.state['rolling'] is True:
			return 'rolling'
		else:
			return 'normal'

	def updateEveAnim(self):
		#print self.characterNP1.getH()
		self.processEveInput()
		if self.currentControllerNode.isOnGround() is True:	
			if self.speed.getY() > 0:
				if self.omega == 0.0:	self.currentNode.setR(0)
				if self.currentState() is 'rolling':
					if self.running.status() == self.running.PLAYING: self.running.stop()
					if self.roll.status() != self.roll.PLAYING: self.roll.play()
					if self.currentNode.getCurrentAnim() != 'roll': self.currentNode.loop('roll')	
				elif self.currentState() is 'normal':	
					if self.roll.status() == self.roll.PLAYING: self.roll.stop()
					if self.running.status() != self.running.PLAYING: self.running.play()
					if self.currentNode.getCurrentAnim() != 'run': self.currentNode.loop('run')	
			else:	
				self.currentNode.stop(self.currentNode.getCurrentAnim())
				self.currentNode.setP(0)
				self.currentNode.setR(0)
				if self.running.status() == self.running.PLAYING: self.running.stop()
				if self.roll.status() == self.roll.PLAYING: self.roll.stop()
				if self.state['rolling'] is True:
					frame = self.currentNode.getCurrentFrame('roll')
					if frame is None: frame = 0
					else: frame = self.currentNode.getCurrentFrame('roll')
					self.currentNode.pose('roll',frame) 			
				elif self.state['normal'] is True:
					self.currentNode.pose('walk',5) 
		#else:
			#if self.state['jumping'] is False:
			#	self.currentNode.pose('jump',20) 
			#if self.state['normal'] is True and self.currentNode.getCurrentFrame('jump') == (self.currentNode.getNumFrames('jump') - 1):
				#if self.land.status() != self.land.PLAYING:
					#self.land.play()
					#self.state['jumping'] = False

	




	
