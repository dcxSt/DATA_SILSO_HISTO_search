#test sound
import os

#os.system("aplay star-wars-cantina-song.mp3")
from pygame import mixer # Load the required library

mixer.init()
mixer.music.load('star-wars-cantina-song.mp3')
mixer.music.play()
input()
print()
