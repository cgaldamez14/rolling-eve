'''
    PLATFORM MODULE
    This module facilitates the creation of platforms by using the provided methods to 
    create bullet nodes, and platforms models with certain position and orientation and with
    specific textures.
    Author: Carlos M. Galdamez
'''

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from pandac.PandaModules import TextureStage

from panda3d.core import Vec3,Texture,SamplerState

from direct.interval.IntervalGlobal import Sequence
from direct.interval.LerpInterval import LerpPosInterval

from direct.showbase.InputStateGlobal import inputState

class Platform():
	# Model used to create platforms
	MODEL = 'models/environ/crate/crate.egg'

	# Textures used for model
	TEXTURES = {'1':'models/textures/grass.jpg',
		    '2':'models/textures/rock.jpg',
		    '3':'models/textures/bricks.jpg',
		    '4':'models/textures/bricks.jpg'}

	'''
	    Constructor create name and mass instance variables for the platform object, and also stores position, 
	    orientation and size in instance variables.
	    @param name - name of platform (eg. ground, wall)
	    @param size - platform scale
	    @param pos - position of the platform
	    @param hpr - heading,pitch and roll or platform
	    @param mass - mass of platform, default is 0
	'''	
	def __init__(self,game,name, size, pos, hpr, mass = 0):
		self.name = name
		self.mass = mass
		(self.x_pos, self.y_pos, self.z_pos) = pos
		(self.x_size, self.y_size, self.z_size) = size
		(self.h,self.p,self.r) = hpr
		self.falling_platform = False
		self.__game = game
	
	'''
	    Creates bullet node to make the platform a collision object
	    @param render - game renderer
	    @param world - game world
	'''
	def create_bullet_node(self,render,world):
		self.shape = BulletBoxShape(Vec3(self.x_size,self.y_size,self.z_size))
            	self.node = BulletRigidBodyNode(self.name)
            	self.node.setMass(self.mass)
           	self.node.addShape(self.shape)
            	world.attachRigidBody(self.node)
            	self.np = render.attachNewNode(self.node)
            	self.np.setPos(self.x_pos, self.y_pos, self.z_pos)
		self.np.setHpr(self.h,self.p,self.r)
		return (self.np,self.node)

	'''
	    Adds model to bullet node
	    @param scale - size of the model
	    @param pos - postion of the model relative to the bullet node 
	'''
	def add_model(self,scale,pos):
		(x_pos, y_pos, z_pos) = pos
		(x_scale, y_scale, z_scale) = scale
		self.model = loader.loadModel(Platform.MODEL)
		self.model.setScale(x_scale,y_scale,z_scale)
                self.model.setPos(x_pos,y_pos,z_pos)
                self.model.reparentTo(self.np)

	'''
	     Adds texture to model that was created. If none was created this will cause a problem.
	     @param tex_path - key of TEXTURES dictionary for texture requested
	'''
	def add_texture(self,tex_path):
		plat_texture = loader.loadTexture(tex_path)
		#plat_texture.setWrapU(Texture.WMRepeat)
		#plat_texture.setWrapV(Texture.WMRepeat)
                self.model.setTexture(plat_texture,1)
        	ts = TextureStage.getDefault()
       	 	texture = self.model.getTexture()
		#self.model.setTexOffset(ts, -0.5, -0.5)
		self.model.setTexScale(ts, 2, 2)


	def add_movement(self, start, end, speed):
		i1 = LerpPosInterval(self.np,speed,end,startPos = start)
		i2 = LerpPosInterval(self.np,speed,start,startPos = end)
		Sequence(i1,i2).loop()
		return self.np

	def set_falling_platform(self):
		self.falling_platform = True

	def sync_movement(self,dx,dy,dz,task):
		self.__game.eve.currentNP.setPos(self.np.getX()+dx,self.np.getY()+dy,self.np.getZ()+dz)
		return task.cont

	def fall_countdown(self,start_time,task):
		if globalClock.getRealTime() - start_time > 2:
			i1 = LerpPosInterval(self.np,20,(self.np.getX(),self.np.getY(),0),startPos = self.np.getPos())
			Sequence(i1).start()
			return task.done
		return task.cont

	def contact_made(self):
		result = self.__game.world.contactTestPair(self.np.node(),self.__game.eve.currentControllerNode)
		if inputState.isSet('forward') and self.name.find('Fall') < 0:
			self.__game.taskMgr.remove(self.name)
			return
		if len(result.getContacts()) > 0:
			if len(self.__game.taskMgr.getTasksNamed(self.name)) == 0 and self.name.find('Fall') < 0:
				p_x = self.np.getX()
				p_y = self.np.getY()
				p_z = self.np.getZ()
				a_x = self.__game.eve.currentNP.getX()
				a_y = self.__game.eve.currentNP.getY()
				a_z = self.__game.eve.currentNP.getZ()

				dx = a_x - p_x
				dy = a_y - p_y
				dz = a_z - p_z
				self.__game.taskMgr.add(self.sync_movement,self.name, extraArgs=[dx,dy,dz],appendTask=True)
				self.__game.tasks.append(self.name)
			elif len(self.__game.taskMgr.getTasksNamed(self.name)) == 0 and self.name.find('Fall') >= 0:
				start = globalClock.getRealTime()
				self.__game.taskMgr.add(self.fall_countdown,self.name, extraArgs=[start],appendTask=True)
				self.__game.tasks.append(self.name)
				
		elif self.name.find('Fall') < 0:
			self.__game.taskMgr.remove(self.name)
		
	

