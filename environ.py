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

from direct.interval.IntervalGlobal import Sequence
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
		self.tokens_np = []
		self.__game = game

	'''
	    Loads everything in the first stage of the game	
	'''
	def loadStage1(self):
		self.set_tokens('L1')
		print '\tSETTING ENVIRONMENT ...'
		self.set_platforms('L1')
		self.set_trees('L1')
		self.set_plants('L1')
		self.set_ramps('L1')
		self.set_rocks('L1')
		self.set_lights()
		self.set_fog((0.5,0.8,0.8),0.0005)
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

	'''
	    Loads everything in the second stage of the game	
	'''
	def loadStage2(self):
		#self.set_tokens('L1')
		print '\tSETTING ENVIRONMENT ...'
		self.set_platforms('L2')
		#Platform,3,12,10,3,8,5,2,1400,875,1200,0,0,0,0,0,0


		#p1= Platform()
		#self.moving_plat.append(p1.create_moving_platform('3',(12,10,3),(1375,1325,1322),(0,0,0),(8,5,2), (0,0,0),(1375,1325,1322),(1300,1325,1322),5))
		

		p1 = Platform("MovingPlat1",(12,10,3),(1425,1325,1322),(0,0,0))
		p1.create_bullet_node(self.__game.render, self.__game.world)
		p1.add_model((8,5,2), (0,0,0))
		p1.add_texture(Platform.TEXTURES['3'])
		p1.add_movement((1425,1325,1322),(1300,1325,1322),5)
		self.moving_plat.append(p1)

		p2 = Platform("MovingPlat2",(12,10,3),(1300,1439,1322),(0,0,0))
		p2.create_bullet_node(self.__game.render, self.__game.world)
		p2.add_model((8,5,2), (0,0,0))
		p2.add_texture(Platform.TEXTURES['3'])
		p2.add_movement((1300,1439,1322),(1425,1439,1322),5)
		self.moving_plat.append(p2)

		p3 = Platform("MovingPlat3",(12,10,3),(1300,1553,1322),(0,0,0))
		p3.create_bullet_node(self.__game.render, self.__game.world)
		p3.add_model((8,5,2), (0,0,0))
		p3.add_texture(Platform.TEXTURES['3'])
		p3.add_movement((1425,1553,1322),(1300,1553,1322),8)
		self.moving_plat.append(p3)

		p4 = Platform("MovingPlat4",(15,15,3),(1250,1667,1322),(0,0,0))
		p4.create_bullet_node(self.__game.render, self.__game.world)
		p4.add_model((10,10,2), (0,0,0))
		p4.add_texture(Platform.TEXTURES['3'])
		#p3.add_movement((1250,1667,1322),(1050,1667,1422),10)
		p4.add_movement((1250,1667,1322),(1250,1667,1422),15)
		self.moving_plat.append(p4)

		p5 = Platform("FallPlat1",(15,15,3),(1150,1667,1422),(0,0,0))
		p5.create_bullet_node(self.__game.render, self.__game.world)
		p5.add_model((10,10,2), (0,0,0))
		p5.add_texture(Platform.TEXTURES['3'])
		p5.set_falling_platform()
		self.moving_plat.append(p5)

		p6 = Platform("FallPlat2",(15,15,3),(858,1667,1422),(0,0,0))
		p6.create_bullet_node(self.__game.render, self.__game.world)
		p6.add_model((10,10,2), (0,0,0))
		p6.add_texture(Platform.TEXTURES['3'])
		p6.set_falling_platform()
		self.moving_plat.append(p6)

		p7 = Platform("FallPlat3",(15,15,3),(566,1667,1422),(0,0,0))
		p7.create_bullet_node(self.__game.render, self.__game.world)
		p7.add_model((10,10,2), (0,0,0))
		p7.add_texture(Platform.TEXTURES['3'])
		p7.set_falling_platform()
		self.moving_plat.append(p7)

		p7 = Platform("FallPlat4",(15,15,3),(274,1667,1422),(0,0,0))
		p7.create_bullet_node(self.__game.render, self.__game.world)
		p7.add_model((10,10,2), (0,0,0))
		p7.add_texture(Platform.TEXTURES['3'])
		p7.set_falling_platform()
		self.moving_plat.append(p7)

		#e1 = Kyklops(self.__game,health = 100, damage=2)
		#e1.render_kyklops(((1363,950,1335)))
		#e1.scout_area((1363,950,1335),(1363,900,1335))
		#e1.attach_actor(e1.actorNP1,'idle')


		#i1 = LerpPosInterval(self.np,5,(1300,1325,1322),startPos = (1375,1325,1322))
		#i2 = LerpPosInterval(self.np,5,(1375,1325,1322),startPos = (1300,1325,1322))
		#Sequence(i1,i2).loop()


		#self.moving_plat.append(self.np)


		

		self.set_trees('L2')
		self.set_gates('L2')
		self.set_plants('L2')
		self.set_statues('L2')
		#self.set_ramps('L1')
		#self.set_rocks('L1')
		self.set_lights()
		self.set_fog((0.1,0.1,0.1),0.0045)
		print '\tSETTING MUSIC AND SOUND EFFECTS ...'
		#self.meadow = base.loader.loadSfx("sfx/meadow_land.wav")
		#self.meadow.setLoop(True)
		#self.meadow.setVolume(.2)
		#self.meadow.play()
		#self.music = base.loader.loadMusic("sfx/nerves.mp3")
		#self.music.setVolume(.07)
		#self.music.setLoop(True)
		#self.music.play()
		print '\tSTAGE 2 SET'
		self.__game.taskMgr.add(self.process_contacts, 'moving')


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
					(node,np) = token.create_token()
					self.tokens.append(node)
					self.tokens_np.append(np)
				elif start == 'L':
					token = Token('BigToken',(int(x),int(y),int(z)),self.__game)
					(node,np) = token.create_big_token()
					self.tokens.append(node)
					self.tokens_np.append(np)
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
				p = Platform(coord[0],(int(coord[2]),int(coord[3]),int(coord[4])),(int(coord[8]),int(coord[9]),int(coord[10])),(int(coord[14]),int(coord[15]),int(coord[16])))
				p.create_bullet_node(self.__game.render, self.__game.world)
				p.add_model((int(coord[5]),int(coord[6]),int(coord[7])), (int(coord[11]),int(coord[12]),int(coord[13])))
				p.add_texture(Platform.TEXTURES[coord[1]])

			start = platform_file.read(1)
		platform_file.close()


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

	def sync_movement(self,node,dx,dy,dz,task):
		self.__game.eve.currentNP.setPos(node.getX()+dx,node.getY()+dy,node.getZ()+dz)
		return task.cont

	def fall_countdown(self,plat,start_time,task):
		print 'waa?'
		if globalClock.getRealTime() - start_time > 2:
			print 'falling'
			i1 = LerpPosInterval(plat.np,20,(plat.np.getX(),plat.np.getY(),0),startPos = plat.np.getPos())
			Sequence(i1).start()
			return task.done
		return task.cont

	def process_contacts(self,task):
	        for plat in self.moving_plat:
	            self.collision_handler(plat)
		return task.cont

	def collision_handler(self,plat):
		#print self.__game.taskMgr.getTasks()
		result = self.__game.world.contactTestPair(plat.np.node(),self.__game.eve.currentControllerNode)
		if inputState.isSet('forward') and plat.np.getName().find('Fall') < 0:
			self.__game.taskMgr.remove(plat.np.getName())
			return
		if len(result.getContacts()) > 0:
			if len(self.__game.taskMgr.getTasksNamed(plat.np.getName())) == 0 and plat.np.getName().find('Fall') < 0:
				# and plat.np.getName().find('Fall') < 0 is False:
				p_x = plat.np.getX()
				p_y = plat.np.getY()
				p_z = plat.np.getZ()
				a_x = self.__game.eve.currentNP.getX()
				a_y = self.__game.eve.currentNP.getY()
				a_z = self.__game.eve.currentNP.getZ()

				dx = a_x - p_x
				dy = a_y - p_y
				dz = a_z - p_z
				self.__game.taskMgr.add(self.sync_movement,plat.np.getName(), extraArgs=[plat.np,dx,dy,dz],appendTask=True)
				self.__game.tasks.append(plat.np.getName())
			elif len(self.__game.taskMgr.getTasksNamed(plat.np.getName())) == 0 and plat.np.getName().find('Fall') >= 0:
				#and plat.np.getName().find('Fall') >= 0:
				start = globalClock.getRealTime()
				self.__game.taskMgr.add(self.fall_countdown,plat.np.getName(), extraArgs=[plat,start],appendTask=True)
				self.__game.tasks.append(plat.np.getName())
				
		elif plat.np.getName().find('Fall') < 0:
			self.__game.taskMgr.remove(plat.np.getName())

				
				

		


	

