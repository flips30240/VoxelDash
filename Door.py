from pandac.PandaModules import Material, Texture, TextureStage
from shapes.shapeGenerator import Cube

class Door():

	def __init__(self, rootNode, x, y, z):
		self.rootNode = rootNode
		self.createDoor(x, y, z)

	def createDoor(self, x, y, z):
		self.tex = loader.loadTexture("./textures/door.jpg")
		#self.tex.setWrapU(Texture.WMRepeat)
		#self.tex.setWrapV(Texture.WMRepeat)

		self.doorNode = self.rootNode.attachNewNode("Door Node")
		self.doorNode.setZ(-1)

		self.leg1Geom = Cube(1, 1, 3)
		self.leg1Geom.reparentTo(self.doorNode)
		self.leg1Geom.setPos(-.5 + 1, -.5, -.5)
		self.leg1Geom.setTexture(self.tex)

		self.leg2Geom = Cube(1, 1, 3)
		self.leg2Geom.reparentTo(self.doorNode)
		self.leg2Geom.setPos(-.5 - 1, -.5, -.5)
		self.leg2Geom.setTexture(self.tex)

		self.roof = Cube(4, 1, 1)
		self.roof.reparentTo(self.doorNode)
		self.roof.setPos(-2, 0, 2.5)
		self.roof.setP(45)
		self.roof.setTexture(self.tex)