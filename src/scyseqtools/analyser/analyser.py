"""
A Tk client for symbolic analysis
"""

from scyseqtools.analyser.kappa import KappaTool
from scyseqtools.analyser.methods import Method
from scyseqtools.analyser.synchronization import SynchronizationTool
from scyseqtools.analyser.symbolix import Symbolix

import os
import sys
import inspect
import pathlib
import copy

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
    metadata = {}
    sites = []
    codes = {}

    for fname in file_tuple:

        fid = os.path.join(data_dir, fname)
        record = IO.read_codix(fid, data_only=False)
        candidates = record['data']
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
        metadata[fname] = {
            key: copy.deepcopy(value)
            for key, value in record.items()
            if key != 'data'
        }

    return {'files': list(file_tuple), 'sites': sites, 'codes': codes,
            'data': data, 'metadata': metadata}


def _empty_appstate():
    """
    Return an empty application state for unloaded data.
    """
    return {'files': [], 'sites': [], 'codes': {}, 'data': {},
            'metadata': {}}


def _append_unique(current, additions):
    """
    Return current plus additions while preserving first-seen order.
    """
    outfiles = []
    seen = set()
    for fname in list(current) + list(additions):
        if fname not in seen:
            outfiles.append(fname)
            seen.add(fname)
    return outfiles


class CheckboxFileList(tkinter.LabelFrame):
    """
    A scrollable list of filenames with one checkbox per row.
    """

    def __init__(self, master, label_text, width=320, height=200):
        tkinter.LabelFrame.__init__(self, master, text=label_text)

        self.items = []
        self.variables = {}

        self.canvas = tkinter.Canvas(self, width=width, height=height,
                                     borderwidth=0, highlightthickness=0)
        self.frame = tkinter.Frame(self.canvas)
        self.yscroll = tkinter.Scrollbar(self, orient=tkinter.VERTICAL,
                                         command=self.canvas.yview)
        self.xscroll = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL,
                                         command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.yscroll.set,
                              xscrollcommand=self.xscroll.set)
        self.window = self.canvas.create_window((0, 0), window=self.frame,
                                                anchor='nw')

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.yscroll.grid(row=0, column=1, sticky='ns')
        self.xscroll.grid(row=1, column=0, sticky='ew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame.bind('<Configure>', self._update_scrollregion)

    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def setlist(self, items):
        """
        Replace the visible filenames and clear checkbox selection.
        """
        for child in self.frame.winfo_children():
            child.destroy()

        self.items = list(items)
        self.variables = {}

        for row, item in enumerate(self.items):
            variable = tkinter.BooleanVar(master=self, value=False)
            checkbutton = tkinter.Checkbutton(self.frame, text=item,
                                              variable=variable,
                                              anchor='w', justify='left')
            checkbutton.grid(row=row, column=0, sticky='w')
            self.variables[item] = variable

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.frame.update_idletasks()
        self._update_scrollregion()

    def getcurselection(self):
        """
        Return filenames with checked boxes in visible order.
        """
        return tuple(
            item for item in self.items
            if self.variables[item].get()
        )

    def clear_selection(self):
        """
        Clear all checked boxes.
        """
        for variable in self.variables.values():
            variable.set(False)


class Application(tkinter.Tk):
    """
    The main frame for the analyzer application
    """

    def __init__(self):
#       Create and pack the NoteBook.
        tkinter.Tk.__init__(self)
        Pmw.initialise(self)

        self.data = {} # data[file][...]
        self.metadata = {}
        self.ddir = tkinter.StringVar()
        self.ddir.set('')
        self.cwd = None
        self.selected_files = []

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
        grp.grid(row=2, column=0, columnspan=3, sticky='nsew')
        grp.interior().grid_columnconfigure(0, weight=1)
        grp.interior().grid_columnconfigure(2, weight=1)
        grp.interior().grid_rowconfigure(2, weight=1)

        self.available = CheckboxFileList(grp.interior(),
                                          label_text='Available files',
                                          width=320, height=300)
        self.available.setlist(filelist)
        self.available.grid(row=2, column=0, sticky='nsew')

        button_frame = tkinter.Frame(grp.interior())
        button_frame.grid(row=2, column=1, padx=10, sticky=tkinter.N)
        self.file_but = tkinter.Button(button_frame, text="Select file(s)",
                                       command=self.load_file)
        self.file_but.grid(row=0, column=0, pady=(35, 0), sticky='ew')

        self.selected = CheckboxFileList(grp.interior(),
                                         label_text='Selected files',
                                         width=320, height=300)
        self.selected.grid(row=2, column=2, sticky='nsew')

        remove_frame = tkinter.Frame(grp.interior())
        remove_frame.grid(row=2, column=3, padx=10, sticky=tkinter.N)
        self.remove_but = tkinter.Button(remove_frame, text='Remove selected',
                                         command=self.remove_selected_files)
        self.remove_but.grid(row=0, column=0, pady=(35, 0), sticky='ew')

        quit_but = tkinter.Button(config_frame, text='Quit', command=self.quit)
        quit_but.grid(column=0, row=4)

        self.kappa_tool = KappaTool(self)
        self.synchronization_tool = SynchronizationTool(self)
        available_meth = inspect.getmembers(Symbolix, predicate=inspect.isfunction)
        self.methods = [self.kappa_tool, self.synchronization_tool]
        self.methods.extend([Method(*m, self) for m in available_meth])
        self._set_startup_window_size()

    def _update_methods(self, appstate):
        """
        Push loaded-file state to every analysis tab.
        """
        for method in self.methods:
            method.update_state(appstate)

    def _apply_appstate(self, appstate):
        """
        Store loaded data and refresh file widgets and analysis tabs.
        """
        self.selected_files = appstate['files']
        self.data = appstate['data']
        self.metadata = appstate['metadata']
        self.selected.setlist(self.selected_files)
        self.selected.clear_selection()
        self.available.clear_selection()
        self._update_methods(appstate)

    def _clear_loaded_files(self):
        """
        Clear selected files, loaded data, and dependent analysis tabs.
        """
        self.cwd = None
        self._apply_appstate(_empty_appstate())

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
        self._clear_loaded_files()

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

        selected_available = self.available.getcurselection()
        if not selected_available:
            tkinter.messagebox.showwarning(title='No file selected',
                    message='Select at least one data file to load.')
            return

        file_tuple = tuple(_append_unique(self.selected_files,
                                          selected_available))
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
        self._apply_appstate(appstate)

    def remove_selected_files(self):
        """
        Remove checked files from the loaded selection.
        """
        selected_for_removal = self.selected.getcurselection()
        if not selected_for_removal:
            tkinter.messagebox.showwarning(title='No selected file checked',
                    message='Check at least one selected file to remove.')
            return

        removal_set = set(selected_for_removal)
        remaining_files = [
            fname for fname in self.selected_files
            if fname not in removal_set
        ]

        if not remaining_files:
            self._clear_loaded_files()
            return

        try:
            appstate = _load_codix_appstate(self.ddir.get(),
                                            tuple(remaining_files))
        except Exception as exc:
            tkinter.messagebox.showerror(title='Could not load data file',
                                         message=str(exc))
            return

        self._apply_appstate(appstate)

######################################################################

if __name__ == '__main__':
    application = Application()
    application.mainloop()
