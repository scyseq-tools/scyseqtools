import os
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import utils as U

from pathlib import Path # Only used once in a comment...
import tkinter.font
from tkinter.colorchooser import askcolor
# from playercontrol import PlayerControl

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

        self.configure(background=info_bg, borderwidth=bd, padx=20, pady=20, 
                       relief=relief, text='Information: ', font=(tkinter.font.BOLD,))
        self.grid(column=1, row=0)
        
        self.code_file = tkinter.StringVar()
        self.media_file = tkinter.StringVar()
        self.data_file = tkinter.StringVar()
        
        # Media File
        self.media_label = tkinter.Label(self, text='Media file: ', background=info_bg)
        self.media_label.grid(row=1, column=0, sticky=tkinter.W)
        media_msg = tkinter.Entry(self, textvariable=self.media_file, 
                                        state=tkinter.DISABLED,
                                        width=filename_width, 
                                        disabledbackground=disabled_bg)
        media_msg.grid(row=1, column=1, sticky=tkinter.W)
        self.media_load = tkinter.Button(self, text='Load', state=states[0],
                                         command=self.ask_media)
        self.media_load.grid(row=1, column=2, sticky=tkinter.W)

        # Code File
        self.code_label = tkinter.Label(self, text='Code file: ', 
                                         background=info_bg)
        self.code_label.grid(row=2, column=0, sticky=tkinter.W)
        code_msg = tkinter.Entry(self, textvariable=self.code_file,
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
        data_msg = tkinter.Entry(self, textvariable=self.data_file, 
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg) 
        data_msg.grid(row=3, column=1, sticky=tkinter.W)
        self.data_load = tkinter.Button(self, text='Load',
                                        state=states[2],
                                        command=self.ask_data)
        self.data_load.grid(row=3, column=2, sticky=tkinter.W)
        self.data_save = tkinter.Button(self, text='Save',
                                        command=self.save_data,
                                        state=tkinter.DISABLED)
        self.data_save.grid(row=3, column=3, sticky=tkinter.W)

        self.bind('<Button-3>', self.change_color)

    def ask_media(self):
        """Load media file
        """
        # fname = "/home/leo/Bureau/leo_dev/video/164360 (720p).mp4"
        fname = "/home/zarpe/Documents/videos_synchrony/vidéosynchrony/208_S2.MPG"  
        if os.path.exists(fname) and U.is_valid_media(fname):
            self.media_file.set(fname)
            self.application.make_media_player(fname)
        else:
            is_valid = False
            while not is_valid:
                fname = tkinter.filedialog.askopenfilename(
                                    initialdir=os.path.expanduser(self.application.cwd))
                # self.loaded_media=False # Not Useful?
                if U.is_valid_media(fname):
                    is_valid = True
                    self.media_file.set(fname)

                    self.application.make_media_player(fname)

                else:
                    tkinter.messagebox.showinfo('Cannot load media file', \
                                                "Cannot load %s file" % fname)
                    self.ask_media()

        self.media_load.config(state='disabled')
        self.code_load.config(state='normal')

    def ask_code(self):
        """Loading files defining a coding framework.
        Now only supports the new .jod (json) files
        """
        # if self.application.control.state == 'c_playing' or self.application.control.state == 's_playing':
        if self.application.control.state in ['c_playing', 's_playing']:
            self.application.control.dopause()
        
        fname = "test2.jod"
        if os.path.exists(fname):
            self.code_file.set(fname)
            self.application.make_coding_frame(fname)
        else :
            fname = tkinter.filedialog.askopenfilename(filetypes=[('New code', '*.jod')],
                                                initialdir=os.path.expanduser(self.application.cwd))
            if U.is_valid_filename(fname, ext='.jod'):
                self.code_file.set(fname)
                self.application.make_coding_frame(fname)
            else:
                tkinter.messagebox.showinfo('Cannot load code file', 'Cannot load %s file' % fname)

        self.code_load.config(state='disabled')

    def ask_data(self):
        raise NotImplementedError()
#            fname = tkinter.filedialog.askopenfilename(filetypes=[('Codix data file', '*.cdx')],
#                                                    initialdir=os.path.expanduser(self.application.cwd))
#            if U.is_valid_filename(fname): 
#                self.read_data(fname)
#            else:
#                tkinter.messagebox.showinfo('Cannot load', 'Cannot load %s file' % fname)
#
#    def read_data(self, fname):
#            with open(fname, 'r') as ff:
#                data = json.load(ff)
#            self.application.data_file.set(fname)
#            self.application.code_file.set('Retrieved from data file')
#            self.application.container.update(data)
#            self.application.parse_code(self.container['code'])
#            # self.code_loaded = True
#            print(self.application.container)
#
#            # Quickly deals with non existent file
#            # First: load media
#            mfile = Path(self.application.container['media'])
#            if mfile.is_file():
#                self.application.make_media_player(self.application.container['media'])
#            else:
#                tkinter.messagebox.showinfo('Problem with media file', 
#                                            'Cannot find media file')
#            self.data_loaded = True
#            self.application.start_processing()

    def save(self):
        filename = self.data_file.get()
        datafile = open(filename, 'w')
        json.dump(self.application.container, datafile)
        datafile.close()
        print('Data saved in %s' % filename)
    
    def save_as(self):
        filename = \
        tkinter.filedialog.asksaveasfilename(initialdir=os.path.expanduser(self.application.cwd))

        # FIXME: does not work if file already exists
        if U.is_valid_filename(filename):
            datafile = open(filename, 'w')
            json.dump(self.application.container, datafile)
            datafile.close()
            print('Data saved in %s' % filename)
            self.data_file.set(filename)
# Do not exist any more in the menu
#            self.menu.fileMenu.entryconfig(8, state=tkinter.NORMAL) # Save
#            self.menu.fileMenu.entryconfig(9, state=tkinter.DISABLED) # Save as
        else:
            tkinter.messagebox.showinfo('File not saved', 'File has not been saved')

    def save_data(self):
#        raise NotImplementedError
        if self.data_file.get() == '':
            self.save_as()
        else:
            self.save()

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 
        self.code_label.configure(background=colortuple[1])
        self.media_label.configure(background=colortuple[1])
        self.data_label.configure(background=colortuple[1])
