import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from MP4 import MP4Generator
from time import sleep

class App(tk.Tk):
  def __init__(self):
    super().__init__()
    ## options of the window
    # set title of app
    self.title('YTMv Generator')

    # set size of app
    window_width = 300
    window_height = 350
    self.resizable(0,0)

    # get size of screen
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # center the app
    self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # create app grid
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

    # set styling
    self.tk.call("source", "azure.tcl")
    self.tk.call("set_theme", "dark")

    # set icon
    self.iconbitmap('./icon.ico')

    ## create content of app

    # generate mp4 file
    self.audioname: str
    self.imagename: str

    # choose image button
    self.image_button = ttk.Button(
      self,
      text='Choose Image',
      command=self.select_image,
    )

    self.image_button.grid(column=1, row=3, sticky=tk.NS, padx=5, pady=5)

    self.image_label = ttk.Label(self)
    self.image_label.grid(column=1, row=4)

    # choose audio button
    self.audio_button = ttk.Button(
      self,
      text='Choose Audio',
      command=self.select_audio
    )

    self.audio_button.grid(column=1, row=5, sticky=tk.NS, padx=5, pady=5)

    self.audio_label = ttk.Label(self)
    self.audio_label.grid(column=1, row=6, pady=0)

    self.generate_button = ttk.Button(
      self,
      command=self.generate,
      text='Generate!'
      )

  def check_files(self):
    """check if files exist and enables generate button"""
    try:
      if self.imagename and self.audioname:
        self.generate_button.grid(column=1, row=7, sticky=tk.NS, padx=5, pady=50)
    except:
      pass
    
  def generate(self):
    """generate mp4 file"""
    showinfo(message="Wait for file to generate!")
    MP4Generator(self.audioname, self.imagename)
    showinfo(message="File generated to output.mp4!")
    sleep(2)
    self.destroy()


  def select_image(self) -> str:
    """choose image file function that returns image filename"""
    filetypes = [
      ('Image File', '*.jpg *.jpeg *.png')
    ]

    filename = fd.askopenfilename(
      title='Choose Image',
      initialdir='/',
      filetypes=filetypes
    )

    self.imagename = filename
    self.image_label.config(text=filename)
    self.check_files()

  def select_audio(self) -> str:
    """choose audio file function that returns audio filename"""
    filetypes = [
      ('Audio File', '*.mp3 *.wav *.ogg')
    ]

    filename = fd.askopenfilename(
      title='Choose Audio',
      initialdir='/',
      filetypes=filetypes
    )

    self.audioname = filename
    self.audio_label.config(text=filename)
    self.check_files()

def main():
  try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
  finally:
    app = App()

    app.mainloop()


if __name__ == '__main__':
  main()