import tkinter
from datetime import datetime
from tkinter.colorchooser import askcolor

import utils as U

bd = 2 # borderwidth
coding_bg = 'cyan' # information background
disabled_bg = 'light gray' # disabled background
relief = 'groove' # ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

panel_max = 5

class FrameworkFrame(tkinter.LabelFrame):

    def __init__(self, application, encoding):
        tkinter.LabelFrame.__init__(self, application)
        self.configure(background=coding_bg, 
                       borderwidth=bd, 
                       padx=20, pady=20, 
                       relief=relief,
                       text='Coding framework: ', font=('bold',))
        self.grid(columnspan=2,
                  row=1)
        self.application = application

        self.spec_frame = SpecificationFrame(self)  
        self.spec_frame.grid(sticky=U.sticky_all)

        self.coding_frame = CodingFrame(self, encoding=encoding)
        self.coding_frame.grid(column=0, columnspan=3, sticky=U.sticky_all)
        self.disable_codes()
        self.bind('<Button-3>', self.change_color)

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 

    def disable_codes(self):
        self.coding_frame.record_but.configure(state=tkinter.DISABLED)
        self.coding_frame.comment_ent.configure(state=tkinter.DISABLED)
        for panel in self.coding_frame.panels:
            for k, v in panel.coding.items():
                for button in v['buttons']:
                    button.configure(state=tkinter.DISABLED)

    def enable_codes(self):
        self.coding_frame.record_but.configure(state=tkinter.NORMAL)
        self.coding_frame.comment_ent.configure(state=tkinter.NORMAL)

## FIXME: what is this try/except for?
#        try:
#            self._root().display_codes(step=self._root().current_step - 1)
#        except IndexError:
#            pass
####
        for panel in self.coding_frame.panels:
            for k, v in panel.coding.items():
                for button in v['buttons']:
                    button.configure(state=tkinter.NORMAL)

    def disable_specifications(self):
        self.spec_frame.person_ent.configure(state=tkinter.DISABLED)
        self.spec_frame.comment_ent.configure(state=tkinter.DISABLED)
        self.spec_frame.start_but.configure(state=tkinter.DISABLED)

    def enable_specifications(self):
        self.spec_frame.person_ent.configure(state=tkinter.NORMAL)
        self.spec_frame.comment_ent.configure(state=tkinter.NORMAL)
        self.spec_frame.start_but.configure(state=tkinter.NORMAL)

class CodingFrame(tkinter.LabelFrame):

    def __init__(self, parent, encoding): # coding is a dict
        tkinter.LabelFrame.__init__(self, parent)
        self.configure(text='Codes', padx=10, pady=10)
        application = parent.application
        
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
                                               command=application.record_state)
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
        application = parent.application

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
                                      textvariable=application.player_mode, 
                                      disabledbackground=disabled_bg,
                                      state=tkinter.DISABLED,
                                      width=21)
        self.mode_ent.grid(column=1, row=1, sticky=tkinter.W)

        period_lab = tkinter.Label(self, text='Step: ')
        period_lab.grid(column=2, row=1)
        self.period_ent = tkinter.Entry(self, 
                                      textvariable=application.period_display,
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
                                         command=application.start_processing)
        self.start_but.grid(row=0, column=5, rowspan=4, sticky=U.sticky_all)

# FIXME: is it useful to pause / stop recording?
#        stop_but = Tkinter.Button(self, text='Stop\nrecording',
#                                                  command=application.stop_record)
#        stop_but.grid(row=0, column=6, rowspan=1, sticky=U.sticky_all)
