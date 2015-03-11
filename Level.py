##############################################
#           #IMPORT#                         #
##############################################
from panda3d.core import Vec3
from pandac.PandaModules import GeoMipTerrain
from panda3d.core import Filename, Shader
from panda3d.core import PNMImage
from pandac.PandaModules import Fog
from direct.task.Task import Task as Task
from direct.task.TaskManagerGlobal import taskMgr
from pandac.PandaModules import Material, Texture, TextureStage
from pandac.PandaModules import VBase4
from random import *
from panda3d.core import Point3
from pandac.PandaModules import TextNode
##############################################
#               #BULLET IMPORT#              #
##############################################
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape, BulletBoxShape
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import ZUp
##############################################
#         #External Class IMPORT#            #
##############################################
from shapes.shapeGenerator import Cube
from pCollisions import *
from Npc import *
from Door import *
##############################################
#             #NEW CLASS#                    #
##############################################


#create a multidimensional array of every platform that moves that can be called and moved by the main task in initGame
#ex:
#array = [[node, str(kind of movement, ex: rotates/slides), rotation speed, xa, ya, za, xb, yb, zb]]
#array = [[finishBox, "rotate", 3, 0, 0, 0, 0, 0, 0], [movingPlatform, "slides", 0, 1, 2, 3, 3, 2, 1]]


