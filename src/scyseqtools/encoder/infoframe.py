import os
import json

# from pathlib import Path # Only used once in a comment...
# import os.path as opath

import tkinter
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
from tkinter.colorchooser import askcolor

from scyseqtools.encoder.config import load_encoder_config
import scyseqtools.encoder.utils as U

#### leomodif : on met ces variables dans config.ini directement

#bd = 2 # borderwidth
#info_bg = 'yellow' # information background
#disabled_bg = 'light grey' # disabled background
#relief = 'groove'
#filename_width = 30
# relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']


def coded_sample_lengths(data):
    """
    Return the lengths of all coded sequences in a ScySeqTools data container.
    """
    lengths = []
    for site_data in data.values():
        if not isinstance(site_data, dict):
            continue
        for sequence in site_data.values():
            if hasattr(sequence, "__len__"):
                lengths.append(len(sequence))
    return lengths


def resume_step_count(data, comments=None):
    """
    Infer how many regular-coding steps can safely be resumed.
    """
    lengths = coded_sample_lengths(data)
    if lengths:
        return min(lengths)
    if comments:
        return len(comments)
    return 0


def normalize_resume_data(record):
    """
    Normalize loaded session state without relying on the number of times.
    """
    data = record.get("data", {})
    comments = list(record.get("comments", []))
    times = list(record.get("times", []))
    count = resume_step_count(data, comments)

    if len(comments) < count:
        comments.extend([""] * (count - len(comments)))
    elif len(comments) > count:
        comments = comments[:count]

    if not times and count:
        period = record.get("code", {}).get("period")
        step = int(float(period) * 1000) if period else 0
        times = [step * index for index in range(count + 1)]

    return {
        "times": times,
        "comments": comments,
        "recorded_steps": set(range(1, count + 1)),
    }

class InfoFrame(tkinter.LabelFrame):

    def __init__(self, parent, states=[None, None, None]):
        tkinter.LabelFrame.__init__(self, parent)
        self.application = parent

        config = load_encoder_config(
            self.application.cwd, required_sections=("infoframe",)
        )

        bd = config['infoframe'].getint('borderwidth')
        info_bg = config['infoframe']['background']
        relief = config['infoframe']['relief']
        disabled_bg = config['infoframe']['disabled_bg']
        filename_width = config['infoframe'].getint('filename_width')
        self.configure(background=info_bg, borderwidth=bd, padx=20, pady=20,
                       relief=relief, text='Information: ', font=(tkinter.font.BOLD,))

        self.grid_columnconfigure(1, weight=1)

        self.code_file = tkinter.StringVar()
        self.media_file = tkinter.StringVar()
        self.data_file = tkinter.StringVar()
        self.directory_file = tkinter.StringVar()

        # Directory
        self.directory_label = tkinter.Label(self, text='Directory: ', background = info_bg)
        self.directory_label.grid(row=1, column=0, sticky=tkinter.W)
        self.directory_msg = tkinter.Label(self, text= 'Please load file', background=info_bg)
        self.directory_msg.configure(anchor=tkinter.W)
        self.directory_msg.grid(row=1, column=1, sticky=U.sticky_all)

        # Media File
        self.media_label = tkinter.Label(self, text='Media file: ', background=info_bg)
        self.media_label.grid(row=2, column=0, sticky=tkinter.W)
        media_msg = tkinter.Entry(self, textvariable=self.media_file,
                                        state=tkinter.DISABLED,
                                        width=filename_width,
                                        disabledbackground=disabled_bg)
        media_msg.grid(row=2, column=1, sticky=U.sticky_all)
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
        code_msg.grid(row=3, column=1, sticky=U.sticky_all)
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
        data_msg.grid(row=4, column=1, sticky=U.sticky_all)
        self.data_load = tkinter.Button(self, text='Load',
                                        state=states[2],
                                        command=self.ask_data)
        self.data_load.grid(row=4, column=2, sticky=tkinter.W)

