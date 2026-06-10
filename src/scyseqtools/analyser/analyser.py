"""
A Tk client for symbolic analysis
"""

from scyseqtools.analyser.methods import Method
from scyseqtools.analyser.symbolix import Symbolix

import os
import sys
import inspect
import pathlib

import tkinter
import tkinter.filedialog
import tkinter.messagebox

import Pmw

# sys.path.append('/home/zarpe/scikits-symbolic/symbolic')
from scyseq import io as IO

__version__ = '0.1'
__author__ = 'L. Pezard'
__licence__ = 'GPL'

# PLATFORM = sys.platform
ANALYZERDIR = 'analyzer_files'


def _analyzer_dir_for(data_dir):
    """
    Return the analyser working directory for a selected data directory.
    """
    parent_dir = os.path.split(data_dir)[0]
    return os.path.join(parent_dir, ANALYZERDIR)


def _load_codix_appstate(data_dir, file_tuple):
    """
    Load selected Codix files and build the application state.
    """
    data = {}
    sites = []
    codes = {}

    for fname in file_tuple:

        fid = os.path.join(data_dir, fname)
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

        data[fname] = candidates

    return {'files': list(file_tuple), 'sites': sites, 'codes': codes,
            'data': data}


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
        self.dir_but = tkinter.Button(config_frame, text='Choose data directory',
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
        self.methods = [self.kappa_tool]
        self.methods.extend([Method(*m, self) for m in available_meth])
        self._set_startup_window_size()

    def _set_startup_window_size(self):
        """
        Size the startup window from the largest fully-built notebook page.
        """
        self.notebook.setnaturalsize()
        self.update_idletasks()

        width = min(self.winfo_reqwidth(), self.winfo_screenwidth())
        height = min(self.winfo_reqheight(), self.winfo_screenheight())

        self.geometry(f'{width}x{height}')
        self.minsize(width, height)

    def get_directory(self):
        """
        returns the selected directory
        """
        initialdir = "/home/zarpe/Documents/tests_scyseqtools/data"

        outdir = tkinter.filedialog.askdirectory(initialdir=initialdir)
        if not outdir:
            return

        #self.filelist = os.listdir(self.ddir.get())
        # self.available.setlist(self.filelist)
        try:
            filelist = os.listdir(outdir)
        except OSError as exc:
            tkinter.messagebox.showerror(title='Could not list directory',
                                         message=str(exc))
            return

        self.ddir.set(outdir)
        self.available.setlist(filelist)
        self.selected.setvalue('')

    def load_file(self):
        """
        Loads the data file

        Puts all the data in memory maybe this is not a good idea...
        """
        data_dir = self.ddir.get()
        if not data_dir:
            tkinter.messagebox.showwarning(title='No directory selected',
                    message='Choose a data directory before selecting files.')
            return

        file_tuple = self.available.getcurselection()
        if not file_tuple:
            tkinter.messagebox.showwarning(title='No file selected',
                    message='Select at least one data file to load.')
            return

        try:
            appstate = _load_codix_appstate(data_dir, file_tuple)
        except Exception as exc:
            tkinter.messagebox.showerror(title='Could not load data file',
                                         message=str(exc))
            return

        cwd = _analyzer_dir_for(data_dir)
        try:
            pathlib.Path(cwd).mkdir(exist_ok=True)
        except OSError as exc:
            tkinter.messagebox.showerror(title='Could not create working directory',
                                         message=str(exc))
            return

        self.cwd = cwd
        self.data = appstate['data']
        self.selected.setvalue('\n'.join(file_tuple))

        for method in self.methods:
            method.update_state(appstate)

######################################################################

if __name__ == '__main__':
    application = Application()
    application.mainloop()
