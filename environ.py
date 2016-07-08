from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import ZUp 

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
				'red_flower':'models/environ/flower/flower.egg'}
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
		
		


	

