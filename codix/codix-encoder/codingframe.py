"""
This module deals with all the encoding procedure:
- builds the interface according to the coding framework
- displays the codes
- records the codes and pass it to the application.
"""

import os
import json
import configparser
from datetime import datetime

import tkinter
import tkinter.simpledialog
import tkinter.messagebox
from tkinter.colorchooser import askcolor

import utils as U

bd = 2 # borderwidth
coding_bg = 'lightsteelblue' # information background
dark_bg = 'dimgray'
light_bg = 'lightsteelblue'
disabled_bg = 'light gray' # disabled background
relief = 'groove' # ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']
panel_max = 5
CONFIG = 'config.ini'


class FrameworkFrame(tkinter.LabelFrame):

    def __init__(self, parent, filename):

# FIXME: this is complicated to have rawcode and incode...
        rawcode, incode = self.load_code(filename)
        self.encoding = incode['code']
        player = incode['player']
        self.application = parent


        # config = configparser.ConfigParser()
        # if os.path.exists(os.path.join(self.application.cwd, CONFIG)):
        #     config.read(os.path.join(self.application.cwd, CONFIG))
        # else:
        #     config.read(CONFIG)

        # bd = config['codingframework']['borderwidth']
        # coding_bg = config['codingframework']['background']
        # relief = config['codingframework']['relief']
        # disabled_bg = config['codingframework']['disabled_bg']
        # panel_max = config['codingframework']['panel_max']


        tkinter.LabelFrame.__init__(self, parent)
        self.configure(background=coding_bg,
                       borderwidth=bd,
                       padx=20, pady=20,
                       relief=relief,
                       text='Coding framework: ', font=('bold',))
        self.grid(columnspan=2, row=2)

        # Interface color
        self.interface_button = tkinter.Button(self, text = "Dark mode",
                                               command = self.application.change_interface)
        self.interface_button.grid(row=3, column = 0, sticky = 'w')

