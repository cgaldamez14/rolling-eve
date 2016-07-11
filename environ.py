from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletConvexHullShape

from panda3d.bullet import ZUp 

from panda3d.core import Point3

class Environment():
	
	def __init__(self, render, world, loader):
		self.models = {
				'mountains':'models/environ/mountain/mountainegg.egg',
				'tree_wo_leaves':'models/environ/plant6/plants6.egg',
				'creepy_tree':'models/environ/plant2/plants2.egg',
				'palm_tree':'models/environ/plant3/plants3.egg',
				'dark_fern':'models/environ/plant1/plants1.egg',
				'light_fern':'models/environ/shrubbery/shrubbery.egg',
				'purple_flower':'models/environ/shrubbery2/shrubbery2.egg',
				'red_flower':'models/environ/flower/flower.egg',
				'wide_ramp' : 'models/environ/wide-ramp/wide-ramp.egg'}
		self.render = render
		self.world = world
		self.loader = loader

	def render_tree_wo_leaves(self,position,scale,r,h):
		(x_pos,y_pos,z_pos) = position			
		(x_scale,y_scale,z_scale) = scale
		radius = r
		height = h
		
		# Create bullet shape for collisions against tree
		shape = BulletCylinderShape(radius,height,ZUp)

		# Create a bullet node and add the shape above to that node
		node = BulletRigidBodyNode('Tree')
		node.setMass(0)	# This might change, leaving as zero for now
		node.addShape(shape)

		np = self.render.attachNewNode(node)
		np.setPos(x_pos,y_pos,z_pos + z_pos * 6)

		self.world.attachRigidBody(node)

		# Place model inside bullet container that was just created
		model = self.loader.loadModel(self.models['tree_wo_leaves'])
		model.setPos(x_pos,y_pos,z_pos)
		model.setScale(x_scale,y_scale,z_scale)
		model.reparentTo(self.render)

	def render_creepy_tree(self,position,scale,r,h):
		(x_pos,y_pos,z_pos) = position			
		(x_scale,y_scale,z_scale) = scale
		radius = r
		height = h
		
		# Create bullet shape for collisions against tree
		shape = BulletCylinderShape(radius,height,ZUp)

		# Create a bullet node and add the shape above to that node
		node = BulletRigidBodyNode('Tree')
		node.setMass(0)	# This might change, leaving as zero for now
		node.addShape(shape)

		np = self.render.attachNewNode(node)
		np.setPos(x_pos,y_pos,z_pos + z_pos * 4)

		self.world.attachRigidBody(node)

		# Place model inside bullet container that was just created
		model = self.loader.loadModel(self.models['creepy_tree'])
		model.setPos(x_pos,y_pos,z_pos)
		model.setScale(x_scale,y_scale,z_scale)
		model.reparentTo(self.render)

	def render_wide_ramp(self,position,scale):
		(x_pos,y_pos,z_pos) = position			
		(x_scale,y_scale,z_scale) = scale
		#p0 = Point3(-10, -40, 2)
		#p1 = Point3(-10, 40, 2)
		#p2 = Point3(-10, -40, 50)
		#p3 = Point3(-40, -40, 2)
		#p4 = Point3(-40, 40, 2)
		#p5 = Point3(-40, -40, 50)
		#p3 = Point3(10, 10, 5)
		#mesh = BulletTriangleMesh()
		#mesh.addTriangle(p0, p1, p2)
		#mesh.addTriangle(p3, p4, p5)
		#shape1 = BulletTriangleMeshShape(mesh, dynamic=False)
		
		
		#shape2 = BulletBoxShape(Vec3(1, 0.1, 0.1))

		#bodyNP.node().addShape(shape1, TransformState.makePos(Point3(0, 0, 0.1)))
		#bodyNP.node().addShape(shape2, TransformState.makePos(Point3(-1, -1, -0.5)))
		#bodyNP.node().addShape(shape3, TransformState.makePos(Point3(-1, 1, -0.5)))
            	shape2 = BulletConvexHullShape()
		y = -300
		for x in range(10,0,-1):
			shape2.addPoint(Point3(-10, y, x * x *2))
			y += 30				
			#shape2.addPoint(Point3(0, 0, 0))
			#shape2.addPoint(Point3(2, 0, 0))
			#shape2.addPoint(Point3(0, 2, 0))
			#shape2.addPoint(Point3(2, 2, 0))		
		shape2.addPoint(Point3(-150, -30, 0))
		y = -60
		for x in range(1,11):
			shape2.addPoint(Point3(-150, y, x * x *2))
			y -= 30	

		#shape = BulletBoxShape(Vec3(1, 0.1, 0.1))
            	node = BulletRigidBodyNode('Ramp')
            	node.setMass(0)
            	node.addShape(shape2)
           	#np = self.render.attachNewNode(node)
            	#np.setPos(xCoord, 0, height)
            	#np.setR(angle)
            	#self.world.attachRigidBody(node)

		np = self.render.attachNewNode(node)
		np.setPos(x_pos,y_pos,z_pos)

		self.world.attachRigidBody(node)
		#(x_pos,y_pos,z_pos) = position			
		#(x_scale,y_scale,z_scale) = scale
		model = self.loader.loadModel(self.models['wide_ramp'])
		model.setPos(-80,-325,0)
		model.setScale(x_scale,y_scale,z_scale)
		model.reparentTo(np)
		
		


	

