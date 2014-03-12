##############################################
#                 #IMPORT#                   #
##############################################
from random import randint
import math

class LevelGenerator():

	def __init__(self, name = "LevelGenerator", load = False, collisions = False):

		self.load = load
		self.collisions = collisions

		self.name = name

		self.numFailed = 0
		self.lastX = 0
		self.lastY = 0
		self.lastZ = 0
		self.createFile()

	def createFile(self):

		self.levelFile = open("./VoxelDash/levels/" + str(self.name) + ".txt", "w")

		self.createSeed(randint(1,99))

	def createSeed(self, num):

		self.seed = math.floor((num/(randint(1,10)/(.8756))*2.1657))
		print(self.seed)

		self.determineNumPlatforms(self.seed)

	def determineNumPlatforms(self, seed):

		try:
			self.numPlat = int(seed*math.floor((randint(randint(1,12), seed)/math.sqrt(randint(1,int(seed + 2))))))
			if self.numPlat > 100:
				self.numPlat = randint(10,100)

			if self.numPlat < 10:
				self.numPlat = randint(10,100)
			print(self.numPlat)

			self.createPlatformArray(self.numPlat)
		except:
			self.createSeed(randint(1,99))
			#self.numFailed += 1
			#self.retry("determineNumPlatforms")
			#print("Failed to load level " + str(self.numFailed) + " times!")

	def createPlatformArray(self, numPlat):

		self.platArray = []
		for i in xrange(numPlat):
			l = randint(10,30)
			w = randint(10,30)
			h = randint(1,2)

			array = []
			array.append(l)
			array.append(w)
			array.append(h)

			self.platArray.append(array)

		print(self.platArray)

		self.placePlatforms(self.platArray)

	def placePlatforms(self, platArray):

		self.coordArray = []
		for x in range(len(platArray)):
			if x == 0:
				l = platArray[x][0]
				w = platArray[x][1]
				h = platArray[x][2]
				posX = 0
				posY = 0
				posZ = 0

				self.levelFile.write("\nSetSpawn\n" + str(l/2) + "\n" + str(w/2) + "\n" + str(h+1) + "\n")
				self.levelFile.write("Platform\n" + str(posX) + "\n" + str(posY) + "\n" + str(posZ) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")

				self.coordArray.append(["First", posX, posY, posZ])

			if x > 0 and x < len(platArray):
				if randint(1,100) <= 75:
					l = platArray[x][0]*3
					w = platArray[x][1]*3
					h = platArray[x][2]*3

					if randint(1,50) > 35:
						posX = ((platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1]))
					else:
						posX = ((platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1]))

					if randint(1,2) == 2:
						posY = ((platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0]))
					else:
						posY = ((platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0]))

					if randint(1,2) == 1:	
						posZ = ((platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2]))
					else:
						posZ = -((platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2]))

					self.lastX = posX
					self.lastY = posY
					self.lastZ = posZ

					self.levelFile.write("Platform\n" + str(posX) + "\n" + str(posY) + "\n" + str(posZ) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n")
					if randint(0, 100) >= 15:
						self.levelFile.write("RotationSidePlatform\n" + str(posX + l) + "\n" + str(posY) + "\n" + str(posZ + (h/2)) + "\n" + str(3) + "\n" + str(w) + "\n" + str(h) + "\n" + str(0) + "\n" + str(0) + "\n" + str(45+180) + "\n")
						self.levelFile.write("RotationPlatform\n" + str(posX) + "\n" + str(posY + w) + "\n" + str(posZ + (h/2)) + "\n" + str(l) + "\n" + str(3) + "\n" + str(h) + "\n" + str(0) + "\n" + str(360-45) + "\n" + str(0) + "\n")
					self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
					self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
					self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
					self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")

					if randint(1,100) <= 70:
						self.levelFile.write("HitBox\n" + str(posX) + "\n" + str(posY + randint(-30,30)) + "\n" + str(posZ + randint(7,30)) + "\n" + str(w/3) + "\n" + str(h/3) + "\n" + str(l/3) + "\n")
					else:
						l = platArray[x][0]*3
						w = platArray[x][1]*3
						h = platArray[x][2]*3

						if randint(1,50) > 35:
							posX = ((platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1]))
						else:
							posX = ((platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1]))

						if randint(1,2) == 2:
							posY = ((platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0]))
						else:
							posY = ((platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0]))

						if randint(1,2) == 1:	
							posZ = ((platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2]))
						else:
							posZ = -((platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2]))



						posX2 = posX + randint(0,20)

						posY2 = posY + randint(0,20)

						posZ2 = posZ + randint(0,20)

						mass = 0

						speed = randint(0,3)

						self.lastX = posX
						self.lastY = posY
						self.lastZ = posZ

						self.levelFile.write("MovingPlatform\n" + str(posX) + "\n" + str(posY) + "\n" + str(posZ) + "\n" + str(l) + "\n" + str(w) + "\n" + str(h) + "\n" + str(posX2) + "\n" + str(posY2) + "\n" + str(posZ2) + "\n" + str(mass) + "\n" + str(speed) + "\n")
						self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
						self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
						self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")
						self.levelFile.write("LightBall\n" + str(posX + randint(-80,80)) + "\n" + str(posY + randint(-80,80)) + "\n" + str(posZ + randint(-80,80)) + "\n" +str(randint(1,5)) + "\n")

						if randint(1,100) <= 70:
							self.levelFile.write("HitBox\n" + str(posX) + "\n" + str(posY + randint(-30,30)) + "\n" + str(posZ + randint(7,30)) + "\n" + str(w/3) + "\n" + str(h/3) + "\n" + str(l/3) + "\n")
						self.coordArray.append(["Middle", posX, posY, posZ])

			if x == len(platArray) - 1:
				l = platArray[x][0]
				w = platArray[x][1]
				h = platArray[x][2]

				if randint(1,50) > 35:
					posX = (platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1])
				else:
					posX = (platArray[x-1][1]/2) + (platArray[x][1]/2 + self.lastX) + (randint(1,4)*platArray[x][1])

				if randint(1,2) == 2:
					posY = (platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0])
				else:
					posY = -(platArray[x-1][0]/2) + (platArray[x][0]/2 + self.lastY) + (randint(1,4)*platArray[x][0])

				if randint(1,2) == 1:	
					posZ = (platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2])
				else:
					posZ = (platArray[x-1][2]/2) + (platArray[x][2]/2 + self.lastZ) + (randint(1,4)*platArray[x][2])

				self.lastX = posX
				self.lastY = posY
				self.lastZ = posZ

				self.levelFile.write("EndGoal\n" + str(posX) + "\n" + str(posY) + "\n" + str(posZ + 3) + "\n" + str(50) + "\n" + str(50) + "\n" + str(50) + "\n")
				print("edgoal")

				self.coordArray.append(["Last", posX, posY, posZ])

				self.levelFile.write("MovePlatforms\n")

				self.levelFile.close()

				if self.load == "loadIt":
					self.collisions.loadLevel(self.name)


	def retry(self, arg):
		if arg == "determineNumPlatforms":
			if self.numFailed > 30:
				self.numPlat = randint(12, 50)
			self.determineNumPlatforms(self.seed)

LevelGenerator()