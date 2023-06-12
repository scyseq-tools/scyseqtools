# -*- encoding:utf8 -*-
"""
A Tk client for web services served by Ladon
"""
import os
import sys
import json
import tkinter
import Pmw
# import tkFileDialog
import tkinter.filedialog

from ladon.clients.jsonwsp import JSONWSPClient
from methods import Method

__version__ = '0.1'
__author__ = 'L. Pezard'
__licence__ = 'GPL'

PLATFORM = sys.platform

SERVICE = 'http://localhost:8081/symbolix/jsonwsp/description'

class Application(tkinter.Tk):

    def __init__(self):
	# Create and pack the NoteBook.
        tkinter.Tk.__init__(self)
        Pmw.initialise(self)
        
        self.service = tkinter.StringVar()
        self.service.set(SERVICE)

        self.data = {} # data[file][...]
        #self.appstate = {}

        self.ddir = tkinter.StringVar()
        self.ddir.set('')
#        self.filelist = tkinter.StringVar()
#        self.filelist.set('')
        self.methods = []
        self.filelist = []
        self.selectedlist = []
        # self.sitelist = tkinter.StringVar()
        # self.codelist = tkinter.StringVar()

        self.json_client = None

        self.notebook = Pmw.NoteBook(self)
        self.notebook.pack(fill = 'both', expand = 1, padx = 10, pady = 10)
        
        # Add the "Configuration" page to the notebook.
        config_frame = self.notebook.add('Configuration')
        self.notebook.tab('Configuration').focus_set()
        
        service_lab = tkinter.Label(config_frame, text='Service: ')
        service_ent = tkinter.Entry(config_frame, textvariable=self.service,
                                    state=tkinter.NORMAL, 
                                    disabledbackground='white',
                                    width=50)
        service_but = tkinter.Button(config_frame, text='Get methods',
                                     command=self.get_methods)
        service_lab.grid(column=0, row=0)
        service_ent.grid(column=1, row=0)
        service_but.grid(column=2, row=0)

        dir_lab = tkinter.Label(config_frame, text='Directory')
        dir_ent = tkinter.Entry(config_frame, textvariable=self.ddir,
                                    state=tkinter.NORMAL, 
                                    disabledbackground='white',
                                    width=50)
        dir_but = tkinter.Button(config_frame, text='Choose directory',
                                     command=self.get_directory)
        dir_lab.grid(column=0, row=1)
        dir_ent.grid(column=1, row=1)
        dir_but.grid(column=2, row=1)
        
        grp = Pmw.Group(config_frame, tag_text='Files')
        grp.grid(row=2, column=0, columnspan=3)
        self.available = Pmw.ScrolledListBox(grp.interior(),
                                             items=self.filelist,
                                             labelpos='nw',
                                             label_text='Available files')
        self.available.configure(listbox_selectmode='multiple',
                                 listbox_exportselection=False)
        self.available.grid(row=2, column=1)
        file_but = tkinter.Button(grp.interior(), text="Select file(s)",
                                  command=self.load_file)
        file_but.grid(row=2, column=2)

        self.selected = Pmw.ScrolledText(grp.interior(), 
                               labelpos='nw',
                               label_text='Selected files')
        self.selected.grid(row=2, column=3)

        quit_but = tkinter.Button(config_frame, text='Quit', command=self.quit)
        quit_but.grid(column=0, row=4)

        self.notebook.setnaturalsize()

    def get_methods(self):
        """
        Ask the service about methods so build the rest of the interface
        """
        self.json_client = JSONWSPClient(self.service.get())
        list_of_methods = self.json_client.list_methods()
        self.methods = [Method(name, self) for name in list_of_methods]

    def get_directory(self):
        #outdir = tkFileDialog.askdirectory()
        outdir = tkinter.filedialog.askdirectory()
        self.ddir.set(outdir)
        self.filelist = os.listdir(self.ddir.get())
        self.available.setlist(self.filelist)
        self.selected.setvalue('')
        
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
            fid = open(os.path.join(self.ddir.get(), fname), 'r')
            wholedata = json.load(fid)
            fid.close()
            candidate = wholedata['data']
            candidate = dict((k.lower(), v) for k,v in candidate.items())
            csites = list(candidate.keys())
            ccodes = {}
            for site in csites:
                candidate[site] = dict((k.lower(), v) 
                                  for k, v in candidate[site].items())
                ccodes[site] = list(candidate[site].keys())
            # Check that files are compatible
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
            self.data[fname] = candidate

        appstate = {'files': list(file_tuple), 'sites': sites, 'codes': codes,
                    'data': self.data}
#         print appstate
        # print appstate
        # FIXME: if self.methods = [] messagebox
        for method in self.methods:
            method.update_state(appstate)


######################################################################

# Create demo in root window for testing.
if __name__ == '__main__':
    application = Application()
    application.mainloop()

