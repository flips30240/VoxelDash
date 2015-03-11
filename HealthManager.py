##############################################
#           #IMPORT#                         #
##############################################
from direct.gui.DirectGui import *
##############################################
#               #BULLET IMPORT#              #
##############################################

##############################################
#         #External Class IMPORT#            #
##############################################

##############################################
#             #NEW CLASS#                    #
##############################################

class HealthManager():
    playerHealth = 10
    aiHealth = 2

    def __init__(self, player):
        self.createHealthGrid(player)
        print(str(player))

    def createHealthGrid(self, player):
        if player == "player":
            self.healthList = {}
            for i in range(self.playerHealth):
                self.healthList[i] = DirectFrame()
                x = self.healthList[i]
                x["image"] = "./graphics/heart.png"
                x.setTransparency(1)
                x.setScale(.02)
                x.setPos(-1.4 + (float(i)/15), 0, -.94)

            return(self.playerHealth)

        if player == "enemy":
            self.healthList = {}
            for i in range(self.aiHealth):
                self.healthList[i] = DirectFrame()
                x = self.healthList[i]
                x["image"] = "./graphics/heart.png"
                x.setTransparency(1)
                x.setScale(.02)
                x.setPos(-1.4 + (float(i)/15), 0, -.94)

            return(self.aiHealth)
        else:
            print("no health implemented for " + str(player))

    def removeHealth(self, node):
        self.playerHealth -= 1
        try:
            self.healthList[int(self.playerHealth)].destroy()

        except:
            print("Your dead lol")

        return(self.playerHealth)

    def getHealth(self, node):
        if node == "player":
            return(self.playerHealth)

        if node == "enemy":
            return(aiHealth)