# Interface elements
        self.elements = [self, self.directory_label, self.media_label, self.data_label, self.code_label, self.directory_msg]

        self.bind('<Button-3>', self.change_color)

    def data_folder(self):
        """
        Return the working directory's data folder, creating it if needed.
        """
        return U.ensure_subdirectory(self.application.cwd, 'data')

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

                directoryFile = '/'.join(fname.split('/')[:-2])
                self.directory_msg.config(text = directoryFile)
                self.media_file.set(self.set_name_of(fname))

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
        code_folder = self.data_folder()
        code_filetypes = [('Code file', '*.cod'), ('New code', '*.jod')]
        fname = tkinter.filedialog.askopenfilename(filetypes= code_filetypes,
                                            initialdir=code_folder)
        if U.is_valid_filename(fname, ext='.jod'):
            self.code_file.set(self.set_name_of(fname))
            self.application.make_coding_frame(fname)
        else:
            tkinter.messagebox.showinfo('Cannot load code file', 'Cannot load %s file' % fname)
            self.ask_code()
        self.code_load.config(state='disabled')

    def ask_data(self):

        #fname = "/home/leo/scyseqtools/scyseqtools/scyseq-encoder/new_record"

        data_folder = self.data_folder()
        data_filetypes = [('ScySeqTools data file', '*.cdx'), ('All files', '*.*')]

        fname = tkinter.filedialog.askopenfilename(filetypes= data_filetypes,
                                                   initialdir= data_folder)
        if U.is_valid_filename(fname):
            self.read_data(fname)
            self.data_file.set(self.set_name_of(fname))
            self.data_load.config(state='disabled')
        else:
            tkinter.messagebox.showinfo('Cannot load code file', " Media file doesn't exist or not in directory %s "  % fname)
            self.ask_data()

    def set_name_of(self, st):# return the localisation of the file after the principal directory
        file_directory = self.directory_msg.cget('text')
        index = st.find(file_directory)
        return st[index+len(file_directory):]

    def read_data(self, fname):
        with open(fname, 'r') as ff:
            data = json.load(ff)

        self.application.state['data_loaded'] = True
        print(data)
        # lpcomment: we do this in newcode BUT user can change the name of the
        # code file and this is not written in the codefile
        code = data['code']['filename']
        media = data['media']
        fileDirectory = '/'.join(media.split('/')[:-2])
        if os.path.exists(media) and U.is_valid_media(media):
            self.directory_msg.config(text = fileDirectory)
            self.media_file.set(self.set_name_of(media))
            self.application.make_media_player(media)
        else :
            tkinter.messagebox.showinfo('Cannot load media file', " Media file doesn't exist or not in directory %s "  % media)
        if os.path.exists(code): # and U.is_valid_filename(code):
            self.code_file.set(self.set_name_of(code))
            self.application.make_coding_frame(code)
        else :
            tkinter.messagebox.showinfo('Cannot load code file', " Code file doesn't exist or not in directory %s "  % code)
# lpcomment: everything at the good place in the container
        resume_state = normalize_resume_data(data)
        data['times'] = resume_state['times']
        data['comments'] = resume_state['comments']
        self.application.container.update(data)
        self.application.recorded_steps = resume_state['recorded_steps']
        print(self.application.recorded_steps)
        print(self.application.container)


    def save_data(self):
        if self.data_file.get() == '':
            self.save_as()
        else:
            self.save()

    def save(self):
        filename = self.directory_msg.cget("text") + self.data_file.get()
        datafile = open(filename, 'w')
        json.dump(self.application.container, datafile)
        datafile.close()
        print('Data saved in %s' % filename)

    def save_as(self):
        fname = self.data_file.get()
        data_folder = self.data_folder()
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
            self.save_data()

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1])
        self.code_label.configure(background=colortuple[1])
        self.media_label.configure(background=colortuple[1])
        self.data_label.configure(background=colortuple[1])
        self.directory_label.configure(background=colortuple[1])
        self.directory_msg.configure(background=colortuple[1])
