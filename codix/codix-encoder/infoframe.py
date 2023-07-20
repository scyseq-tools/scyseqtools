import os
import json
import configparser

# from pathlib import Path # Only used once in a comment...
# import os.path as opath

import tkinter
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
from tkinter.colorchooser import askcolor

import utils as U


#### leomodif : on met ces variables dans config.ini directement

#bd = 2 # borderwidth
#info_bg = 'yellow' # information background
#disabled_bg = 'light grey' # disabled background
#relief = 'groove'
#filename_width = 30
CONFIG = 'config.ini'
# relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

class InfoFrame(tkinter.LabelFrame):

    def __init__(self, parent, states=[None, None, None]):
        tkinter.LabelFrame.__init__(self, parent)
        self.application = parent

        config = configparser.ConfigParser()
        if os.path.exists(os.path.join(self.application.cwd, CONFIG)):
            config.read(os.path.join(self.application.cwd, CONFIG))
        else:
            config.read(CONFIG)

        bd = config['infoframe']['borderwidth']
        info_bg = config['infoframe']['background']
        relief = config['infoframe']['relief']
        disabled_bg = config['infoframe']['disabled_bg']
        filename_width = config['infoframe']['filename_width']

        self.configure(background=info_bg, borderwidth=bd, padx=20, pady=20, 
                       relief=relief, text='Information: ', font=(tkinter.font.BOLD,))

        self.grid(column=1, row=0)

        
        self.code_file = tkinter.StringVar()
        self.media_file = tkinter.StringVar()
        self.data_file = tkinter.StringVar()
        self.directory_file = tkinter.StringVar()
        

        # Directory
        self.directory_label = tkinter.Label(self, text='Directory: ', background = info_bg)
        self.directory_label.grid(row =1, column =0)
        self.directory_msg = tkinter.Label(self, text= 'Please load file', background=info_bg)
        self.directory_msg.grid(row=1, column = 1,)
        

        
        # Media File
        self.media_label = tkinter.Label(self, text='Media file: ', background=info_bg)
        self.media_label.grid(row=2, column=0, sticky=tkinter.W)
        media_msg = tkinter.Entry(self, textvariable=self.media_file, 
                                        state=tkinter.DISABLED,
                                        width=filename_width, 
                                        disabledbackground=disabled_bg)
        media_msg.grid(row=2, column=1, sticky=tkinter.W)
        self.media_load = tkinter.Button(self, text='Load', state=states[0],
                                         command=self.ask_media)
        self.media_load.grid(row=2, column=2, sticky=tkinter.W)

        # Code File
        self.code_label = tkinter.Label(self, text='Code file: ', 
                                         background=info_bg)
        self.code_label.grid(row=3, column=0, sticky=tkinter.W)
        
        code_msg = tkinter.Entry(self, textvariable=self.code_file,
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg)
        code_msg.grid(row=3, column=1, sticky=tkinter.W)
        self.code_load = tkinter.Button(self, text='Load',
                                        state=states[1],
                                        command=self.ask_code)
        self.code_load.grid(row=3, column=2, sticky=tkinter.W)

        # Data File
        self.data_label = tkinter.Label(self, text='Data file: ', 
                                         background=info_bg)
        self.data_label.grid(row=4, column=0, sticky=tkinter.W)
        data_msg = tkinter.Entry(self, textvariable=self.data_file, 
                                       state=tkinter.DISABLED, 
                                       width=filename_width,
                                       disabledbackground=disabled_bg) 
        data_msg.grid(row=4, column=1, sticky=tkinter.W)
        self.data_load = tkinter.Button(self, text='Load',
                                        state=states[2],
                                        command=self.ask_data)
        self.data_load.grid(row=4, column=2, sticky=tkinter.W)
        
        self.bind('<Button-3>', self.change_color)


    def ask_media(self):
        """Load media file
        """
        is_valid = False
        while not is_valid:
            # We suppose that media files are in cwd/media folder
            media_folder = os.path.join(os.path.expanduser(self.application.cwd), 'media') 
            fname = tkinter.filedialog.askopenfilename(initialdir=media_folder)
            # self.loaded_media=False # Not Useful?
            if U.is_valid_media(fname):
                is_valid = True
                # mediaFile = fname.split('/')
                # self.media_file.set(mediaFile[-1])
                self.media_file.set(self.set_name_of(fname))

                directoryFile = '/'.join(fname.split('/')[:-1])                
                self.directory_msg.config(text = directoryFile)

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
        if self.application.control.state in ['c_playing', 's_playing']:
            self.application.control.dopause()
       
        # lpcomment: 
        # Finally, I don't like .jod extension. maybe go back to .cod?
        code_folder = os.path.expanduser(self.application.cwd)
        code_filetypes = [('Code file', '*.cod'), ('New code', '*.jod')]
        fname = tkinter.filedialog.askopenfilename(filetypes= code_filetypes,
                                            initialdir=code_folder)
        if U.is_valid_filename(fname, ext='.jod'):
            self.code_file.set(self.set_name_of(fname))
            self.application.make_coding_frame(fname)
        else:
            tkinter.messagebox.showinfo('Cannot load code file', 'Cannot load %s file' % fname)
        self.code_load.config(state='disabled')

    def ask_data(self):
        
        #fname = "/home/leo/codix-suite/codix/codix-encoder/new_record"

        data_folder = os.path.join(os.path.expanduser(self.application.cwd), 'data')
        data_filetypes = [('Codix data file', '*.cdx'), ('All files', '*.*')]
        
        fname = tkinter.filedialog.askopenfilename(filetypes= data_filetypes,
                                                   initialdir= data_folder)
        if U.is_valid_filename(fname): 
            self.data_file.set(self.set_name_of(fname))
            self.read_data(fname)
            self.data_load.config(state='disabled')
        else:
            tkinter.messagebox.showinfo('Cannot load code file', " Media file doesn't exist or not in directory %s "  % fname)

    def set_name_of(self, st):
        file = st.split('/')
        return file[-1]


    def read_data(self, fname):
        with open(fname, 'r') as ff:
            data = json.load(ff)

        self.application.state['data_loaded'] = True
        print(data)
        # lpcomment: we do this in newcode BUT user can change the name of the
        # code file and this is not written in the codefile
        code = data['code']['filename']
        media = data['media']
        fileDirectory = '/'.join(media.split('/')[:-1])
        if os.path.exists(media) and U.is_valid_media(media):
            self.media_file.set(self.set_name_of(media))
            self.directory_msg.config(text = fileDirectory)
            self.application.make_media_player(media)
        else :
            tkinter.messagebox.showinfo('Cannot load media file', " Media file doesn't exist or not in directory %s "  % media)
        if os.path.exists(code): # and U.is_valid_filename(code):
            self.code_file.set(self.set_name_of(code))
            self.application.make_coding_frame(code)
        else :
            tkinter.messagebox.showinfo('Cannot load code file', " Code file doesn't exist or not in directory %s "  % code)     
