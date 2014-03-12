##############################################
#              #IMPORT#                      #
##############################################

##############################################
#            #BULLET IMPORT#                 #
##############################################

##############################################
#       #External Class IMPORT#              #
##############################################
from Story import *
##############################################
#             #NEW CLASS#                    #
##############################################


class StoryParser():

    def __init__(self, fileLocation):
        self.initParse(fileLocation)

    def initParse(self, fileLocation):

        self.story = Story()

        self.f = open(fileLocation)
        self.lines = self.f.readlines()
        self.f.close()

        print(self.lines)

        for x in range(len(self.lines)):
            if self.lines[x].strip() == "Dialogue":
                print("String (Dialogue) found on line: " + str(x))
                try:
                    if self.lines[x + 1] != "Dialogue":
                        for y in range(len(self.lines)):
                            if self.lines[y].strip() != "Dialogue":
                                print("String (Not Dialogue) found on line: " + str(y))
                                self.story.getStoryDialogue(self.lines[y], y)
                except:
                    print("Out of Dialogue!")
                    self.story.compareLists()
                    self.story.createFinalDialogueList()
                    self.story.printDialogue()