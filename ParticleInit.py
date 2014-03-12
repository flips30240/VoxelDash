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


class ParticleInit():
    
    def __init__(self, type, nodeToEmit, world):
        self.nodeToEmit = nodeToEmit
        self.world = world

        if type == "cube":
            self.cubeRender = render.attachNewNode("cubeRender")
            for x in range(10):
                self.makeCube()

            self.cleanUp(self.cubeRender)
        
        if type == "sphere":
            self.sphereRender = render.attachNewNode("sphereRender")
            for x in range(5):
                self.makeSphere()

            self.cleanUp(self.sphereRender)

        else:
            print(str(type) + " not implemented yet in particle system!")

    def makeSphere(self):
         #nodes
        self.playerBulletNode = BulletRigidBodyNode('PlayerBox')
        self.playerBulletNode.setMass(1.0)
        self.np = self.sphereRender.attachNewNode(self.playerBulletNode)
        self.np.setPos(self.nodeToEmit.getPos() + Vec3(0, 1, 0))

        #shapes
        shape = BulletSphereShape(.1)
        model = Sphere(.1)
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

        myTexture = loader.loadTexture("player.png")
        self.np.setTexture(myTexture)
        self.np.setMaterial(material)

        #bullet world
        self.world.attachRigidBody(self.playerBulletNode)

    def makeCube(self):
        #nodes
        self.playerBulletNode = BulletRigidBodyNode('PlayerBox')
        self.playerBulletNode.setMass(1.0)
        self.np = self.cubeRender.attachNewNode(self.playerBulletNode)
        self.np.setPos(self.nodeToEmit.getPos() + Vec3(0, 1, 0))

        #shapes
        shape = BulletBoxShape(Vec3(.1, .1, .1))
        model = Cube(.2, .2, .2)
        model.reparentTo(self.np)
        model.setPos(-.1, -.1, -.1)

        #nodes
        self.playerBulletNode.addShape(shape)

        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))# -*- coding: utf-8 *-*
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        #material.setSpecular(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        myTexture = loader.loadTexture("player.png")
        self.np.setTexture(myTexture)
        self.np.setMaterial(material)

        #bullet world
        self.world.attachRigidBody(self.playerBulletNode)

    def cleanUp(self, node):
        task = Task(self.destroyTask)
        taskMgr.add(task, "particleCleaning", extraArgs = [task, node])

    def destroyTask(self, task, node):
        if task.time > 1:
            node.removeNode()
            return Task.done

        return Task.cont
