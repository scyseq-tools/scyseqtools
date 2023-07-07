import vlc
import tkinter
import tkinter.messagebox
from tkinter.colorchooser import askcolor

import time
from threading import Timer

#vlc states : 
#{0: 'NothingSpecial',
# 1: 'Opening',
# 2: 'Buffering',
# 3: 'Playing',
# 4: 'Paused',
# 5: 'Stopped',
# 6: 'Ended',
# 7: 'Error'}

# Graphical parameters
bd = 2 # borderwidth
ctrl_bg = 'magenta' #control background
relief = 'groove'
# relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

DTIME = 10000 # ms forward and back time period for continuous play

class PlayerControl(tkinter.LabelFrame):
    
    def __init__(self, parent, file_name):
        """
        Creates player control buttons
        """
        self.application = parent

        tkinter.LabelFrame.__init__(self, parent)
        self.configure(background=ctrl_bg, borderwidth=bd, padx=20, pady=20,
                       relief=relief, text='Control: ', font=('bold',))
        self.grid(column=1, row=0)
        
        self._mode = tkinter.StringVar(value='continuous')
        self._period = tkinter.StringVar(value='5')
        self._time = tkinter.StringVar(value='0')

        # Control panel
        self.back_but = tkinter.Button(self, text='Back', command=self.backward) 
        self.back_but.grid(row=1, column=0, sticky=tkinter.W)

        self.play_but = tkinter.Button(self, text='Play/Pause', command=self.playpause)
        self.play_but.grid(row=1, column=1, sticky=tkinter.W)
        
        self.forward_but = tkinter.Button(self, text='Forward', command=self.forward)
        self.forward_but.grid(row=1, column=2)
       
        self.mode_check = tkinter.Checkbutton(self, text='By period of ',
                                              variable=self._mode, 
                                              onvalue='regular', offvalue='continuous',
                                              background=ctrl_bg)
        self.mode_check.grid(column=0, row=2, sticky=tkinter.W)
        # FIXME: is it useful?
        # self.mode_check.bind('<Button>', self.change_mode)

        self.period_ent = tkinter.Entry(self, width=4,
                                        textvariable=self._period)
        self.period_ent.grid(column=1, row=2, sticky=tkinter.W)
        # FIXME:  is it useful?
        # self.period_ent.bind('<Return>', self.kb_set_period)
        
        self.period_lab = tkinter.Label(self, text=' sec.', background=ctrl_bg)
        self.period_lab.grid(row=2, column=2, sticky=tkinter.W)

        self.time_lab = tkinter.Label(self, text='Time', background=ctrl_bg)
        self.time_lab.grid(row=1, column=6)
        self.time_ent = tkinter.Entry(self, bg="white", width=7,
                                      textvariable=self._time)
        self.time_ent.grid(row=1, column=7)
        self.time_ent.bind('<Return>', self.kb_set_time)

        self.unit_lab = tkinter.Label(self, text='sec.', background=ctrl_bg)
        self.unit_lab.grid(row=1, column=8)
        
        self.bind('<Button-3>', self.change_color)

        # player instance 
        args = ['--no-xlib']
        instance = vlc.Instance(args)
        self.player = instance.media_player_new()

        self.player.set_mrl(file_name)
        # This is a hack for time initialization: reads 1s and then goes back to 0 
        self.player.play()
        time.sleep(1) # 0.1 is too short I loose sound!?
        self.player.set_pause(do_pause=1)
        self._state = "paused"
        self.max_time = self.player.get_length() # a long in ms
        self.time = 0 # 'Initial time')
        if self.max_time == -1:
            tkinter.messagebox.showinfo('Cannot get max time', 
                                  'Cannot get max time; this may cause problems')
        print('Length of media file: ', self.max_time, ' ms.')

        self.application.state['media_loaded'] = True
        
    def step_play(self, dt):
        self.play_but.update()
        print('Start step play at: ', self.time)
        self.state = "s_playing"
        tt = Timer(dt, self.dopause)
        self.player.play()
        tt.start()
        if self.application._context == 'processing' :
            self.application.framework.config_processing_buttons('normal')
    
    def cont_play(self):
        print('Start continuous play at: ', self.time)
        self.state = "c_playing"
        self.player.play()

    def dopause(self):
        self.player.set_pause(do_pause=1)
        self.state = "paused"

        # if self.application.is_code():
        if self.application.state['code_loaded'] and self.application._context != 'processing':
            self._root().framework.spec_frame.start_but.config(state='normal')
            
        if self.application.state['code_loaded'] and self.application._context == 'processing':
            self.config_buttons({self.play_but :'disabled',
                                 self.back_but : 'disabled',
                                 self.forward_but : 'disabled'})

    def playpause(self):
        # if self.application.is_code() :
        if self.application.state['code_loaded'] :
            self._root().framework.spec_frame.start_but.config(state='disabled')
        #if self.application._context == 'processing' :
        #    self.application.framework.config_processing_buttons('normal')
        if self.mode == 'regular':
            if self.period is not None :
                itime = self.player.get_time()

                self.step_play(self.period)         
                
                while self.state != 'paused':
                    pass # wait for state == 'paused'
                print('End time: ', self.time)
                ftime = itime + int(self.period*1000)
                self.time = ftime #, 'Synchronized time')

                # FIXME: check how we deal with `step`...
                # FIXME: do not use _root()...
                if self._root().current_step is not None:
                    self._root().current_step += 1
                print('End PP current step: ', self._root().current_step)
            else:
                pass

        if self.mode =='continuous':
            if self.state == "c_playing": 
                self.dopause()
                self.time = self.player.get_time()

            elif self.state == "paused":
                self.cont_play()           
            
            else:
                raise ValueError(f'Unknown player state ' + self.state)
     
    def backward(self):
        itime = self.time 
        # FIXME: do not use _root()...
        print('Start backward current step: ', self._root().current_step)
        if self.mode == "continuous":
            self.time = itime - DTIME

        elif self.mode == 'regular':
            if self.period is not None:
