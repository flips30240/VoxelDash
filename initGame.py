##############################################
#                 #IMPORT#                   #
##############################################
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
import math
from direct.gui.OnscreenImage import OnscreenImage
import os
##############################################
#              #BULLET IMPORT#               #
##############################################
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
##############################################
#         #External Class IMPORT#            #
##############################################
from GameLight import *
from Player import *
from ControlHandler import *
from Level import *
from gameCamera import *
from SkyBox import *
from KeepTime import *
from LevelParser import *
from pCollisions import *
from ScoreHandler import *
from StoryParser import *
from Music import *
from LevelSelection import *
##############################################
#              #NEW CLASS#                   #
##############################################


class initGame():

    def __init__(self, windowProps, user, connection):
        self.user = user
        self.connection = connection
        render.setShaderAuto()

        self.wp = windowProps
        # keeps the game running the same on all systems (kinda sorta barely)#
        FPS = 60
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(FPS)
        globalClock.setMaxDt(1)

        self.world = BulletWorld()
        self.fakeNode = render.attachNewNode("fakeNode")

        self.initFakeGui()
        self.playIntroLevelMusic()
        self.initBullet()
        self.initScore()
        self.initCollisions()
        self.loadPlayer()
        self.createCamera(self.player.np)
        self.parseLevelFile("Home")
        self.getLevelBounds()
        self.startTime()
        self.createLight()
        self.loadSkyBox()
        self.loadControls()
        #self.parseStory()

        colour = (0.5,0.8,0.8)
        expfog = Fog("Scene-wide exponential Fog object")
        expfog.setColor(*colour)
        expfog.setExpDensity(0.0005)
        render.setFog(expfog)
        base.setBackgroundColor(*colour)

        base.camLens.setFar(1000)

    def playIntroLevelMusic(self):
        self.music = Music("play","./sounds/batfeet.mp3", .1, True)

    def getLevelBounds(self):
        self.levelNodeBounds = render.find("renderDummy").getBounds()

    def parseStory(self):
        self.story = StoryParser("./stories/Story.txt")

    def searchDirectories(self):
        for root, dirs, files in os.walk("./"):
            for name in files:
                if name.endswith((".txt")):
                    print(name)
            for name in dirs:
                if name == "textures":
                    for root, dirs, files in os.walk(name):
                        for name in files:
                            if name.endswith(".jpg"):
                                print(name)
    def initFakeGui(self):
        self.menuBar = OnscreenImage(image = './graphics/MenuBar.png', pos = (0,0,-.94))
        self.userText = OnscreenText(text = self.user, pos = (-1.05, -.9625), scale = 0.1)
        self.menuBar.setScale(1.625, 1, .0625)

    def initScore(self):
        self.scoreHandler = ScoreHandler()

    def initCollisions(self):
        self.collisions = pCollisions(self.scoreHandler, self.music)

    def parseLevelFile(self, arg):
        if arg == "Home":
            self.parsedLevel = LevelParser("./levels/HomeLevel.txt", self.collisions, self.player.np, self.world, self.scoreHandler)

    def startTime(self):
        self.time = KeepTime()

    def initBullet(self):
        self.world.setGravity(Vec3(0, 0, -9.81))

        self.debugNode = BulletDebugNode('Debug')
        self.debugNode.showWireframe(True)
        self.debugNode.showConstraints(True)
        self.debugNode.showBoundingBoxes(False)
        self.debugNode.showNormals(False)

        self.debugNP = render.attachNewNode(self.debugNode)
        self.world.setDebugNode(self.debugNP.node())

    def loadSkyBox(self):
        self.skyBox = SkyBox("Box")

    def createCamera(self, nodePath):
        self.camera = gameCamera(nodePath, self.world, self.collisions)

    def loadControls(self):
        #args order = bullet update loop, bullet debug node, camera, windowProps, player class, spotLightNode, windowProps, timerTask, bulletWorld, collisions#
        self.controlHandler = ControlHandler(self.update, self.debugNP, self.camera, self.wp, self.player, self.time.timerTask, self.world, self.collisions, self.music)

    def loadPlayer(self):
        self.player = Player(self.collisions, "sphere", self.world, self.music, self.scoreHandler)
        #self.player = Player("sphere", self.world, 0, 0, 16)

    def createLight(self):
        self.lightSource = GameLight(self.player.np)

    def update(self, task):
        ##############################################
        #              #BULLET UPDATE#               #
        ##############################################
        dt = globalClock.getDt()
        #self.dtTimer()
        self.world.doPhysics(dt*2, 7)

        #############################################
        #            #CAMERA UPDATE#                #
        #############################################
        self.camera.cn.setPos(self.player.np.getPos())
        #self.fakeNode.setPos(self.player.np.getPos())
        self.camera.hNode.setPos(self.player.np.getPos())
        self.camera.pNode.setPos(self.player.np.getPos())

        self.camera.cn.setP(self.camera.pNode.getP())
        self.camera.cn.setH(self.camera.hNode.getH())

        pointer = base.win.getPointer(0)
        pointerX = pointer.getX()
        pointerY = pointer.getY()

        if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize ()/2):
            if self.camera.inverted == "yes":
                Pitch = -((pointerY - base.win.getYSize()/2)*.1)
            else:
                Pitch = ((pointerY - base.win.getYSize()/2)*.1)
            Heading = -((pointerX - base.win.getXSize()/2)*.1)

            #endValue = 0
            #endValue += Pitch

            self.camera.pNode.setP(self.camera.pNode, Pitch)
            self.camera.hNode.setH(self.camera.hNode, Heading)

            #self.fakeNode.setH(self.fakeNode, Heading)

        #############################################
        #             #PLAYER UPDATE#               #
        #############################################
        force = Vec3(0, 0, 0)

        if inputState.isSet('up'):
            force.setY(10.0)
        if inputState.isSet('down'):
            force.setY(-10.0)
        if inputState.isSet('left'):
            force.setX(-10.0)
        if inputState.isSet('right'):
            force.setX(10.0)

        #force *= 10
        force = render.getRelativeVector(self.camera.cn, force)

        self.player.np.node().setActive(True)
        self.player.np.node().applyCentralForce(force)
        #self.player.np.setColor(random.random(), random.random(), random.random(), random.random())

        if self.player.np.getZ() < 0 - (self.levelNodeBounds.getRadius() * 6):
            self.player.np.setPos(self.collisions.level.spawn)
            self.player.np.node().setLinearVelocity(Vec3(0,0,0))

        return task.cont
