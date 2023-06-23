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
    
    def __init__(self, application):
        """
        Creates player control buttons
        """
        tkinter.LabelFrame.__init__(self, application)
        self.configure(background=ctrl_bg, borderwidth=bd, padx=20, pady=20,
                       relief=relief, text='Control: ', font=('bold',))
        
        # player instance 
        args = ['--no-xlib']
        instance = vlc.Instance(args)
        self.player = instance.media_player_new()
        
        # Control panel
        self.back_but = tkinter.Button(self, text='Back', command=self.backward) 
        self.back_but.grid(row=1, column=0, sticky=tkinter.W)

        self.play_but = tkinter.Button(self, text='Play/Pause', command=self.playpause)
        self.play_but.grid(row=1, column=1, sticky=tkinter.W)
        
        self.forward_but = tkinter.Button(self, text='Forward', command=self.forward)
        self.forward_but.grid(row=1, column=2)
       
        self.stop_but = tkinter.Button(self, text='Stop', command=self.stop)
        self.stop_but.grid(row=1, column=4)

        self.mode_check = tkinter.Checkbutton(self, text='By period of ',
                                              variable=application.player_mode, 
                                              onvalue='regular', offvalue='continuous',
                                              background=ctrl_bg)
        self.mode_check.grid(column=0, row=2, sticky=tkinter.W)
        self.mode_check.bind('<Button>', self.change_mode)

        self.period_ent = tkinter.Entry(self, width=4,
                                      textvariable=application.period_display)
        self.period_ent.grid(column=1, row=2, sticky=tkinter.W)
        # FIXME: 
        # self.period_ent.bind('<Return>', self.kb_set_period)
        
        self.period_lab = tkinter.Label(self, text=' sec.')
        self.period_lab.grid(row=2, column=2, sticky=tkinter.W)

        self.time_lab = tkinter.Label(self, text='Time', background=ctrl_bg)
        self.time_lab.grid(row=1, column=6)
        self.time_ent = tkinter.Entry(self, bg="white", width=7,
                                      textvariable=application.time_display)
        self.time_ent.grid(row=1, column=7)
        # FIXME
        self.time_ent.bind('<Return>', self.kb_set_time)

        self.unit_lab = tkinter.Label(self, text='sec.', background=ctrl_bg)
        self.unit_lab.grid(row=1, column=8)
        
        self.bind('<Button-3>', self.change_color)

    def playpause(self):
        mode = self._root().player_mode.get()
        pstate = self.player.get_state()
        print(mode, pstate)
        print('Start PP current step: ', self._root().current_step)

        if mode == "continuous":
            if pstate == 3: # Playing
                self.player.set_pause(do_pause=1)
                # self._root().show_time(self.player.get_time())
                self.set_time(self.player.get_time())
            elif pstate == 4: # Paused
                self.player.set_pause(do_pause=0)
            else:
                raise ValueError(f'Unknown player state {pstate}') 
        
        elif mode== "regular":
            assert(pstate == 4)
            period = self.get_period()
            if period is not None:
                itime = self.player.get_time()
                print('Start step play: ', itime)
                self.play_but.config(state=tkinter.DISABLED)
                self.player.set_pause(do_pause=0)
                start_time = time.monotonic()
                while time.monotonic() - start_time < period:
                    time.sleep(0.01)
                self.player.set_pause(do_pause=1)
                print('End time: ', self.player.get_time())
                ftime = itime + int(period*1000)
                self.set_time(ftime, 'Synchronized time')
                if self._root().current_step is not None:
                    self._root().current_step += 1
                print('End PP current step: ', self._root().current_step)
                self.play_but.config(state=tkinter.NORMAL)

        else:
            raise ValueError(f'Unknown player mode {mode}') 
    
    def backward(self):
        mode = self._root().player_mode.get()
        itime = self.player.get_time()
        print('Start backward current step: ', self._root().current_step)

        if mode == "continuous":
            self.set_time(itime - DTIME)

        elif mode == 'regular':
            period = self.get_period()
            if period is not None:
                if not self._root().data_loaded:
                    self.set_time(itime - int(period*1000))
                else:
                    cstep = self._root().current_step
                    # if cstep is not None and cstep > 1:
                    assert(cstep is not None)
                    if cstep >= 1:
                        self.set_time(itime - int(period*1000))
                        self._root().current_step -= 1
                        print('End backward current step: ', self._root().current_step)
                    else:
                        tkinter.messagebox.showinfo('Value Error', 
                              'Beginning of recording reached.')
            else:
                pass
        else:
            raise ValueError(f'Unknown player mode {mode}') 