# FIXME: context is not processing
                # FIXME: do not use _root()...
                if not self._root().data_loaded:
                    self.time = itime - int(self.period*1000)
                else:
                    # FIXME: do not use _root()...
                    cstep = self._root().current_step
                    # if cstep is not None and cstep > 1:
                    assert(cstep is not None)
                    if cstep >= 1:
                        self.set_time(itime - int(self.period*1000))
                        # FIXME: do not use _root()...
                        self._root().current_step -= 1
                        print('End backward current step: ', self._root().current_step)
                    else:
                        tkinter.messagebox.showinfo('Value Error', 
                              'Beginning of recording reached.')
            else:
                pass
        else:
            raise ValueError(f'Unknown player mode {self.mode}') 

    #            dt = self._root().period_display.get()
    #            if self.is_set_start_time:
    #                self.referenced_step(-1, 'Referenced Back')
    #                if self.is_recording:
    #                    self.control.play_but.config(state=tkinter.NORMAL)
    #                    self.framework.disable_codes()
    #            else:
    #                self.free_step(-1, 'Free back')

    def forward(self):
        itime = self.player.get_time()
        # FIXME: do not use _root()...
        print('Start forward current step: ', self._root().current_step)
        if self.mode == "continuous":
            self.time = itime + DTIME

        elif self.mode == 'regular':
            if self.period is not None:
# See backward...
                # FIXME: do not use _root()...
                if not self._root().data_loaded:
                    self.time = itime + int(self.period*1000)
                else:
# See backward...
                    # FIXME: do not use _root()...
                    cstep = self._root().current_step
                    mstep = self._root().max_step
                    # if cstep is not None and cstep > 1:
                    assert(cstep is not None)
                    if cstep <= mstep:
                        self.time = itime + int(self.period*1000)
                        self._root().current_step += 1
                        print('End forward current step: ', self._root().current_step)
                    else:
                        tkinter.messagebox.showinfo('Value Error', 'End of recording reached.')
            else:
                pass
        else:
            raise ValueError(f'Unknown player mode {self.mode}') 

    #        step = self.player_mode.get()
    #        if step == "continuous":
    #            self.control.continuous_forward()
    #        elif step == 'step':
    #            if self.is_set_start_time:
    #                self.referenced_step(1, 'Referenced Forward')
    #                if self.is_recording:
    #                    self.control.play_but.config(state=tkinter.NORMAL)
    #                    try:
    #                        self.display_codes(self.current_step)# + 1)
    #                    except IndexError:
    #                        self.erase_codes()
    #            else:
    #                self.free_step(1, 'Free forward')

    #        self.application.period

    def kb_set_time(self, tkevent):
        """
        Keyboard set time i.e. when the time is changed in the time entry
        """
        t = self._time.get()
        try:
            self.time = int(float(t)*1000) # in ms
        except ValueError:
            tkinter.messagebox.showinfo('Value Error', 
                              'Time cannot be converted to float')
            return None

    @property
    def time(self):
        return self.player.get_time() # in ms

    @time.setter
    def time(self, value):

        if value < 0:
            tkinter.messagebox.showinfo('Value Error', 
                              'cannot set time before beginning sets to zero')
            tval = 0
        elif value > self.max_time:
            tkinter.messagebox.showinfo('Value Error', 
                              'cannot set time after end sets to max time')
            tval = self.max_time
        else:
            tval = value

        self.player.set_time(tval)
        time_sec = '%10.3f' % (tval/1000.)
        self._time.set(time_sec)
        print('Player time setter: %s' % self.time)

