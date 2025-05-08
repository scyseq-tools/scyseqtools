"""
Module that controls VLC player for codix encoder
"""

import os
import time
import configparser


from threading import Timer

import tkinter
import tkinter.messagebox
from tkinter.colorchooser import askcolor

import vlc

#vlc states :
#{0: 'NothingSpecial',
# 1: 'Opening',
# 2: 'Buffering',
# 3: 'Playing',
# 4: 'Paused',
# 5: 'Stopped',
# 6: 'Ended',
# 7: 'Error'}

## Graphical parameters
#bd = 2 # borderwidth
#ctrl_bg = 'magenta' #control background
#relief = 'groove'
## relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

DTIME = 10000 # ms forward and back time period for continuous play
CONFIG = 'config.ini'

class PlayerControl(tkinter.LabelFrame):
    """
    Defines the widgets where all the control is done with
    - play / pause button
    - back and forward buttons
    - a timer
    - a checkbox for setting regular playing
    """

    def __init__(self, parent, file_name):
        """
        Creates player control buttons
        """
        self.application = parent

        config = configparser.ConfigParser()
        if os.path.exists(os.path.join(self.application.cwd, CONFIG)):
            config.read(os.path.join(self.application.cwd, CONFIG))
        else:
            config.read(CONFIG)

        border_width = config['playercontrol']['borderwidth']
        ctrl_bg = config['playercontrol']['background']
        relief = config['playercontrol']['relief']
        self.dark_bg = config['playercontrol']['dark_bg']
        self.light_bg = config['playercontrol']['light_bg']

        tkinter.LabelFrame.__init__(self, parent)

        self.configure(background=ctrl_bg, borderwidth=border_width, padx=20, pady=20,
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
        self.mode_check.grid(row=2, column=1, sticky=tkinter.W)

        # FIXME: is it useful?
        # self.mode_check.bind('<Button>', self.change_mode)

        self.period_ent = tkinter.Entry(self, width=4,
                                        textvariable=self._period)
        self.period_ent.grid(column=2, row=2, sticky=tkinter.W)
        # FIXME:  is it useful?
        # self.period_ent.bind('<Return>', self.kb_set_period)

        self.period_lab = tkinter.Label(self, text=' sec.', background=ctrl_bg)
        self.period_lab.grid(row=2, column=3, sticky=tkinter.W)

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

        self.elements = [self, self.period_lab, self.time_lab, self.mode_check, self.unit_lab]

        self.times = []

    def step_play(self, time_interval):
        """
        Plays for a time step 'time_interval'
        """
        # if self.application.state['code_loaded'] and self.application.context != 'processing':
        #             self._root().framework.spec_frame.start_but.config(state='disabled')
        print('Start step play at: ', self.time)
        self.state = "s_playing"
        interval_timer = Timer(time_interval, self.dopause)
        self.player.play()
        interval_timer.start()

    def cont_play(self):
        """
        Plays continuously (until play/pause button is pressed).
        """
        print('Start continuous play at: ', self.time)
        self.state = "c_playing"
        self.player.play()

    def dopause(self):
        """
        Pause the player.
        """
        self.player.set_pause(do_pause=1)
        self.state = "paused"
#        #### leomodif
#        LP: passé dans fonction playpause.
#        if self.application.context == 'processing':
#            self.play_but.config(state='disabled')

    def playpause(self):
        """
        Function associated with the play/pause button:
        - plays if the player is paused
        - pause if the player is playing.
        """
        if self.mode == 'regular':
            if self.period is not None :
                itime = self.player.get_time()
                self.step_play(self.period)

                while self.state != 'paused':
                    pass # wait for state == 'paused'
                print('End time: ', self.time)

                ftime = itime + int(self.period*1000)
                self.time = ftime #, 'Synchronized time')

                if self.application.context == "processing":
                    self.play_but.config(state='disabled')
                    self.application.time_step = '1p'

                    print('End PP time step: ', self.application.time_step)
            else:
                pass

        elif self.mode =='continuous':
            if self.state == "c_playing":
                self.dopause()
                self.time = self.player.get_time()

            elif self.state == "paused":
                self.cont_play()
            else:
                raise ValueError(f'Unknown player state: {self.state}.')
        else:

            raise ValueError('Unknown player mode' + self.mode)

        if self.application.context == 'processing' :
            self.application.context = 'not_recorded'

        print("context :" , self.application.context)

    def backward(self):
        """
        Move backward.
        """
        self.move('back')

    def forward(self):
        """
        Move forward
        """
        self.move('forward')

    def move(self, arg):
        """
        Generic function that move either backward or forward.
        """
        dtmp = {'back': -1, 'forward': 1}
        bck_or_fwd = dtmp[arg]

        itime = self.time
        if self.mode == "continuous":
            self.time = itime + bck_or_fwd * DTIME
            # FIXME: no processing context taken into account.

        elif self.mode == 'regular':
            if self.period is not None:
                if self.application.context == "processing":
                    self.application.time_step = bck_or_fwd
                else:
                    self.time = itime + bck_or_fwd * int(self.period * 1000)
        else:
            raise ValueError(f'Unknown player mode {self.mode}')

    def kb_set_time(self, tkevent):
        """
        Keyboard set time i.e. when the time is changed in the time entry
        """
        loc_time = self._time.get()
        try:
            self.time = int(float(loc_time)*1000) # in ms
        except ValueError:
            tkinter.messagebox.showinfo('Value Error',
                              'Time cannot be converted to float')
    #        return None

    @property
    def time(self):
        """
        Time comes from the player but we need more control. We set it as a
        property to have more control.
        """
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
        time_sec = '{:10.3f}'.format(tval/1000.)
        self._time.set(time_sec)
        print(f'Player time setter: {self.time}.')

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
        """
        The state of the player has consequences on the interface according to
        application context, etc. so we control it with a property.
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        State of the widget according to player state
        """
        if value == "s_playing" :
            self._state = "s_playing"
            print('State: step playing')
            self.config_buttons({self.play_but : 'disabled',
                                 self.back_but : 'disabled',
                                 self.forward_but : 'disabled',
                                 self.mode_check : 'disabled',
                                 self.period_ent : 'disabled'})

            tmp_context = self.application.context
            self.application.context = tmp_context

        elif value == "c_playing" :
            self._state = "c_playing"
            print('State: continuous playing')
            self.config_buttons({self.play_but : 'normal',
                                 self.back_but : 'disabled',
                                 self.forward_but : 'disabled',
                                 self.mode_check : 'disabled',
                                 self.period_ent : 'disabled'})

            tmp_context = self.application.context
            self.application.context = tmp_context

        elif value == "paused":
            self._state = "paused"
            print('State: paused')

            if self.application.context != 'processing':
                self.config_buttons({self.play_but : 'normal',
                                     self.back_but : 'normal',
                                     self.forward_but : 'normal',
                                     self.mode_check : 'normal',
                                     self.period_ent : 'normal'})
# FIXME: why do we need to deal with framework state here!?

            # processing => code_loaded
            elif self.application.context == 'processing':
                self.config_buttons({self.play_but :'disabled',
                                     self.back_but : 'disabled',
                                     self.forward_but : 'disabled'})
            tmp_context = self.application.context
            self.application.context = tmp_context

# *** From dopause ***
## FIXME: maybe should be in state.setter ^^^
#            if self.application.state['code_loaded'] and self.application.context != 'processing':
#                self._root().framework.spec_frame.start_but.config(state='normal')
#
#            if self.application.state['code_loaded'] and self.application.context == 'processing':
#                self.config_buttons({self.play_but :'disabled',
#                                     self.back_but : 'disabled',
#                                     self.forward_but : 'disabled'})
## ^^^ Check with context and so on...
# *** END from dopause ***

## FIXME: Not sure processing is useful -> done in application.context setter?
#            if self.application.context == "processing":
#                self.config_buttons({self.play_but : 'normal',
#                                     self.back_but : 'normal',
#                                     self.forward_but : 'normal',
#                                     self.mode_check : 'disabled',
#                                     self.period_ent : 'disabled'})
#            else:
#                self.config_buttons({self.play_but : 'normal',
#                                     self.back_but : 'normal',
#                                     self.forward_but : 'normal',
#                                     self.mode_check : 'normal',
#                                     self.period_ent : 'normal'})

    @property
    def mode(self):
        """
        The player's mode: regular or continuous
        """
        return self._mode.get()

    @mode.setter
    def mode(self, value):
        """
        Sets the mode
        """
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
        """
        Time period for regular playing
        """
        tmp_period = self._period.get()
        try:
            return float(tmp_period)
        except ValueError:
            tkinter.messagebox.showinfo('Value Error',
                              'Period cannot be converted to float')
            return None

    @period.setter
    def period(self, value):
        """
        Sets period
        """
        self._period.set(value)

    def config_buttons(self, dico):
        for b, s in dico.items():
            b.update()
            b.config(state=s)
            b.update()

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
        # self.mode_lab.configure(background=colortuple[1])
        self.time_lab.configure(background=colortuple[1])
        self.unit_lab.configure(background=colortuple[1])
