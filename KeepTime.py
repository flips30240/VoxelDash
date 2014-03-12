##############################################
#                 #IMPORT#                   #
##############################################
from direct.gui.DirectGui import *
from direct.task import Task
##############################################
#             #BULLET IMPORT#                #
##############################################

##############################################
#       #External Class IMPORT#              #
##############################################

##############################################
#             #NEW CLASS#                    #
##############################################

class KeepTime():

    def __init__(self):
        self.mytimer = DirectLabel()
        self.mytimer.setX(1.35)
        self.mytimer.setZ(-.9625)
        self.mytimer.setScale(.1)
        taskMgr.add(self.timerTask, 'timerTask')

    def dCharstr(self, theString):
        if len(theString) != 2:
            theString = '0' + theString
        return theString

    def timerTask(self, task):
      self.millisecondsTime = int(task.time*100)
      self.secondsTime = int(task.time)
      self.minutesTime = int(self.secondsTime/60)
      self.hoursTime = int(self.minutesTime/60)
      #self.mytimer['text'] = str(self.hoursTime) + ':' + self.dCharstr(str(self.minutesTime%60)) + ':' + self.dCharstr(str(self.secondsTime%60)) + ':' + self.dCharstr(str(self.millisecondsTime%60))
      self.mytimer['text'] =self.dCharstr(str(self.minutesTime%60)) + ':' + self.dCharstr(str(self.secondsTime%60)) + ':' + self.dCharstr(str(self.millisecondsTime%60))
      return Task.cont