#    def kb_set_period(self, tkevent):
#        """
#        Keyboard set time i.e. when the time is changed in the time entry
#        """
#        t = int(float(self._root().period_display.get())*1000) # in ms
#        self.set_time(t, msg='keyboard set time')

#    def change_mode(self, tk_event):
#        """ Handler for mouse click on the modeButton of control panel
#        """
#        mode = self._root().player_mode.get()
#        if mode == 'continuous': # ie regular play...
#            print('change mode: regular')
#            
#        else:
#            print('change mode: continuous')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value == "s_playing" :
            self._state = "s_playing"
            print('State: step playing')
            self.config_buttons({self.play_but : 'disabled', 
                                 self.back_but : 'disabled',
                                 self.forward_but : 'disabled', 
                                 self.mode_check : 'disabled',
                                 self.period_ent : 'disabled'})

        elif value == "c_playing" :
            self._state = "c_playing"
            print('State: continuous playing')
            self.config_buttons({self.play_but : 'normal', 
                                 self.back_but : 'disabled',
                                 self.forward_but : 'disabled', 
                                 self.mode_check : 'disabled',
                                 self.period_ent : 'disabled'})

        elif value == "paused":
            self._state = "paused"
            print('State: paused')

            if self.application.context == "processing":
# FIXME: deal with back and forward according to steps...
                self.config_buttons({self.play_but : 'normal', 
                                     self.back_but : 'normal',
                                     self.forward_but : 'normal', 
                                     self.mode_check : 'disabled',
                                     self.period_ent : 'disabled'})
            else:
                self.config_buttons({self.play_but : 'normal', 
                                     self.back_but : 'normal',
                                     self.forward_but : 'normal', 
                                     self.mode_check : 'normal',
                                     self.period_ent : 'normal'})

    @property
    def mode(self):
        return self._mode.get()

    @mode.setter
    def mode(self, value):
        if value == "regular":
            self._mode.set(value)
            print('Mode: regular')
        elif value == "continuous":
            self._mode.set(value)
            print('Mode: continuous')
        else:
            raise ValueError

    @property
    def period(self):
        pp = self._period.get()
        try:
            return float(pp)
        except ValueError:
            tkinter.messagebox.showinfo('Value Error', 
                              'Period cannot be converted to float')
            return None
    
    @period.setter
    def period(self, value):
        self._period.set(value)


    def config_buttons(self, dico):
        for b, s in dico.items():
            b.update()
            b.config(state=s)
            b.update()
                
    #        print('End change mode: ', mode)

    #        # FIXME: does the first test useful. Tackle this more elegantly?
    #        if self._root().data_loaded:
    #            pass
    #        else:
    #            mode = self._root().player_mode.get()
    #            if mode == 'regular': # ie step_play
    #             #   self.pause_but.config(state=tkinter.DISABLED)
    #                self.period_ent.config(state=tkinter.NORMAL)
    #                self.back_but.config(state=tkinter.NORMAL)
    #                self.forward_but.config(state=tkinter.NORMAL)
    #            else:
    #            #    self.pause_but.config(state=tkinter.NORMAL)
    #                self.period_ent.config(state=tkinter.DISABLED)
    #                self.back_but.config(state=tkinter.DISABLED)
    #                self.forward_but.config(state=tkinter.DISABLED)

    #    def notimplemented(self):
    #        tkinter.messagebox.showinfo('Not implemented', 'Not implemented')

    def change_color(self, event):
        colortuple = askcolor()
        self.configure(background=colortuple[1]) 
        self.mode_check.configure(background=colortuple[1])
        self.mode_lab.configure(background=colortuple[1])
        self.time_lab.configure(background=colortuple[1])
        self.unit_lab.configure(background=colortuple[1])
