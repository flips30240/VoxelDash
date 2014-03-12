##############################################
#                 #IMPORT#                   #
##############################################
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
import sys
##############################################
#        #External Class IMPORT#             #
##############################################
from ControlSetter import *
##############################################
#              #NEW CLASS#                   #
##############################################d
#make full screen
loadPrcFileData("", "fullscreen f")
#loadPrcFileData("", "sync-video #f")
loadPrcFileData("", 'show-frame-rate-meter #t')

#get rid of any variable passing between classes of nodes, you can just find them from render >.<


class maine(ShowBase):

    def __init__(self, user, connection):
        self.user = user
        self.connection = connection
        print("Maine!")
        self.begin()

    def begin(self):
        ShowBase.__init__(self)
        self.wp = WindowProperties()
        base.makeAllPipes()
        pipe = base.pipeList[0]
        self.wp.setSize(pipe.getDisplayWidth() - 60, pipe.getDisplayHeight() - 60)
        self.wp.setOrigin(30, 30)

        #render.explore()

        self.backFrame = DirectFrame()
        self.backFrame['frameColor'] = (0, 0, 0, .5)
        self.backFrame['frameSize'] = (2, -2, 2, -2)
        self.backFrame.setPos(0, 0, 0)

        self.menuFrame = DirectFrame()
        self.menuFrame.reparentTo(self.backFrame)
        self.menuFrame['frameColor'] = (1, 1, 1, .5)
        self.menuFrame['frameSize'] = (.5, -.5, .5, -.5)
        self.menuFrame.setPos(0, 0, 0)

        self.startMenu()

    def startMenu(self):
        self.startButton = DirectButton()
        self.startButton.reparentTo(self.menuFrame)
        self.startButton['text'] = ('Start Game!')
        self.startButton['text_scale'] = (.1)
        self.startButton['text_pos'] = (0, -0.03)
        self.startButton['frameVisibleScale'] = (2, 0.5, 0)
        self.startButton['frameColor'] = (1, 1, 1, 0)
        self.startButton['command'] = (self.beginStartProcess)
        self.startButton.setPos(0, 0, 0.4)

        self.exitButton = DirectButton()
        self.exitButton.reparentTo(self.menuFrame)
        self.exitButton['text'] = ('Exit')
        self.exitButton['text_scale'] = (.1)
        self.exitButton['text_pos'] = (0, -0.03)
        self.exitButton['frameVisibleScale'] = (2, 0.5, 0)
        self.exitButton['frameColor'] = (1, 1, 1, 0)
        self.exitButton['command'] = (self.exit)
        self.exitButton.setPos(0, 0, 0)

    def destroyAllMenus(self, arg):
        print("destroying Menu")

        if arg == str("startMenu"):
            self.backButton.destroy()
            self.startMenu()

        if arg == str("allMenus"):
            self.backFrame.destroy()
            self.menuFrame.destroy()

    def exit(self):
        sys.exit()

    def beginStartProcess(self):
        self.destroyAllMenus("allMenus")
        ControlSetter(self.wp, self.user, self.connection)