##############################################
#               #IMPORT#                     #
##############################################
from panda3d.core import Vec3
from pandac.PandaModules import Material
from pandac.PandaModules import VBase4
import random
from direct.task.Task import Task as Task
from direct.task.TaskManagerGlobal import taskMgr
from direct.interval.IntervalGlobal import *
import math
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
##############################################
#         #NEW CLASS#                        #
##############################################

class Npc(object):

    aggroDist = Vec3(3, 3, 3)

    def __init__(self, renderNode, world, collisions, playerNode, Type, x, y, z, numNpc):

        self.numNpc = numNpc

        self.world = world
        self.renderDummy = renderNode
        self.collisions = collisions
        self.player = playerNode

        self.levelNodeBounds = self.renderDummy.getBounds()

        if Type == "Enemy":
            self.createEnemy(x, y, z)
            print("aiudsrfbcweruifhcboieruhfnowi3eu4ghfnrweiugfhresiougfhnresikugfhrwesik")

        else:
            print("No Implementation of " + str(Type) + " yet!")

    def createEnemy(self, x, y, z):
        #nodes
        self.enemyBulletNode = BulletRigidBodyNode('PlayerBox')
        self.enemyBulletNode.setMass(1.0)
        self.enemyNp = self.renderDummy.attachNewNode(self.enemyBulletNode)
        self.enemyNp.setPos(x, y, z)
        print(x, y, z)

        #shapes
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        model = Cube(1, 1, 1)
        model.reparentTo(self.enemyNp)
        model.setPos(-.5, -.5, -.5)

        #nodes
        self.enemyBulletNode.addShape(shape)

        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))# -*- coding: utf-8 *-*
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        #material.setSpecular(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        myTexture = loader.loadTexture("./textures/enemy.jpg")
        self.enemyNp.setTexture(myTexture)
        self.enemyNp.setMaterial(material)

        #bullet world
        self.world.attachRigidBody(self.enemyBulletNode)

        taskMgr.add(self.enemyUpdate, "EnemyUpdateTask#" + str(self.numNpc))

    def shoot(self):
        self.ammoUsed = 0
        self.ammoUsed += 1
        #nodes
        node = BulletRigidBodyNode('Box')
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

        ammoNode.setX(self.enemyNp.getX())
        ammoNode.setY(self.enemyNp.getY())
        ammoNode.setZ(self.enemyNp.getZ() + 1)

        force = Vec3(0, 0, 0)
        force.setY(5)
        force.setZ(1)
        force*=50
        force = render.getRelativeVector(self.player, force)

        ammoNode.node().applyCentralForce(force)

        print(force)

        #bullet world
        self.world.attachRigidBody(node)

        #taskMgr.remove('ammoDestroy')
        task = Task(self.destroyAmmoNode)
        taskMgr.add(task, 'ammoDestroy', extraArgs = [task, ammoNode, node, self.world])
        #self.collisions.initAmmoCollisions(ammoNode, self.np, 0, 0, 0)

    def destroyAmmoNode(self, task, arg, bulletArg, world):
        if task.time > 3:
            print(task.time)
            arg.removeNode()
            world.removeRigidBody(bulletArg)
            print('mmmmm?')
            return Task.done
        return Task.cont

    def removeTask(self):
        taskMgr.remove("EnemyUpdateTask#" + str(self.numNpc))


    def enemyUpdate(self, task):
        if math.fabs(self.player.getX() - self.enemyNp.getX()) <= 20 and math.fabs(self.player.getY() - self.enemyNp.getY()) <= 20 and math.fabs(self.player.getZ() - self.enemyNp.getZ()) <= 20:
                    #self.r = random.randint(1, 100)
                    #if self.r == random.randint(1, 100):
                        #self.shoot()
                    #self.enemyLerp = LerpPosInterval(self.enemyNp, .4, self.player.getPos())
                    #self.enemyLerp.start()
            self.velocity = Vec3(self.player.getPos() - self.enemyNp.getPos())

            self.enemyBulletNode.setLinearVelocity(self.velocity * 2)

        if math.fabs(self.enemyNp.getX()) > math.fabs(self.levelNodeBounds.getRadius()) * 2:
            self.removeTask()

        if math.fabs(self.enemyNp.getY()) > math.fabs(self.levelNodeBounds.getRadius())  * 2:
            self.removeTask()

        if math.fabs(self.enemyNp.getZ()) > math.fabs(self.levelNodeBounds.getRadius())  * 2:
            self.removeTask()



        return Task.cont
