from moviepy.editor import *

# Import the audio(Insert to location of your audio instead of audioClip.mp3)
audio = AudioFileClip("0.mp3")

# Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
clip = ImageClip("img.png").set_duration(audio.duration)

# Set the audio of the clip
clip = clip.set_audio(audio)

# Export the clip
clip.write_videofile("render.mp4", fps=24)
