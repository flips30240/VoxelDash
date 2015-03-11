##############################################
#              #IMPORT#                      #
##############################################
from pandac.PandaModules import *
from shapes.shapeGenerator import Cube, Sphere
from pandac.PandaModules import Material
from pandac.PandaModules import *
import random
##############################################
#         #External Class IMPORT#            #
##############################################

##############################################
#               #NEW CLASS#                  #
##############################################


class SkyBox():

    def __init__(self, boxOrSphere):
        if boxOrSphere == str("Box"):
            self.loadSkyBox()
        if boxOrSphere == str("Sphere"):
            self.loadSkySphere()

    def loadSkyBox(self):
        self.sky_material = Material()
        self.sky_material.clearAmbient()
        self.sky_material.clearEmission()
        self.sky_material.setAmbient(VBase4(1,1,1,1))

        #This loads "basic_skybox_#" # being 0-6
        #If the skybox was made in spacescape the files must be renamed to
        #work properly, and the 2 and 3 files should be switched.
        self.skybox_texture = loader.loadCubeMap("./textures/SkyBox/box_#.png")
        self.skybox_texture.setAnisotropicDegree(16)
        #self.skybox_texture.setMinfilter(Texture.FTLinearMipmapLinear)

        #TODO: Figure out a way (if possible) to allow 3d objects to be seen
        #through the skysphere, It already kinda does this, but its weird.

        self.skybox = NodePath(loader.loadModel("./models/skybox.x"))
        self.skybox.setHpr(90,90,90)
        self.skybox.setLightOff()
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        #self.skybox.setTwoSided(True) BETTER ^
        self.skybox.setScale(2)
        self.skybox.clearDepthWrite
        self.skybox.setDepthWrite(False)
        self.skybox.setMaterial(self.sky_material, 1)
        self.skybox.setTexture(self.skybox_texture)
        self.skybox.setTexGen(TextureStage.getDefault(),
        TexGenAttrib.MWorldPosition)
        #This makes it so objects behind the skybox are rendered
        self.skybox.setBin("back_to_front", 20)
        #projects the texture as it looks from render
        self.skybox.setTexProjector(TextureStage.getDefault(),
        render, self.skybox)
        self.skybox.setCompass()
        self.skybox.reparentTo(base.camera)

    def loadSkySphere(self):
        material = Material()
        material.setAmbient(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setDiffuse(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setEmission(VBase4(random.random(), random.random(), random.random(), random.random()))
        material.setShininess(random.random())

        self.Sphere = Sphere(20)
        self.snp = render.attachNewNode("Sphere Node")
        self.Sphere.reparentTo(self.snp)
        self.Sphere.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        #self.snp.setTwoSided(True)
        self.snp.setMaterial(material)
        texture = loader.loadTexture("./textures/SpaceTexture.jpg")
        self.Sphere.setTexture(texture)
        self.snp.reparentTo(base.camera)
        self.snp.setBin("Background", 1)
        self.snp.setDepthWrite(False)
        self.snp.setCompass()