class Level():

    def __init__(self, collisions, playerNode, world, fileLocation, score):

        score.removeTask()
        score.setScore(10000)
        score.initTask()

        self.numNpc = 0
        
        if render.find("renderDummy") != "renderDummy":
            self.renderDummy = render.attachNewNode("renderDummy")

        self.playerNode = playerNode
        self.world = world
        self.collisions = collisions
        self.giveVar()

        self.platformArray = []

        self.collisions.obtainVar(self.renderDummy)
        self.collisions.obtainMoreVar(self.world)

        tempName = fileLocation.split("./levels/")[1]
        self.name = tempName.split(".txt")[0]
        print("Level name is " + str(self.name))

        #self.makeBottomPlane()
        #self.collisions.obtainMoreMoreMoreVar(self.BPnode)
        #self.setFog()

        self.setUpTexs()

        self.flattenRootNode()

        base.messenger.send("1")

    def movePlatforms(self):
        self.slides = []
        self.rotates = []

        self.parsePlatforms(self.platformArray)
        #print(self.collisions.level.platformArray)

    def parsePlatforms(self, arg):
        for x in range(len(arg)):
            print(arg[x])
            if arg[x][1] == "slides":
                self.slides.append(arg[x])

            if arg[x][1] == "rotate":
                self.rotates.append(arg[x])

        print(self.slides, self.rotates)

        self.createLerps()

    def createLerps(self):
        for x in range(len(self.slides)):
            self.pos = self.slides[x][0].getPos()
            self.sL1 = LerpPosInterval(self.slides[x][0], self.slides[x][7], Point3(self.slides[x][3], self.slides[x][4], self.slides[x][5]))
            self.sl2 = LerpPosInterval(self.slides[x][0], self.slides[x][7], self.pos)
            sequence1 = Sequence(Wait(0.0), self.sL1, Wait(0.0), self.sl2)
            sequence0 = Sequence(Wait(0.0), self.sL1, Wait(0.0), self.sl2, Func(self.replayLerp, sequence1))
            sequence1.append(Func(self.replayLerp, sequence0))
            sequence0.start()

    def replayLerp(self, arg):
        arg.start()

    def giveVar(self):
        self.collisions.obtainEvenEvenEvenMoreVar(self)

    def setUpTexs(self):
        self.platformTex = loader.loadTexture("./textures/Platform/platform.jpg")
        self.platformTex.setWrapU(Texture.WMRepeat)
        self.platformTex.setWrapV(Texture.WMRepeat)

        self.movingPlatformTex = loader.loadTexture("./textures/MovingPlatform/MovingPlatform.png")
        self.movingPlatformTex.setWrapU(Texture.WMRepeat)
        self.movingPlatformTex.setWrapV(Texture.WMRepeat)

        self.RotationPlatformTex = loader.loadTexture("./textures/RotationPlatform/RotationPlatform.png")
        self.RotationPlatformTex.setWrapU(Texture.WMRepeat)
        self.RotationPlatformTex.setWrapV(Texture.WMRepeat)

        self.RotationSidePlatformTex = loader.loadTexture("./textures/RotationPlatform/RotationSidePlatform.png")
        self.RotationSidePlatformTex.setWrapU(Texture.WMRepeat)
        self.RotationSidePlatformTex.setWrapV(Texture.WMRepeat)

        self.hitBoxTex = loader.loadTexture("./textures/HitBox/HitBox.png")
        self.hitBoxTex.setWrapU(Texture.WMRepeat)
        self.hitBoxTex.setWrapV(Texture.WMRepeat)

        self.finishBoxTex = loader.loadTexture("./textures/finishBox.png")
        self.finishBoxTex.setWrapU(Texture.WMRepeat)
        self.finishBoxTex.setWrapV(Texture.WMRepeat)

        self.loadLevelTex = loader.loadTexture("./textures/loadLevel.jpg")
        self.loadLevelTex.setWrapU(Texture.WMRepeat)
        self.loadLevelTex.setWrapV(Texture.WMRepeat)

        self.loadLevelEditTex = loader.loadTexture("./textures/loadLevelEdit.png")
        self.loadLevelEditTex.setWrapU(Texture.WMRepeat)
        self.loadLevelEditTex.setWrapV(Texture.WMRepeat)

        self.lightBallTex = loader.loadTexture("./textures/lightBall.jpg")
        self.lightBallTex.setWrapU(Texture.WMRepeat)
        self.lightBallTex.setWrapV(Texture.WMRepeat)

    def createNpc(self, renderNode, world, collisions, playerNode, Type, x, y, z):
        self.numNpc += 1
        npc = Npc(renderNode, world, collisions, playerNode, Type, x, y, z, self.numNpc)
        print("wqieduhfgbciwuehnfiudwnfhgikudgfnikdsfgnsidukfngikudnsfgisudnfgi")

    def setSpawn(self, x, y, z):
        self.spawn = Vec3(x, y, z)
        self.playerNode.setPos(self.spawn)

    def material(self, r, g, b, a):
        mat = Material()
        mat.setAmbient(VBase4(float(r/2.5), float(g/2.5), float(b/2.5), a))
        mat.setDiffuse(VBase4(float(r/2.5), float(g/2.5), float(b/2.5), a))
        mat.setEmission(VBase4(float(r/2.5), float(g/2.5), float(b/2.5), a))
        mat.setShininess(1000)
        mat.setSpecular(VBase4(float(r/2.5), float(g/2.5), float(b/2.5), a))
        
        return(mat)
        
    def Platform(self, x, y, z, l, w, h, H = 0, p = 0, r = 0):
        #nodes
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        np = self.renderDummy.attachNewNode(node)
        np.setPos(x + ((l / float(2) - .5)), y + ((w / float(2) - .5)), z)
        np.setMaterial(self.material(0, 1, 0, .5))

        np.setHpr(H, p, r)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(np)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))
        model.setTexture(self.platformTex)
        model.setTexScale(TextureStage.getDefault(), 1, 1, 1)

        node.addShape(shape)

        self.world.attachRigidBody(node)

    def RotationPlatform(self, x, y, z, l, w, h, H, p, r):
        #nodes
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        np = self.renderDummy.attachNewNode(node)
        np.setPos(x + ((l / float(2) - .5)), y + ((w / float(2) - .5)), z)
        np.setMaterial(self.material(0, 1, 0, .5))

        np.setP(p)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(np)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))
        model.setTexture(self.RotationPlatformTex)
        model.setTexScale(TextureStage.getDefault(), 1, 1, 1)

        node.addShape(shape)

        self.world.attachRigidBody(node)

    def RotationSidePlatform(self, x, y, z, l, w, h, H, p, r):
        #nodes
        node = BulletRigidBodyNode('Box')
        node.setMass(0)
        np = self.renderDummy.attachNewNode(node)
        np.setPos(x + ((l / float(2) - .5)), y + ((w / float(2) - .5)), z)
        np.setMaterial(self.material(0, 1, 0, .5))

        np.setR(r)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(np)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))
        model.setTexture(self.RotationSidePlatformTex)
        model.setTexScale(TextureStage.getDefault(), 1, 1, 1)

        node.addShape(shape)

        self.world.attachRigidBody(node)

    def movingPlatform(self, x, y, z, l, w, h, Xa, Ya, Za, mass, speed):
        #nodes
        node = BulletRigidBodyNode('movingBox')
        node.setMass(0)
        np = self.renderDummy.attachNewNode(node)
        np.setPos(x + ((l / float(2) - .5)), y + ((w / float(2) - .5)), z)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(np)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))

        model.setTexture(self.movingPlatformTex)
        model.setTexScale(TextureStage.getDefault(), w/2, l/2, h/2)

        #nodes
        node.addShape(shape)

        #np.reparentTo(self.flattenRoot)
        np.setMaterial(self.material(0, 0, 1, 1))
        np.setTexture(self.movingPlatformTex)

        #bullet world
        self.world.attachRigidBody(node)

        array = [np, "slides", 0, (Xa + (l / float(2))) - .5, (Ya + (w / float(2))) - .5, Za,  mass, speed]
        self.platformArray.append(array)

        #Notes - should prolly flattenstrong all of these to increase performance -dont believe it changes any of the visual properties :D

    def flattenRootNode(self):
        self.renderDummy.flattenStrong()

    def finishBox(self, x, y, z, l, w, h):
        #nodes
        node = BulletRigidBodyNode('finishBox')
        node.setMass(0)
        self.finishNode = self.renderDummy.attachNewNode(node)
        self.finishNode.setPos(x, y, z)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(self.finishNode)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))

        model.setTexture(self.finishBoxTex)
        model.setTexScale(TextureStage.getDefault(), w/2, l/2, h/2)

        #nodes
        node.addShape(shape)

        self.finishNode.setMaterial(self.material(0, 1, 1, 1))
        self.finishNode.setTexture(self.finishBoxTex)

        #bullet world
        self.world.attachRigidBody(node)

        self.collisions.initFinishCollisions(model, self.playerNode, l, w, h)

        array = [self.finishNode, "rotate", 3, 0, 0, 0, 0, 0, 0]
        self.platformArray.append(array)

    def loadLevelBox(self, x, y, z, l, w, h, name):
        #nodes
        node = BulletRigidBodyNode(name)
        node.setMass(0)
        menuNode = self.renderDummy.attachNewNode(node)
        menuNode.setName(name)
        menuNode.setPos(x, y, z)

        door = Door(menuNode, x, y, z)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(menuNode)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))

        model.setTexture(self.loadLevelTex)
        model.setTexScale(TextureStage.getDefault(), w/2, l/2, h/2)

        #nodes
        node.addShape(shape)

        menuNode.setMaterial(self.material(.5, .2, .1, 1))
        menuNode.setTexture(self.loadLevelTex)

        #bullet world
        self.world.attachRigidBody(node)


        nameText = TextNode(name)
        nameText.setText(name)
        nameTextPath = menuNode.attachNewNode(nameText)
        nameTextPath.setPos(0, -1.5, 2.5)
        nameText.setFrameColor(0, 0, 1, 1)
        nameText.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0,1,0,1)
        nameTextPath.setScale(0.3)

        if name == "Random Level!":
            self.collisions.initMenuCollisions("LoadRandom", model, self.playerNode, l, w, h)
        else:
            self.collisions.initMenuCollisions("LoadLevel", model, self.playerNode, l, w, h)

    def loadLevelEditBox(self, x, y, z, l, w, h):
        #nodes
        node = BulletRigidBodyNode('loadLevelEditBox')
        node.setMass(0)
        menuNode = self.renderDummy.attachNewNode(node)
        menuNode.setPos(x, y, z)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(menuNode)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))

        model.setTexture(self.loadLevelEditTex)
        model.setTexScale(TextureStage.getDefault(), w/2, l/2, h/2)

        #nodes
        node.addShape(shape)

        menuNode.setMaterial(self.material(.3, .2, .9, 1))
        menuNode.setTexture(self.loadLevelEditTex)

        #bullet world
        self.world.attachRigidBody(node)

        self.collisions.initMenuCollisions("LevelEditor", model, self.playerNode, l, w, h)

    def HitBox(self, x, y, z, l, w, h):
        #nodes
        node = BulletRigidBodyNode('hitBox')
        node.setMass(0)
        self.hitNode = self.renderDummy.attachNewNode(node)
        self.hitNode.setPos(x, y, z)

        #shapes
        shape = BulletBoxShape(Vec3(l / float(2), w / float(2), h / float(2)))
        model = Cube(l, w, h)
        model.reparentTo(self.hitNode)
        model.setPos(0 - (l / float(2)), 0 - (w / float(2)), 0 - (h / float(2)))

        #model.setTexture(self.hitBoxTex)
        #model.setTexScale(TextureStage.getDefault(), w/2, l/2, h/2)

        #nodes
        node.addShape(shape)

        #self.hitNode.setMaterial(self.material(0, 1, 0, 1))
        self.hitNode.setColor(0, 1, 0, 1)
        self.hitNode.setTexture(self.hitBoxTex)

        #bullet world
        self.world.attachRigidBody(node)

        self.collisions.initAmmoCollisions("false", self.hitNode, node, l, w, h)

    def LightBall(self, x, y, z, r):
        #nodes
        node = BulletRigidBodyNode('LightBall')
        node.setMass(0)
        self.hitNode = self.renderDummy.attachNewNode(node)
        self.hitNode.setPos(x, y, z)

        #shapes
        model = Sphere(r)
        model.reparentTo(self.hitNode)

        self.hitNode.setColor(randint(0,1), randint(0,1), randint(0,1), randint(0,1))
        self.hitNode.setTexture(self.lightBallTex)

    def makeBottomPlane(self):
        #nodes
        self.BPnode = BulletRigidBodyNode('BPBox')
        self.BPnode.setMass(0)
        np = self.renderDummy.attachNewNode(self.BPnode)

        #shapes
        shape = BulletPlaneShape(Vec3(0, 0, 1), -2)

        #nodes
        self.BPnode.addShape(shape)

        #bullet world
        self.world.attachRigidBody(self.BPnode)

    def setFog(self):
        colour = (0.5 ,0.8 ,0.8)
        expfog = Fog("Scene-wide exponential Fog object")
        expfog.setColor(*colour)
        expfog.setExpDensity(0.01)
        render.setFog(expfog)
        base.setBackgroundColor(*colour)

    def createHeightMap(self):
        tex = loader.loadTexture("./textures/sand.jpg")
        node = BulletRigidBodyNode('HMBox')
        node.setMass(0)

        height = 26
        img = PNMImage(Filename('./heightmaps/map.png'))
        shape = BulletHeightfieldShape(img, height, ZUp)
        node.addShape(shape)
        self.world.attachRigidBody(node)

        offset = img.getXSize() / 2.0 - 0.5
        terrain = GeoMipTerrain('terrain')
        terrain.setHeightfield(img)
        self.terrainNP = terrain.getRoot()
        self.terrainNP.setSz(height)
        self.terrainNP.setPos(-offset, -offset, -height / 2.0)
        self.terrainNP.reparentTo(self.renderDummy)
        terrain.generate()
        self.terrainNP.setTexture(tex)
        #terrainNP.setTwoSided(True)
        #terrainNP.flattenStrong()

    def flattenLevel(self):
        self.terrainNP.flattenStrong()