#FIXME: Not sure this is the best place...
        self.application.container['code'] = rawcode

        # variables related to player BUT ***taken from coding file***
        self.player_mode = tkinter.StringVar(value=player['mode'])
        self.period_display = tkinter.StringVar(value=str(player['period']))

        self.spec_frame = SpecificationFrame(self)
        self.spec_frame.grid(sticky=U.sticky_all)

        self.coding_frame = CodingFrame(parent=self, encoding=self.encoding)
        self.coding_frame.grid(column=0, columnspan=2, sticky=U.sticky_all)
        self.config_processing_buttons('disabled')
        self.bind('<Button-3>', self.change_color)

        self.dark_bg = dark_bg
        self.light_bg = light_bg
        self.data = {}
        self.coding_comments = []
        self.elements = [self]

    def load_code(self, fname):

        with open(fname, 'r') as ff:
            rawcode = json.load(ff)

        period = rawcode['period']
        if period is None:
            mode = "continuous"
        else:
            mode = "regular"

        # sites = rawcode['sites']
        codes = rawcode['codes']
        codeframe = {}
        for site, scodes in rawcode['sites'].items():
            code_site = {}
            for lcode in scodes:
                code_site.update({lcode: codes[lcode]})
            codeframe[site] = code_site

        outcode = {'code': codeframe, 'player': {'mode': mode, 'period': period}}

        return rawcode, outcode

    def start_processing(self):
        """
        Start processing and fill the container with:
        - observer, date, comments
        - start time
        - code and media file names => INFOFRAME!!!
        - encoding specifications
        """

        self.spec_frame.start_but.config(state='disabled')
        # ----
        # Get and set specifications before disabling entries
        observer = self.spec_frame.person.get()
        while observer == '' or observer is None :
            name = tkinter.simpledialog.askstring('Please identify', 'Please identify yourself')
            observer = name
        self.spec_frame.person.set(observer)

        date = datetime.now().strftime('%c')
        self.spec_frame.timestamp.set(date)
        comment = self.spec_frame.comment.get()

        self.application.container['history'].append((date, observer, comment))

        self.config_specifications('disabled')
        # ----
        # Coding frame imposes the mode and period of player Control
        self.application.control.mode = self.player_mode.get()
        self.application.control.period = self.period_display.get()

        if self.application.state['data_loaded']: # resume session
            self.application.context = "resume"

        else: # starts a new session
            self.application.context = "initial"
            self.init_data()

    def init_data(self):
        panellist = self.coding_frame.panels
        for pan in panellist:
            self.data[pan.name] = {}
            #for cname, v in pan.coding.items():
            for cname in pan.coding.keys():
                self.data[pan.name][cname] = []
        print(self.data)

    def display_codes(self, time_step):
        """
        Displays the codes and comments
        """
        panellist = self.coding_frame.panels

        if self.application.time_step in self.application.recorded_steps:
            comment = self.coding_comments[time_step-1]
            self.coding_frame.comment.set(comment)

            for pan in panellist:
                # pan.name = recording site
                for cname, v in pan.coding.items():
                    idx = self.data[pan.name][cname][time_step-1]
                    local_str = self.encoding[pan.name][cname][idx]
                    v['var'].set(local_str)
        else:
            comment = ''
            self.coding_frame.comment.set(comment)

            for pan in panellist:
                # pan.name = recording site
                for cname, v in pan.coding.items():
                    local_str = '-'
                    v['var'].set(local_str)

    def record_state(self):
        """
        Record a step
        """
        panellist = self.coding_frame.panels
        # comments = self.application.container['comments']
        mode = self.application.control.mode

        if mode == 'regular': # regular sampling
            # First passage for checking presence of all symbols
            tmp_symbols = [v['var'].get() for pan in panellist
                                          for v in pan.coding.values()]

            if not all([s != '-' for s in tmp_symbols]):
                tkinter.messagebox.showinfo('Code missing', 'A code is missing')
                return

            self.config_processing_buttons('disabled')

            # Second passage to record the symbols
            if self.application.time_step not in self.application.recorded_steps :
                # Append new symbol / comment
                self.set_data(method='append')
            else:
                # Replace previous symbols / comments
                self.set_data(method='replace')

            # Since recorded_steps is a set, duplicated time_step are not taken
            # into account.
            self.application.recorded_steps.add(self.application.time_step)
            self.application.container['data'] = self.data
            self.application.container['comments'] = self.coding_comments
            print(self.application.container)

            self.application.info.save_data()
            self.application.context = 'processing'

        else: # continuous coding
            raise NotImplementedError

    def set_data(self, method):
        panellist = self.coding_frame.panels
        time_step = self.application.time_step
        for pan in panellist:
            for cname in pan.coding.keys():
                symbol = pan.coding[cname]['var'].get()
                intval = self.encoding[pan.name][cname].index(symbol)
                if method == "append":
                    # Append new symbol
                    self.data[pan.name][cname].append(intval)
                elif method == "replace":
                    # Replace previous symbols
                    self.data[pan.name][cname][time_step-1] = intval
                else: # raise error?
                    pass

        # deal with coding comments
        local_comment = self.coding_frame.comment.get()
        if method == "append":
            self.coding_comments.append(local_comment)
        elif method == "replace":
            self.coding_comments[time_step-1] = local_comment


    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1])

    def config_processing_buttons(self,st):
        self.coding_frame.record_but.configure(state=st)
        self.coding_frame.comment_ent.configure(state=st)
        for panel in self.coding_frame.panels:
            # for k, v in panel.coding.items():
            for v in panel.coding.values():
                for button in v['buttons']:
                    button.configure(state=st)

    def config_specifications(self,st):
        self.spec_frame.person_ent.configure(state=st)
        self.spec_frame.comment_ent.configure(state=st)
        self.spec_frame.start_but.configure(state=st)


class CodingFrame(tkinter.LabelFrame):

    def __init__(self, parent, encoding): # coding is a dict
        tkinter.LabelFrame.__init__(self, parent)
        self.configure(text='Codes', padx=10, pady=10)
        self.parent = parent

        sites = list(encoding.keys())
        sites.sort()
        self.panels = [Panel(parent=self, name=site, codes=encoding[site]) for site in sites]

        # Set the panels on several rows and columns according to panel_max
        # panels per row. Better ergonomy when there is a lot of recording sites.
        for no_col, panel in enumerate(self.panels):
            col = no_col % panel_max
            row = no_col // panel_max
            panel.rowconfigure(row, weight=3)
            panel.columnconfigure(col, weight=1)
            panel.grid(row=row, column=col, sticky=U.sticky_all)

        comment_frame = tkinter.LabelFrame(self, text='Comment: ')
        comment_frame.grid(row=col+1, column=0, columnspan=len(self.panels),
                                            sticky=U.sticky_all)
        self.comment = tkinter.StringVar()
        self.comment_ent = tkinter.Entry(comment_frame,
                                         textvariable=self.comment,
                                         disabledbackground=disabled_bg,
                                         width=60)
        self.comment_ent.grid(sticky=U.sticky_all)

        self.record_but = tkinter.Button(self, text="Record",
                                               height=2,
                                               command=parent.record_state)
        self.record_but.grid(column=panel_max+1, row=0, rowspan=2, sticky=U.sticky_all)

