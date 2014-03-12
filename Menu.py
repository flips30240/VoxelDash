##############################################
#              #NEW CLASS#                   #
##############################################
from direct.gui.DirectGui import *
import sys


class Menu():

    def __init__(self, escMenu, wp, arg = False):
        self.collisions = arg
        self.wp = wp
        self.escMenu = escMenu
        print('this is lonely')

    def loadPauseMenu(self):
        print("loaded! Pause menu")

        self.backFrame = DirectFrame()
        self.backFrame['frameColor'] = (0, 0, 0, .5)
        self.backFrame['frameSize'] = (2, -2, 2, -2)
        self.backFrame.setPos(0, 0, 0)

        self.menuFrame = DirectFrame()
        self.menuFrame.reparentTo(self.backFrame)
        self.menuFrame['frameColor'] = (1, 1, 1, .5)
        self.menuFrame['frameSize'] = (1, -1, .25, -.25)
        self.menuFrame.setPos(0, 0, .75)

        self.resumeButton = DirectButton()
        self.resumeButton.reparentTo(self.menuFrame)
        self.resumeButton['text'] = ('Resume')
        self.resumeButton['text_scale'] = (.1)
        self.resumeButton['text_pos'] = (0, -0.03)
        self.resumeButton['frameVisibleScale'] = (2, 0.5, 0)
        self.resumeButton['frameColor'] = (1, 1, 1, 0)
        self.resumeButton['command'] = (self.escMenu)
        self.resumeButton.setPos(-.5, 0, 0)

        self.HomeButton = DirectButton()
        self.HomeButton.reparentTo(self.menuFrame)
        self.HomeButton['text'] = ('Return to Home!')
        self.HomeButton['text_scale'] = (.1)
        self.HomeButton['text_pos'] = (0, -0.03)
        self.HomeButton['frameVisibleScale'] = (2, 0.5, 0)
        self.HomeButton['frameColor'] = (1, 1, 1, 0)
        self.HomeButton['command'] = (self.loadHome)
        self.HomeButton.setPos(0, 0, -.2)

        self.exitButton = DirectButton()
        self.exitButton.reparentTo(self.menuFrame)
        self.exitButton['text'] = ('Exit')
        self.exitButton['text_scale'] = (.1)
        self.exitButton['text_pos'] = (0, -0.03)
        self.exitButton['frameVisibleScale'] = (2, 0.5, 0)
        self.exitButton['frameColor'] = (1, 1, 1, 0)
        self.exitButton['command'] = (self.exit)
        self.exitButton.setPos(.5, 0, 0)

        self.pauseText = OnscreenText()
        self.pauseText['text'] = ('PAUSED')
        self.pauseText['scale'] = (.1)
        self.pauseText['fg'] = (1, 1, 1, 1)
        self.pauseText.setPos(0, .9)

    def loadHome(self):
        print("Go Home Your Drunk!")
        self.collisions.loadLevel("HomeLevel")

    def destroyAllMenus(self, arg):
        print("destroyinf Menu")

        if arg == str("pauseMenu"):
            self.backFrame.destroy()
            self.menuFrame.destroy()
            self.pauseText.destroy()
            self.loadPauseMenu()
        else:
            self.pauseText.destroy()
            self.backFrame.destroy()
            self.menuFrame.destroy()
            self.resumeButton.destroy()
            self.HomeButton.destroy()

    def exit(self):
        sys.exit()
