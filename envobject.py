'''
    ENVOBJECT MODULE
    This module facilitates the redering of objects in any level in the game. It provides a method that
    creates a triangle mesh on any model given if the user requires it.
    Author: Carlos M. Galdamez
'''
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh

from pandac.PandaModules import TextureStage

class EnvObject():

	# Dictionary for all available models for the game
	MODELS = {
		'mountains':'models/environ/mountain/mountainegg.egg',
		'tree1':'models/environ/plant6/plants6.egg',				# Leaf less tree
		'tree2':'models/environ/plant2/plants2.egg',				# Creepy Tree
		'tree3':'models/environ/plant3/plants3.egg',				# Palm Tree
		'dark_fern':'models/environ/plant1/plants1.egg',
		'light_fern':'models/environ/shrubbery/shrubbery.egg',
		'purple_flower':'models/environ/shrubbery2/shrubbery2.egg',
		'red_flower':'models/environ/flower/flower.egg',
		'wide_ramp' : 'models/environ/wide-ramp/wide-ramp.egg',
		'ramp' : 'models/environ/ramp/ramp.egg',
		'bridge' : 'models/environ/bridge/bridge.egg',
		'gate' : 'models/environ/gate/gate.egg',
		'statue' : 'models/environ/statue/Statue.egg',
		'tombstone' : 'models/environ/tombstone/tombstone.egg',
		'rock1' : 'models/environ/rock/rock.egg',
		'rock2' : 'models/environ/rock2/rock2.egg',}
	
	'''
	    Constructor creates instance variables for the names of the object, position of the object and a
	    reference to the current game.
	    @param name - name can be any of the keys in the model dictionary
	    @param pos - position were model will be placed
	    @param game - reference to the current game
	'''
	def __init__(self,name,pos,game):
		self.name = name
		self.__game = game
		self.model = self.__game.loader.loadModel(EnvObject.MODELS[self.name])
		(self.x,self.y,self.z) = pos


	'''
	    Renders object to the current world. 
	    @param scale - size of model relative to its normal size
	    @param hpr - heading, pitch and roll of the model
	    @param collisionOn - True if collision node is required to be made for object. Default is False.
	'''
	def renderObject(self,scale,hpr,collisionOn=False):
		(x_scale,y_scale,z_scale) = scale
		(h,p,r) = hpr
		if collisionOn is True:
			if self.name is 'wide_ramp':
				(x_c,y_c,z_c) = (x_scale + .2,y_scale+2.5,z_scale+1.75)
			if self.name is 'tree1':
				(x_c,y_c,z_c) = (x_scale,y_scale,z_scale)
			if self.name is 'tree2':
				(x_c,y_c,z_c) = (x_scale,y_scale,z_scale)
			if self.name is 'rock1':
				(x_c,y_c,z_c) = (x_scale * 2,y_scale * 2,z_scale*2)
			if self.name is 'rock2':
				(x_c,y_c,z_c) = (x_scale*100,y_scale*100,z_scale*100)
			if self.name is 'gate':
				(x_c,y_c,z_c) = (x_scale * 10,y_scale,z_scale*3.5)
			if self.name is 'statue':
				(x_c,y_c,z_c) = (x_scale,y_scale,z_scale)

       			mesh = BulletTriangleMesh()
        		for geomNP in self.model.findAllMatches('**/+GeomNode'):
            			geomNode = geomNP.node()
            			ts = geomNP.getTransform(self.model)
          		for geom in geomNode.getGeoms():
                		mesh.addGeom(geom, ts)

        		shape = BulletTriangleMeshShape(mesh, dynamic=False)

            		node = BulletRigidBodyNode(self.name)
            		node.setMass(0)
            		node.addShape(shape)

			np = self.__game.render.attachNewNode(node)
			np.setPos(self.x,self.y,self.z)
			np.setHpr(h,p,r)
			np.setScale(x_c,y_c,z_c)

			self.__game.world.attachRigidBody(node)
		self.model.setPos(self.x,self.y,self.z)
		self.model.setHpr(h,p,r)
		self.model.setScale(x_scale,y_scale,z_scale)
		self.model.reparentTo(self.__game.render)
		
		if self.name is 'statue':
			plat_texture = loader.loadTexture('models/textures/rocky.jpg')
		        self.model.setTexture(plat_texture,1)
			ts = TextureStage.getDefault()
	       	 	texture = self.model.getTexture()
			self.model.setTexScale(ts, 1, 1)

		#if self.name is 'tree1':
		#	plat_texture = loader.loadTexture('models/textures/bark.jpg')
		#       self.model.setTexture(plat_texture,1)
		#	ts = TextureStage.getDefault()
	       	# 	texture = self.model.getTexture()
		#	self.model.setTexScale(ts, 4, 4)


				
			

		
		
