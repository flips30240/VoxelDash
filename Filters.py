##############################################
#          #IMPORT#                          #
##############################################
from direct.filter.CommonFilters import CommonFilters
from pandac.PandaModules import Material, Texture, TextureStage
from panda3d.core import Shader
##############################################
#            #NEW CLASS#                     #
##############################################


class Filters():

    def __init__(self):
        self.filters = CommonFilters(base.win, base.cam)
        self.glowShader = loader.loadShader("./shaders/glowShader.sha")

    def enableFilters(self, player):
        #self.filters.setBloom(mintrigger=.35)
        self.filters.setBloom(blend=(1, 0, .2, 1), desat=-1, intensity=10, size="small")
        #self.filters.setCartoonInk(separation=-5)
        self.filters.setAmbientOcclusion(numsamples = 2, radius = 0.0025, amount = 2, strength = 0.001, falloff = 0.01)

        player.setShader(self.glowShader)
        player.setShaderInput("scale",4,4)

        path = render.find("renderDummy")

        path.setShader(self.glowShader)
        path.setShaderInput("scale",1,1,1)
        
