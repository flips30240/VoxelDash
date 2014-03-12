##############################################
#              #IMPORT#                      #
##############################################
from panda3d.core import *
##############################################
#             #NEW CLASS#                    #
##############################################


class GameLight():

    def __init__(self, player):
        self.ambientLight()
        self.directionalLight()
        #self.spotLightFollow(player)

    def ambientLight(self):
        self.alight = render.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
        render.setLight(self.alight)

    def spotLightFollow(self, player):
        slight = Spotlight('slight')
        slight.setColor(VBase4(1, 1, 1, .5))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        self.slnp.node().setShadowCaster(True)
        render.setLight(self.slnp)

    def directionalLight(self):
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        render.setLight(dlnp)
