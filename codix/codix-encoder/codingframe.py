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

        self.application.state['code_loaded'] = True

    def load_code(self, fname):

        with open(fname, 'r') as ff:
            encoding = json.load(ff)

#        self.application.container['code'] = encoding
#        self.application.parse_code(encoding)
#        self.application.code_file.set(fname)
#        #### leocomment self.code_loaded forcément à True car ask_code verifie 
#        """ self.code_loaded = True
#        self.configure_interface() """

#    def parse_code(self, encoding):

#        self.get_mode_and_period(encoding)
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

#        # self.framework = FrameworkFrame(parent=self, encoding=codeframe)
#        self.framework = FrameworkFrame(parent=self, incode=outcode)
#        self.framework.grid(row=2, column=0, sticky=U.sticky_all)


    def start_processing(self):
        """
        Start processing and fill the container with:
        - observer, date, comments
        - start time
        - code and media file names
        - encoding specifications 
        """
        #self.application.current_step = 0
        self.application.context = "processing"
        self.spec_frame.start_but.config(state='disabled')
        #self.config_processing_buttons('normal')
#        self.control.config_buttons({self.control.play_but : 'disabled', 
#                                    self.control.back_but : 'disabled',
#                                    self.control.forward_but : 'disabled', 
#                                    self.control.mode_check : 'disabled',
#                                    self.control.period_ent : 'disabled'})
        

        observer = self.spec_frame.person.get()
        while observer == '' or observer is None :
            name = tkinter.simpledialog.askstring('Please identify', 'Please identify yourself')
            observer = name
            self.spec_frame.person.set(name)
        
        date = datetime.now().strftime('%c')
        self.spec_frame.timestamp.set(date)
        comment = self.spec_frame.comment.get()
        self.application.container['history'].append((date, observer, comment))

        # if self.application.data_loaded: # resume session
        if self.application.state['data_loaded']: # resume session
            raise NotImplementedError # FIXME: resume session not implemented yet

#            self.control.set_time(self.container['times'][0], msg='Start processing')
#            self.current_step = 0
#            self.max_step = len(self.container['times'])
#            
        else: # starts a new session

## lpcomment: les boutons doivent être désactivés au début. Ils ne sont activés
## qu'à la pause après la première période de "play".

            # self.application.container['media'] = self.media_file.get()

# Le coding frame doit imposer ses valeurs au player au moment du "start
# processing"

            self.application.control.mode = self.player_mode.get()
            self.application.control.period = self.period_display.get()

#            self.framework.config_specifications('disabled')

