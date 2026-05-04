
import vlc
import time

player = vlc.MediaPlayer("../../../media/videotest.mp4")
player.play()

# Attend que la vidéo soit lue (ici 10s)
time.sleep(10)

