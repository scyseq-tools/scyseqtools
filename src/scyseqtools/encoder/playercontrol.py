"""
Module that controls media playback for ScySeqTools encoder
"""

import time

import tkinter
import tkinter.messagebox
from tkinter.colorchooser import askcolor

from scyseqtools.encoder.config import load_encoder_config
from scyseqtools.encoder.playerbackends import (
    PlayerBackendError,
    configured_backend_name,
    create_player_backend,
)

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


def bound_time_to_media(value, max_time):
    """Return a media time inside known bounds.

    VLC reports non-positive durations while the media length is not available
    yet. In that case only the lower bound can be enforced.
    """
    if value < 0:
        return 0, "before_start"
    if max_time > 0 and value > max_time:
        return max_time, "after_end"
    return value, None


def regular_step_target(start_time, period_seconds, max_time):
    """Return the intended end time for a regular playback step."""
    target_time = start_time + int(round(period_seconds * 1000))
    return bound_time_to_media(target_time, max_time)


class PlayerControl(tkinter.LabelFrame):
    """
    Defines the widgets where all the control is done with
    - play / pause button
    - back and forward buttons
    - a timer
    - a checkbox for setting regular playing
    """

    def __init__(self, parent, file_name, application=None):
        """
        Creates player control buttons
        """
        self.application = application or parent

        config = load_encoder_config(
            self.application.cwd, required_sections=("playercontrol",)
        )

        player_config = config['playercontrol']
        border_width = player_config.getint('borderwidth')
        ctrl_bg = player_config['background']
        relief = player_config['relief']
        backend_name = configured_backend_name(player_config)
        tkinter.LabelFrame.__init__(self, parent)

        self.configure(background=ctrl_bg, borderwidth=border_width, padx=20, pady=20,
                                relief=relief, text='Control: ', font=('bold',))

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
        try:
            self.player = create_player_backend(backend_name, file_name)
        except PlayerBackendError as exc:
            tkinter.messagebox.showinfo('Media player backend error', str(exc))
            raise

        self._state = "paused"
        self._current_time = 0
        self._step_after_id = None
        self.max_time = self.refresh_max_time() # a long in ms
        self.time = 0 # 'Initial time')
        print('Length of media file: ', self.max_time, ' ms.')

        self.elements = [self, self.period_lab, self.time_lab, self.mode_check, self.unit_lab]

        self.times = []

    def refresh_max_time(self, attempts=5, delay=0.1):
        """
        Ask the media backend for the media length, allowing a short warm-up window.
        """
        max_time = self.player.get_length()
        for _ in range(attempts):
            if max_time > 0:
                break
            time.sleep(delay)
            max_time = self.player.get_length()
        self.max_time = max_time
        return max_time

    def shutdown(self):
        """Pause playback and cancel delayed callbacks before the UI closes."""
        if self._step_after_id is not None:
            try:
                self.after_cancel(self._step_after_id)
            except tkinter.TclError:
                pass
            self._step_after_id = None

        try:
            self.player.pause()
        except Exception:
            pass
        self._state = "paused"

    def step_play(self, time_interval, target_time=None):
        """
        Plays for a time step 'time_interval'
        """
        # if self.application.state['code_loaded'] and self.application.context != 'processing':
        #             self._root().framework.spec_frame.start_but.config(state='disabled')
        start_time = self.time
        print('Start step play at: ', start_time)
        if target_time is None:
            target_time, _ = regular_step_target(
                start_time,
                time_interval,
                self.max_time,
            )
        self.state = "s_playing"
        self.player.play()
        delay = max(0, int(round(time_interval * 1000)))
        self._step_after_id = self.after(delay, self.finish_step_play, target_time)

    def finish_step_play(self, target_time):
        """
        Pause after a regular step and snap the player to the intended target.
        """
        self._step_after_id = None
        self.player.pause()
        print('Raw stop time before snap: ', self.player.get_time() if hasattr(self.player, 'get_time') else self._current_time)
        self.time = target_time
        self.state = "paused"
        print('End time: ', target_time)

        if self.application.context == "processing":
            self.play_but.config(state='disabled')
            self.application.time_step = '1p'

            print('End PP time step: ', self.application.time_step)

        self.finish_playpause()

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
        self.player.pause()
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
            period = self.period
            if period is not None :
                itime = self.time
                target_time, _ = regular_step_target(
                    itime,
                    period,
                    self.max_time,
                )
                self.step_play(period, target_time)
                return
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

        self.finish_playpause()

    def finish_playpause(self):
        """
        Apply common post-play/pause context updates.
        """
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
        if self.state == "paused":
            return self._current_time

        player_time = self.player.get_time()
        if player_time >= 0:
            self._current_time = player_time
        return player_time # in ms

    @time.setter
    def time(self, value):

        if value > 0 and self.max_time <= 0:
            self.refresh_max_time()
        tval, bound = bound_time_to_media(value, self.max_time)
        if bound == "before_start":
            tkinter.messagebox.showinfo('Value Error',
                              'cannot set time before beginning sets to zero')
        elif bound == "after_end":
            tkinter.messagebox.showinfo('Value Error',
                              'cannot set time after end sets to max time')

        self.player.set_time(tval)
        self._current_time = tval
        time_sec = '{:10.3f}'.format(tval/1000.)
        self._time.set(time_sec)
        print(f'Player time setter: {tval}.')

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
