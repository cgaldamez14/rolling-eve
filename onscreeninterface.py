from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame,DGG

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import TextNode,VBase4,Vec4,LVecBase3f,TransparencyAttrib

from direct.interval.IntervalGlobal import *

from direct.task import Task

class OnScreenInterface():
	
	def __init__(self,eve,game):
		self.pc = eve
		self.game = game
		self.main_frame = DirectFrame(frameColor = (0,0,0,0),frameSize=(-2,2,-1,1), pos=(0,0,0))
		self.hover = base.loader.loadSfx("sfx/hover.mp3")
		self.click = base.loader.loadSfx("sfx/click.wav")
		self.pause = base.loader.loadSfx("sfx/pause.wav")
		self.intro = base.loader.loadMusic("sfx/not_seems.mp3")
		self.hover.setPlayRate(5)
		self.hover.setVolume(.05)
		self.intro.setVolume(.5)
		self.intro.setLoop(True)

	def load_interface(self):
		self.create_start()
		self.create_health_bar()
		self.create_token_counter()
		self.set_coordinate_view()	
		self.create_help_menu()
		self.create_control_guide()

	def create_start(self):
		self.start_frame = DirectFrame(parent = self.main_frame,frameColor = (.05,0,.05,1),frameSize=(-2,2,-1,1), pos=(0,0,0))
		kyklops1 = OnscreenImage(parent=self.start_frame,image = 'kyklops.png', pos = (.9, 0, .3), scale = (.3,0,.3))
		kyklops1.setTransparency(TransparencyAttrib.MAlpha)
		title = OnscreenImage(parent=self.start_frame,image = 'title.png', pos = (0, 0, 0), scale = (.8,0,.3))
		title.setTransparency(TransparencyAttrib.MAlpha)
		rolling_eve = OnscreenImage(parent=self.start_frame,image = 'rolling-eve.png', pos = (-.95, 0, -.1), scale = (.5,0,.5))
		rolling_eve.setTransparency(TransparencyAttrib.MAlpha)
		start_btn = DirectButton(parent=self.start_frame,
					 text="START",
					 pos=LVecBase3f(0,0,-.5),
					 scale=.2,
					 command=self.game.setup,
					 pressEffect=1,
					 text_scale=(.45,.45),
					 text_pos=(.1,.1),
					 text_fg=(.1,.1,.1,1),
					 text_shadow=(1,1,1,1),
					 image='btn.png',
					 image_scale=(2,0,.7),
					 image_pos=(0,0,.25),
					 relief=None,
					 rolloverSound = self.hover,
					 clickSound=self.click)
		self.intro.play()



	def create_health_bar(self):
		self.health_frame = DirectFrame(parent=self.main_frame,frameColor=(0, 0, 0, .4),frameSize=(-2, 3, -.1, 1),pos=(-.6, 0, .9))
		self.bar = DirectWaitBar(parent=self.health_frame,text = "HEALTH", value = 100, range=100, pos = (.15,0,-.02))
		self.bar['barColor'] = VBase4(0,.2,.2,1)
		self.bar.setScale(self.bar, .6)
		eve_icon = OnscreenImage(parent=self.bar,image = 'eve_face.png', pos = (-1.15, 0, -.075), scale = (.25,0,.25))
		eve_icon.setTransparency(TransparencyAttrib.MAlpha)
		self.health_frame.hide()

	def create_token_counter(self):
		self.shape = OnscreenImage(image = 'tire_score.png', pos = (1, 0, -.85), scale = (.3,0,.1))
		self.shape.setTransparency(TransparencyAttrib.MAlpha)
		self.tire = OnscreenImage(parent=self.shape,image = 'tire.png', pos = (-1, 0, 0), scale = (.4,1,1))
		self.tire.setTransparency(TransparencyAttrib.MAlpha)
		self.score = OnscreenText(parent=self.shape, text = str(self.pc.tiresCollected), pos = (0, -.1), scale = (.3,.8), fg=(255,255,255,1))
		self.shape.hide()

	def show_game_interface(self):
		self.health_frame.show()
		self.shape.show()

	def hide_game_interface(self):
		self.health_frame.hide()
		self.shape.hide()
	
	def create_menu_button(self,parent,btn_text,btn_pos,cmd):
		start_btn = DirectButton(parent=parent,
					 text=btn_text,
					 pos=btn_pos,
					 scale=(.2,0,.15),
					 command=cmd,
					 pressEffect=1,
					 text_scale=(.4,.4),
					 text_pos=(.1,.1),
					 text_fg=(.1,.1,.1,1),
					 text_shadow=(1,1,1,1),
					 image='btn2.png',
					 image_scale=(2.50,0,.7),
					 image_pos=(0,0,.25),
					 relief=None,
					 rolloverSound = self.hover,
					 clickSound=self.click)
		start_btn.setTransparency(TransparencyAttrib.MAlpha)

	def create_help_menu(self):
		self.help_frame = DirectFrame(parent=self.main_frame,frameColor = (.6,.6,.6,.7),frameSize=(-2,2,-1,1), pos=(0,0,0))
		title = OnscreenText(parent=self.help_frame, text = 'MENU', pos = (0, .4), scale = 0.2, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1) )
		self.create_menu_button(self.help_frame,'Controls',LVecBase3f(0,0,.1),self.show_controls)
		self.create_menu_button(self.help_frame,'Level Select',LVecBase3f(0,0,-.1),self.show_controls)
		self.create_menu_button(self.help_frame,'Leaderboard',LVecBase3f(0,0,-.3),self.show_controls)
		self.create_menu_button(self.help_frame,'Quit',LVecBase3f(0,0,-.5),self.show_controls)

		self.help_frame.hide()

	def create_control_guide(self):
		self.control_frame = DirectFrame(frameColor = (.9,.9,.9,.9),frameSize=(-2,2,-1,1), pos=(0,0,0))
		textObject1 = OnscreenText(parent=self.control_frame, text = 'CONTROL KEYS', pos = (0, .5), scale = 0.1, fg=(0,.2,.2,1),shadow=(.5,.5,.5,1))
		textObject1 = OnscreenText(parent=self.control_frame, text = '[w] - Forward', pos = (0, .2), scale = 0.07, fg=(0,0,0,1))
		textObject2 = OnscreenText(parent=self.control_frame, text = '[a] - Left', pos = (0, .1), scale = 0.07,fg=(0,0,0,1))
		textObject3 = OnscreenText(parent=self.control_frame, text = '[d] - Right', pos = (0, 0), scale = 0.07,fg=(0,0,0,1))
		textObject4 = OnscreenText(parent=self.control_frame, text = '[space] - Jump', pos = (0, -.1), scale = 0.07,fg=(0,0,0,1))
		textObject5 = OnscreenText(parent=self.control_frame, text = '[1] - Change character mode', pos = (0, -.2), scale = 0.07,fg=(0,0,0,1))
		textObject6 = OnscreenText(parent=self.control_frame, text = '[h] - Help Menu', pos = (0, -.3), scale = 0.07,fg=(0,0,0,1))
		self.create_menu_button(self.control_frame,'Back',LVecBase3f(0,0,-.7),self.show_menu)
		self.control_frame.hide()

	def show_menu(self):
		if self.control_frame.isHidden() is False:
			self.control_frame.hide()
		self.help_frame.show()

	def show_controls(self):
		self.help_frame.hide()
		self.control_frame.show()
		

	def toggleHelp(self):
		if self.help_frame.isHidden():
			self.pause.play()
			self.game.taskMgr.remove('update')
			self.hide_game_interface()
			self.help_frame.show()
		else:
			self.pause.play()
			self.game.taskMgr.add(self.game.update,'update')            # Add task to task manager
			self.show_game_interface()
			self.help_frame.hide()

	def set_coordinate_view(self):
		self.coord = OnscreenText(parent=self.main_frame,text='1', style = 1, fg= (1,1,1,1),  pos=(0,-0.95), align=TextNode.A_right, scale=0.08)
		self.coord.hide()

	def updateCoord(self, task):
        	x = self.game.eve.currentNP.getX()
       		y = self.game.eve.currentNP.getY()
        	z = self.game.eve.currentNP.getZ()
        	self.coord.setText(str(x) + " , " + (str(y)) + " , "  + str(z))
        	return Task.cont
	
