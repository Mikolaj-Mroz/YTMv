import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from MP4 import MP4Generator
from time import sleep
from uploader import Uploader, Login
import os
import json


class App(tk.Tk):
  def __init__(self):
    super().__init__()

    self.setup_window()
    self.setup_widgets()

  def setup_window(self):
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

  def setup_widgets(self):
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

    self.image_label = ttk.Label(self)
    self.image_label.grid(column=1, row=4)

    # choose audio button
    self.audio_button = ttk.Button(
      self,
      text='Choose Audio',
      command=self.select_audio
    )

    self.audio_label = ttk.Label(self)
    self.audio_label.grid(column=1, row=6, pady=0)

    self.upload_button = ttk.Button(
      self,
      command=self.upload,
      text='Upload!',
      style='Accent.TButton'
      )

    # youtube details button
    self.edit_details_button = ttk.Button(
      self,
      command=self.edit_details,
      text='Edit details',
      style='Accent.TButton'
    )
    
    # youtube login button
    self.login_button = ttk.Button(
      self,
      command=self.login,
      text='Login',
      style='Accent.TButton'
    )

    # show buttons if logged in
    if os.path.exists('token_youtube_v3.pickle'):
      self.show_buttons()
    else:
      self.show_login()

  def show_buttons(self):
    self.image_button.grid(column=1, row=3, sticky=tk.NSEW, padx=5, pady=5)
    self.audio_button.grid(column=1, row=5, sticky=tk.NSEW, padx=5, pady=5)
    self.edit_details_button.grid(column=1, row=8, sticky=tk.NSEW, padx=5, pady=5)
  
  def show_login(self):
    self.login_button.grid(column=1, row=7, sticky=tk.NSEW)
  
  def hide_login(self):
    self.login_button.grid_forget()

  def check_files(self):
    """check if files exist and enables upload button"""
    try:
      if self.imagename and self.audioname:
        self.upload_button.grid(column=1, row=7, sticky=tk.NSEW, padx=5, pady=50)
    except:
      pass
    
  def upload(self):
    """generate mp4 file and upload to youtube"""
    global yt_data
    showinfo(message="Wait for file to generate!")
    MP4Generator(self.audioname, self.imagename)
    showinfo(message="File generated to output.mp4!")
    uploader = Uploader(yt_data['categId'], yt_data['title'], yt_data['description'], yt_data['tags'], yt_data['status'])
    showinfo(message='File uploaded to youtube!')
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

  def login(self):
    """youtube login handler"""
    login_handler = Login()
    self.hide_login()
    self.show_buttons()
  
  def edit_details(self):
    """open window where user can edit movie details"""
    e = DataWindow(self)


class DataWindow(tk.Toplevel):
  def __init__(self, master = None) -> None:
    
    super().__init__(master=master)

    self.setup_window()
    self.setup_widgets()
  
  def setup_window(self):
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
    self.columnconfigure(1, weight=2)

    # set icon
    self.iconbitmap('./icon.ico')

  
  def setup_widgets(self):
    global yt_data

    self.title = ttk.Label(self, text='Title')
    self.title.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NSEW)

    self.title_entry = ttk.Entry(self)
    self.title_entry.insert(0, yt_data['title'])
    self.title_entry.grid(column=1, row=0, padx=5, pady=5, sticky=tk.NSEW)

    self.description = ttk.Label(self, text='Description')
    self.description.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW)

    self.description_entry = ttk.Entry(self)
    self.description_entry.insert(0, yt_data['description'])
    self.description_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.NSEW)

    self.tags = ttk.Label(self, text='Tags')
    self.tags.grid(column=0, row=2, padx=5, pady=5, sticky=tk.NSEW)

    self.tags_entry = ttk.Entry(self)
    self.tags_entry.insert(0, yt_data['tags'])
    self.tags_entry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.NSEW)

    self.status = ttk.Label(self, text='Status')
    self.status.grid(column=0, row=3, padx=5, pady=5, sticky=tk.NSEW)

    self.options = ['private', 'public']
    self.value = tk.StringVar()
    self.status_option = ttk.OptionMenu(
      self,
      self.value,
      yt_data['status'],
      *self.options
      )
    self.status_option.grid(column=1, row=3, padx=5, pady=5, sticky=tk.NSEW)


    self.save_button = ttk.Button(
      self,
      command=self.save,
      text='Save changes!',
      style='Accent.TButton'
      )
    
    self.save_button.grid(column=1, row=4, padx=5, pady=5, sticky=tk.NSEW)
  
  def save(self):
    """edit youtube film details and save them to json file"""
    global yt_data
    yt_data['title'] = self.title_entry.get()
    yt_data['description'] = self.description_entry.get()
    yt_data['tags'] = self.tags_entry.get().split(' ')
    yt_data['status'] = self.value.get()
    with open('data.json', 'w') as f:
      f.write(json.dumps(yt_data))
    self.destroy()



def main():
  # global variables
  global yt_data
  if os.path.exists('data.json'):
    with open('data.json', 'r') as f:
      yt_data = json.load(f) 
  else:
    yt_data = {
      'categId': 19,
      'title': 'title',
      'description': 'description',
      'tags': ['tag1', 'tag2'],
      'status': 'private'
    }

  try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
  finally:
    app = App()

    app.mainloop()


if __name__ == '__main__':
  main()