# FIXME: mode appartient au player mais pas à l'application
#            mode = self.player_mode.get()
# FIXME: change control for player?
#            mode = self.control.mode
#            if mode == 'regular': # regular sampling
#                #period = self.control.get_period()
#                period = self.control.period
#                if period is not None:
#                    self.freeze()
#                print('period: ', period)
#                assert(len(self.container['times']) == 0)
#                self.container['times'].append(self.current_time)
#                self.max_step = len(self.container['times']) - 1
#                self.current_step = 0
#                self.data_loaded = True
#                print(self.container)
#                self.info.data_save.configure(state=tkinter.NORMAL)
#    #                    if self.current_step == 0 or \
#    #                       self.control.player.get_state() == 3: # playing
#    #                    while self.control.player.get_state() != 5: # 5: Stopped
#    #                        print(self.control.player.get_state())
#    #                        # time.sleep(5)
#                if self.control._state == 'paused': 
#                    self.current_step += 1
#                    print("current step: ", self.current_step)
#    #                        self.config_processing_buttons('normal')
#            else:
#                raise NotImplementedError('Continuous coding is not implemented')
#            
#            self.framework.config_processing_buttons('normal')
#
#
#                # self.current_step = 0
#
##            if not self.data_loaded:
##                self.container['times'][0] = self.current_time
##                self.is_set_start_time = True
##                self.control.set_time(self.current_time, msg='Start processing')
##            else:
##                self.control.set_time(self.container['times'][0], msg='Start processing')
##            self.set_step(0)
##            self.is_recording = True
##
##            self.control.forward_but.configure(state=tkinter.NORMAL)
##            self.control.back_but.configure(state=tkinter.NORMAL)
##
##            FrameworkFrame.config_specifications('disabled')
##            self.info.code_load.configure(state=tkinter.DISABLED)
##            self.info.media_load.configure(state=tkinter.DISABLED)
##   #         self.menu.fileMenu.entryconfig(8, state=Tkinter.NORMAL) # Save
##            self.menu.fileMenu.entryconfig(9, state=tkinter.NORMAL) # Save as
##            self.info.data_save.configure(state=tkinter.NORMAL)
##                self.period_display.set(str(period))
##                self.dt = int(float(period) * 1000)
##                print('dt: ', self.dt)
##                self.control.step_check.select()
##                self.control.pause_but.configure(state=tkinter.DISABLED)
##                # can't go back 
##                self.control.back_but.configure(state=tkinter.DISABLED)
#                else:
#                    raise NotImplementedError('Continuous coding is not implemented')
##                self.player_mode.set('continuous')
##                self.control.step_check.deselect()
##                self.control.back_but.configure(state=Tkinter.DISABLED)
##            step = self.framework.spec_frame.step.get()
##            self.period_display.set(step)
##           #  self.freeze_step()
#
#                print('period: ', period)
#                self.data_loaded = True
#                assert(len(self.container['times']) == 0)
#                self.container['times'].append(self.current_time)
#                # self.current_step = 0
#
##            if not self.data_loaded:
##                self.container['times'][0] = self.current_time
##                self.is_set_start_time = True
##                self.control.set_time(self.current_time, msg='Start processing')
##            else:
##                self.control.set_time(self.container['times'][0], msg='Start processing')
##            self.set_step(0)
##            self.is_recording = True
##
##            self.control.forward_but.configure(state=tkinter.NORMAL)
##            self.control.back_but.configure(state=tkinter.NORMAL)
##
##            FrameworkFrame.config_specifications('disabled')
##            self.info.code_load.configure(state=tkinter.DISABLED)
##            self.info.media_load.configure(state=tkinter.DISABLED)
##   #         self.menu.fileMenu.entryconfig(8, state=Tkinter.NORMAL) # Save
##            self.menu.fileMenu.entryconfig(9, state=tkinter.NORMAL) # Save as
##            self.info.data_save.configure(state=tkinter.NORMAL)
#            while self.control.player.get_state() != 5: # 5: Stopped
#               if self.control.player.get_state() == 4: # 4: Paused
#                   self.framework.config_processing_buttons('normal')
#                   print(self.container)

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
#    
#    def erase_codes(self):
#        panellist = self.framework.coding_frame.panels
#        for pan in panellist:
#            # pan.name = recording site
#            for cname, v in pan.coding.items():
#            # cname = code_name
#                v['var'].set('')
#        self.framework.coding_frame.comment.set('')
#


                    

    def record_state(self):
        """
        Record a step
        """
        # local "pointers"
       
        
        panellist = self.coding_frame.panels
        times = self.application.container['times']
        comments = self.application.container['comments']
        self.application.control.play_but.config(state='normal')
        self.config_processing_buttons('disabled')

        #mode = self.player_mode.get()
        print(" Current step " , self.application.current_step)
        mode = self.application.control.mode
        if mode == 'regular': # regular sampling
            print('times', times)
            if self.application.current_step < 0: # Should not happen...
                tkinter.messagebox.showinfo('Before beginning', 'Before beginning')
                return
            
            elif self.application.current_step > len(times):
                tkinter.messagebox.showinfo('Discontinuous coding', 
                                      'Discontinuous coding')
                return
            else:
                # First passage for checking presence of all symbols
                tmp_symbol = {}
                for pan in panellist:
                    tmp_symbol[pan.name] = {}
                    # print pan.name # rec_site
                    for cname,v in pan.coding.items():
                    # k: code_name
                        symbol = v['var'].get()
                        # sequence = self.container['data'][pan.name][cname]['seq']
                        if symbol == '':
                            tkinter.messagebox.showinfo('Code missing', 'A code is missing')
                            return
                        else:
                            # sequence.append(self.str2int[pan.name][cname][symbol])
                            tmp_symbol[pan.name][cname] = symbol
                
                local_comment = self.coding_frame.comment.get()
                
                # self.config_processing_buttons('disabled')
                # Seconde passage to record the symbol
                print('ct_step', self.application.current_step, 'ct_time', self.application.current_time, 'time', times)

                if self.application.current_step == len(times):
                    print('==')
                    times.append(self.application.current_time)
                    comments.append(local_comment)
                    
                    for pan in panellist:
                        # print pan.name # rec_site
                        for cname,v in pan.coding.items():
                            sequence = self.application.container['data'][pan.name][cname]['seq']
                            tsymbol = tmp_symbol[pan.name][cname]
                            print(sequence, tsymbol)
                            #sequence.append(self.str2int[pan.name][cname][tsymbol])
                            sequence.append([pan.name][cname][tsymbol])
                        print(str(sequence))
                else:
                    print('else')
                    times[self.application.current_step] = self.application.current_time
                    comments[self.application.current_step ] = local_comment
                    for pan in panellist:
                        # print pan.name # rec_site
                        for cname,v in pan.coding.items():
                            sequence = self.application.container['data'][pan.name][cname]['seq']
                            tsymbol = tmp_symbol[pan.name][cname]
                            print(sequence, tsymbol)
                            #sequence[self.application.current_step ] = self.str2int[pan.name][cname][tsymbol]
                            sequence[self.application.current_step ] = [pan.name][cname][tsymbol]
            try:
                self.application.display_codes(self.current_step)
            except IndexError:
                self.application.erase_codes()
            self.spec_frame.disable_codes()
            print(self.application.container)
            self.application.save_data()

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

#        for panel in self.coding_frame.panels:
#            for k, v in panel.coding.items():
#                for button in v['buttons']:
#                    button.configure(state=tkinter.NORMAL)


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


    


