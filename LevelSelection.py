##############################################
#                 #IMPORT#                   #
##############################################
import os

class LevelSelection():

	def __init__(self):

		self.createFile()
		self.beginSearch()
		self.createLevelSelection()

	def createFile(self):
		self.levelFile = open("./VoxelDash/levels/" + "levelSelect.txt", "w")

	def beginSearch(self):
		self.levels = []
		for root, dirs, files in os.walk("./VoxelDash/levels"):
			for name in files:
				if name.endswith((".txt")) and name != "levelSelect.txt":
					levelName = name[:-4]
					print(levelName)
					self.levels.append(levelName)

	def createLevelSelection(self):
		for i in range(len(self.levels)):
			try:
				x = i*10
				self.levelFile.write("LoadLevelBox\n" + str(x + 3) + "\n" + str(len(self.levels) * 5) + "\n" + str(2) + "\n" + str(1) + "\n" + str(.25) + "\n" + str(4) + "\n" + self.levels[i] + "\n")
			except:
				print("left list index range!")

		w = len(self.levels)*10

		self.levelFile.write("Platform\n" + str(0) + "\n" + str(0) + "\n" + str(0) + "\n" + str(w) + "\n" + str(w) + "\n" + str(1) + "\n")
		self.levelFile.write("SetSpawn\n" + str(0) + "\n" + str(0) + "\n" + str(1) + "\n")

		self.levelFile.close()

level = LevelSelection()