#            dt = self._root().period_display.get()
#            if self.is_set_start_time:
#                self.referenced_step(-1, 'Referenced Back')
#                if self.is_recording:
#                    self.control.play_but.config(state=tkinter.NORMAL)
#                    self.framework.disable_codes()
#            else:
#                self.free_step(-1, 'Free back')

    def forward(self):
        mode = self._root().player_mode.get()
        itime = self.player.get_time()
        print('Start forward current step: ', self._root().current_step)

        if mode == "continuous":
            self.set_time(itime + DTIME)

        elif mode == 'regular':
            period = self.get_period()
            if period is not None:
                if not self._root().data_loaded:
                    self.set_time(itime + int(period*1000))
                else:
                    cstep = self._root().current_step
                    mstep = self._root().max_step
                    # if cstep is not None and cstep > 1:
                    assert(cstep is not None)
                    if cstep <= mstep:
                        self.set_time(itime + int(period*1000))
                        self._root().current_step += 1
                        print('End forward current step: ', self._root().current_step)
                    else:
                        tkinter.messagebox.showinfo('Value Error', 'End of recording reached.')
            else:
                pass
        else:
            raise ValueError(f'Unknown player mode {mode}') 


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

    def kb_set_time(self, tkevent):
        """
        Keyboard set time i.e. when the time is changed in the time entry
        """
        t = int(float(self._root().time_display.get())*1000) # in ms
        self.set_time(t, msg='keyboard set time')

    def set_time(self, time, msg=None):
        """Sets time
        time is an int in ms
        """
        max_time = self._root().max_time
        if time < 0:
            tkinter.messagebox.showinfo('Value Error', 
                              'cannot set time before beginning sets to zero')
            self.set_time(0)
        
        elif time > max_time:
            tkinter.messagebox.showinfo('Value Error', 
                              'cannot set time after end sets to max time')
            self.set_time(max_time)
        else:
            self.player.set_time(time)
            self._root().current_time = time # time in ms
            time_sec = '%10.3f' % (time/1000.)
            self._root().time_display.set(time_sec)
            print('Player time: set at %s (for %s) %s' % \
                  (self.player.get_time(), str(time), msg))

    def get_period(self):
        """Returns period in seconds
        """
        dt = self._root().period_display.get()
        try:
            return float(dt)
        except ValueError:
            tkinter.messagebox.showinfo('Value Error', 
                              'Period cannot be converted to float')
            return None

#    def kb_set_period(self, tkevent):
#        """
#        Keyboard set time i.e. when the time is changed in the time entry
#        """
#        t = int(float(self._root().period_display.get())*1000) # in ms
#        self.set_time(t, msg='keyboard set time')

#    def continuous_forward(self):
#        self.notimplemented()
#    
#    def continuous_back(self):
#        self.notimplemented()

    def stop(self):
        self.player.stop()

#    def show_time(self, msg=None): 
#        time = self.player.get_time()
#        self._root().time_in_ms = time
#        time_sec = int(round(time/1000.))
#        # self._root().player_time.set(str(time_sec))
#        self._root().current_time.set(time_sec)
#        print 'player time: ', time, msg
    
    def change_mode(self, tk_event):
        """ Handler for mouse click on the modeButton of control panel
        """
        mode = self._root().player_mode.get()
        print('change mode: ', mode)
        if mode == 'continuous': # ie regular play...
            self.period_ent.config(state=tkinter.NORMAL)
            self.back_but.config(state=tkinter.NORMAL)
            self.forward_but.config(state=tkinter.NORMAL)
        else:
            self.period_ent.config(state=tkinter.DISABLED)
            self.back_but.config(state=tkinter.DISABLED)
            self.forward_but.config(state=tkinter.DISABLED)
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
