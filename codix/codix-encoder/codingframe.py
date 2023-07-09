import json
import tkinter
import tkinter.simpledialog
import tkinter.messagebox
from datetime import datetime
from tkinter.colorchooser import askcolor


import utils as U

bd = 2 # borderwidth
coding_bg = 'cyan' # information background
disabled_bg = 'light gray' # disabled background
relief = 'groove' # ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

panel_max = 5

class FrameworkFrame(tkinter.LabelFrame):

    def __init__(self, parent, filename):

        incode = self.load_code(filename)
        encoding = incode['code']
        player = incode['player']

        tkinter.LabelFrame.__init__(self, parent)
        self.configure(background=coding_bg, 
                       borderwidth=bd, 
                       padx=20, pady=20, 
                       relief=relief,
                       text='Coding framework: ', font=('bold',))
        self.grid(columnspan=2, row=1)

        self.application = parent
        
        # variables related to player ***from coding file***
        self.player_mode = tkinter.StringVar(value=player['mode'])
        self.period_display = tkinter.StringVar(value=str(player['period']))

        self.spec_frame = SpecificationFrame(self)  
        self.spec_frame.grid(sticky=U.sticky_all)

        self.coding_frame = CodingFrame(parent=self, encoding=encoding)
        self.coding_frame.grid(column=0, columnspan=3, sticky=U.sticky_all)
        self.config_processing_buttons('disabled')
        self.bind('<Button-3>', self.change_color)

        # self.application.state['code_loaded'] = True

        self.data = {}

    def load_code(self, fname):

        with open(fname, 'r') as ff:
            encoding = json.load(ff)

        period = encoding['period']
        if period is None:
            mode = "continuous"
        else:
            mode = "regular"

        sites = encoding['sites']
        codes = encoding['codes']
        codeframe = {}
        for site, scodes in encoding['sites'].items():
            data_site = {}
            code_site = {}
            for lcode in scodes:
                data_site.update({lcode: {'alphabet': codes[lcode], 'seq': []}})
                code_site.update({lcode: codes[lcode]})
            # lpcomment application related 
            # self.container['data'].update({site: data_site})
            codeframe[site] = code_site
       
        outcode = {'code': codeframe, 'player': ({'mode': mode, 'period': period})}

        return outcode

    def start_processing(self):
        """
        Start processing and fill the container with:
        - observer, date, comments
        - start time
        - code and media file names => INFOFRAME!!!
        - encoding specifications 
        """
        self.spec_frame.start_but.config(state='disabled')
        self.application.context = "processing"
        
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

        if self.application.state['data_loaded']: # resume session
            # get times and steps lists for data
            raise NotImplementedError # FIXME: resume session not implemented yet

#            self.control.set_time(self.container['times'][0], msg='Start processing')
#            self.current_step = 0
#            self.max_step = len(self.container['times'])
#            
        else: # starts a new session
            # Coding frame imposes the mode and period of player Control
            self.application.control.mode = self.player_mode.get()
            self.application.control.period = self.period_display.get()
            # Set initial time
            self.application.time_step = 0

    def init_data(self):
        panellist = self.coding_frame.panels
        for pan in panellist:
            self.data[pan.name] = {}
            for cname, v in pan.coding.items():
                self.data[pan.name][cname] = []

        print(self.data)

#    def display_codes(self, step):
#        # self.framework.config_processing_buttons('normal')
#        panellist = self.framework.coding_frame.panels
#        for pan in panellist:
#            # pan.name = recording site
#            for cname, v in pan.coding.items():
#            # cname = code_name
#                sequence = self.container['data'][pan.name][cname]['seq']
#                local_int = sequence[step]
#                local_str = self.int2str[pan.name][cname][local_int]
#                v['var'].set(local_str)
#        comment = self.container['comments'][step]
#        self.framework.coding_frame.comment.set(comment)
    
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
            tmp_symbols = []
            for pan in panellist:
                # print pan.name # rec_site
                for cname, v in pan.coding.items():
                    tmp_symbols.append(v['var'].get())

            if not all([s != '' for s in tmp_symbols]): 
                tkinter.messagebox.showinfo('Code missing', 'A code is missing')
                return
            
            self.config_processing_buttons('disabled')

            # Second passage to record the symbols
#            panellist = self.coding_frame.panels
#            for pan in panellist:
#                self.data[pan.name] = {}
#                for cname, v in pan.coding.items():
#                    self.data[pan.name][cname] = []

            lseq = [self.data[site.name][code] for site in panellist 
                                               for code in site.coding.keys()]
            assert (all([len(s) == len(lseq[0]) for s in lseq]))

            coding_length = len(lseq[0])
            time_step = self.application.time_step

            print('coding_length: ', coding_length)
            print('Time length: ', self.application.max_step)
            print('Time step: ', time_step)

            if coding_length == self.application.max_step - 2:
                # Append new symbol
                for pan in panellist:
                    for cname in pan.coding.keys():
                        self.data[pan.name][cname].append(coding_length) # FIXME
            else:
                # Replace previous symbols
                for pan in panellist:
                    for cname in pan.coding.keys():
                        self.data[pan.name][cname][time_step-1] = "m" # FIXME
            print(self.data)

            local_comment = self.coding_frame.comment.get()
            comments.append(local_comment)
            self.application.context = 'processing'
#            sequence = []
#
#            print('RECORD THE DATA...')
#            self.application.time_step = 1
            
#            for pan in panellist:
#                # print pan.name # rec_site
#                for cname,v in pan.coding.items():
#                    # sequence = self.application.container['data'][pan.name][cname]['seq']
#                    tsymbol = tmp_symbol[pan.name][cname]
#                    print(sequence, tsymbol)
#                    #sequence.append(self.str2int[pan.name][cname][tsymbol])
#                    sequence.append([pan.name][cname][tsymbol])
#                print(str(sequence))

            # FIXME: deal with steps_idx
            # self.coding_steps.append('data')

#            print('Times', self.application.control.times)
#            print('Current time index', self.application.control.current_time_idx)
#            print('Coding steps', self.coding_steps)
#            self.config_processing_buttons('disabled')
#
#            self.application.control.play_but.config(state='normal')
#            self.application.control.back_but.config(state='normal')

#            else:
#                print('else')
#                times[self.application.current_step] = self.application.current_time
#                comments[self.application.current_step ] = local_comment
#                for pan in panellist:
#                    # print pan.name # rec_site
#                    for cname,v in pan.coding.items():
#                        sequence = self.application.container['data'][pan.name][cname]['seq']
#                        tsymbol = tmp_symbol[pan.name][cname]
#                        print(sequence, tsymbol)
#                        #sequence[self.application.current_step ] = self.str2int[pan.name][cname][tsymbol]
#                        sequence[self.application.current_step ] = [pan.name][cname][tsymbol]
##        try:
##            self.application.display_codes(self.current_step)
##        except IndexError:
##            self.application.erase_codes()
##        self.spec_frame.disable_codes()
##        print(self.application.container)
##        self.application.save_data()

        else: # continuous coding
            raise NotImplementedError

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

## FIXME: what is this try/except for?
#        try:
#            self._root().display_codes(step=self._root().current_step - 1)
#        except IndexError:
#            pass
####

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

    



# FIXME: is it useful to pause / stop recording?
#        stop_but = Tkinter.Button(self, text='Stop\nrecording',
#                                                  command=application.stop_record)
#        stop_but.grid(row=0, column=6, rowspan=1, sticky=U.sticky_all)


    


