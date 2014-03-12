##############################################
#              #IMPORT#                      #
##############################################
from pandac.PandaModules import *
from shapes.shapeGenerator import Cube, Sphere
from pandac.PandaModules import Material
import random
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import *
from panda3d.core import Point3
from direct.interval.IntervalGlobal import *
##############################################
#          #External Class IMPORT#           #
##############################################
from shapes.shapeGenerator import *
##############################################
#           #NEW CLASS#                      #
##############################################


class LevelEditor(DirectObject.DirectObject, object):

    l = 1
    w = 1
    h = 1

    cameraDist = 10

    ForwardSpeed = .3
    BackwardSpeed = .3
    Forward = Vec3(0, 2, 0)
    Stop = Vec3(0, 1, 0)
    Back = Vec3(0, -.5, 0)
    Movement = Stop
    MaxSpeed = 2.5

    def __init__(self, fileName, new = True):

        #base.disableMouse()
        #base.hideMouse()

        self.bool = True


        if new:
            self.levelFile = fileName

            self.initEditor()
            self.initPlayer()
            self.setCamera()
            self.skyBox()
            self.informationText()
            self.controlListener()
            taskMgr.add(self.update, "LevelEditUpdate")

            self.ambientLight()
            self.directionalLight()

        if new == False:
            self.parseFile(fileName)

    def parseFile(self, fileName):
        #self.levelFile = fileName

        self.initEditor()
        self.initPlayer()
        self.setCamera()
        self.skyBox()
        self.informationText()
        self.controlListener()
        taskMgr.add(self.update, "LevelEditUpdate")

        self.ambientLight()
        self.directionalLight()

        self.levelFile = open(fileName)
        self.lines = self.levelFile.readlines()
        self.levelFile.close()

        print(self.lines)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "Platform":
                self.name = str("Platform")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                self.createCube(self.name, self.l, self.w, self.h, self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "MovingPlatform":
                self.name = str("MovingPlatform" + str(x))
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])
                self.Xa = float(self.lines[x + 7])
                self.Ya = float(self.lines[x + 8])
                self.Za = float(self.lines[x + 9])
                self.mass = float(self.lines[x + 10])
                self.speed = float(self.lines[x + 11])
                
                self.createMovingPlatform(self.l, self.w, self.h, self.x, self.y, self.z, self.Xa, self.Ya, self.Za, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "EndGoal":
                self.name = str("EndGoal")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                self.createCube(self.name, self.l, self.w, self.h, self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "HitBox":
                self.name = str("HitBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                self.createCube(self.name, self.l, self.w, self.h, self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LoadLevelBox":
                self.name = str("loadLevelBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                self.createCube(self.name, self.l, self.w, self.h, self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LevelEditBox":
                self.name = str("LevelEditBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                self.createCube(self.name, self.l, self.w, self.h, self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "PlaceEnemy":
                self.name = str("Enemy")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])

                self.placeEnemy(self.x, self.y, self.z, False)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "SetSpawn":
                self.name = str("Spawn")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])

                self.setSpawn(self.x, self.y, self.z, False)

        self.levelFile = open(fileName, "a+")
        self.l = 1
        self.w = 1
        self.h = 1

    def ambientLight(self):
        self.alight = self.myRender.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.myRender.setLight(self.alight)

    def directionalLight(self):
        dlight = DirectionalLight('my dlight')
        dlnp = self.myRender.attachNewNode(dlight)
        self.myRender.setLight(dlnp)

    def informationText(self):
        self.pText = DirectButton()
        self.pText.reparentTo(self.myRender)
        self.pText['text'] = str(self.ghostNode.getPos())
        self.pText['frameVisibleScale'] = (2, 0.5, 0)
        self.pText['frameColor'] = (1, 1, 1, 0)
        self.pText['textMayChange'] = 0
        self.pText.setScale(.25)
        self.pText.setTwoSided(True)

        self.iText = DirectButton()
        self.iText.reparentTo(self.myRender)
        self.iText['text'] = "0: Place Platform\n9: Place HitBox\n8: Place EndGoal\n7: Place Moving Platform\n6: Set Player Spawn\n5: Place Enemy"
        self.iText['frameVisibleScale'] = (2, 0.5, 0)
        self.iText['frameColor'] = (1, 1, 1, 0)
        self.iText['textMayChange'] = 0
        self.iText.setScale(.25)
        self.iText.setTwoSided(True)

        self.lText = DirectButton()
        self.lText.reparentTo(self.myRender)
        self.lText['text'] = "1) Press Escape To Pause and Show Mouse\n2) Hit Enter While Paused to Exit the Level Editor\n3) Level Saves Every Time a Blocked is Placed"
        self.lText['frameVisibleScale'] = (2, 0.5, 0)
        self.lText['frameColor'] = (1, 1, 1, 0)
        self.lText['textMayChange'] = 0
        self.lText.setScale(.25)
        self.lText.setTwoSided(True)

    def initPlayer(self):
        #self.cube = Cube(1, 1, 1)
        self.node = self.myRender.attachNewNode("node")
        #self.cube.reparentTo(self.node)
        #self.cube.setPos(-0.5, 0, 0)
        #self.node.setPos(0, 0, 0)

        tex = loader.loadTexture("./VoxelDash/textures/player.png")
        #self.cube.setTexture(tex)


        self.ghostCube = Cube(1, 1, 1)
        self.ghostNode = self.myRender.attachNewNode('Ghost Cube')
        self.ghostCube.reparentTo(self.ghostNode)
        self.ghostCube.setPos(-0.5, 0, 0)
        self.ghostNode.setPos(self.node.getPos())
        self.ghostNode.setColor(.1, .1, .1, 1)

    def makePlatform1(self, arg, dimension, tipe):
        name = str(arg)
        pType = str(tipe)
        self.keyPress = True

        if dimension == "l":
            self.lengthText = DirectButton()
            self.lengthText.reparentTo(self.myRender)
            self.lengthText['text'] = ('Use Arrow Keys To Change The ' + str(name) + ' Dimesnions')
            self.lengthText['frameVisibleScale'] = (2, 0.5, 0)
            self.lengthText['frameColor'] = (1, 1, 1, 0)
            self.lengthText.setPos(self.node.getPos() + Vec3(0, 0, 2))
            self.lengthText.setScale(.25)
            self.lengthText.setTwoSided(True)

            self.Text = DirectButton()
            self.Text.reparentTo(self.myRender)
            self.Text['text'] = ("Current Dimension = Length: " + str(self.l))
            self.Text['frameVisibleScale'] = (2, 0.5, 0)
            self.Text['frameColor'] = (1, 1, 1, 0)
            self.Text['textMayChange'] = 0
            self.Text.setPos(self.node.getPos() + Vec3(0, 0, 3))
            self.Text.setScale(.25)
            self.Text.setTwoSided(True)

            self.accept("arrow_up", self.increaseSize, extraArgs = ["l"])
            self.accept("arrow_down", self.decreaseSize, extraArgs = ["l"])


            self.accept("enter", self.nextStat, extraArgs = ["w", name, pType])

        if dimension == "w":
            self.widthText = DirectButton()
            self.widthText.reparentTo(self.myRender)
            self.widthText['text'] = ('Use Arrow Keys To Change The ' + str(name) + ' Dimesnions')
            self.widthText['frameVisibleScale'] = (2, 0.5, 0)
            self.widthText['frameColor'] = (1, 1, 1, 0)
            self.widthText.setPos(self.node.getPos() + Vec3(0, 0, 2))
            self.widthText.setScale(.25)
            self.widthText.setTwoSided(True)

            self.Text = DirectButton()
            self.Text.reparentTo(self.myRender)
            self.Text['text'] = ("Current Dimension = Width: " + str(self.w))
            self.Text['frameVisibleScale'] = (2, 0.5, 0)
            self.Text['frameColor'] = (1, 1, 1, 0)
            self.Text['textMayChange'] = 0
            self.Text.setPos(self.node.getPos() + Vec3(0, 0, 3))
            self.Text.setScale(.25)
            self.Text.setTwoSided(True)


            self.accept("arrow_up", self.increaseSize, extraArgs=["w"])
            self.accept("arrow_down", self.decreaseSize, extraArgs = ["w"])

            self.accept("enter", self.nextStat, extraArgs = ["h", name, pType])

        if dimension == "h":
            self.heightText = DirectButton()
            self.heightText.reparentTo(self.myRender)
            self.heightText['text'] = ('Use Arrow Keys To Change The ' + str(name) + ' Dimesnions')
            self.heightText['frameVisibleScale'] = (2, 0.5, 0)
            self.heightText['frameColor'] = (1, 1, 1, 0)
            self.heightText.setPos(self.node.getPos() + Vec3(0, 0, 2))
            self.heightText.setScale(.25)
            self.heightText.setTwoSided(True)

            self.Text = DirectButton()
            self.Text.reparentTo(self.myRender)
            self.Text['text'] = ("Current Dimension = Height: " + str(self.w))
            self.Text['frameVisibleScale'] = (2, 0.5, 0)
            self.Text['frameColor'] = (1, 1, 1, 0)
            self.Text['textMayChange'] = 0
            self.Text.setPos(self.node.getPos() + Vec3(0, 0, 3))
            self.Text.setScale(.25)
            self.Text.setTwoSided(True)

            self.accept("arrow_up", self.increaseSize, extraArgs = ["h"])
            self.accept("arrow_down", self.decreaseSize, extraArgs = ["h"])

            self.accept("enter", self.nextStat, extraArgs = ["makeCube", name, pType])

        if dimension == "Pos":
            self.posText = DirectButton()
            self.posText.reparentTo(self.myRender)
            self.posText['text'] = ('Move to Desired Position Then hit Enter to Record the First Position')
            self.posText['frameVisibleScale'] = (2, 0.5, 0)
            self.posText['frameColor'] = (1, 1, 1, 0)
            self.posText.setPos(self.node.getPos() + Vec3(0, 0, 2))
            self.posText.setScale(.25)
            self.posText.setTwoSided(True)

            self.accept("enter", self.nextStat, extraArgs = ["getPosA", name, pType])

        if dimension == "PosA":
            self.posText = DirectButton()
            self.posText.reparentTo(self.myRender)
            self.posText['text'] = ('Move to Desired Position Then hit Enter to Record the Move-To Position')
            self.posText['frameVisibleScale'] = (2, 0.5, 0)
            self.posText['frameColor'] = (1, 1, 1, 0)
            self.posText.setPos(self.node.getPos() + Vec3(0, 0, 2))
            self.posText.setScale(.25)
            self.posText.setTwoSided(True)

            self.accept("enter", self.nextStat, extraArgs = ["makeMovingPlatform", name, pType])

    def nextStat(self, arg, name, tipe):
        if arg == "w":
            self.lengthText.destroy()
            self.Text.destroy()
            self.makePlatform1(name, "w", tipe)

        if arg == "h":
            self.widthText.destroy()
            self.Text.destroy()
            self.makePlatform1(name, "h", tipe)

        if arg == "makeCube" and tipe != "moving":
            self.createCube(name, self.l, self.w, self.h, self.dX, self.dY, self.dZ)

        if arg == "makeCube" and tipe == "moving":
            self.heightText.destroy()
            self.Text.destroy()

            self.makePlatform1(name, "Pos", tipe)

        if arg == "getPosA":
            self.posText.destroy()

            self.Xa = self.dX
            self.Ya = self.dY
            self.Za = self.dZ

            self.placeMarker = self.myRender.attachNewNode("placeMarker")
            cube = Cube(self.l, self.w, self.h)
            cube.reparentTo(self.placeMarker)
            self.placeMarker.setPos(self.Xa, self.Ya, self.Za)

            self.makePlatform1(name, "PosA", tipe)

        if arg == "makeMovingPlatform":
            #b is actually the PosA in the array used by the movement handler!
            self.Xb = self.dX
            self.Yb = self.dY
            self.Zb = self.dZ

            self.placeMarker.removeNode()

            self.createMovingPlatform(self.l, self.w, self.h, self.Xa, self.Ya, self.Za, self.Xb, self.Yb, self.Zb)

    def createMovingPlatform(self, l, w, h, Xa, Ya, Za, Xb, Yb, Zb, write = True):
        node = self.myRender.attachNewNode("cube" + str(Xa) + str(Ya) + str(Za))
        cube = Cube(l, w, h)
        cube.reparentTo(node)
        node.setX(Xa)
        node.setY(Ya)
        node.setZ(Za)
        cube.setColor(.25, .5, .75, 1)


        sL1 = LerpPosInterval(node, 4, Point3(Xb, Yb, Zb))
        sl2 = LerpPosInterval(node, 4, Point3(Xa, Ya, Za))
        sequence1 = Sequence(Wait(0.0), sL1, Wait(0.0), sl2)
        sequence0 = Sequence(Wait(0.0), sL1, Wait(0.0), sl2, Func(self.replayLerp, sequence1))
        sequence1.append(Func(self.replayLerp, sequence0))
        sequence0.start()

        if write:
            self.levelFile.write("MovingPlatform\n" + str(Xa) + "\n" + str(Ya) + "\n" + str(Za) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n" + str(Xb) + "\n" + str(Yb) + "\n" + str(Zb) + "\n" + str(10) + "\n" + str(4) + "\n")


        if write:
            self.posText.destroy()

            self.ghostCube.detachNode()
            self.ghostCube = Cube(self.l, self.w, self.h)
            self.ghostCube.reparentTo(self.ghostNode)
            self.ghostNode.setColor(.1, .1, .1, 1)

            self.l = 1
            self.w = 1
            self.h = 1

    def replayLerp(self, arg):
        arg.start()

    def increaseSize(self, arg):
        if arg == "l":
            #Length is ---->this way<-----
            self.l += 1
            self.Text["text"] = "Current Dimesnion = length: " + str(self.l)
            print(self.l)

            self.ghostCube.addGeometry(Cube2Data(self.l, self.w, self.h))

        if arg == "w":
            #width is ^ that way
            self.w += 1
            self.Text["text"] = "Current Dimesnion = Width: " + str(self.w)
            print(self.w)

            self.ghostCube.addGeometry(Cube2Data(self.l, self.w, self.h))

        if arg == "h":
            #height is up and down

            try:
                self.Text["text"] = "Current Dimesnion = Height: " + str(self.h)
                self.h += 1
                self.ghostCube.addGeometry(Cube2Data(self.l, self.w, self.h))

            except:
                print("idk man")

            print(self.h)

    def decreaseSize(self, arg):
        if arg == "l":
            if self.l >= 2:
                self.l -= 1
                self.Text["text"] = "Current Dimesnion = length: " + str(self.l)
                print(self.l)

                self.ghostCube.detachNode()
                self.ghostCube = Cube(self.l, self.w, self.h)
                self.ghostCube.reparentTo(self.ghostNode)
                self.ghostNode.setColor(.1, .1, .1, 1)

        if arg == "w":
            if self.w >= 2:
                self.w -= 1
                self.Text["text"] = "Current Dimesnion = Width: " + str(self.w)
                print(self.w)

                self.ghostCube.detachNode()
                self.ghostCube = Cube(self.l, self.w, self.h)
                self.ghostCube.reparentTo(self.ghostNode)
                self.ghostNode.setColor(.1, .1, .1, 1)

        if arg == "h":
            if self.h >= 2:
                self.h -= 1
                self.Text["text"] = "Current Dimesnion = Height: " + str(self.h)
                print(self.h)

                self.ghostCube.detachNode()
                self.ghostCube = Cube(self.l, self.w, self.h)
                self.ghostCube.reparentTo(self.ghostNode)
                self.ghostNode.setColor(.1, .1, .1, 1)

    def setSpawn(self, x = 0, y = 0, z = 0, write = True):
        self.spawnIndicatorNode = self.myRender.attachNewNode("spawnIndicatorNode")
        spawnSphere = Cube(.3, .3, .3)
        spawnSphere.reparentTo(self.spawnIndicatorNode)
        if write:
            spawnSphere.setPos(self.dX + .5, self.dY + .5, self.dZ + .5)

        if write == False:
            spawnSphere.setPos(x + .5, y + .5, z + .5)

        self.spawnIndicatorNode.setColor(0, 1, 0, 1)

        if write:
            self.levelFile.write("SetSpawn\n" + str(self.dX) + "\n" + str(self.dY) + "\n" + str(self.dZ) + "\n")

    def placeEnemy(self, x = 0, y = 0, z = 0, write = True):
        self.placeEnemyNode = self.myRender.attachNewNode("placeEnemyNode")
        placeEnemyCube = Cube(.3, .3, .3)
        placeEnemyCube.reparentTo(self.placeEnemyNode)
        if write:
            placeEnemyCube.setPos(self.dX + .5, self.dY + .5, self.dZ + .5)
        if write == False:
            placeEnemyCube.setPos(x + .5, y + .5, z + .5)
        self.placeEnemyNode.setColor(1, 0, 0, 1)

        if write:
            self.levelFile.write("PlaceEnemy\n" + str(self.dX) + "\n" + str(self.dY) + "\n" + str(self.dZ) + "\n")

    def createCube(self, name, l, w, h, x, y, z, write = True):
        if name == "Platform":
            node = self.myRender.attachNewNode("cube" + str(x) + str(y) + str(z))
            cube = Cube(l, w, h)
            cube.reparentTo(node)
            node.setX(x)
            node.setY(y)
            node.setZ(z)
            cube.setColor(1, 1, 0, 1)

            if write:
                self.levelFile.write("Platform\n" + str(x) + "\n" + str(y) + "\n" + str(z) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

        if name == "HitBox":
            node = self.myRender.attachNewNode("cube" + str(x) + str(y) + str(z))
            cube = Cube(l, w, h)
            cube.reparentTo(node)
            node.setX(x)
            node.setY(y)
            node.setZ(z)
            cube.setColor(0, 1, 0, 1)

            if write:
                self.levelFile.write("HitBox\n" + str(x) + "\n" + str(y) + "\n" + str(z) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

        if name == "EndGoal":
            node = self.myRender.attachNewNode("cube" + str(x) + str(y) + str(z))
            cube = Cube(l, w, h)
            cube.reparentTo(node)
            node.setX(x)
            node.setY(y)
            node.setZ(z)
            cube.setColor(1, 0, 0, 1)

            if write:
                self.levelFile.write("EndGoal\n" + str(x) + "\n" + str(y) + "\n" + str(z) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

        if name == "LoadLevelBox":
            node = self.myRender.attachNewNode("cube" + str(x) + str(y) + str(z))
            cube = Cube(l, w, h)
            cube.reparentTo(node)
            node.setX(x)
            node.setY(y)
            node.setZ(z)
            cube.setColor(0, 0, 1, 1)

            if write:
                self.levelFile.write("LoadLevelBox\n" + str(x) + "\n" + str(y) + "\n" + str(z) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

        if name == "LevelEditBox":
            node = self.myRender.attachNewNode("cube" + str(x) + str(y) + str(z))
            cube = Cube(l, w, h)
            cube.reparentTo(node)
            node.setX(x)
            node.setY(y)
            node.setZ(z)
            cube.setColor(1, 0, 1, 1)

            if write:
                self.levelFile.write("LevelEditBox\n" + str(x) + "\n" + str(y) + "\n" + str(z) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

        print(l, w, h, x, y, z)

        if write:
            self.heightText.destroy()
            self.Text.destroy()

            self.l = 1
            self.w = 1
            self.h = 1

            self.ghostCube.detachNode()
            self.ghostCube = Cube(self.l, self.w, self.h)
            self.ghostCube.reparentTo(self.ghostNode)
            self.ghostNode.setColor(.1, .1, .1, 1)

    def setCamera(self):
        self.cameraNode = self.myRender.attachNewNode("Camera Node 1")
        self.hNode = self.myRender.attachNewNode("h node")
        self.pNode = self.myRender.attachNewNode("p node")
        #self.cameraNode.reparentTo(self.fakeNode)
        base.camera1.setPos(0, 0 - self.cameraDist, self.cameraDist)
        base.camera1.reparentTo(self.cameraNode)

    def controlListener(self):
        inputState.watchWithModifiers("for", "w")
        inputState.watchWithModifiers("back", "s")
        inputState.watchWithModifiers("left", "a")
        inputState.watchWithModifiers("right", "d")
        inputState.watchWithModifiers("up", "shift")
        inputState.watchWithModifiers("down", "space")

        self.accept("0", self.makePlatform1, extraArgs = ["Platform", "l", "static"])
        self.accept("9", self.makePlatform1, extraArgs = ["HitBox", "l", "static"])
        self.accept("8", self.makePlatform1, extraArgs = ["EndGoal", "l", "static"])
        self.accept("7", self.makePlatform1, extraArgs = ["MovingPlatform", "l", "moving"])
        self.accept("6", self.setSpawn)
        self.accept("5", self.placeEnemy)
        self.accept("4", self.makePlatform1, extraArgs = ["LoadLevelBox", "l", "static"])
        self.accept("3", self.makePlatform1, extraArgs = ["LevelEditBox", "l", "static"])

        self.accept("wheel_up", self.cameraScroll, extraArgs = ["Plus"])
        self.accept("wheel_down", self.cameraScroll, extraArgs = ["Minus"])

        self.accept("escape", self.esc)

    def esc(self):
        #base.closeWindow(self.win1)
        taskMgr.remove("LevelEditUpdate")
        self.wp.setCursorHidden(False)
        self.win1.requestProperties(self.wp)

        self.pauseText = DirectButton()
        self.pauseText.reparentTo(self.myRender)
        self.pauseText['text'] = "Paused!\nHit Escape to Resume\nHit Enter to Leave (all level progress is saved automatically!)"
        self.pauseText['frameVisibleScale'] = (2, 0.5, 0)
        self.pauseText['frameColor'] = (1, 1, 1, 0)
        self.pauseText['textMayChange'] = 0
        self.pauseText.setScale(.5)
        self.pauseText.setTwoSided(True)
        self.pauseText.setH(self.hNode.getH())
        self.pauseText.setP(self.pNode.getP())

        self.accept("escape", self.resumeUpdate)
        self.acceptOnce("enter", self.exitWindow)

    def exitWindow(self):
        base.closeWindow(self.win1)

    def resumeUpdate(self):
        taskMgr.add(self.update, "LevelEditUpdate")
        self.wp.setCursorHidden(True)
        self.win1.requestProperties(self.wp)
        self.pauseText.destroy()
        self.accept("escape", self.esc)

    def cameraScroll(self, arg):
        if arg == "Plus":
            self.cameraDist -= 1
            base.camera1.setPos(0, 0 - self.cameraDist, self.cameraDist)

        if arg == "Minus":
            self.cameraDist += 1
            base.camera1.setPos(0, 0 - self.cameraDist, self.cameraDist)

    def initEditor(self):
        #win = base.openWindow()
        self.wp = WindowProperties()
        #base.makeAllPipes()
        pipe = base.pipeList[0]
        self.wp.setSize(pipe.getDisplayWidth() - 60, pipe.getDisplayHeight() - 60)
        self.wp.setOrigin(30, 30)
        self.wp.setCursorHidden(True)

        self.win1 = base.openWindow(props = self.wp)
        #base.setupMouse

        self.myRender = NodePath('myRender')
        base.camList[-1].reparentTo(self.myRender)

        base.camera1 = base.camList[-1]
        #base.camera1.lookAt(self.node)


        self.buttonThrowers = []
        for i in range(self.win1.getNumInputDevices()):
            name = self.win1.getInputDeviceName(i)
            mk = base.dataRoot.attachNewNode(MouseAndKeyboard(self.win1, i, name))
            mw = mk.attachNewNode(MouseWatcher(name))
            bt = mw.attachNewNode(ButtonThrower("buttons%s" % (i)))
            if (i != 0):
                bt.node().setPrefix('mousedev'+str(i)+'-')
            mods = ModifierButtons()
            bt.node().setModifierButtons(mods)
            self.buttonThrowers.append(bt)

    def LoadLevel(self, location):
        print(location)

    def skyBox(self):
        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        self.Sphere = Sphere(20)
        self.snp = self.myRender.attachNewNode("Sphere Node")
        self.Sphere.reparentTo(self.snp)
        self.snp.setTwoSided(True)
        self.snp.setMaterial(material)
        texture = loader.loadTexture("./textures/levelEditorSkyBox.jpg")
        self.Sphere.setTexture(texture)
        self.snp.reparentTo(base.camera1)
        self.snp.setBin("Background", 1)
        self.snp.setDepthWrite(False)
        self.snp.setCompass()

    def update(self, task):

        #############################################
        #             #CAMERA UPDATE#               #
        #############################################

        self.hNode.setPos(self.node.getPos())
        self.pNode.setPos(self.node.getPos())

        self.cameraNode.setH(self.hNode.getH())
        self.cameraNode.setP(self.pNode.getP())
        self.cameraNode.setPos(self.node.getPos())

        pointer = self.win1.getPointer(0)
        pointerX = pointer.getX()
        pointerY = pointer.getY()

        if self.win1.movePointer(0, self.win1.getXSize()/2, self.win1.getYSize ()/2):
            Pitch = -((pointerY - self.win1.getYSize()/2)*.1)
            Heading = -((pointerX - self.win1.getXSize()/2)*.1)

            self.pNode.setP(self.pNode, Pitch)
            self.hNode.setH(self.hNode, Heading)

        if self.bool:
            base.camera1.lookAt(self.node)
            self.bool = False

        #############################################
        #            #PLAYER UPDATE#                #
        #############################################

        if inputState.isSet("up"):
            self.node.setZ(self.node.getZ() - 0.1)

        if inputState.isSet("down"):
            self.node.setZ(self.node.getZ() + 0.1)

        if inputState.isSet("for"):
            self.node.setY(self.node.getY() + 0.1)
            self.node.setZ(self.node.getZ() + 0.1)

        if inputState.isSet("back"):
            self.node.setY(self.node.getY() - 0.1)
            self.node.setZ(self.node.getZ() - 0.1)

        if inputState.isSet("left"):
            self.node.setX(self.node.getX() - 0.1)

        if inputState.isSet("right"):
            self.node.setX(self.node.getX() + 0.1)

        #############################################
        #              #GRID UPDATE#                #
        #############################################
        self.posX = self.node.getX()
        self.posY = self.node.getY()
        self.posZ = self.node.getZ()
        self.dX, self.posX = divmod(self.posX, 1)
        self.dY, self.posY = divmod(self.posY, 1)
        self.dZ, self.posZ = divmod(self.posZ, 1)

        #print(self.dX, self.posX)
        #print(self.dY, self.posY)
        #print(self.dZ, self.posZ)

        if self.posX < .5 or self.posX > -.5:
            self.ghostCube.setX(self.dX)

        if self.posY < .5 or self.posY > -.5:
            self.ghostCube.setY(self.dY)

        if self.posZ < .5 or self.posZ > -.5:
            self.ghostCube.setZ(self.dZ)

        #if self.node.getX() % 1 == 0:
         #   self.ghostNode.setX(self.node.getX())

        #if self.node.getY() % 1 == 0:
         #   self.ghostNode.setX(self.node.getY())

        #if self.node.getZ() % 1 == 0:
         #   self.ghostNode.setX(self.node.getZ())

         #############################################
        #              #TEXT UPDATE#                #
        #############################################
        self.pText["text"] = "Current Position: " + str(self.dX) + ", " + str(self.dY) + ", " + str(self.dZ)
        self.pText.setPos(self.node.getPos() + Vec3(4, 0, 3))

        self.pText.setH(self.hNode.getH())
        self.pText.setP(self.pNode.getP())

        self.iText.setPos(self.node.getPos() + Vec3(-3.25, 0, 3))

        self.iText.setH(self.hNode.getH())
        self.iText.setP(self.pNode.getP())

        self.lText.setPos(self.node.getPos() + Vec3(-3.25, 0, 1))

        self.lText.setH(self.hNode.getH())
        self.lText.setP(self.pNode.getP())

        return task.cont


