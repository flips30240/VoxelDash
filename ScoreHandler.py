##############################################
#                  #IMPORT#                  #
##############################################
from direct.gui.DirectGui import *
from direct.task import Task
import math
##############################################
#            #BULLET IMPORT#                 #
##############################################

##############################################
#        #External Class IMPORT#             #
##############################################
from ScoreBoard import *
##############################################
#              #NEW CLASS#                   #
##############################################


class ScoreHandler():

    def __init__(self):
        self.score = 10000
        self.hitScore = 0
        self.finishScore = 0
        self.jumpScore = 0
        self.scoreText = OnscreenText(text = "", pos = (.55, -.9625), scale = 0.1)
        self.initTask()

    def initTask(self):
        taskMgr.add(self.scoreTask, "ScoreTask")

    def removeTask(self):
        taskMgr.remove("ScoreTask")

    def setScore(self, amount):
        self.score = amount

    def addToScore(self, label, amount):
        if label == "HitBox":
            self.hitScore += amount
            print(self.score)

        if label == "FinishBox":
            self.finishScore += amount * 3.14159

        if label == "Jump":
            self.jumpScore += 0 - amount

        self.score += self.hitScore
        self.score += self.finishScore
        self.score += self.jumpScore

        self.hitScore = 0
        self.finishScore = 0
        self.jumpScore = 0

    def scoreTask(self, task):
        if task.time > 0:
            self.scoreText.setText(str(math.ceil((self.score - (task.time * (math.sqrt(task.time)))))))
        return Task.cont

    def createScoreBoard(self):
        self.scoreBoard = ScoreBoard()

    def getLevelName(self, levelName):
        self.levelName = levelName
        print(self.levelName)

    def parseScoreFile(self):
        self.scoreFile = open("./VoxelDash/scoreboard/ScoreBoard.txt", "a")
        self.scoreFile.write(str(self.levelName) + ':' + self.scoreText.getText() + "\n")
        self.scoreFile.close()



