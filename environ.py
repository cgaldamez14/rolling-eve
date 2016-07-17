from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletConvexHullShape
from panda3d.core import AmbientLight,DirectionalLight,Spotlight,PerspectiveLens

from panda3d.bullet import ZUp 

from panda3d.core import Point3,Vec4,Vec3
from panda3d.core import Fog

from tokens import Token
from envobject import EnvObject
from platform import Platform

class Environment():
	def __init__(self, game):
		self.tokens = []
		self.tokens_np = []
		self.__game = game

	def loadStage1(self):
		self.set_tokens('L1')
		print '\tSETTING ENVIRONMENT ...'
		self.set_platforms('L1')
		self.set_trees('L1')
		self.set_plants('L1')
		self.set_ramps('L1')
		self.set_lights()
		self.set_fog()
		print '\tSETTING MUSIC AND SOUND EFFECTS ...'
		self.meadow = base.loader.loadSfx("sfx/meadow_land.wav")
		self.meadow.setLoop(True)
		self.meadow.setVolume(.2)
		self.meadow.play()
		self.music = base.loader.loadMusic("sfx/nerves.mp3")
		self.music.setVolume(.07)
		self.music.setLoop(True)
		self.music.play()
		print '\tSTAGE 1 SET'

	def set_tokens(self, level):
		print "\tGENERATING TOKENS ..."
		token_file = open('.tokens.txt','r')
		start_read = False
		start = token_file.read(1)
		while len(start) != 0:
			if start == '#': token_file.readline()
			elif start == '@'and start_read is False:
				if token_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = token_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				if start == 'R':
					token = Token('Token',(int(x),int(y),int(z)),self.__game)
					(node,np) = token.create_token()
					self.tokens.append(node)
					self.tokens_np.append(np)
				elif start == 'L':
					token = Token('BigToken',(int(x),int(y),int(z)),self.__game)
					(node,np) = token.create_big_token()
					self.tokens.append(node)
					self.tokens_np.append(np)
			start = token_file.read(1)

	def set_trees(self, level):
		tree_file = open('.trees.txt','r')
		start_read = False
		start = tree_file.read(1)
		while len(start) != 0:
			if start == '#': tree_file.readline()
			elif start == '@'and start_read is False:
				if tree_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = tree_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				if start == 'L':
					tree = EnvObject('tree1',(int(x),int(y),int(z)),self.__game)
					tree.renderObject((7,7,5),(int(h),int(p),int(r)),collisionOn = True)
				elif start == 'C':
					tree = EnvObject('tree2',(int(x),int(y),int(z)),self.__game)
					tree.renderObject((1,1,1),(int(h),int(p),int(r)),collisionOn = True)
			start = tree_file.read(1)

	def set_plants(self, level):
		plant_file = open('.plants.txt','r')
		start_read = False
		start = plant_file.read(1)
		while len(start) != 0:
			if start == '#': plant_file.readline()
			elif start == '@'and start_read is False:
				if plant_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = plant_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				if start == 'D':
					plant = EnvObject('dark_fern',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((1,1,1),(int(h),int(p),int(r)),collisionOn = False)
			start = plant_file.read(1)

	def set_ramps(self, level):
		ramp_file = open('.ramps.txt','r')
		start_read = False
		start = ramp_file.read(1)
		while len(start) != 0:
			if start == '#': ramp_file.readline()
			elif start == '@'and start_read is False:
				if ramp_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = ramp_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				if start == 'W':
					ramp = EnvObject('wide_ramp',(int(x),int(y),int(z)),self.__game)
					ramp.renderObject((.1,1,.75),(int(h),int(p),int(r)),collisionOn = True)
			start = ramp_file.read(1)

	def set_platforms(self,level):
		platform_file = open('.platforms.txt','r')
		start_read = False
		start = platform_file.read(1)
		while len(start) != 0:
			if start == '#': platform_file.readline()
			elif start == '@'and start_read is False:
				if platform_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = platform_file.readline().split(',')
				p = Platform(coord[0],(int(coord[2]),int(coord[3]),int(coord[4])),(int(coord[8]),int(coord[9]),int(coord[10])),(int(coord[14]),int(coord[15]),int(coord[16])))
				p.create_bullet_node(self.__game.render, self.__game.world)
				p.add_model((int(coord[5]),int(coord[6]),int(coord[7])), (int(coord[11]),int(coord[12]),int(coord[13])))
				p.add_texture(Platform.TEXTURES[coord[1]])

			start = platform_file.read(1)

	def set_lights(self):
		print "\tSETTING LIGHTS ..."
        	ambientLight = AmbientLight("ambientLight")
        	ambientLight.setColor(Vec4(.3, .3, .3, 1))
        	directionalLight = DirectionalLight("directionalLight")
        	directionalLight.setDirection(Vec3(-5, -5, -5))
        	directionalLight.setColor(Vec4(1, 1, 1, 1))
        	directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        	self.__game.render.setLight(self.__game.render.attachNewNode(ambientLight))
        	self.__game.render.setLight(self.__game.render.attachNewNode(directionalLight))

	def set_fog(self):
		print "\tGENERATING FOG ..."
		colour = (0.5,0.8,0.8)
		expfog = Fog("Scene-wide exponential Fog object")
		expfog.setColor(*colour)
		expfog.setExpDensity(0.0005)
		self.__game.render.setFog(expfog)
		base.setBackgroundColor(*colour)
				
				

		


	

