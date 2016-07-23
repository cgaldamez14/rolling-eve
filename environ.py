'''
    ENVIRONMENT MODULE
    This module facilitates the creation of each stage by providing methods that read off text files the information 
    regarding location and orientation of objects in each stage
    Author: Carlos M. Galdamez 
'''

from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import ZUp 

from panda3d.core import Point3,Vec4,Vec3
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Spotlight
from panda3d.core import PerspectiveLens
from panda3d.core import Fog

from envobject import EnvObject
from platform import Platform
from tokens import Token
from kyklops import Kyklops

from direct.interval.IntervalGlobal import Sequence,Parallel,Func
from direct.interval.LerpInterval import LerpPosInterval

from direct.showbase.InputStateGlobal import inputState

class Environment():

	'''
	    Constructor creates instance variables to keep track of the pointers and ghost nodes for the tokens created and keeps
	    a reference to the current game.
	'''
	def __init__(self, game):
		self.moving_plat = []
		self.tokens = []
		self.enemies = []
		self.__game = game

	'''
	    Loads everything in the first stage of the game	
	'''
	def loadStage1(self):
		self.set_tokens('L1')
		self.set_enemies('L1')
		print '\tSETTING ENVIRONMENT ...'
		self.set_platforms('L1')
		self.set_mountains('L1')
		self.set_trees('L1')
		self.set_plants('L1')
		self.set_ramps('L1')
		self.set_rocks('L1')
		self.set_lights()
		self.set_fog((0.5,0.8,0.8),0.0005)
		print '\tSETTING MUSIC AND SOUND EFFECTS ...'
		self.__game.meadow.play()
		self.music = base.loader.loadMusic("sfx/nerves.mp3")
		self.music.setVolume(.07)
		self.music.setLoop(True)
		self.music.play()
		self.total_tokens = len(self.tokens)
		self.__game.taskMgr.add(self.manage_tokens, 'tokens')
		print '\tSTAGE 1 SET'

	'''
	    Loads everything in the second stage of the game	
	'''
	def loadStage2(self):
		self.set_tokens('L2')
		print '\tSETTING KYKLOPS ...'
		self.set_enemies('L2')
		print '\tSETTING ENVIRONMENT ...'
		self.set_platforms('L2')
		self.set_mountains('L2')
		self.set_trees('L2')
		self.set_gates('L2')
		self.set_plants('L2')
		self.set_statues('L2')
		self.set_ramps('L2')
		self.set_rocks('L2')
		self.set_lights()
		self.set_fog((0.1,0.1,0.1),0.0045)
		print '\tSETTING MUSIC AND SOUND EFFECTS ...'
		self.__game.night.play()
		self.music = base.loader.loadMusic("sfx/darkest_child.mp3")
		self.music.setVolume(.07)
		self.music.setLoop(True)
		self.music.play()
		print '\tSTAGE 2 SET'
		self.total_tokens = len(self.tokens)
		self.__game.taskMgr.add(self.manage_platforms, 'moving')
		self.__game.taskMgr.add(self.manage_enemies, 'enemies')
		self.__game.taskMgr.add(self.manage_tokens, 'tokens')


	#--------------------------------------------------------------- FILE READING METHODS -----------------------------------------------------------#

	'''
	    Reads from file information regarding the tokens of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_tokens(self, level):
		print "\tGENERATING TOKENS ..."
		token_file = open('files/.tokens.txt','r')
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
					token.create_token()
				elif start == 'L':
					token = Token('BigToken',(int(x),int(y),int(z)),self.__game)
					token.create_big_token()
			start = token_file.read(1)
		token_file.close()

	'''
	    Reads from file information regarding the trees of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_trees(self, level):
		tree_file = open('files/.trees.txt','r')
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
		tree_file.close()

	'''
	    Reads from file information regarding the plants of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_plants(self, level):
		plant_file = open('files/.plants.txt','r')
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
				elif start == 'P':
					plant = EnvObject('purple_flower',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((.03,.03,.03),(int(h),int(p),int(r)),collisionOn = False)
				elif start == 'R':
					plant = EnvObject('red_flower',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((.15,.15,.15),(int(h),int(p),int(r)),collisionOn = False)
				elif start == 'L':
					plant = EnvObject('light_fern',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((1,1,1),(int(h),int(p),int(r)),collisionOn = False)
			start = plant_file.read(1)
		plant_file.close()

	'''
	    Reads from file information regarding the rocks of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_rocks(self, level):
		rock_file = open('files/.rocks.txt','r')
		start_read = False
		start = rock_file.read(1)
		while len(start) != 0:
			if start == '#': rock_file.readline()
			elif start == '@'and start_read is False:
				if rock_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = rock_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				if start == 'B':
					plant = EnvObject('rock1',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((1,1,1),(int(h),int(p),int(r)),collisionOn = True)
				elif start == 'G':
					plant = EnvObject('rock2',(int(x),int(y),int(z)),self.__game)
					plant.renderObject((1,1,1),(int(h),int(p),int(r)),collisionOn = True)
			start = rock_file.read(1)
		rock_file.close()

	'''
	    Reads from file information regarding the gates of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_gates(self, level):
		gate_file = open('files/.gates.txt','r')
		start_read = False
		start = gate_file.read(1)
		while len(start) != 0:
			if start == '#': gate_file.readline()
			elif start == '@'and start_read is False:
				if gate_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = gate_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				plant = EnvObject('gate',(int(x),int(y),int(z)),self.__game)
				plant.renderObject((.07,.07,.07),(int(h),int(p),int(r)))
			start = gate_file.read(1)
		gate_file.close()


	'''
	    Reads from file information regarding the statues of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_statues(self, level):
		statue_file = open('files/.statues.txt','r')
		start_read = False
		start = statue_file.read(1)
		while len(start) != 0:
			if start == '#': statue_file.readline()
			elif start == '@'and start_read is False:
				if statue_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = statue_file.readline().split(',')
				x = coord[0]
				y = coord[1]
				z = coord[2]
				h = coord[3]
				p = coord[4]
				r = coord[5]
				plant = EnvObject('statue',(int(x),int(y),int(z)),self.__game)
				plant.renderObject((15,15,15),(int(h),int(p),int(r)))
			start = statue_file.read(1)
		statue_file.close()

	'''
	    Reads from file information regarding the ramps of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_ramps(self, level):
		ramp_file = open('files/.ramps.txt','r')
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
		ramp_file.close()

	'''
	    Reads from file information regarding the plants of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_mountains(self, level):
		mountain_file = open('files/.mountains.txt','r')
		start_read = False
		start = mountain_file.read(1)
		while len(start) != 0:
			if start == '#': mountain_file.readline()
			elif start == '@'and start_read is False:
				if mountain_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				coord = mountain_file.readline().split(',')				
				mountain = EnvObject('mountains',(int(coord[3]),int(coord[4]),int(coord[5])),self.__game)
				mountain.renderObject((int(start + coord[0]),int(coord[1]),int(coord[2])),(int(coord[6]),int(coord[7]),int(coord[8])))
				
			start = mountain_file.read(1)
		mountain_file.close()


	'''
	    Reads from file information regarding the platforms of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_platforms(self,level):
		platform_file = open('files/.platforms.txt','r')
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
				p = Platform(self.__game,start + coord[0],(int(coord[2]),int(coord[3]),int(coord[4])),(int(coord[8]),int(coord[9]),int(coord[10])),(int(coord[14]),int(coord[15]),int(coord[16])))
				p.create_bullet_node(self.__game.render, self.__game.world)
				p.add_model((int(coord[5]),int(coord[6]),int(coord[7])), (int(coord[11]),int(coord[12]),int(coord[13])))
				p.add_texture(Platform.TEXTURES[coord[1]])
				# means that it is a moving platform not falling
				if coord[17].strip() == 'True' and (start + coord[0]).find('Fall') < 0:
					p.add_movement((int(coord[18]),int(coord[19]),int(coord[20])),(int(coord[21]),int(coord[22]),int(coord[23])),int(coord[24]))
					self.moving_plat.append(p)
				elif coord[17].strip() == 'True' and (start + coord[0]).find('Fall') >= 0:
					p.set_falling_platform()
					self.moving_plat.append(p)
			start = platform_file.read(1)
		platform_file.close()


	'''
	    Reads from file information regarding the enemies of a specific level in the game and creates them for that level
	    @ param level - level that needs to be rendered	
	'''
	def set_enemies(self,level):
		enemy_file = open('files/.enemies.txt','r')
		start_read = False
		start = enemy_file.read(1)
		while len(start) != 0:
			if start == '#': enemy_file.readline()
			elif start == '@'and start_read is False:
				if enemy_file.readline().split()[0] == level:
					start_read = True
			elif start == '@'and start_read is True:
				break
			elif start_read is True:
				results = enemy_file.readline().split(',')
				e1 = Kyklops(self.__game,start + results[0],health = int(results[1]), damage=float(results[2]))
				e1.render_kyklops(Point3(int(results[3]),int(results[4]),int(results[5])),Point3(int(results[6]),int(results[7]),int(results[8])))
				self.enemies.append(e1)
			start = enemy_file.read(1)
		enemy_file.close()


	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

	'''
	    Sets ambient and directional lights to the game	
	'''
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

	'''
	    Creates fog in the game	
	'''
	def set_fog(self,colour,density):
		print "\tGENERATING FOG ..."
		expfog = Fog("Scene-wide exponential Fog object")
		expfog.setColor(*colour)
		expfog.setExpDensity(density)
		self.__game.render.setFog(expfog)
		base.setBackgroundColor(*colour)


	def manage_platforms(self,task):
	        for plat in self.moving_plat:
	            plat.contact_made()
		return task.cont

	def manage_enemies(self,task):
		if len(self.enemies) == 0:
			return task.done
		for enemy in self.enemies:
			enemy.follow()
			enemy.detect_contact()
			enemy.monitor_health()
		return task.cont

	def manage_tokens(self,task):
		if len(self.tokens) == 0:
			return task.done
	        for token in self.tokens:
	            	token.collected()
			token.spinToken()
		self.__game.interface.score['text'] = str(self.__game.eve.tiresCollected)
		return task.cont

				
				

		


	

