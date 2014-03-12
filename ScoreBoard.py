from direct.gui.DirectGui import *

class ScoreBoard():

	def __init__(self):

		self.scoreList = []

		self.scoreLocation = "./VoxelDash/scoreboard/ScoreBoard.txt"

		print("Score Board Initialized!")

		self.parseScoreFile(self.scoreLocation)

		base.accept("9", self.destroyBoard)

	def parseScoreFile(self, location):
		space = open(location)
		self.lines = space.readlines()
		space.close()

		print(self.lines)

		for x in range(len(self.lines)):
			z = self.lines[x].strip()
			a = z.split(":")
			print(a)

			name = a[0]
			print(name)

			score = a[1]
			print(score)

			b = [a[0], a[1]]
			print(b)

			self.scoreList.append(b)
			b = []

		print(self.scoreList)

		self.createBoard()

	def createBoard(self):
		base.messenger.send("escape")

		numItemsVisible = 4
		itemHeight = 0.11
 
		self.myScrolledList = DirectScrolledList(
		    decButton_pos= (0.35, 0, 0.53),
		    decButton_text = "UP",
		    decButton_text_scale = 0.04,
		    decButton_borderWidth = (0.005, 0.005),
		 
		    incButton_pos= (0.35, 0, -0.02),
		    incButton_text = "DOWN",
		    incButton_text_scale = 0.04,
		    incButton_borderWidth = (0.005, 0.005),
		 
		    frameSize = (0.0, 0.7, -0.05, 0.59),
		    frameColor = (1,0,0,0.5),
		    pos = (-1, 0, 0),
		    numItemsVisible = numItemsVisible,
		    forceHeight = itemHeight,
		    itemFrame_frameSize = (-0.2, 0.2, -0.37, 0.11),
		    itemFrame_pos = (0.35, 0, 0.4),
		    )

		for x in range(len(self.scoreList)):
			for y in range(len(self.scoreList[x])):
				l = DirectLabel(text = self.scoreList[x][y], text_scale = 0.1)
				self.myScrolledList.addItem(l)

	def destroyBoard(self):

		try:
			self.myScrolledList.destroy()

		except:
			print("destroy must not be how i get rid of it lol")

			##need to position it corrdctly and add a listener in controlHandler so this doesnt use the pause screen, also need scoreBoard at top and clean up##
