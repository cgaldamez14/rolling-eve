from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode

from panda3d.core import Vec3,Texture

class Platform():
	MODEL = 'models/environ/crate/crate.egg'

	TEXTURES = {'1':'models/textures/grass.jpg',
		    '2':'models/textures/rock.jpg'}
	
	def __init__(self, name, size, pos, hpr, mass = 0):
		self.name = name
		self.mass = mass
		(self.x_pos, self.y_pos, self.z_pos) = pos
		(self.x_size, self.y_size, self.z_size) = size
		(self.h,self.p,self.r) = hpr
	
	def create_bullet_node(self,render,world):
		self.shape = BulletBoxShape(Vec3(self.x_size,self.y_size,self.z_size))
            	self.node = BulletRigidBodyNode(self.name)
            	self.node.setMass(self.mass)
           	self.node.addShape(self.shape)
            	world.attachRigidBody(self.node)
            	self.np = render.attachNewNode(self.node)
            	self.np.setPos(self.x_pos, self.y_pos, self.z_pos)
		self.np.setHpr(self.h,self.p,self.r)

	def add_model(self,scale,pos):
		(x_pos, y_pos, z_pos) = pos
		(x_scale, y_scale, z_scale) = scale
		self.model = loader.loadModel(Platform.MODEL)
		self.model.setScale(x_scale,y_scale,z_scale)
                self.model.setPos(x_pos,y_pos,z_pos)
                self.model.reparentTo(self.np)

	def add_texture(self,tex_path):
		plat_texture = loader.loadTexture(tex_path)
		plat_texture.setWrapU(Texture.WM_repeat)
		plat_texture.setWrapV(Texture.WM_repeat)
                self.model.setTexture(plat_texture,1)
	

