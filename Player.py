##############################################
#               #IMPORT#                     #
##############################################
from panda3d.core import Vec3
from pandac.PandaModules import Material
from pandac.PandaModules import VBase4
import random
from direct.task.Task import Task as Task
from direct.task.TaskManagerGlobal import taskMgr
##############################################
#               #BULLET IMPORT#              #
##############################################
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
##############################################
#           #External Class IMPORT#          #
##############################################
from shapes.shapeGenerator import Cube, Sphere
from ParticleInit import *
##############################################
#         #NEW CLASS#                        #
##############################################


class Player():

    def __init__(self, collisions, shape, world, music, score):
        self.score = score
        self.world = world
        self.collisions = collisions
        self.music = music
        self.collisions.passPlayer(self)
        if shape == str("cube"):
            self.makeCube()
        if shape == str("sphere"):
            self.makeSphere()

        self.setPlayerColor(0.3, 0.7, 0.4, 0.8)
        self.ammoUsed = 0
        
        self.setUpAmmo()

    def makeSphere(self):
         #nodes
        self.playerBulletNode = BulletRigidBodyNode('PlayerBox')
        self.playerBulletNode.setMass(1.0)
        self.np = render.attachNewNode(self.playerBulletNode)
        self.playerBulletNode.setRestitution(-1000.0)

        #shapes
        shape = BulletSphereShape(.5)
        model = Sphere(.5)
        model.reparentTo(self.np)
        model.setPos(0,0,0)

        #nodes
        self.playerBulletNode.addShape(shape)

        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))# -*- coding: utf-8 *-*
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        #material.setSpecular(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        myTexture = loader.loadTexture("./textures/player.png")
        self.np.setTexture(myTexture)
        self.np.setMaterial(material)

        #bullet world
        self.world.attachRigidBody(self.playerBulletNode)

        self.collisions.obtainMoreMoreVar(self.playerBulletNode)
        self.collisions.obtainFinalVar(self.np)


    def makeCube(self):
        #nodes
        self.playerBulletNode = BulletRigidBodyNode('PlayerBox')
        self.playerBulletNode.setMass(1.0)
        self.np = render.attachNewNode(self.playerBulletNode)

        #shapes
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        model = Cube(1, 1, 1)
        model.reparentTo(self.np)
        model.setPos(-.5, -.5, -.5)

        #nodes
        self.playerBulletNode.addShape(shape)

        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))# -*- coding: utf-8 *-*
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        #material.setSpecular(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        myTexture = loader.loadTexture("./textures/player.png")
        self.np.setTexture(myTexture)
        self.np.setMaterial(material)

        #bullet world
        self.world.attachRigidBody(self.playerBulletNode)

        self.collisions.obtainMoreMoreVar(self.playerBulletNode)
        self.collisions.obtainFinalVar(self.np)

    def setPlayerColor(self, r, g, b, a):
        self.np.setColor(r, g, b, a)

    def jump(self):
        vec3 = self.np.node().getLinearVelocity()

        if vec3[2] <= 1 and vec3[2] >= -.5:
            self.np.node().setLinearVelocity(self.np.node().getLinearVelocity() + Vec3(0, 0, 10))
            self.music.playSound("./sounds/jump.mp3", .01, False)
            self.score.addToScore("Jump", 200)
        else:
            print("can't jump'")
            print(self.np.node().getLinearVelocity())

    def setUpAmmo(self):
        self.ammoList = []
        for x in range(5):
            print(str(x) + "ammmmmmmmmmmmmmmo")
            node = BulletRigidBodyNode('Ammo Node ' + str(x))
            node.setMass(.1)
            ammoNode = render.attachNewNode(node)

            #shapes
            shape = BulletSphereShape(.2)
            model = Sphere(.2)
            model.reparentTo(ammoNode)
            model.setPos(0, 0, 0)

            #nodes
            node.addShape(shape)

            material = Material()
            material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
            material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))
            material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
            material.setShininess(random.random())

            #myTexture = loader.loadTexture("player.png")
            #ammoNode.setTexture(myTexture)
            ammoNode.setMaterial(material)

            ammoNode.setX(self.np.getX())
            ammoNode.setY(self.np.getY())
            ammoNode.setZ(self.np.getZ() + 1)

            #bullet world
            self.world.attachRigidBody(node)

            #taskMgr.remove('ammoDestroy')
            #task = Task(self.destroyAmmoNode)
            #taskMgr.add(task, 'ammoDestroy', extraArgs = [task, ammoNode, node, self.world])
            self.collisions.initAmmoCollisions(ammoNode, self.np, 0, 0, 0, 0)

            ammoNode.hide()

            self.ammoList.append(ammoNode)

    def newShoot(self):
        self.ammoUsed += 1
        ammo = self.ammoList[self.ammoUsed - 1]
        ammo.setPos(self.np.getPos() + Vec3(0, 0, 1))
        ammo.show()
        self.music.playSound("./sounds/shoot.mp3", .05)

        ammo.node().setLinearVelocity(Vec3(0,0,0))

        force = Vec3(0, 0, 0)
        force.setY(5)
        force.setZ(1)
        force*=50
        force = render.getRelativeVector(base.camera, force)

        ammo.node().applyCentralForce(force)

        print(force)

        if self.ammoUsed == 5:
            self.ammoUsed = 0
