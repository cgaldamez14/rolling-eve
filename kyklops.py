'''
    KYKLOPS MODULE
    This module inherits from the character class. It contains all tools necessary for the main enemy of this game.
    It has functionality for attacking, decreasing its own health when attacked and playing death and attacking 
    animations when needed. It also contains all sound effects pertaining to this character.
    Author: Carlos Galdamez
'''

from character import Character

from panda3d.core import Point3
from panda3d.core import Vec3

from direct.actor.Actor import Actor

from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import ZUp

from direct.interval.IntervalGlobal import Sequence

from direct.interval.LerpInterval import LerpPosInterval


class Kyklops(Character):

	RADIUS = 12		# Will be used for cylindrical bullet capsule
	HEIGHT = 30		# Will be used for cylindrical bullet capsule

	FOLLOW_SPEED = .3
	ATTACK_SPEED = .2

	'''
	    Constructor calls the super class constructor to initialize damage, health and enemy name. Additionally it
	    instantiates the main model for the enemy and sets dictionary for the animations.	
	'''
	def __init__(self,game,name,health=100,damage=0):
		super(Kyklops,self).__init__(name,health,damage)
		
		# Private instance variable
		self.__game = game
		
		self.__attack = Sequence()	# Initialize an empty sequence

		#----- ACTOR SETUP -----#
		self.actorNP = Actor('models/kyklops/monster1.egg', {'idle':'models/kyklops/monster1.egg'})

		# Grunting sound effect when kyklops is hit by enemy
		self.grunt = base.loader.loadSfx("sfx/pain_monster.wav")
		self.grunt.setLoop(False)
		self.grunt.setVolume(1)

		# Splat sound effect when kyklops is killed by enemy
		self.splat = base.loader.loadSfx("sfx/monster_splat.wav")
		self.splat.setLoop(False)
		self.splat.setVolume(1)

	'''
	    This method is used to attach the kyklops model to a bullet world node. This is necessary in order
	    to conclude when there is a collision between the PC and NPC.
	'''	
	def render_kyklops(self,pos,hpr):

		self.initial_pos = pos		# Initial pos where kyklops will be guarding
		self.initial_hpr = hpr

		shape = BulletCylinderShape(Kyklops.RADIUS,Kyklops.HEIGHT,ZUp)
		self.node = BulletRigidBodyNode('Enemy')
		self.node.addShape(shape)
 
		self.np = self.__game.render.attachNewNode(self.node)
		self.np.setPos(self.initial_pos)
 
		self.__game.world.attachRigidBody(self.node)

		self.actorNP.reparentTo(self.np)
        	self.actorNP.setScale(4.0)
        	self.actorNP.setHpr(self.initial_hpr)
        	self.actorNP.setPos(0,0,5)
		self.actorNP.loop('idle')

		# Set 3d audio for the kyklops so that the PC can hear it only when it is close by
		self.snarl = self.__game.audio3d.loadSfx('sfx/monster_idle.wav')
		self.__game.audio3d.attachSoundToObject(self.snarl,self.actorNP)
		self.__game.audio3d.setSoundVelocity(self.snarl,Vec3(2,2,2))
		self.__game.audio3d.setListenerVelocity(Vec3(2,2,2))
		self.__game.audio3d.setDistanceFactor(2)
		self.__game.audio3d.setDropOffFactor(1)
		self.snarl.setLoop(True)
		self.snarl.setVolume(2)
		self.snarl.play()

	'''
	    This method monitors the health of this instance of kyklops. If health goes below 0 then
	    the bullet node is detached from the world and the old model is replaced by the model
	    with the explode animation. 
	'''
	def monitor_health(self):
		if self.health < 0:
			# Pos and hpr are needed to set the new model in the same location and 
			# and facing the same direction as the old one was before it was detached from the bullet world
			pos = self.np.getPos()
			hpr = self.np.getHpr()

			# Remove bullet node
			self.__game.e.enemies.remove(self)
			self.__game.world.removeRigidBody(self.node)
			self.np.remove_node()

			# Stop default snarl sound
			self.snarl.stop()

			# Set new actor with explode animation and play explode as well as the sound effect
			self.actorNP = Actor('models/kyklops/monster1-explode.egg', {'explode':'models/kyklops/monster1-explode.egg'})
			self.actorNP.reparentTo(self.__game.render)
        		self.actorNP.setScale(4.0)
        		self.actorNP.setHpr(hpr)
        		self.actorNP.setPos(pos)
			self.splat.play()
			self.actorNP.play('explode')

			# This task will run until the explode animation is done playing. At that point
			# the task will remove all remaining tasks and models of the instance of kyklops
			self.__game.taskMgr.add(self.remove_kyklops,self.name)
	
	'''
	    This task is only played at the end of the kyklops life. It checks if the explode animation has stopped playing
	    at which point it removes the model and ends the task.
	'''
	def remove_kyklops(self,task):
		if self.actorNP.getCurrentAnim() != 'explode':
			self.actorNP.remove_node()		# Remove model
			return task.done
		return task.cont
	

	'''
	    The follow method is used to check if the PC is within range. If it is this method causes the kyklops
	    to adjust its position in order to get closer to the PC and attack
	'''
	def follow(self):
		self.guard()	# Checks if the kyklop has reached its maximum following limit
		
		actorPosVec = self.__game.eve.currentNP.getPos() - self.np.getPos()
		
		# Check if distance from NPC and PC is between 20 and 100
		if actorPosVec.length() < 100 and actorPosVec.length() > 20:
			# Increase snarl sound play rate
			self.snarl.setPlayRate(2)
			# Make NPC look at PC
			self.actorNP.lookAt(self.__game.eve.currentNP)
			# Increase animation play rate
			self.actorNP.setPlayRate(3,'idle')
	
			# Check if distance from NPC and PC is between 20 and 25
			if self.__attack.isPlaying() is False and actorPosVec.length() < 25 and actorPosVec.length() > 20:
				# Increase animation play rate
				self.actorNP.setPlayRate(5,'idle')
				# Play attack sequence				
				self.attack()

			# The following are if conditions to alter NPC position when it is following the PC
            		if actorPosVec[0] < 0 and actorPosVec[1] < 0 :
                		self.np.setPos(self.np.getX() - Kyklops.FOLLOW_SPEED, self.np.getY() - Kyklops.FOLLOW_SPEED,self.np.getZ())
           		elif actorPosVec[0] < 0 and actorPosVec[1] > 0 :
                		self.np.setPos(self.np.getX() - Kyklops.FOLLOW_SPEED, self.np.getY() + Kyklops.FOLLOW_SPEED,self.np.getZ())
           		elif actorPosVec[0] > 0 and actorPosVec[1] < 0 :
                		self.np.setPos(self.np.getX() + Kyklops.FOLLOW_SPEED, self.np.getY() - Kyklops.FOLLOW_SPEED,self.np.getZ())
          		else:
               			self.np.setPos(self.np.getX() + Kyklops.FOLLOW_SPEED, self.np.getY() + Kyklops.FOLLOW_SPEED,self.np.getZ())
		
		# Checks if PC outran the NPC if it did then NPC goes back to its guard position
		if actorPosVec.length() > 100:
			# Decrease animation play rate
			self.actorNP.setPlayRate(.3,'idle')
			# Decrease snarl sound play rate
			self.snarl.setPlayRate(1)
			self.np.setPos(self.initial_pos)
	
	'''
	    This method checks if the guard followed the PC too far from its guard position. If
	    it did then it changes the NPC position to its original guard position. 	
	'''
	def guard(self):
		actorPosVec = self.initial_pos - self.np.getPos()
		if actorPosVec.length() > 200:
			# Decrease animation play rate
			self.actorNP.setPlayRate(.3,'idle')
			# Decrease snarl sound play rate
			self.snarl.setPlayRate(1)
			self.np.setPos(self.initial_pos)

	'''
	    This method plays a sequence that causes the NPC for lounge to the players position, pushing the PC 
	    a little bit and causing damage to the PC.
	'''	
	def attack(self):
		originalPos= self.np.getPos()
		originalEvePos = self.__game.eve.currentNP.getPos()
		i1 = LerpPosInterval(self.np,Kyklops.ATTACK_SPEED,originalEvePos,startPos = originalPos)
		i2 = LerpPosInterval(self.np,Kyklops.ATTACK_SPEED,originalPos,startPos = originalEvePos)
		self.__attack = Sequence(i1,i2)
		self.__attack.start()

	'''
	    This method checks whether there was a collision between the PC and NPC. If there is then
	    the PC takes damage.	
	'''
	def detect_contact(self):
		result = self.__game.world.contactTestPair(self.np.node(),self.__game.eve.currentControllerNode)
		
		# If results is greater than 0 then that means there was a collision		
		if len(result.getContacts()) > 0:
			self.__game.eve.take_damage(self.damage)

	'''
	    This method is called when ever the PC successfully attacks the NPC. 
	    Grunt sound effect is played and damage is taken.
	'''
	def take_damage(self,damage):
		self.grunt.play()
		self.health -= damage		


		
		

