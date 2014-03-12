##############################################
#                #IMPORT#                    #
##############################################

##############################################
#         #External Class IMPORT#            #
##############################################
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
##############################################
#            #NEW CLASS#                     #
##############################################


class gameCamera():

    def __init__(self, nodeToFollow, world, collisions):
        self.np = nodeToFollow
        self.world = world
        collisions.initCameraCollisions()

        self.hNode = render.attachNewNode("H Node")
        self.pNode = render.attachNewNode("P Node")

        self.parseControls()

        self.attachCamera()
        base.accept("wheel_up", self.cameraMove, extraArgs=[1])
        base.accept("wheel_down", self.cameraMove, extraArgs=[-1])
        #self.makeCameraCollision()

    def parseControls(self):
        self.file = open("./VoxelDash/controls/ControlsFileConfig.txt")
        self.lines = self.file.readlines()
        self.file.close()

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "Mouse Y Axis Inverted":
                self.inverted = (self.lines[x+1].rstrip())

    def attachCamera(self):
        self.cn = render.attachNewNode('cameraNode')
        self.cn.setPos(self.np.getPos())
        base.camera.reparentTo(self.cn)
        base.camera.setPos(0, -10, 10)
        base.camera.lookAt(self.np)

    def cameraMove(self, arg):
        base.camera.setY(base.camera.getY() + arg)
        base.camera.setZ(base.camera.getZ() - arg)

    def makeCameraCollision(self):
        #nodes
        node = BulletRigidBodyNode('Box')
        #node.setMass(0)
        self.ccnp = render.attachNewNode(node)
        self.ccnp.reparentTo(base.camera)

        #shapes
        shape = BulletSphereShape(.5)

        #nodes
        node.addShape(shape)

        #bullet world
        self.world.attachRigidBody(node)
