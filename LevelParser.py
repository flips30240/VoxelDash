##############################################
#              #IMPORT#                      #
##############################################

##############################################
#            #BULLET IMPORT#                 #
##############################################

##############################################
#       #External Class IMPORT#              #
##############################################
from Level import *
##############################################
#             #NEW CLASS#                    #
##############################################


class LevelParser():

    def __init__(self, fileLocation, collisions, playerNode, world, score):
        self.file = open(str(fileLocation))

        self.player = playerNode

        self.initParse(fileLocation, collisions, playerNode, world, score)

    def initParse(self, fileLocation, collisions, playerNode, world, score):

        collisions.obtainEvenMoreVar(self)

        level = Level(collisions, playerNode, world, fileLocation, score)

        self.f = open(fileLocation)
        self.lines = self.f.readlines()
        self.f.close()

        print(self.lines)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "Platform":
                self.name = str("Platform")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])
                try:
                    H = float(self.lines[x + 7])
                    p = float(self.lines[x + 8])
                    r = float(self.lines[x + 9])
                except:
                    print("No Hpr Values!")

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                try:
                    level.Platform(self.x, self.y, self.z, self.l, self.w, self.h, H, p, r)
                except:
                    level.Platform(self.x, self.y, self.z, self.l, self.w, self.h)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "RotationPlatform":
                    self.name = str("Platform")
                    self.x = float(self.lines[x + 1])
                    self.y = float(self.lines[x + 2])
                    self.z = float(self.lines[x + 3])
                    self.l = float(self.lines[x + 4])
                    self.w = float(self.lines[x + 5])
                    self.h = float(self.lines[x + 6])
                    self.H = float(self.lines[x + 7])
                    self.p = float(self.lines[x + 8])
                    self.r = float(self.lines[x + 9])

                    print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")" + " With Hpr:" + "(" + str(self.H) + " X " + str(self.p) + " X " + str(self.r) + ")")
                    level.RotationPlatform(self.x, self.y, self.z, self.l, self.w, self.h, self.H, self.p, self.r)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "RotationSidePlatform":
                    self.name = str("Platform")
                    self.x = float(self.lines[x + 1])
                    self.y = float(self.lines[x + 2])
                    self.z = float(self.lines[x + 3])
                    self.l = float(self.lines[x + 4])
                    self.w = float(self.lines[x + 5])
                    self.h = float(self.lines[x + 6])
                    self.H = float(self.lines[x + 7])
                    self.p = float(self.lines[x + 8])
                    self.r = float(self.lines[x + 9])

                    print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")" + " With Hpr:" + "(" + str(self.H) + " X " + str(self.p) + " X " + str(self.r) + ")")
                    level.RotationSidePlatform(self.x, self.y, self.z, self.l, self.w, self.h, self.H, self.p, self.r)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "MovingPlatform":
                self.name = str("MovingPlatform" + str(x))
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])
                self.Xa = float(self.lines[x + 7])
                self.Ya = float(self.lines[x + 8])
                self.Za = float(self.lines[x + 9])
                self.mass = float(self.lines[x + 10])
                self.speed = float(self.lines[x + 11])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.movingPlatform(self.x, self.y, self.z, self.l, self.w, self.h, self.Xa, self.Ya, self.Za, self.mass, self.speed)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "EndGoal":
                self.name = str("EndGoal")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.finishBox(self.x, self.y, self.z, self.l, self.w, self.h)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "HitBox":
                self.name = str("HitBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.HitBox(self.x, self.y, self.z, self.l, self.w, self.h)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LightBall":
                self.name = str("LightBall")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.r = float(self.lines[x + 4])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Radius" + "(" + str(self.r) + ")")
                level.LightBall(self.x, self.y, self.z, self.r)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LoadLevelBox":
                self.name = str("loadLevelBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])
                self.name = self.lines[x + 7].strip()

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.loadLevelBox(self.x, self.y, self.z, self.l, self.w, self.h, self.name)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LevelEditBox":
                self.name = str("LevelEditBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.loadLevelEditBox(self.x, self.y, self.z, self.l, self.w, self.h)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "LevelSelection":
                self.name = str("LevelEditBox")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])
                self.l = float(self.lines[x + 4])
                self.w = float(self.lines[x + 5])
                self.h = float(self.lines[x + 6])
                self.name = "LevelSelect"

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " With Dimensions" + "(" + str(self.l) + " X " + str(self.w) + " X " + str(self.h) + ")")
                level.loadLevelBox(self.x, self.y, self.z, self.l, self.w, self.h, self.name)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "PlaceEnemy":
                self.name = str("Enemy")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")")
                level.createNpc(level.renderDummy, world, collisions, playerNode, "Enemy", self.x, self.y, self.z)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "SetSpawn":
                self.name = str("Spawn")
                self.x = float(self.lines[x + 1])
                self.y = float(self.lines[x + 2])
                self.z = float(self.lines[x + 3])

                print(str(self.name) + ": At Pos" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")")
                level.setSpawn(self.x, self.y, self.z)

                self.player.setPos(level.spawn)
                self.player.node().setLinearVelocity(Vec3(0,0,0))

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "StartFlatten":
                level.flattenRootNode()
                print("Flattening Platforms!")

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "CreateHeightMap":
                level.createHeightMap()
                print("Making Height Map!")


        for x in range(len(self.lines)):
            if self.lines[x].strip() == "MakeBottomPlane":
                level.makeBottomPlane()
                print("Making Bottom PLane!")

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "MovePlatforms":
                try:
                    level.movePlatforms()
                except:
                    print("No platforms to move!")
                print("MovingPlatforms!")

        level.giveVar()


