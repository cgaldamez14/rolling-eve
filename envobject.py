from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh

class EnvObject():
	MODELS = {
		'mountains':'models/environ/mountain/mountainegg.egg',
		'tree1':'models/environ/plant6/plants6.egg',				# Leaf less tree
		'tree2':'models/environ/plant2/plants2.egg',				# Creepy Tree
		'tree3':'models/environ/plant3/plants3.egg',				# Palm Tree
		'dark_fern':'models/environ/plant1/plants1.egg',
		'light_fern':'models/environ/shrubbery/shrubbery.egg',
		'purple_flower':'models/environ/shrubbery2/shrubbery2.egg',
		'red_flower':'models/environ/flower/flower.egg',
		'wide_ramp' : 'models/environ/wide-ramp/wide-ramp.egg'}
	
	def __init__(self,name, pos, render, world, loader):
		self.name = name
		self.render = render
		self.world = world

		self.model = loader.loadModel(EnvObject.MODELS[self.name])
		(self.x,self.y,self.z) = pos

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

			np = self.render.attachNewNode(node)
			np.setPos(self.x,self.y,self.z)
			np.setHpr(h,p,r)
			np.setScale(x_c,y_c,z_c)

			self.world.attachRigidBody(node)
		self.model.setPos(self.x,self.y,self.z)
		self.model.setHpr(h,p,r)
		self.model.setScale(x_scale,y_scale,z_scale)
		self.model.reparentTo(self.render)
				
			

		
		
