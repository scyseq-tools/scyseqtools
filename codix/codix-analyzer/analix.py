"""
A Tk client for symbolic analysis
"""

from methods import Method
from symbolix import Symbolix

import os
import sys
import inspect
import pathlib

import tkinter
import tkinter.filedialog
import tkinter.messagebox

import Pmw

sys.path.append('/home/zarpe/scikits-symbolic/symbolic')
import iosymb as IO

__version__ = '0.1'
__author__ = 'L. Pezard'
__licence__ = 'GPL'

# PLATFORM = sys.platform
ANALYZERDIR = 'analyzer_files'

class Application(tkinter.Tk):
    """
    The main frame for the analyzer application
    """

    def __init__(self):
#       Create and pack the NoteBook.
        tkinter.Tk.__init__(self)
        Pmw.initialise(self)

        self.data = {} # data[file][...]
        self.ddir = tkinter.StringVar()
        self.ddir.set('')
        self.cwd = None

        # self.filelist = []
        filelist = []
#        self.selectedlist = []

        self.notebook = Pmw.NoteBook(self)
        self.notebook.pack(fill = 'both', expand = 1, padx = 10, pady = 10)
        # Add the "Configuration" page to the notebook.
        config_frame = self.notebook.add('Configuration')
        self.notebook.tab('Configuration').focus_set()

        dir_lab = tkinter.Label(config_frame, text='Directory')
        dir_ent = tkinter.Entry(config_frame, textvariable=self.ddir,
                                    state=tkinter.NORMAL,
                                    disabledbackground='white',
                                    width=50)
        self.dir_but = tkinter.Button(config_frame, text='Choose directory',
                                     command=self.get_directory)
        dir_lab.grid(column=0, row=1)
        dir_ent.grid(column=1, row=1)
        self.dir_but.grid(column=2, row=1)

        grp = Pmw.Group(config_frame, tag_text='Files')
        grp.grid(row=2, column=0, columnspan=3)
        self.available = Pmw.ScrolledListBox(grp.interior(),
                                             # items=self.filelist,
                                             items=filelist,
                                             labelpos='nw',
                                             label_text='Available files')
        self.available.configure(listbox_selectmode='multiple',
                                 listbox_exportselection=False)
        self.available.grid(row=2, column=1)
        self.file_but = tkinter.Button(grp.interior(), text="Select file(s)",
                                  command=self.load_file)
        self.file_but.grid(row=2, column=2)

        self.selected = Pmw.ScrolledText(grp.interior(),
                               labelpos='nw',
                               label_text='Selected files')
        self.selected.grid(row=2, column=3)

        quit_but = tkinter.Button(config_frame, text='Quit', command=self.quit)
        quit_but.grid(column=0, row=4)

        self.notebook.setnaturalsize()

        available_meth = inspect.getmembers(Symbolix, predicate=inspect.isfunction)
        self.methods = [Method(*m, self) for m in available_meth]

    def get_directory(self):
        """
        returns the selected directory
        """
        initialdir = "/home/zarpe/Documents/tests_codix/data"

        outdir = tkinter.filedialog.askdirectory(initialdir=initialdir)
        self.ddir.set(outdir)
        wdy = os.path.split(outdir)[0]
        cwd = os.path.join(wdy, ANALYZERDIR)
        if not os.path.exists(cwd):
            if tkinter.messagebox.askokcancel(\
                       title='Create working directory?',
                       message=f'Create {cwd}?'):
                pathlib.Path(cwd).mkdir()
#            else:
#                cwd = wdy
        tkinter.messagebox.showinfo(title='Current working directory',
                       message=f'Files will be saved in folders of {cwd}')
        self.cwd = cwd

        #self.filelist = os.listdir(self.ddir.get())
        # self.available.setlist(self.filelist)
        filelist = os.listdir(self.ddir.get())
        self.available.setlist(filelist)
        self.selected.setvalue('')
        self.dir_but.config(state='disabled')

    def load_file(self):
        """
        Loads the data file

        Puts all the data in memory maybe this is not a good idea...
        """
        file_tuple = self.available.getcurselection()
        self.selected.setvalue('\n'.join(file_tuple))

        self.data = {} # clear previous data
        sites = []
        codes = {}

        for fname in file_tuple:

            fid = os.path.join(self.ddir.get(), fname)
            candidates = IO.read_codix(fid) # data only = True
            csites = list(candidates.keys())
            ccodes = {site: list(candidates[site].keys()) for site in csites}

            # FIXME: Check that files are compatible
            if sites == [] or csites == sites:
                sites = csites
                if codes == {}:
                    codes = ccodes
                elif any(c1.lower() != c2.lower() \
                         for c1, c2 in zip(ccodes, codes)):
                    # FIXME: make a message box
                    raise ValueError('Incompatible codes')
            elif any(c1.lower() != c2.lower() \
                     for c1, c2 in zip(csites, sites)):
                    # FIXME: make a message box
                raise ValueError('Incompatible sites')

            self.data[fname] = candidates

        appstate = {'files': list(file_tuple), 'sites': sites, 'codes': codes,
                    'data': self.data}

        self.file_but.config(state='disabled')

        for method in self.methods:
            method.update_state(appstate)

######################################################################

if __name__ == '__main__':
    application = Application()
    application.mainloop()
