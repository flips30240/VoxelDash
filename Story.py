##############################################
#              #IMPORT#                      #
##############################################
import math
##############################################
#            #BULLET IMPORT#                 #
##############################################

##############################################
#       #External Class IMPORT#              #
##############################################

##############################################
#             #NEW CLASS#                    #
##############################################

class Story():

    def __init__(self):
        self.storyDialogue = []
        self.storyNumber = []
        self.dialogue = []
        self.reccurenceList = []
        self.finalDialogue = []
        self.reccurence = 0
        self.ticker = 0

    def getStoryDialogue(self, arg, number):
        if arg in self.storyDialogue:
            print(str(arg) + " already exists!")
        else:
            self.storyDialogue.append(arg)

        if number in self.storyNumber:
            print(str(number) + " already exists!")
        else:
            self.storyNumber.append(number)
        print(self.storyDialogue)
        print(self.storyNumber)

    def compareLists(self):
        print("comparing (" + str(self.storyDialogue) + ")" + " to (" + str(self.storyNumber) + ")")

        for x in range(len(self.storyNumber)):
            if self.storyNumber[x] - self.storyNumber[x -1] != 1:
                self.reccurence += 1
                print("There is a dialogue block at line " + str(x) + "\nThere are a total of " + str(self.reccurence) + " dialogue blocks found so far")
                self.editDialogue(x)

    def editDialogue(self, x):
        self.reccurenceList.append(x)
        print(self.reccurenceList)

    def createFinalDialogueList(self):
        for x in range(len(self.reccurenceList)):
            if x > 0:
                print(int(math.fabs(self.reccurenceList[x - 1]  - self.reccurenceList[x])))
                lines = int(math.fabs(self.reccurenceList[x - 1]  - self.reccurenceList[x])) 

                self.finishDialogue(lines)

    def finishDialogue(self, arg):
        self.storyDialogue[0:arg] = [''.join(self.storyDialogue[0:arg])]

        self.finalDialogue.append(self.storyDialogue[0])

        del self.storyDialogue[0]

        if len(self.finalDialogue) == self.reccurence - 1:
            self.storyDialogue[0:arg] = [''.join(self.storyDialogue[0:arg])]

            self.finalDialogue.append(self.storyDialogue[0])

            del self.storyDialogue[0]

        print(self.storyDialogue, self.finalDialogue)
        self.ticker += 1

    def printDialogue(self):
        print(str(self.finalDialogue))
