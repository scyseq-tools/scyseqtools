import os
import json
import tkinter
import configparser
import tkinter.simpledialog
import tkinter.messagebox
from datetime import datetime
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
        self.interface_button = tkinter.Button(self, text = "Dark mode", command = self.application.change_interface)
        self.interface_button.grid(row=3, column = 1, sticky = 'w')

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
        # self.strdata = {}
        self.coding_comments = []
        self.elements = [self]
        #self.nb_records = 0


    def load_code(self, fname):

        with open(fname, 'r') as ff:
            rawcode = json.load(ff)

        period = rawcode['period']
        if period is None:
            mode = "continuous"
        else:
            mode = "regular"

        sites = rawcode['sites']
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

#            # Coding frame imposes the mode and period of player Control
#            self.application.control.mode = self.player_mode.get()
#            self.application.control.period = self.period_display.get()
            
            # get times and steps lists for data
            # raise NotImplementedError # FIXME: resume session not implemented yet

#            self.control.set_time(self.container['times'][0], msg='Start processing')
#            self.current_step = 0
#            self.max_step = len(self.container['times'])
#            
        else: # starts a new session
            self.application.context = "initial"
#            # Coding frame imposes the mode and period of player Control
#            self.application.control.mode = self.player_mode.get()
#            self.application.control.period = self.period_display.get()
            # Set initial time
            self.init_data()


    def init_data(self):
        panellist = self.coding_frame.panels
        for pan in panellist:
            self.data[pan.name] = {}
            # self.strdata[pan.name] = {}
            for cname, v in pan.coding.items():
                # self.strdata[pan.name][cname] = []
                self.data[pan.name][cname] = []

        print(self.data)
        # print(self.strdata)

    def display_codes(self, time_step):
        panellist = self.coding_frame.panels
        for pan in panellist:
            # pan.name = recording site
            for cname, v in pan.coding.items():
#            # cname = code_name
                if time_step == 0 or \
                    (time_step == self.application.times_length-1 and \
                    self.coding_length == self.application.times_length-2):
                    local_str = '-'
                else:
                    idx = self.data[pan.name][cname][time_step-1]
                    local_str = self.encoding[pan.name][cname][idx]
                v['var'].set(local_str)

        if time_step == 0 or \
            (time_step == self.application.times_length-1 and \
            self.coding_length == self.application.times_length-2):
            comment = ''
        else :
            comment = self.coding_comments[time_step-1]
       
        self.coding_frame.comment.set(comment)
        

#    def erase_codes(self):
#        panellist = self.framework.coding_frame.panels
#        for pan in panellist:
#            # pan.name = recording site
#            for cname, v in pan.coding.items():
#            # cname = code_name
#                v['var'].set('')
#        self.framework.coding_frame.comment.set('')

    def record_state(self):
        """
        Record a step
        """
        panellist = self.coding_frame.panels
        comments = self.application.container['comments']
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
            if self.application.time_step <= self.coding_length :
                # Replace previous symbols / comments
                self.set_data(method='replace')
            else :
                # Append new symbol / comment
                
                self.set_data(method='append')
            




#            print(self.data)
#            print(self.strdata)
#            print(self.coding_comments)

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
                    # self.strdata[pan.name][cname].append(symbol) # FIXME
                    self.data[pan.name][cname].append(intval) # FIXME
                elif method == "replace":
                    # Replace previous symbols
                    # self.strdata[pan.name][cname][time_step-1] = symbol # FIXME
                    self.data[pan.name][cname][time_step-1] = intval # FIXME
                else: # raise error?
                    pass

        # deal with coding comments
        local_comment = self.coding_frame.comment.get()
        if method == "append":
            self.coding_comments.append(local_comment)
        elif method == "replace":
            self.coding_comments[time_step-1] = local_comment

    @property
    def coding_length(self):
        if len(self.data) == 0 :
            return 0
        else :
            panellist = self.coding_frame.panels
            lseq = [self.data[site.name][code] for site in panellist 
                                            for code in site.coding.keys()]
            assert (all([len(s) == len(lseq[0]) for s in lseq]))

            return len(lseq[0])

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 

    def config_processing_buttons(self,st):
        self.coding_frame.record_but.configure(state=st)
        self.coding_frame.comment_ent.configure(state=st)
        for panel in self.coding_frame.panels:
            for k, v in panel.coding.items():
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
        # application = parent.application
        self.parent = parent
        
        sites = list(encoding.keys())
        sites.sort()
        self.panels = [Panel(parent=self, name=site, codes=encoding[site]) for site in sites]

        # Set the panels on several rows and columns according to panel_max
        # panels per row. Better ergonomy when ther is a lot of recording sites. 
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
                                               # command=application.record_state)
                                               command=parent.record_state)
        self.record_but.grid(column=panel_max+1, row=0, rowspan=2, sticky=U.sticky_all)

class Panel(tkinter.LabelFrame):

    def __init__(self, parent, name, codes):
        tkinter.LabelFrame.__init__(self, parent)
        self.name = name
        self.configure(text=name, padx=10, pady=10, labelanchor='n')
        
        max_symbols = max([len(codes[k]) for k in codes.keys()])
        nb_code = len(codes)
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

        tkinter.LabelFrame.__init__(self, parent)

        self.configure(text='Specifications', padx=10, pady=10)
        
        # application = parent.application
        self.parent = parent

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

        self.mode_ent = tkinter.Entry(self, 
                                      textvariable=parent.player_mode, 
                                      disabledbackground=disabled_bg,
                                      state=tkinter.DISABLED,
                                      width=21)
        self.mode_ent.grid(column=1, row=1, sticky=tkinter.W)

        period_lab = tkinter.Label(self, text='Step: ')
        period_lab.grid(column=2, row=1)
        self.period_ent = tkinter.Entry(self, 
                                      # textvariable=application.period_display,
                                      textvariable=parent.period_display,
                                      disabledbackground=disabled_bg,
                                      state=tkinter.DISABLED,
                                      width=5)
        self.period_ent.grid(column=3, row=1, sticky=tkinter.W)
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
                                         command=self.parent.start_processing)
        self.start_but.grid(row=0, column=5, rowspan=4, sticky=U.sticky_all)
