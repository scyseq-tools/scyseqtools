import os
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import utils as U

from pathlib import Path
import tkinter.font
from tkinter.colorchooser import askcolor
from playercontrol import PlayerControl

bd = 2 # borderwidth
info_bg = 'yellow' # information background
disabled_bg = 'light grey' # disabled background
relief = 'groove'
filename_width = 50
# relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

class InfoFrame(tkinter.LabelFrame):

    def __init__(self, parent, states=[None, None, None]):
        tkinter.LabelFrame.__init__(self, parent)
        self.application = parent

        self.configure(background=info_bg, 
                       borderwidth=bd,
                       padx=20, pady=20, 
                       relief=relief,
                       text='Information: ', font=(tkinter.font.BOLD,))
        self.grid(column=1,
                  row=0)
        
        # Media File
        self.media_label = tkinter.Label(self, text='Media file: ', 
                                         background=info_bg)
        self.media_label.grid(row=1, column=0, sticky=tkinter.W)
        media_msg = tkinter.Entry(self, textvariable=parent.media_file, 
                                        state=tkinter.DISABLED,
                                        width=filename_width, 
                                        disabledbackground=disabled_bg)
        media_msg.grid(row=1, column=1, sticky=tkinter.W)
        self.media_load = tkinter.Button(self, text='Load', state=states[0],
                                         #command=parent.ask_media)
                                         command=self.ask_media)
        self.media_load.grid(row=1, column=2, sticky=tkinter.W)

        # Code File
        self.code_label = tkinter.Label(self, text='Code file: ', 
                                         background=info_bg)
        self.code_label.grid(row=2, column=0, sticky=tkinter.W)
        code_msg = tkinter.Entry(self, textvariable=parent.code_file,
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg)
        code_msg.grid(row=2, column=1, sticky=tkinter.W)
        self.code_load = tkinter.Button(self, text='Load',
                                        state=states[1],
                                        command=self.ask_code)
        self.code_load.grid(row=2, column=2, sticky=tkinter.W)

        # Data File
        self.data_label = tkinter.Label(self, text='Data file: ', 
                                         background=info_bg)
        self.data_label.grid(row=3, column=0, sticky=tkinter.W)
        data_msg = tkinter.Entry(self, textvariable=parent.data_file, 
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg) 
        data_msg.grid(row=3, column=1, sticky=tkinter.W)
        self.data_load = tkinter.Button(self, text='Load',
                                        state=states[2],
                                        command=self.ask_data)
        self.data_load.grid(row=3, column=2, sticky=tkinter.W)
        self.data_save = tkinter.Button(self, text='Save',
                                        command=parent.save_data,
                                        state=tkinter.DISABLED)
        self.data_save.grid(row=3, column=3, sticky=tkinter.W)

        self.bind('<Button-3>', self.change_color)

    def ask_media(self):
        """Load media file
        """
        self.media_load.config(state='disabled')
        fname = "/home/leo/Bureau/leo_dev/video/164360 (720p).mp4"
#        if os.path.exists(fname):
#            fileInfo = MediaInfo.parse(fname)
#            for track in fileInfo.tracks:
#                if track.track_type == "Video" or track.track_type == "Audio":
#                    self.loaded_media = True 
#                    self.application.read_media(fname)
        if os.path.exists(fname) and U.is_valid_media(fname):
            self.loaded_media = True 
            self.application.read_media(fname)
        else:
            is_valid = False
            while not is_valid:
                fname = tkinter.filedialog.askopenfilename(
                                    initialdir=os.path.expanduser('~'))
                self.loaded_media=False
                if U.is_valid_media(fname):
#                    fileInfo = MediaInfo.parse(fname)
#                    for track in fileInfo.tracks:
#                        if track.track_type == "Video" or track.track_type == "Audio":
                    is_valid = True
                    self.loaded_media = True 
                    self.application.read_media(fname)
                else:
#                    if not self.media_loaded:
                    tkinter.messagebox.showinfo('Cannot load', "Cannot load %s file" % fname)
                    self.ask_media()
#                else :
#                    tkinter.messagebox.showinfo('Cannot load', "File doesn't exist %s file" % fname)
#                    self.ask_media()

        self.code_load.config(state='normal')
        
        # FIXME: make this more systematic...
        self.application.period_display.set(self.application.control.default_period)
         
    def ask_code(self):
            """Loading files defining a coding framework.
            Now only supports the new .jod (json) files
            """
            if self.application.control.state == 'c_playing' or self.application.control.state == 's_playing':
                self.application.control.dopause()
            
            fname = "test2.jod"
            if os.path.exists(fname):
                self.read_code(fname)
            else :
                fname = tkinter.filedialog.askopenfilename(filetypes=[('New code', '*.jod')],
                                                    initialdir=os.path.expanduser('~'))
                if U.is_valid_filename(fname, ext='.jod'):
                    self.read_code(fname)
                else:
                    tkinter.messagebox.showinfo('Cannot load', 'Cannot load %s file' % fname)
            self.code_load.config(state='disabled')

    def read_code(self, fname):
            with open(fname, 'r') as ff:
                encoding = json.load(ff)

            self.application.container['code'] = encoding
            self.application.parse_code(encoding)
            self.application.code_file.set(fname)
            #### leocomment self.code_loaded forcément à True car ask_code verifie 
            """ self.code_loaded = True
            self.configure_interface() """

    def ask_data(self):
            # raise NotImplementedError()
            fname = tkinter.filedialog.askopenfilename(filetypes=[('Codix data file', '*.cdx')],
                                                    initialdir=os.path.expanduser('~'))
            if U.is_valid_filename(fname): 
                self.read_data(fname)
            else:
                tkinter.messagebox.showinfo('Cannot load', 'Cannot load %s file' % fname)

    def read_data(self, fname):
            with open(fname, 'r') as ff:
                data = json.load(ff)
            self.application.data_file.set(fname)
            self.application.code_file.set('Retrieved from data file')
            self.application.container.update(data)
            self.application.parse_code(self.container['code'])
            self.code_loaded = True
            print(self.application.container)

            # Quickly deals with non existent file
            # First: load media
            mfile = Path(self.application.container['media'])
            if mfile.is_file():
                self.application.read_media(self.application.container['media'])
            else:
                tkinter.messagebox.showinfo('Problem with media file', 
                                            'Cannot find media file')
            self.data_loaded = True
            self.application.start_processing()

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 
        self.code_label.configure(background=colortuple[1])
        self.media_label.configure(background=colortuple[1])
        self.data_label.configure(background=colortuple[1])
