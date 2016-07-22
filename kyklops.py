from character import Character

from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import ZUp

from direct.interval.IntervalGlobal import Sequence,Func,Wait
from direct.actor.Actor import Actor

from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.LerpInterval import LerpHprInterval

from panda3d.core import Point3
class Kyklops(Character):

	RADIUS = 12
	HEIGHT = 30

	def __init__(self,game,health=100,damage=0):
		super(Kyklops,self).__init__('Kyklops',health,damage)
		self.return_scout = Sequence()
		self.returning = False

		self.__game = game

		#----- ACTOR SETUP -----#
		self.actorNP1 = Actor('models/kyklops/monster1.egg', {'idle':'models/kyklops/monster1.egg'})
		#self.actorNP2 = Actor('models/kyklops/monster1-pincer-attack-left.egg.', {'attack':'models/kyklops/monster1-pincer-attack-right.egg.'})

	def render_kyklops(self,pos):

		
		(self.init_x,self.init_y,self.init_z) = pos

		#self.__capsule_shape = BulletCapsuleShape(Kyklops.RADIUS, Kyklops.HEIGHT - 2 * Kyklops.RADIUS, ZUp)
		
		# Create bullet character controller
		#self.character1= BulletCharacterControllerNode(self.__capsule_shape,0.4,self.name)	

		shape = BulletCylinderShape(Kyklops.RADIUS,Kyklops.HEIGHT,ZUp)
		self.node = BulletRigidBodyNode('Enemy')
		self.node.addShape(shape)
 
		self.np = self.__game.render.attachNewNode(self.node)
		self.np.setPos(self.init_x,self.init_y,self.init_z)
		self.np.setH(0)
 
		self.__game.world.attachRigidBody(self.node)

		self.actorNP1.reparentTo(self.np)
        	self.actorNP1.setScale(4.0)
        	self.actorNP1.setH(180)
        	self.actorNP1.setPos(0,0,5)
		self.actorNP1.loop('idle')

		#self.actorNP1.lookAt(self.__game.eve.currentNode)

		#self.actorNP1.lookAt(self.__game.eve.currentNP)

		self.__game.taskMgr.add(self.dummy,'dummy task')				# for some reason i need to ass this task or animation does not start
		self.__game.taskMgr.add(self.follow,'follow')
		self.__game.taskMgr.add(self.monitor_health,'health')
		self.set_attack_sequence()


	def dummy(self,task):
		return task.cont

	def scout_area(self,start,end):
		self.start = Point3(start[0],start[1],start[2])
		self.end = end
		i1 = LerpPosInterval(self.np,5,end,startPos = start)
		i2 = LerpPosInterval(self.np,5,start,startPos = end)
		i3 = LerpHprInterval(self.np,2,(0,0,0),startHpr=(180,0,0))
		i4 = LerpHprInterval(self.np,2,(180,0,0),startHpr=(0,0,0))
		self.scout = Sequence(i1,i3,i2,i4)
		self.scout.loop()

	def return_to_scout(self):
		actorPosVec = Point3(self.init_x,self.init_y,self.init_z) - self.np.getPos()
		print actorPosVec.length()
		if actorPosVec.length() > 200 and self.returning is False:
			self.np.setPos(self.init_x,self.init_y,self.init_z)
			


	def set_attack_sequence(self):
		originalPos=startPos = self.np.getPos()
		originalEvePos = self.__game.eve.currentNP.getPos()
		i1 = LerpPosInterval(self.np,.2,originalEvePos,startPos = originalPos)
		i2 = LerpPosInterval(self.np,.2,originalPos,startPos = originalEvePos)
		self.attack = Sequence(i1,i2)

	def set_returned(self):
		self.returning = False

	def monitor_health(self,task):

		pos = self.np.getPos()
		hpr = self.np.getHpr()
		if self.health < 0:
			self.__game.taskMgr.remove('dummy task')		
			self.__game.taskMgr.remove('follow')
			self.__game.taskMgr.remove('attacked')
			self.__game.enemies.remove(self)
			self.__game.world.removeRigidBody(self.node)
			self.np.remove_node()

			self.actorNP = Actor('models/kyklops/monster1-explode.egg', {'explode':'models/kyklops/monster1-explode.egg'})
			self.actorNP.reparentTo(self.__game.render)
        		self.actorNP.setScale(4.0)
        		self.actorNP.setHpr(hpr)
        		self.actorNP.setPos(pos)
			self.actorNP.play('explode')
			self.__game.taskMgr.add(self.dummy,'dummy task')				# for some reason i need to ass this task or animation does not start

			#self.actorNP.remove_node()
			#self.__game.taskMgr.remove('dummy task')
			return task.done
		return task.cont

	def follow(self,task):
		self.actorNP1.setPlayRate(.3,'idle')
		self.return_to_scout()
		actorPosVec = self.__game.eve.currentNP.getPos() - self.np.getPos()
		if actorPosVec.length() < 100 and actorPosVec.length() > 20:
			self.actorNP1.lookAt(self.__game.eve.currentNP)
			#if self.returning is True:
				#self.return_scout.finish()
			self.actorNP1.setPlayRate(3,'idle')	
			#self.scout.finish()
           		#actor.setHpr(self.panda1.getH() + 180,0,0)

			if self.attack.isPlaying() is False and actorPosVec.length() < 25 and actorPosVec.length() > 20:
				self.actorNP1.setPlayRate(5,'idle')				
				self.set_attack_sequence()
				self.attack.start()



            		if actorPosVec[0] < 0 and actorPosVec[1] < 0 :
                		self.np.setPos(self.np.getX() - .3, self.np.getY() - .3,self.np.getZ())
           		elif actorPosVec[0] < 0 and actorPosVec[1] > 0 :
                		self.np.setPos(self.np.getX() - .3, self.np.getY() + .3,self.np.getZ())
           		elif actorPosVec[0] > 0 and actorPosVec[1] < 0 :
                		self.np.setPos(self.np.getX() + .3, self.np.getY() - .3,self.np.getZ())
          		else:
               			self.np.setPos(self.np.getX() + .3, self.np.getY() + .3,self.np.getZ())
		#print actorPosVec.length()

		if actorPosVec.length() > 100:
			self.np.setPos(self.init_x,self.init_y,self.init_z)
		return task.cont

	def detect_collision(self,task):
		if self.health < 0:
			return task.done
		result = self.__game.world.contactTestPair(self.np.node(),self.__game.eve.currentControllerNode)
		if len(result.getContacts()) > 0:
			self.__game.eve.health -= self.damage
			#print 'ouch'
		return task.cont
		

