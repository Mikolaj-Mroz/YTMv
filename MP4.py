from moviepy import editor

class MP4Generator():
  def __init__(self, audiofile:str, imagefile:str):
    self.music = editor.AudioFileClip(audiofile)
    self.clip = editor.ImageClip(imagefile, duration=self.music.duration)

    self.generate()

  def generate(self) -> None:
    new_audioclip = editor.CompositeAudioClip([self.music])
    self.clip.audio = new_audioclip
    self.clip.write_videofile(filename='output.mp4', fps=30)
    self.clip.close()
