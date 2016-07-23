'''
	ONSCREEN INTERFACE MODULE
	Module contains all necessary methods needed for anything being parented to render2d or aspect2d.
	All create methods are called in the beginning of the game and all frames are hidden. They are
	only displayed only when certain actions are taken (eg. button clicks).
	Author: Carlos M Galdamez
'''

from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import DirectFrame

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import TransparencyAttrib
from panda3d.core import LVecBase3f
from panda3d.core import TextNode
from panda3d.core import VBase4

from direct.task import Task

from user import User
import time,sys

class OnScreenInterface():
	
	# Time users have for each level will be listed here
	LEVEL_1_TIME = (2,59)
	LEVEL_2_TIME = (3,59)
	
	'''
	    Constructor takes a reference of the current game, creates a direct frame that everything
	    will be parented to and also sets the sound effect that will be used for aything on the 
	    onscreen interface class.
	    @param game - pointer to current game
	'''
	def __init__(self,game):
		self.previous = 0
		self.min = 0
		self.sec = 0
		self.__game = game
		self.create_main_frame()
		self.set_sound()

	'''
	    Creates instance variables for all sounds effects that will be used for this
	    instance of the class. Volume and playrate is also set.
	'''
	def set_sound(self):
		self.intro = base.loader.loadMusic("sfx/not_seems.mp3")
		self.hover = base.loader.loadSfx("sfx/hover.mp3")
		self.click = base.loader.loadSfx("sfx/click.wav")
		self.pause = base.loader.loadSfx("sfx/pause.wav")
		self.blocked = base.loader.loadMusic("sfx/blocked.wav")
		self.blocked.setVolume(.05)
		self.hover.setPlayRate(5)
		self.hover.setVolume(.05)
		self.intro.setVolume(.5)
		self.intro.setLoop(True)

	'''
	    Creates instance variable that decides how much time user will have to complete the current level
	'''
	def set_timer(self):
		if self.__game.current_level == 'L1':
			self.level_time = OnScreenInterface.LEVEL_1_TIME
		elif self.__game.current_level == 'L2':
			self.level_time = OnScreenInterface.LEVEL_2_TIME
	
	'''
	   Creates the initial two frames that are needed in the game before the gameplay starts
	'''
	def load_initial_interface(self):
		self.create_player()
		self.create_start()
		self.create_stage_selector(button=False)
	
	'''
	   Creates the rest of the frames that are needed once gameplay has started
	'''
	def load_essentials(self):
		self.create_health_bar()
		self.create_token_counter()
		self.create_coordinate_view()	
		self.create_help_menu()
		self.create_control_guide()
		self.create_stage_selector()
		self.create_leaderboard_selector()
		self.create_leaderboard(self.__game.current_level)

	#------------------------------------------------------------------------- CREATE METHODS -----------------------------------------------------------------#

	'''
	    Creates frame that will be the parent of all the other frames created for this game.
	    This is done so that when all gui interfaces need to be destroyed they can be destroyed with 
	    on call to destroy.
	'''
	def create_main_frame(self):
		self.main_frame = DirectFrame(frameColor = (0,0,0,0),frameSize=(-2,2,-1,1), pos=(0,0,0))

	
	'''
	    Creates game start frame. This frame is not hidden because it is the first thing the user sees.	
	'''
	def create_start(self):
		# Direct frame to hold contents of start frame
		self.start_frame = DirectFrame(parent = self.main_frame,frameColor = (0,0,0,1),frameSize=(-2,2,-1,1), pos=(0,0,0))
		
		# Onscreen image of kyklops
		kyklops = OnscreenImage(parent=self.start_frame,image = 'img/kyklops.png', pos = (.9, 0, .3), scale = (.3,0,.3))
		kyklops.setTransparency(TransparencyAttrib.MAlpha)
		
		# Onscreen image of game title
		title = OnscreenImage(parent=self.start_frame,image = 'img/title.png', pos = (0, 0, 0), scale = (.8,0,.3))
		title.setTransparency(TransparencyAttrib.MAlpha)
		
		# Onscreen image of eve rolling
		rolling_eve = OnscreenImage(parent=self.start_frame,image = 'img/rolling-eve.png', pos = (-.95, 0, -.1), scale = (.5,0,.5))
		rolling_eve.setTransparency(TransparencyAttrib.MAlpha)

		# Create button to start game
		self.create_menu_button(self.start_frame,'START',LVecBase3f(0,0,-.5),self.show_input)

		# Play intro music		
		self.intro.play()

	'''
	    Creates a fields so the player can input his/her name at the beginning of the game. This is used
	    to store the name and user score at the end of each stage in the game.
	'''
	def create_player(self):
		# Direct frame to hold input field
		self.input_frame = DirectFrame(parent=self.main_frame,frameColor = (0,0,0,1),frameSize=(-2,2,-1,1), pos=(0,0,0))
		
		# Instructions for user
		instructions = OnscreenText(parent=self.input_frame, text = 'Enter your name: ', pos = (0,.2), scale = 0.1, fg=(0,.2,.2,1),shadow=(1,1,1,.7))
		
		# Name input field
		self.entry = DirectEntry(parent=self.input_frame,text = "",scale=(.1,1,.08),pos=(-.5,0,0),command=self.set_player,numLines=1,focus=1)

		# Hide frame
		self.input_frame.hide()

	'''
	    Creates help menu frame with buttons for each option in the menu. This frame is hidden.
	'''
	def create_help_menu(self):
		# Direct frame to hold buttons and text
		self.help_frame = DirectFrame(parent=self.main_frame,frameColor = (.6,.6,.6,.7),frameSize=(-2,2,-1,1), pos=(0,0,0))
		
		# Title for frame
		title = OnscreenText(parent=self.help_frame, text = 'MENU', pos = (0, .4), scale = 0.2, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1) )
		
		# Buttons for menu frame
		self.create_menu_button(self.help_frame,'Controls',LVecBase3f(0,0,.1),self.show_controls)
		self.create_menu_button(self.help_frame,'Level Select',LVecBase3f(0,0,-.1),self.show_level_select)
		self.create_menu_button(self.help_frame,'Leaderboard',LVecBase3f(0,0,-.3),self.show_lb_selection)
		self.create_menu_button(self.help_frame,'Quit',LVecBase3f(0,0,-.5),sys.exit)
		
		# Hide frame 
		self.help_frame.hide()

	'''
	    Creates control instruction frame. This frame hidden. 
	'''
	def create_control_guide(self):
		# Direct frame to hold player control instructions
		self.control_frame = DirectFrame(frameColor = (.9,.9,.9,.9),frameSize=(-2,2,-1,1), pos=(0,0,0))

		# Title for frame
		frame_title = OnscreenText(parent=self.control_frame, text = 'CONTROL KEYS', pos = (0, .5), scale = 0.1, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1))

		# Player control instructions
		t1 = OnscreenText(parent=self.control_frame, text = '[w] - Forward', pos = (0, .2), scale = 0.07, fg=(0,0,0,1))
		t2 = OnscreenText(parent=self.control_frame, text = '[a] - Left', pos = (0, .1), scale = 0.07,fg=(0,0,0,1))
		t3 = OnscreenText(parent=self.control_frame, text = '[d] - Right', pos = (0, 0), scale = 0.07,fg=(0,0,0,1))
		t4 = OnscreenText(parent=self.control_frame, text = '[space] - Jump', pos = (0, -.1), scale = 0.07,fg=(0,0,0,1))
		t5 = OnscreenText(parent=self.control_frame, text = '[1] - Change character mode', pos = (0, -.2), scale = 0.07,fg=(0,0,0,1))
		t6 = OnscreenText(parent=self.control_frame, text = '[h] - Help Menu', pos = (0, -.3), scale = 0.07,fg=(0,0,0,1))

		# Create button to go back to main menu
		self.create_menu_button(self.control_frame,'Back',LVecBase3f(0,0,-.7),self.show_menu)

		# Hide frame
		self.control_frame.hide()
	'''
	    Creates stage selection frame. This frame is hidden.
	'''
	def create_stage_selector(self,button=True):
		# Direct frame to hold stage selection buttons
		self.stage_select_frame = DirectFrame(parent=self.main_frame,frameColor = (.8,.8,.8,.9),frameSize=(-2,2,-1,1), pos=(0,0,0))
		
		title = OnscreenText(parent=self.stage_select_frame, text = 'Stage Selection', pos = (0, .7), scale = .15,fg=(0,.2,.2,1))

		# Stage select buttons with title for each button 
		t1 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 1', pos = (-.9, .5), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/stage1.png','',LVecBase3f(-.9,0,.2),self.__game.clean_and_set,'L1')
		# Stage 2 will be unlocked when stage 2 is made		
		t2 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 2', pos = (-.3, .5), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(-.3,0,.2),self.__game.clean_and_set,'L2')
		
		t3 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 3', pos = (.3, .5), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(.3,0,.2),self.__game.clean_and_set,'L3')
		
		t4 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 4', pos = (.9, .5), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(.9,0,.2),self.__game.clean_and_set,'L4')
		
		t5 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 5', pos = (-.9, -.1), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(-.9,0,-.4),self.__game.clean_and_set,'L5')
		
		t6 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 6', pos = (-.3, -.1), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(-.3,0,-.4),self.__game.clean_and_set,'L6')
		
		t7 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 7', pos = (.3, -.1), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(.3,0,-.4),self.__game.clean_and_set,'L7')
			
		t8 = OnscreenText(parent=self.stage_select_frame, text = 'STAGE 8', pos = (.9, -.1), scale = 0.07,fg=(0,.2,.2,1))
		self.create_stage_button(self.stage_select_frame,'img/locked.jpg','',LVecBase3f(.9,0,-.4),self.__game.clean_and_set,'L8')
		
		if button is True:		
			# Create button to go back to main menu
			self.create_menu_button(self.stage_select_frame,'Back',LVecBase3f(0,0,-.8),self.show_menu)
		
		# Hide frame
		self.stage_select_frame.hide()

	
	'''
	    Creates leaderboard selection frame which will contain links to the leaderboard for the different game stages. This frame is hidden.
	'''
	def create_leaderboard_selector(self):
		# Direct frame to hold links to the leaderboards for different levels
		self.leaderboard_selection_frame = DirectFrame(parent=self.main_frame,frameColor = (.8,.8,.8,.9),frameSize=(-2,2,-1,1), pos=(0,0,0))

		# Frame title
		title = OnscreenText(parent=self.leaderboard_selection_frame, text = 'LEADERBOARD SELECTION', pos = (0, .6), scale = 0.15, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1))
		
		# Links to leaderboards for the stages that are currently made
		self.link(self.leaderboard_selection_frame,'STAGE 1',LVecBase3f(0,0,.0),self.show_leaderboard,'L1')
		self.link(self.leaderboard_selection_frame,'STAGE 2',LVecBase3f(0,0,-.1),self.show_leaderboard,'L2')
		
		# Create button to go back to main menu
		self.create_menu_button(self.leaderboard_selection_frame,'Back',LVecBase3f(0,0,-.4),self.show_menu)

		# Hide frame 
		self.leaderboard_selection_frame.hide()

	'''
	    Leaderboard is created based on the level that was clicked on the leaderboard selector frame. This information is gathered from the stored information in
	    .leaderboard.txt. This method will look for the correct section in the file and output the information for the stage choosen onto a direct frame.
	'''
	def create_leaderboard(self,level):
		# Direct frame to hold all contents of the leaderboard
		self.leaderboard_frame = DirectFrame(parent=self.main_frame,frameColor = (.8,.8,.8,.9),frameSize=(-2,2,-1,1), pos=(0,0,0))

		# Create a scroll_frame to hold contents of leaderboard file
		scroll_frame = DirectScrolledFrame(parent = self.leaderboard_frame,
						   canvasSize=(-1,1,-4,4),
					           frameColor = (1,1,1,.9),
						   frameSize=(-1,1,-.5,.5), 
						   pos=(0,0,0),
						   manageScrollBars=True,
						   scrollBarWidth = .04, 
					           autoHideScrollBars = True)

		# Frame title
		title = OnscreenText(parent=self.leaderboard_frame, text = 'LEADERBOARD', pos = (0, .6), scale = 0.15, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1))
		
		# Open .leaderboard.txt file as read only
		leaderboard_file = open('files/.leaderboard.txt','r')
		start_read = False					# Boolean that will used to notify loop when to start generating text on the scroll canvas
		start = leaderboard_file.read(1)			# Reads only the first byte of the file, equivalent to a character

		# Guide for leaderboard
		name = OnscreenText(parent=scroll_frame.getCanvas(), text = 'NAME', pos = (-.1, 3.9), scale = 0.075,fg=(0,.2,.2,1))
		score = OnscreenText(parent=scroll_frame.getCanvas(), text = 'SCORE', pos = (.5, 3.9), scale = 0.075,fg=(0,.2,.2,1))
		
		index = 1
		v_pos = 3.8

		# Loop will iterate through the contents of the file
		while len(start) != 0:
			if start == '#': leaderboard_file.readline()			# Comments in text file start with an octothorpe and are ignored
			elif start == '@'and start_read is False:			# Line with @ signify the beginning of a set of level info
				if leaderboard_file.readline().split()[0] == level:	# This checks if the info that follows is the information we need
					start_read = True
			elif start == '@'and start_read is True:			# If this condition is true then we read through all the information we need
				break
			elif start_read is True:
				coord = leaderboard_file.readline().split(',')
				name = start + coord[0]					# Name of user
				score = coord[1]					# User score
				entry_text = str(index) + ".\t " + name + '\t\t' + score
				# Create onscreen text for each entry
				entry = OnscreenText(parent=scroll_frame.getCanvas(), text = entry_text, pos = (0,v_pos), scale = 0.07,fg=(0,0,0,1))
				# Increase index and decrease vertical position
				index += 1
				v_pos -= .1
			# Read the first byte of the next line
			start = leaderboard_file.read(1)

		leaderboard_file.close()

		# Create button to go back to the leaderboard selection frame
		self.create_menu_button(self.leaderboard_frame,'Back',LVecBase3f(0,0,-.7),self.show_lb_selection)

		# Hide frame
		self.leaderboard_frame.hide()
	
	'''
	    Creates a frame in the top of the window that shows player health and timer. Frame is hidden.
	'''
	def create_health_bar(self):
		# Direct frame that holds all contents such as timer and health bar
		self.health_frame = DirectFrame(parent=self.main_frame,frameColor=(0, 0, 0, .4),frameSize=(-2, 3, -.1, 1),pos=(-.6, 0, .9))
		
		# Create a direct wait bar that will be used as the health gauge.
		self.bar = DirectWaitBar(parent=self.health_frame,
					 text = "HEALTH",
					 text_fg=(1,1,1,1), 
					 value = 100, 
					 range=100, 
					 pos = (.15,0,-.02),
					 barColor=VBase4(0,.2,.2,1),
					 scale=.6)

		# Onscreen image for eve face icon on health gauge
		eve_icon = OnscreenImage(parent=self.bar,image = 'img/eve_face.png', pos = (-1.15, 0, -.075), scale = (.25,1,.25))
		eve_icon.setTransparency(TransparencyAttrib.MAlpha)
		
		# Create a node for timer
		timer_txt = str(OnScreenInterface.LEVEL_1_TIME[0]) + ' min ' + str(OnScreenInterface.LEVEL_1_TIME[1]) + ' seconds'
		self.timer = OnscreenText(parent=self.health_frame, text = timer_txt, pos = (1.5, -.02), scale = 0.07, fg=(1,1,1,1))

		# Hide frame
		self.health_frame.hide()
	
	'''
	    Creates an a token counter in the right bottom corner of screen. This image is hidden.
	'''
	def create_token_counter(self):
		# Set onscreen image and set transparency
		self.shape = OnscreenImage(image = 'img/tire_score.png', pos = (1, 0, -.85), scale = (.3,1,.1))
		self.shape.setTransparency(TransparencyAttrib.MAlpha)
		
		# Set another onscreen image and set transparency
		tire = OnscreenImage(parent=self.shape,image = 'img/tire.png', pos = (-1, 0, 0), scale = (.4,1,1))
		tire.setTransparency(TransparencyAttrib.MAlpha)

		# Set text displaying the number of token collected
		self.score = OnscreenText(parent=self.shape, text = str(self.__game.eve.tiresCollected), pos = (0, -.1), scale = (.3,.8), fg=(255,255,255,1))

		# Hide token counter
		self.shape.hide()

	'''
	    Creates a frame that displays the name of the stage at the beginning of every stage in the game. Only level 1 and 2 are set.
	'''
	def create_stage_title(self,level):
		s_text = ""
		t_text = ""

		# The following if statement set the text that will be displayed
		if level == 'L1':
			s_text = "Stage 1:"
			t_text = "The Journey Begins"
		elif level == 'L2':
			s_text = "Stage 2:"
			t_text = "The Dark Place"
		
		# Direct frame to hold stage title
		self.stage_frame = DirectFrame(parent=self.main_frame,frameColor=(0, 0, 0, .6),frameSize=(-2, 3, -.1, .4),pos=(0, 0, 0))
		
		stage_name = OnscreenText(parent=self.stage_frame, text = s_text, pos = (0, .2), scale = 0.16, fg=(1,.84,0,1),shadow=(1,1,1,.2))
		stage_title = OnscreenText(parent=self.stage_frame, text = t_text, pos = (0, 0), scale = 0.12, fg=(1,.84,0,1),shadow=(1,1,1,.2))

	'''
	    Creates onscreen text showing current position of the character
	'''
	def create_coordinate_view(self):
		self.coord = OnscreenText(parent=self.main_frame,text='1', style = 1, fg= (1,1,1,1),  pos=(0,-0.95), align=TextNode.A_right, scale=0.08)
		self.coord.hide()

	#------------------------------------------------------------------------- SHOW METHODS -----------------------------------------------------------------#

	'''
	    Shows input frame so user can enter his/her name. 	
	'''	
	def show_input(self):
		self.__game.accept('h', self.do_nothing)
		self.start_frame.destroy()
		self.input_frame.show()	
	
	'''
	    Shows menu frame and hides anything else that may be showing	
	'''
	def show_menu(self):
		if self.control_frame.isHidden() is False:
			self.control_frame.hide()
		elif self.leaderboard_selection_frame.isHidden() is False:
			self.leaderboard_selection_frame.hide()
		elif self.stage_select_frame.isHidden() is False:
			self.stage_select_frame.hide()
		self.__game.accept('h', self.toggleHelp)
		self.help_frame.show()
	
	'''
	    Shows frame that contains the game instructions
	'''
	def show_controls(self):
		self.__game.accept('h', self.do_nothing)
		self.help_frame.hide()
		self.control_frame.show()

	'''
	    Shows stage select frame
	'''
	def show_level_select(self):
		self.__game.accept('h', self.do_nothing)
		self.help_frame.hide()
		self.stage_select_frame.show()

	'''
	    Shows leaderboard selector frame
	'''
	def show_lb_selection(self):
		if self.leaderboard_frame.isHidden() is False:
			self.leaderboard_frame.hide()
		elif self.help_frame.isHidden() is False:
			self.__game.accept('h', self.do_nothing)
			self.help_frame.hide()
		self.leaderboard_selection_frame.show()
	
	'''
	    Shows leaderboard frame for a specific level
	    @param level - stage whose leaderboard will be displayed
	'''
	def show_leaderboard(self,level):
		self.leaderboard_selection_frame.hide()
		self.create_leaderboard(level)
		self.leaderboard_frame.show()

	'''
	    Shows in game stats, which is health gauge, timer and token counter
	'''
	def show_game_interface(self):
		self.health_frame.show()
		self.shape.show()

	'''
	    Hides the game interface. This is used when the help menu us shown.
	'''
	def hide_game_interface(self):
		self.health_frame.hide()
		self.shape.hide()


	#------------------------------------------------------------------------- CREATE BTN METHODS -----------------------------------------------------------------#

	'''
	    Creates a button with an= simple button image as the background. This is the default btn.
	    @param parent - who the button will be parented to
	    @param btn_text - text that will be displayed on button
	    @param btn_pos - position of the button
	    @param cmd - command that will be executed when button is clicked
	    @param level - each link created is based on a stage, this is the stage this btn represents
	'''
	def create_menu_button(self,parent,btn_text,btn_pos,cmd):
		start_btn = DirectButton(parent=parent,
					 text=btn_text,
					 pos=btn_pos,
					 scale=(.2,1,.15),
					 command=cmd,
					 pressEffect=1,
					 text_scale=(.4,.4),
					 text_pos=(.1,.1),
					 text_fg=(.1,.1,.1,1),
					 text_shadow=(1,1,1,1),
					 image='img/btn2.png',
					 image_scale=(2.50,1,.7),
					 image_pos=(0,1,.25),
					 relief=None,
					 rolloverSound = self.hover,
					 clickSound=self.click)
		start_btn.setTransparency(TransparencyAttrib.MAlpha)

	'''
	    Creates a button that contains an image of a stage or if it was not yet created it contains an image of a lock
	    @param parent - who the button will be parented to
	    @param btn_text - text that will be displayed on button
	    @param btn_pos - position of the button
	    @param cmd - command that will be executed when button is clicked
	    @param level - each link created is based on a stage, this is the stage this btn represents
	'''
	def create_stage_button(self,parent,img,btn_text,btn_pos,cmd,level):

		click_sound = self.blocked
		hover_sound = self.blocked
		
		# This if statement sets the sound that each button will have. 
		# Everything that is not level 1 or level 2 will have the blocked sound effect and will do nothing
		if level == 'L1' or level == 'L2':
			click_sound = self.click
			hover_sound = self.hover

		btn = DirectButton(parent=parent,
					 text=btn_text,
					 pos=btn_pos,
					 scale=(.2,1,.15),
					 command=cmd,
					 pressEffect=1,
					 text_scale=(.4,.4),
					 text_pos=(.1,.1),
					 text_fg=(.1,.1,.1,1),
					 text_shadow=(1,1,1,1),
					 image=img,
					 image_scale=(1,1,1),
					 image_pos=(0,1,.25),
					 relief=None,
					 rolloverSound = hover_sound,
					 clickSound=click_sound,
					 extraArgs=[level])
		btn.setTransparency(TransparencyAttrib.MAlpha)

	'''
	    Creates a button with no relief and no background image or color.
	    @param parent - who the button will be parented to
	    @param btn_text - text that will be displayed on button
	    @param btn_pos - position of the button
	    @param cmd - command that will be executed when button is clicked
	    @param level - each link created is based on a stage, this is the stage this btn represents
	'''
	def link(self,parent,btn_text,btn_pos,cmd,level):
		btn = DirectButton(parent=parent,
					 text=btn_text,
					 pos=btn_pos,
					 scale=(.2,1,.15),
					 command=cmd,
					 pressEffect=1,
					 text_scale=(.4,.4),
					 text_pos=(.1,.1),
					 text_fg=(.1,.1,.1,1),
					 relief=None,
					 rolloverSound = self.hover,
					 clickSound=self.click,
					 extraArgs = [level])


	#------------------------------------------------------------------------- TASK METHODS -----------------------------------------------------------------#
	
	'''
	    At the beginning of every stage the title is show. This task only runs for the first 2 seconds of each stage. It shows
	    the stage title for 2 seconds and then destroys the frame containing the title and the task ends.
	'''	
	def show_title(self,task):
		if globalClock.getRealTime() - self.__game.actual_start > 2:	# Wait two seconds
			self.stage_frame.destroy()
			self.show_game_interface()
			self.__game.eve.enable_character_controls()		# Enable character controls only after the two seconds have passed
			self.__game.accept('h', self.toggleHelp)
			self.__game.accept('f1', self.__game.toggleDebug)
			return Task.done
		return Task.cont
	
	'''
	    This task runs continuously throughout each stage. It updates the time remaining in the current level.
	    This task ends when the minutes and seconds reach 0.
	'''
	def update_timer(self,task):
		elapsed_time = globalClock.getRealTime() - self.__game.actual_start
		change_time = int(elapsed_time) % 60
		if change_time == 0:
			self.min = self.level_time[0] - int(elapsed_time) / 60
			self.sec = 59
		else:
			if self.previous != int(elapsed_time):
				self.sec = 59 - change_time 
	
		self.timer['text'] = str(self.min) + ' min ' + str(self.sec) + ' seconds'
		self.previous = int(elapsed_time)
		if self.min == 0 and self.sec == 0:
			return Task.done
		return Task.cont 

	'''
	    In debug mode the user can view the players current position in the left bottom corner. This task
	    takes care of updating that position onscreen text.
	'''
	def updateCoord(self, task):
        	x = self.__game.eve.currentNP.getX()
       		y = self.__game.eve.currentNP.getY()
        	z = self.__game.eve.currentNP.getZ()
        	self.coord.setText(str(x) + " , " + (str(y)) + " , "  + str(z))
        	return Task.cont

	'''
	    After user inputs his/her name in the beginning of the game, this method is execute and a new user is instantiated and the game is setup.
	    Aside from this two things are added to the task manager...the timer and the stage title.
	'''
	def set_player(self,entry):
		print '\tWELCOME ' + entry + ' ...'
		print '\tSETTING UP USER ...'
		self.input_frame.destroy()				# Destroy the input frame
		self.__game.user = User(entry)		# Frame title

		self.stage_select_frame.show()

		#self.__game.setup('L1')
		#self.create_leaderboard(self.__game.current_level)
		#self.__game.taskMgr.add(self.show_title,'Title')
		#self.__game.taskMgr.add(self.update_timer,'Timer')
		# The code below was used for testing purposes to add the user to the leaderboard file
		#self.game.user.add_to_leaderboard(self.game.current_level)
	
	'''
	   Method used to toggle between the help menu and the game.
	'''
	def toggleHelp(self):
		if self.help_frame.isHidden():
			# Stop update task and disable character controls when help is activated
			self.pause.play()
			self.__game.taskMgr.remove('update')
			self.hide_game_interface()
			self.__game.eve.disable_character_controls()
			self.help_frame.show()
		else:
			# Restart update task and enable character controls when help is deactivated
			self.pause.play()
			self.__game.taskMgr.add(self.__game.update,'update')            # Add task to task manager
			self.show_game_interface()
			self.__game.eve.enable_character_controls()
			self.help_frame.hide()
	
	'''
	    Method does nothing but is important to stop the h key from working when help menu is in a sub menu or frame
	'''
	def do_nothing(self):
		pass



	
		
	
