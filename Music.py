class Music():

	def __init__(self, play, sound, volume, loop = False):
		print("Sound!!")
		if play == "play":
			self.playSound(sound, volume, loop)

	def playSound(self, sound, volume, loop = False):
		self.sound = base.loader.loadSfx(sound)
		self.sound.play()
		self.sound.setLoop(True)
		self.sound.setVolume(volume)
		self.volume = volume

	def setVolume(self, volume):
		self.sound.setVolume(volume)