class Panel(tkinter.LabelFrame):

    def __init__(self, parent, name, codes):
        tkinter.LabelFrame.__init__(self, parent)
        self.name = name
        self.configure(text=name, padx=10, pady=10, labelanchor='n')

        max_symbols = max([len(codes[k]) for k in codes.keys()])
        # nb_code = len(codes)
        code_names = list(codes.keys())
        code_names.sort()

        local_col = 0
        self.coding = {}

        for code_name in code_names:
            self.coding[code_name] = {}
            self.coding[code_name]['var'] = tkinter.StringVar()

            label = tkinter.Label(self, text=code_name, padx=10, pady=10)
            label.grid(row=0, column=local_col, sticky=U.sticky_all)

            symbols = codes[code_name]
            self.coding[code_name]['buttons'] = [tkinter.Button(self, text=symbol,
                   command=lambda s=self, n=code_name, kk=symbol: s.set_msg(kk,n))
                                                 for symbol in symbols]
            for nb_symbols, sbut in enumerate(self.coding[code_name]['buttons']):
                sbut.grid(row=nb_symbols+1, column=local_col, sticky=U.sticky_all)


            msg = tkinter.Entry(self, state=tkinter.DISABLED,
                                      width=10,
                                      disabledbackground=disabled_bg,
                                      disabledforeground='black',
                                      textvariable=self.coding[code_name]['var'])
            msg.grid(row=max_symbols+1, column=local_col, sticky=U.sticky_all)
            local_col += 1

    def set_msg(self, symbol, code_name):
        """Show the selected code in the message box
        """
        self.coding[code_name]['var'].set(symbol)

class SpecificationFrame(tkinter.LabelFrame):

    def __init__(self, parent):

        # self.parent = parent
        tkinter.LabelFrame.__init__(self, parent)

        self.configure(text='Specifications', padx=10, pady=10)


        # date in local format
        self.timestamp = tkinter.StringVar()
        self.timestamp.set(datetime.now().strftime('%c'))

        date_lab = tkinter.Label(self, text='Date: ')
        date_lab.grid(column=0, row=0, sticky=tkinter.W)
        self.date_ent = tkinter.Entry(self,
                                      textvariable=self.timestamp,
                                      state=tkinter.DISABLED,
                                      disabledbackground=disabled_bg,
                                      width=21)
        self.date_ent.grid(column=1, row=0, sticky=tkinter.W)

        # observer name
        self.person = tkinter.StringVar()

        person_lab = tkinter.Label(self, text='Observer: ')
        person_lab.grid(row=0, column=2, sticky=tkinter.E)
        self.person_ent = tkinter.Entry(self,
                                        textvariable=self.person,
                                        disabledbackground=disabled_bg,
                                        width=15)
        self.person_ent.grid(row=0, column=3, sticky=tkinter.W, columnspan=4)

        # coding / player  mode
        mode_lab = tkinter.Label(self, text='Coding mode: ')
        mode_lab.grid(column=0, row=1, sticky=tkinter.W)

        mode_ent = tkinter.Entry(self,
                                      textvariable=parent.player_mode,
                                      disabledbackground=disabled_bg,
                                      state=tkinter.DISABLED,
                                      width=21)
        mode_ent.grid(column=1, row=1, sticky=tkinter.W)

        period_lab = tkinter.Label(self, text='Step: ')
        period_lab.grid(column=2, row=1)
        period_ent = tkinter.Entry(self,
                                      textvariable=parent.period_display,
                                      disabledbackground=disabled_bg,
                                      state=tkinter.DISABLED,
                                      width=5)
        period_ent.grid(column=3, row=1, sticky=tkinter.W)
        # time units is given in seconds - mandatory
        unit_lab = tkinter.Label(self, text='second(s)')
        unit_lab.grid(column=4, row=1, sticky=tkinter.W)

        # Comments for the coding session
        self.comment = tkinter.StringVar()
        comment_lab = tkinter.Label(self, text='Comment: ')
        comment_lab.grid(row=3, column=0, sticky=tkinter.W)
        self.comment_ent = tkinter.Entry(self, textvariable=self.comment,
                                         disabledbackground=disabled_bg,
                                         width=45)
        self.comment_ent.grid(row=3, column=1, columnspan=4, sticky=tkinter.W)

        # Start processing / coding / recording button...
# FIXME: place this button in a better way.
        self.start_but = tkinter.Button(self, text='Start\nprocessing',
                                         # command=self.parent.start_processing)
                                         command=parent.start_processing)
        self.start_but.grid(row=0, column=5, rowspan=4, sticky=U.sticky_all)
