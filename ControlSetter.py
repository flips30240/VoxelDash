##############################################
#                 #IMPORT#                   #
##############################################
from direct.gui.DirectGui import *
import sys
import os
##############################################
#        #External Class IMPORT#             #
##############################################
from initGame import *


class ControlSetter():
	def __init__(self, windowProps, user, connection):
		print("Running Controls Manager!")
		self.wp = windowProps
		self.user = user
		self.connection = connection
		self.checkForExistingFile()

	def checkForExistingFile(self):
		for root, dirs, files in os.walk("./controls"):
			if files == []:
				self.beginControlWizard(0)
			else:
				self.beginGame()

	def beginControlWizard(self, arg):
		if arg == 0:
			self.controlFile = open("./controls/ControlsFileConfig.txt", "w")
			print("wtf!!")
			self.nextControl("forward")
		if arg == 1:
			self.nextControl("reverse")
		if arg == 2:
			self.nextControl("left")
		if arg == 3:
			self.nextControl("right")
		if arg == 4:
			self.nextControl("Mouse")

	def nextControl(self, arg):
		if arg == "forward":
			 self.controlEntry = DirectEntry(text="", scale=.05, command=self.createAndCloseControlFile, initialText="", numLines=1, focus=1, extraArgs=["forward"])
			 self.controlEntry.setPos(-.225, 0, 0.2)

			 self.levelLoadIntroText = OnscreenText(text = 'What key do you want to move forward with? (Hit enter After!)', pos = (0.0, 0.02), scale = 0.07)

		if arg == "reverse":
			 self.controlEntry = DirectEntry(text="", scale=.05, command=self.createAndCloseControlFile, initialText="", numLines=1, focus=1, extraArgs=["reverse"])
			 self.controlEntry.setPos(-.225, 0, 0.2)

			 self.levelLoadIntroText = OnscreenText(text = 'What key do you want to move in reverse with? (Hit enter After!)', pos = (0.0, 0.02), scale = 0.07)

		if arg == "left":
			 self.controlEntry = DirectEntry(text="", scale=.05, command=self.createAndCloseControlFile, initialText="", numLines=1, focus=1, extraArgs=["left"])
			 self.controlEntry.setPos(-.225, 0, 0.2)

			 self.levelLoadIntroText = OnscreenText(text = 'What key do you want to move left with? (Hit enter After!)', pos = (0.0, 0.02), scale = 0.07)

		if arg == "right":
			 self.controlEntry = DirectEntry(text="", scale=.05, command=self.createAndCloseControlFile, initialText="", numLines=1, focus=1, extraArgs=["right"])
			 self.controlEntry.setPos(-.225, 0, 0.2)

			 self.levelLoadIntroText = OnscreenText(text = 'What key do you want to move right with? (Hit enter After!)', pos = (0.0, 0.02), scale = 0.07)

		if arg == "Mouse":
			self.controlEntry = DirectEntry(text="", scale=.05, command=self.createAndCloseControlFile, initialText="no", numLines=1, focus=1, extraArgs=["Mouse"])
			self.controlEntry.setPos(-.225, 0, 0.2)

			self.levelLoadIntroText = OnscreenText(text = 'Do you want your y axis inverted? (where moving the mouse forward moves the camera down)\nIf so type yes then hit enter; Otherwise just hit enter!)', pos = (0.0, 0.02), scale = 0.07)

	def createAndCloseControlFile(self, keyValue, Control):
		if Control == "forward":
			self.controlFile.write("forward\n" + str(keyValue) + "\n")

			self.controlEntry.destroy()
			self.levelLoadIntroText.destroy()

			self.beginControlWizard(1)

		if Control == "reverse":
			self.controlFile.write("reverse\n" + str(keyValue) + "\n")

			self.controlEntry.destroy()
			self.levelLoadIntroText.destroy()

			self.beginControlWizard(2)

		if Control == "left":
			self.controlFile.write("left\n" + str(keyValue) + "\n")

			self.controlEntry.destroy()
			self.levelLoadIntroText.destroy()

			self.beginControlWizard(3)

		if Control == "right":
			self.controlFile.write("right\n" + str(keyValue) + "\n")

			self.controlEntry.destroy()
			self.levelLoadIntroText.destroy()

			self.beginControlWizard(4)

		if Control == "Mouse":
			self.controlFile.write("Mouse Y Axis Inverted\n" + str(keyValue))

			self.controlEntry.destroy()
			self.levelLoadIntroText.destroy()

			self.controlFile.close()

			self.beginGame()


	def beginGame(self):
		initGame(self.wp, self.user, self.connection)

