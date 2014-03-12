##############################################
#             #IMPORT#                       #
##############################################
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import CollisionNode, CollisionSphere, CollisionBox, BitMask32, CollisionSegment
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpPosInterval
import math
import os
##############################################
#             #BULLET IMPORT#                #
##############################################

##############################################
#          #External Class IMPORT#           #
##############################################
import LevelEditor as LevelEditor
import LevelGenerator as LevelGenerator
##############################################
#          #NEW CLASS#                       #
##############################################


class pCollisions(DirectObject):

    def __init__(self, score, sound):
        self.scoreHandler = score
        self.music = sound

        self.collHandEvent = CollisionHandlerEvent()
        self.collHandEvent.addInPattern('%fn-into-%in')
        self.collHandEvent.addOutPattern('%fn-outof-%in')

        self.hitBoxCollEvent = CollisionHandlerEvent()
        self.hitBoxCollEvent.addInPattern('into-%fn')
        self.hitBoxCollEvent.addOutPattern('outof-%in')

        self.rayCollEvent = CollisionHandlerEvent()
        self.rayCollEvent.addInPattern('%fn-into')


        base.cTrav = CollisionTraverser()

        self.collCount = 0

    def passPlayer(self, arg):
        self.player = arg

    def obtainVar(self, arg):
        self.levelNode = arg

    def obtainMoreVar(self, arg):
        self.world = arg

    def obtainMoreMoreVar(self, arg):
        self.playerBulletNode = arg

    def obtainMoreMoreMoreVar(self, arg):
        self.BPnode = arg

    def obtainEvenMoreVar(self, arg):
        self.levelParser = arg

    def obtainFinalVar(self, arg):
        self.playerNP = arg

    def obtainEvenEvenEvenMoreVar(self, arg):
        self.level = arg

    def initAmmoCollisions(self, intoNode, fromNode, bulletNode, l, w, h):
        if intoNode == "false":
            hitBoxColl = self.initCollisionCube(fromNode, l, w, h, False)
            base.cTrav.addCollider(hitBoxColl[0], self.hitBoxCollEvent)
            self.accept('into-' + hitBoxColl[1], self.ammoCollide, [fromNode, hitBoxColl[0], bulletNode])
        else:
            ammoColl = self.initCollisionSphere(intoNode, False)
            base.cTrav.addCollider(ammoColl[0], self.collHandEvent)

            #self.accept(hitBoxColl[1] + '-into-' + ammoColl[1], self.ammoCollide, [fromNode])

    def initCameraCollisions(self):
        self.cnodePath = base.camera.attachNewNode(CollisionNode('CollisionSphereCamera'))

        self.csphere = CollisionSphere(0, 0, 0, 4)
        self.cnodePath.node().addSolid(self.csphere)
        self.cnodePath.node().setFromCollideMask(BitMask32.bit(1))
        self.cnodePath.node().setIntoCollideMask(BitMask32.allOff())

        base.cTrav.addCollider(self.cnodePath, self.hitBoxCollEvent)

        self.accept('into-' + 'CollisionSphereCamera', self.cameraCollision)

        #self.rayNode = self.playerNP.attachNewNode(CollisionNode('rayCollide'))
        #self.cSegment = CollisionSegment(self.playerNP.getPos(), base.camera.getPos())
        #self.rayNode.node().addSolid(self.cSegment)
        #base.cTrav.addCollider(self.rayNode, self.rayCollEvent)

        #self.accept('rayCollide-into', self.cameraCollision)

    def cameraCollision(self, collEntry):
        #base.camera.setY(base.camera.getY() + 1)
        #base.camera.setZ(base.camera.getZ() - 1)
        #base.camera.setPos(0, -2, 2)

        intoNode = collEntry.getIntoNodePath()

        bounds = intoNode.getParent().getTightBounds()
        print(bounds)
        print(intoNode)
        dimensions = bounds[1] - bounds[0]

        print(dimensions)

        camDist = math.fabs(base.camera.getY() + math.ceil(dimensions[1]))

        cameraLerp = LerpPosInterval(base.camera, 0.1, Vec3(0, -camDist, camDist))
        cameraLerp.start()

        print("Camera Pos: " + str(base.camera.getPos()))

        print("camera Collided")

    def ammoCollide(self, fromNode, collNode, bulletNode, collEntry):
        print("ammo collision")
        if fromNode.getName() == "hitBox":
            fromNode.clearTexture()
            fromNode.setColor(1, 0, 0, 1)
            fromNode.setShaderAuto()
            self.music.playSound("./VoxelDash/sounds/thump.mp3", .03, False)
        #self.world.removeRigidBody(bulletNode)
        #fromNode.remove()
        collNode.removeNode()
        self.scoreHandler.addToScore("HitBox", 500)

    def initFinishCollisions(self, intoNode, fromNode, l, w, h):

        fCubeColl = self.initCollisionCube(intoNode, l, w, h, False)
        pCubeColl = self.initCollisionSphere(fromNode, False)

        base.cTrav.addCollider(fCubeColl[0], self.collHandEvent)
        base.cTrav.addCollider(pCubeColl[0], self.collHandEvent)

        self.accept(pCubeColl[1] + '-into-' + fCubeColl[1], self.finish, [fromNode])
        #self.accept(fCubeColl[1] + '-into-' + pCubeColl[1], self.finish, [fromNode])

    def initMenuCollisions(self, MenuName, intoNode, fromNode, l, w, h):

        fCubeColl = self.initCollisionCube(intoNode, l, w, h, False)
        pCubeColl = self.initCollisionSphere(fromNode, False)

        base.cTrav.addCollider(fCubeColl[0], self.collHandEvent)
        base.cTrav.addCollider(pCubeColl[0], self.collHandEvent)

        if MenuName == "LevelEditor":
            self.accept(pCubeColl[1] + '-into-' + fCubeColl[1], self.menu, ["LevelEditor"])
            #self.accept(fCubeColl[1] + '-into-' + pCubeColl[1], self.menu, ["LevelEditor"])

        if MenuName == "LoadLevel":
            self.accept(pCubeColl[1] + '-into-' + fCubeColl[1], self.menu, ["LoadLevel", fromNode])

        if MenuName == "LoadRandom":
            self.accept(pCubeColl[1] + '-into-' + fCubeColl[1], self.menu, ["LoadRandom", fromNode])
            #self.acceptOnce(fCubeColl[1] + '-into-' + pCubeColl[1], self.menu, ["LoadLevel"])

    def menu(self, arg0, arg, fromNode = False):
        self.levelEditorBool = False
        self.levelLoadBool = False

        try:
            self.errorText.destroy()
        except:
            print("No previous entry errors!")

        self.frame = DirectFrame()
        self.frame['frameColor'] = (0, 0, 0, .5)
        self.frame['frameSize'] = (2, -2, 2, -2)
        self.frame.setPos(0, 0, 0)

        self.frame1 = DirectFrame()
        self.frame1.reparentTo(self.frame)
        self.frame1['frameColor'] = (1, 1, 1, .5)
        self.frame1['frameSize'] = (1, -1, .5, -.5)
        self.frame1.setPos(0, 0, 0)

        if self.levelEditorBool == False:
            if arg == "LevelEditor" or arg0 == "LevelEditor":

                base.messenger.send("escape")

                self.levelNameInput = DirectEntry(text="", scale=.05, command=self.levelGenerate, initialText="", numLines=1, focus=1)
                self.levelNameInput.setPos(-.225, 0, 0.2)

                self.levelEditIntroText = OnscreenText(text = 'Enter the Name of the Level!\n PS! - Hit Tab to Cancel This', pos = (0.0, 0.02), scale = 0.07)
                self.acceptOnce("tab", self.exitCollisionMenu, extraArgs = [self.levelNameInput, self.levelEditIntroText])
                self.levelEditorBool = True

        if self.levelLoadBool == False:
            if arg == "LoadLevel" or arg0 == "LoadLevel":

                base.messenger.send("escape")

                print(fromNode.getIntoNode().getParent(0).getParent(0).getName())
                self.levelName = str(fromNode.getIntoNode().getParent(0).getParent(0).getName()).rstrip()

                #self.levelNode.removeNode() #this causes issues if you dont type in a level name fast enough

                self.levelLoadEntry = DirectEntry(text="", scale=.05, command=self.loadLevel, initialText=self.levelName, numLines=1, focus=1)
                self.levelLoadEntry.setPos(-.225, 0, 0.2)

                self.levelLoadIntroText = OnscreenText(text = 'Load This Level?\n PS! - Hit Tab to Cancel This', pos = (0.0, 0.02), scale = 0.07)
                self.acceptOnce("tab", self.exitCollisionMenu, extraArgs = [self.levelLoadEntry, self.levelLoadIntroText])
                self.levelLoadBool = True

        if self.levelLoadBool == False:
            if arg == "LoadRandom" or arg0 == "LoadRandom":

                base.messenger.send("escape")

                print(fromNode.getIntoNode().getParent(0).getParent(0).getName())
                self.levelName = str(fromNode.getIntoNode().getParent(0).getParent(0).getName()).rstrip()

                #self.levelNode.removeNode() #this causes issues if you dont type in a level name fast enough

                self.levelNameInput = DirectEntry(text="", scale=.05, command=self.levelGenerate, initialText="", numLines=1, focus=1, extraArgs = ["loadIt"])
                self.levelNameInput.setPos(-.225, 0, 0.2)

                self.levelEditIntroText = OnscreenText(text = 'What Shall you name this random Level?\n PS! - Hit Tab to Cancel This', pos = (0.0, 0.02), scale = 0.07)
                self.acceptOnce("tab", self.exitCollisionMenu, extraArgs = [self.levelNameInput, self.levelEditIntroText])
                self.levelLoadBool = True

    def exitCollisionMenu(self, arg, arg1):
        arg.destroy()
        arg1.destroy()
        self.frame.destroy()
        self.levelEditorBool = False

    def levelGenerate(self, arg, arg1 = False):

        base.messenger.send("escape")
        
        for root, dirs, files in os.walk("./VoxelDash/levels/"):
            for name in files:
                if name == str(arg) + ".txt":
                    print(name + " Already Exists!")
                    self.bool = True
                else:
                    self.levelNameInput.destroy()
                    self.levelEditIntroText.destroy()
                    self.frame.destroy()
                    self.LevelGeneratorInit = LevelGenerator.LevelGenerator(arg, arg1, self)

    #def levelEdit(self, arg):
        #self.levelNameInput.destroy()
        #self.levelEditIntroText.destroy()

        #self.bool = False

        #for root, dirs, files in os.walk("./levels/"):
            #for name in files:
               # if name == str(arg) + ".txt":
                   # print(name + " Already Exists!")
                    #self.bool = True

        #if self.bool:
            ####foo = open("./levels/" + str(arg) + '.txt')
            #self.levelEditorInit = LevelEditor.LevelEditor("./levels/" + str(arg) + ".txt", False)
            #self.bool = False

        #else:
            #foo = open("./levels/" + str(arg) + '.txt', 'w')
            #self.levelEditorInit = LevelEditor.LevelEditor(foo)

    def loadLevel(self, arg):
        try:
            base.messenger.send("escape")
            self.levelLoadEntry.destroy()
            self.levelLoadIntroText.destroy()
            self.frame.destroy()
        except:
            print("Must be going home")
            
        try:
            self.level.scoreHandler.removeTask()
            self.level.scoreHandler.scoreLabel.destroy()
        except:
            print("meh")

        try:
            self.scoreHandler.removeTask()
            self.scoreHandler.scoreLabel.destroy()
        except:
            print("Meh")

        for i in range(self.world.getNumRigidBodies()):
            if i < self.world.getNumRigidBodies() and self.world.getRigidBody(i) != self.playerBulletNode:
                node = self.world.getRigidBody(i)
                self.world.removeRigidBody(node)

        self.player.setUpAmmo()
        try:
            arg.strip(".txt")
        except:
            print( str(arg) + " does not contain .txt!")
        #try:
        self.levelNode.removeNode()
        self.levelParser.initParse("./VoxelDash/levels/" + str(arg) + ".txt", self, self.playerNP, self.world, self.scoreHandler)
        self.levelLoadBool = False
        #except:
            #self.errorText = OnscreenText(text = 'That Level Name Does Not Exist!\n Hit Shift to Try Again', pos = (0.0, 0.02), scale = 0.07)
            #base.acceptOnce("shift", self.menu, extraArgs = ["LoadLevel", "LoadLevel"])

    def finish(self, fromNode, collEntry):
        fromNode = fromNode
        print(fromNode)
        self.scoreHandler.addToScore("FinishBox", 10000)
        self.scoreHandler.removeTask()
        self.scoreHandler.getLevelName(self.level.name)
        self.scoreHandler.parseScoreFile()
        self.scoreHandler.createScoreBoard()
        fromNode.node().setLinearVelocity(fromNode.node().getLinearVelocity() + Vec3(0, 0, 100))

    def initCollisionSphere(self, obj, show=False):
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()
        radius = bounds.getRadius() * 1.1

        collSphereStr = 'CollisionHull' + str(self.collCount) + "_" + obj.getName()
        self.collCount += 1
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere(center, radius))

        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()

        return (cNodepath, collSphereStr)

    def initCollisionCube(self, obj, l, w, h, show=False):
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()

        collCubeStr = 'CollisionHull' + str(self.collCount) + "_" + obj.getName()
        self.collCount += 1
        cNode = CollisionNode(collCubeStr)
        cNode.addSolid(CollisionBox(center, l / 1.8, w / 1.8, h / 1.8))

        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()

        return (cNodepath, collCubeStr)

