"""
Module to deal with parameters
"""
import re
import os
import tkinter

import scyseqtools.analyser.utils as U
from scyseqtools.analyser import symbolix

ITEMSEP = ' |,|-|;|:|/'

class Parameter():
    """
    Class to deal with different parameter types
    """
    def __init__(self, name, annotation, method):
        """
        Initialize interface and getters
        """
        self.name = name
        self.annotation = annotation
        # mframe = method.tab
        self.method = method
        mframe = self.method.tab
        self.frame = tkinter.LabelFrame(mframe, text=self.name)
        pframe = self.frame
        description = tkinter.LabelFrame(pframe, text='Description')

        tkinter.Label(description,
                text=' '.join(['Type:', str(annotation)])).grid()

#        tkinter.Label(description,
##                text='\n'.join(status['doc_lines'])).grid()
#        tkinter.Label(description,
##          text=' '.join(['Optional: ', str(status['optional'])])).grid()
        description.grid(sticky=tkinter.W)

        if annotation is symbolix.Data:
            self.value = Sequence()
            self.tk = InputSequence(pframe, variable=self.value)
        else:
            self.value = tkinter.StringVar()
            self.tk = tkinter.Entry(pframe, textvariable=self.value)

        self.tk.grid()
        self.gdata = {}
        self.gfiles = []

    def get(self):
        """
        How to get the value of the parameter
        """
        if self.annotation is symbolix.Data:
            outval = self.value.get()
            s_site, s_code = outval['site'], outval['code']
            retval = []
            for fichier in self.method.selected_files:
                seq = self.gdata[fichier][s_site][s_code]
                retval.append({'filename': os.path.basename(fichier),
                               'sitename': s_site,
                               'codename': s_code,
                               'sequence': seq})
        else:
            val = self.value.get()
            tmp = [c for c in re.split(ITEMSEP, val) if c!='']
            print('tmp: ', tmp)
            print(self.annotation)
            if len(tmp) == 1:
                if self.annotation is str:
                    print("string case")
                    retval = tmp[0]
                elif self.annotation is int:
                    print("int case")
                    try:
                        retval = int(tmp[0])
                    except:
                        raise ValueError(f'Bad parameter {self.name}')
                else:
                    raise ValueError(f'Bad parameter {self.name}')
            else:
                if self.annotation == list[str]:
                    print("list string case")
                    retval = tmp
                elif self.annotation == list[int]:
                    print("list int case")
                    try:
                        retval = [int(s) for s in tmp]
                    except:
                        raise ValueError(f'Bad parameter {self.name}')
                else:
                    raise ValueError(f'Bad parameter {self.name}')

        return retval

    def update(self, state):
        """
        Update the interface when loading a file has some consequences
        """
        self.gdata = state['data']
        self.gfiles = state['files']

        if self.annotation is symbolix.Data:
            self.tk.update(state)
            self.value.update(state)

class Sequence(object):
    """
    List of sequences with a get method
    """

    def __init__(self):
        """
        All set to None
        """
        self.site = None
        self.code = None
        self.sget = None
        self.cget = None

    def get(self):
        """
        get the value
        """
        site_index = self.sget.curselection()[0]
        s_site = self.gsites[int(site_index)]
        code_index = self.cget.curselection()[0]
        s_code = self.gcodes[s_site][int(code_index)]

        return {'site': s_site, 'code': s_code}

    def update(self, state):
        """
        set the value
        """
        self.gsites = state['sites']
        self.gcodes = state['codes']

class InputSequence(tkinter.Frame):
    """
    Input of list of sequences
    """

    def __init__(self, master, variable):
        """
        Widget for input a sequence
        """
        self.sites = []
        self.codes = {}

        def set_code():
            """
            Local function to set the code when th recording site is selected
            """
            site_index = s_choice.curselection()[0]
            codes = self.codes[self.sites[int(site_index)]]
            self.codelist.set(' '.join(codes))

        tkinter.Frame.__init__(self, master)
        self.sitelist = tkinter.StringVar()
        self.codelist = tkinter.StringVar()

        s_lb, s_choice = U.listbox(self, 'Site', self.sitelist, multiple=False)
        s_lb.grid(column=1, row=0)

        c_lb, c_choice = U.listbox(self, 'Code', self.codelist, multiple=False)
        c_lb.grid(column=2, row=0)

        site_but = tkinter.Button(self, text='Select', command=set_code)
        site_but.grid(column=1, row=1)

        # this is the trick to get access to the listboxes
        variable.sget = s_choice
        variable.cget = c_choice

    def update(self, state):
        """
        Update
        """
        self.sites = state['sites']
        self.codes = state['codes']
        self.sitelist.set(' '.join(self.sites))
        self.codelist.set('')
