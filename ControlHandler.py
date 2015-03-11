##############################################
#                 #IMPORT#                   #
##############################################
from pandac.PandaModules import Mat4
from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
##############################################
#         #External Class IMPORT#            #
##############################################
from Menu import *
from Filters import *
#from LevelEditor import *
from LevelParser import *
##############################################
#           #NEW CLASS#                      #
##############################################


class ControlHandler():
    fsmState = True


    def __init__(self, update, bulletDebugNode, camera, windowProps, player, timerTask, bulletWorld, collisions, music):
        #args
        self.update = update
        self.debugNP = bulletDebugNode
        self.camera = camera
        self.music = music
        #self.cameraTask = camera.thisTask - ill need some camera shit later prolly
        self.wp = windowProps
        self.player = player
        #self.level = level
        self.timerTask = timerTask
        self.world = bulletWorld
        self.collisions = collisions
        self.filters = Filters()

        self.frustumIsEnabled = False

        self.parseControlFile()
        self.createControls()
        self.singleSM(self.pauseGame, self.resumeGame)
        base.messenger.send("1")

    def parseControlFile(self):
        self.f = open("./controls/ControlsFileConfig.txt")
        self.lines = self.f.readlines()
        self.f.close()

        #validLetters = "abcdefghijklmnopqrstuvwxyz"

        #for x in range(len(self.lines)):
         #   for char in self.lines[x]:
          #      for char in validLetters:
           #         self.lines[x] += char

                    #gotta figure out how aND WHY THE NEWLINES ARENT GOIGN AWAY!

        print(self.lines)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "forward":
                self.forward = str(self.lines[x + 1].rstrip("\n"))

            if self.lines[x].strip() == "reverse":
                self.reverse = str(self.lines[x + 1].rstrip("\n"))

            if self.lines[x].strip() == "left":
                self.left = str(self.lines[x + 1].rstrip("\n"))

            if self.lines[x].strip() == "right":
                self.right = str(self.lines[x + 1].rstrip("\n"))

    def singleSM(self, onFunction, offFunction):
        '''"Single State Machine"
        Takes two methods as args, runs onFunction
        when self.fsmState = False(Default state),
        runs offFunction when self.fsmState = True'''
        if self.fsmState:
            self.fsmState = False
            offFunction()
        else:
            self.fsmState = True
            onFunction()

    def escMenu(self):
        '''Runs functions when escape is pressed'''
        self.singleSM(self.pauseGame, self.resumeGame)

    def pauseGame(self):
        '''Pauses the game by removing any taskmgr'''
        self.wp.setCursorHidden(False)
        base.win.requestProperties(self.wp)

        mat = Mat4(camera.getMat())
        mat.invertInPlace()
        base.mouseInterfaceNode.setMat(mat)
        base.enableMouse()

        self.menu = Menu(self.escMenu, self.wp, self.collisions)
        taskMgr.remove('update')
        taskMgr.remove('timerTask')
        self.menu.loadPauseMenu()

    def resumeGame(self):
        self.wp.setCursorHidden(True)
        base.win.requestProperties(self.wp)
        try:
            self.menu.destroyAllMenus("meh")
        except AttributeError:
            print("Nothing to destroy!")
        taskMgr.add(self.update, 'update')
        taskMgr.add(self.timerTask, 'timerTask')
        base.disableMouse()

    def debugBullet(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def createControls(self):
        #Sets up the controls
        inputState.watchWithModifiers('up', self.forward)
        inputState.watchWithModifiers('left', self.left)
        inputState.watchWithModifiers('down', self.reverse)
        inputState.watchWithModifiers('right', self.right)
        inputState.watchWithModifiers('up-up', self.forward + '-up')
        inputState.watchWithModifiers('left-up', self.left + '-up')
        inputState.watchWithModifiers('down-up', self.reverse + '-up')
        inputState.watchWithModifiers('right-up', self.right + '-up')

        base.accept("escape", self.escMenu)
        base.accept("f1", self.debugBullet)
        base.accept("space", self.player.jump)
        base.accept("mouse1", self.player.newShoot)
        base.accept("1", self.filters.enableFilters, extraArgs = [self.player.np])
        #base.accept("3", self.level.flattenLevel)
        #base.accept("4", self.edit)
        #base.accept("5", self.removeLevel)

    #def removeLevel(self):
     #   self.level.renderDummy.removeNode()
      #  for i in range(self.world.getNumRigidBodies()):
       #     if i < self.world.getNumRigidBodies() and self.world.getRigidBody(i) != self.player.playerBulletNode and self.world.getRigidBody(i) != self.level.BPnode:
        #        node = self.world.getRigidBody(i)
         #       self.world.removeRigidBody(node)

        #self.levelLoadEntry = DirectEntry(text="", scale=.05, command=self.loadLevel, initialText="Enter Name of Level To Load", numLines=1, focus=1)
        #self.levelLoadEntry.setPos(-.225, 0, 0.2)

    #def loadLevel(self, arg):
     #   self.level = LevelParser(str(arg), self.collisions, self.player.np, self.world, True)
      #  self.levelLoadEntry.destroy()

    #def edit(self):
     #   self.LevelNameEntry = DirectEntry(text="", scale=.05, command=self.initLevelEditor, initialText="Enter Level Name", numLines=1, focus=1)
      #  self.LevelNameEntry.setPos(-.225, 0, 0.2)

    #def initLevelEditor(self, arg):
     #   self.LevelNameEntry.destroy()
      #  foo = open(str(arg) + '.txt', 'w')
       # self.levelEdit = LevelEditor(foo)