# lpcomment: everything at the good place in the container
        self.application.container.update(data)
        print(self.application.container)
        

    def save_data(self):
        if self.data_file.get() == '':
            self.save_as()
        else:
            self.save()


    def save(self):
        filename = self.directory_msg.cget("text") +'/data/'+ self.data_file.get() 
        datafile = open(filename, 'w')
        json.dump(self.application.container, datafile)
        datafile.close()
        print('Data saved in %s' % filename)
    
    def save_as(self):
        fname = self.data_file.get()
        data_folder = os.path.join(os.path.expanduser(self.application.cwd), 'data')
        filename = \
        tkinter.filedialog.asksaveasfilename(initialdir=data_folder)

        # FIXME: does not work if file already exists
        if U.is_valid_filename(filename):
            if not filename.endswith('.cdx'):
                filename += '.cdx'
            datafile = open(filename, 'w')
            json.dump(self.application.container, datafile)
            datafile.close()
            print('Data saved in %s' % filename)
            self.data_file.set(self.set_name_of(filename))
# Do not exist any more in the menu
#            self.menu.fileMenu.entryconfig(8, state=tkinter.NORMAL) # Save
#            self.menu.fileMenu.entryconfig(9, state=tkinter.DISABLED) # Save as
        else:
            tkinter.messagebox.showinfo('File not saved', 'File has not been saved')

    

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 
        self.code_label.configure(background=colortuple[1])
        self.media_label.configure(background=colortuple[1])
        self.data_label.configure(background=colortuple[1])
        self.directory_label.configure(background=colortuple[1])
        self.directory_msg.configure(background=colortuple[1])
