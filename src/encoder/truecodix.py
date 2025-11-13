"""
Main application module

.. todo:: All the "print" should be moved to some logging process...

We need doc
"""

import os
# import json
#import time
import pathlib

import tkinter
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog

# tk colors : https://www.tcl.tk/man/tcl/TkCmd/colors.html

# from datetime import datetime # datetime.now().strftime('%c')

import utils as U
from .infoframe import InfoFrame
from .playercontrol import PlayerControl
from .applicationmenu import ApplicationMenu
from .codingframe import FrameworkFrame
from .newcode import NewCode

__version__ = '0.9'
__author__ = 'L. Pezard'
__licence__ = 'GPL'

CWD_FILE = 'cwdfile.ini'
DEFAULT_CWD = '~'
# DEFAULT_CWD = "~/Documents/videos_synchrony/vidéosynchrony/"

class Application(tkinter.Tk):
    """
    Main codix application class
    """
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.resizable(tkinter.TRUE, tkinter.TRUE)
        # Menu
        self.menu = ApplicationMenu(master=self)
        self['menu'] = self.menu
        # Variables
        self.state = {'media_loaded': False,
                      'code_loaded': False,
                      'data_loaded': False}

        self.__time_step = None

        self.container = {'history': [], # [(date, observer, comment), ...]
                          'media': '', # path for the media file
                          'code': {}, # dictionary taken from the code file
                          'times': [], # sample times (in ms) taken from the player
                          'comments': [], # sample comments taken from codingframe
                          'data': {},
                          'version': __version__} # data

        self._context = "standard"
        self.cwd = self.__set_cwd()
        print('Current working directory set to :', self.cwd)
        self.interface = True
        # FIXME: this is related to coding framework.
        # self.recorded_steps = []
        self.recorded_steps = set()

# Working directory

    def __set_cwd(self):
        """
        Reads initial cwd from file or from default value and set cwd to the one
        provided through filedialog.
     
        Also make sure that the folders "media" and "data" are present. Create
        them if they are lacking.
        """
        if os.path.exists(CWD_FILE):
            with open(CWD_FILE, 'r', encoding='utf-8') as cwdfile:
                initdir = os.path.expanduser(cwdfile.readline())
                # print('initdir from file: ', initdir)
        else:
            initdir = os.path.expanduser(DEFAULT_CWD)
            # print('initdir default: ', initdir)

        cwd = ''
        while cwd == '':
            cwd = filedialog.askdirectory(title="Choose working directory",
                                          initialdir=initdir, mustexist=True)
        with open(CWD_FILE, 'w', encoding='utf-8') as cwdfile:
            cwdfile.write(cwd)

        # check that subfolders 'media' and 'data' exist. If not create them
        if not os.path.exists(os.path.join(cwd, 'media')):
            pathlib.Path(os.path.join(cwd, 'media')).mkdir()
        if not os.path.exists(os.path.join(cwd, 'data')):
            pathlib.Path(os.path.join(cwd, 'data')).mkdir()

        return cwd

# Interface fonction

    def change_interface(self):
        """
        Change the interface looking.
        """
        if self.interface :
            self.change_color(['light_to_dark',self.control.elements,
                                self.framework.elements, self.info.elements])
            self.interface = False
            self.framework.interface_button.config(text='Light mode')
        else :
            self.change_color(['dark_to_light', self.control.elements,
                                self.framework.elements, self.info.elements])
            self.framework.interface_button.config(text='Dark mode')
            self.interface = True

    def change_color(self, inlist):
        """
        Change color theme
        """
        if inlist[0] == 'light_to_dark':
            for zone in inlist[1:] :
                for elem in zone :
                    if elem == self.control.elements :
                        elem.config(background = self.control.dark_bg)
                    if elem == self.info.elements :
                        elem.config(background = self.info.dark_bg)
                    else :
                        elem.config(background = self.framework.dark_bg)
        else :
            for zone in inlist[1:] :
                for elem in zone :
                    if elem == self.control.elements :
                        elem.config(background = self.control.light_bg)
                    if elem == self.info.elements :
                        elem.config(background = self.info.light_bg)
                    else:
                        elem.config(background = self.framework.light_bg)

# Menu related functions
#-----------------------

    def new_code(self):
        """Application for defining a new coding framework.
        """
        self.newcode = NewCode(parent=self)
        self.newcode.grid(row=1, column=1, sticky=U.sticky_all)
        self.menu.disable_actions()

    def start_session(self):
        """Starting a new coding session
        """
        self.info = InfoFrame(parent=self,
                              states=(tkinter.NORMAL,    # load media
                                      tkinter.DISABLED,  # load code
                                      tkinter.DISABLED)) # load data
        self.info.grid(row=1, column=1, sticky=U.sticky_all)
        self.menu.disable_actions()

    def retrieve_session(self):
        """Resume an interrupted coding session
        """
        self.info = InfoFrame(parent=self,
                              states=(tkinter.DISABLED, # load code
                                      tkinter.DISABLED, # load media
                                      tkinter.NORMAL))  # load data
        self.info.grid(row=1, column=1, sticky=U.sticky_all)
        self.menu.disable_actions()

    def reset(self):
        """Reset the file menu and all the current variables.
        """
        raise NotImplementedError
#        self.info.destroy()
#        self.framework.destroy()
#        self.control.destroy()
#        self.init_variables()

    def help_browser(self):
        """Calls the browser and open the documentation
        """
        self.notimplemented()

    def about_handler(self):
        """Gives some information about codix-suite
        """
        self.notimplemented()

# Functions related to infoframe
#-------------------------------

    def make_media_player(self, fname):
        """
        create a player control frame
        """
        self.control = PlayerControl(parent=self, file_name = fname)
        self.control.grid(row=1, column=0, sticky=U.sticky_all)
        self.state['media_loaded'] = True

    def make_coding_frame(self, fname):
        """
        creates the coding frame
        """
        self.framework = FrameworkFrame(parent=self, filename=fname)
        self.framework.grid(row=2, column=0, sticky=U.sticky_all)
        self.state['code_loaded'] = True

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        if value == "initial":
            self._context = "processing"
            print('Context Initial')
            self.control.config_buttons({self.control.play_but : 'normal',
                                    self.control.back_but : 'disabled',
                                    self.control.forward_but : 'disabled',
                                    self.control.mode_check : 'disabled',
                                    self.control.period_ent : 'disabled',
                                    self.control.time_ent: 'disabled'})
            assert len(self.control.times) == 0
            self.control.times.append(self.control.time)

            self.container['times'] = self.control.times
            self.container['data'] = self.framework.data
# FIXME: check this...
            self.container['media'] = \
            self.info.directory_msg.cget("text") + '/' + self.info.media_file.get()


            self.__time_step = 0
            print('TIME_STEP: ', self.time_step)

        elif value == "resume":
            self._context = "processing"
            print('Context Resume session')
            #### leomodif : j'ai commenté le premier bouton et
            #### je l'ai réactivé quand on clique sur record
            self.control.config_buttons({#self.control.play_but : 'normal',
                                    self.control.back_but : 'disabled',
                                    self.control.forward_but : 'disabled',
                                    self.control.mode_check : 'disabled',
                                    self.control.period_ent : 'disabled',
                                    self.control.time_ent: 'disabled'})

            # assert(len(self.control.times) == 0)
            # self.control.times.append(self.control.time)
            # self.container['times'] = self.control.times
            # self.container['data'] = self.framework.data
            # self.container['media'] = self.info.media_file.get()

            self.control.times = self.container['times']
            self.framework.data = self.container['data']
            self.framework.coding_comments = self.container['comments']
            # self.container['media'] = self.info.media_file.get()

            self.time_step = 'last'
            print('TIME_STEP: ', self.time_step)

        elif value == "processing":
            print('Context Processing')
            print("Recorded steps : ", self.recorded_steps)
            self.control.play_but.config(state='normal')
            # if self.time_step == self.times_length - 1 :
            #     self.control.forward_but.config(state='disabled')
            #     self.control.back_but.config(state='normal')
            # elif self.time_step == 0 :
            #     self.control.back_but.config(state='disabled')
            # else:
            #     self.control.back_but.config(state='normal')

            # if len(self.recorded_steps) > self.time_step :
            #     self.control.forward_but.config(state='normal')

            if self.time_step == 0 :
                self.control.back_but.config(state='disabled')
            else:
                self.control.back_but.config(state='normal')

            if len(self.recorded_steps) > self.time_step :
                self.control.forward_but.config(state='normal')
            else :
                self.control.forward_but.config(state='disabled')

            self.framework.display_codes(self.time_step)

        elif value == 'not_recorded':
            self.control.config_buttons({self.control.play_but : 'disabled',
                                         self.control.back_but : 'disabled',
                                         self.control.forward_but : 'disabled',
                                         self.control.mode_check : 'disabled',
                                         self.control.period_ent : 'disabled',
                                         self.control.time_ent: 'disabled'})
            self.framework.config_processing_buttons('normal')
            # self.info.save_data()

        elif value == 'standard':
            if self.state['code_loaded'] :
                if self.control.state == 'paused' :
                    self.framework.spec_frame.start_but.config(state='normal')

                elif self.control.state in ['s_playing', 'c_playing']:
                    self.framework.spec_frame.start_but.config(state='disabled')
                    # update is needed because of the timer in regular playing
                    self.framework.spec_frame.start_but.update()

        else: # FIXME: raise error?
            pass

    @property
    def times_length(self):
        return len(self.control.times)

    @property
    def time_step(self):
        return self.__time_step

    @time_step.setter
    def time_step(self, value):

        if value == '1p':
            if self.control.time > self.control.times[-1]:
                self.control.times.append(self.control.time)
                self.__time_step += 1
            else:
                self.__time_step = min(self.__time_step + 1, self.times_length-1)
                self.control.time = self.control.times[self.time_step]
            self.framework.config_processing_buttons('normal')

        elif value == 1:
            self.__time_step = min(self.__time_step + 1, self.times_length-1)
            self.control.time = self.control.times[self.time_step]
            self.framework.config_processing_buttons('disabled')

        elif value == -1:
            self.__time_step = max(0, self.__time_step - 1)
            self.control.time = self.control.times[self.time_step]
            self.framework.config_processing_buttons('disabled')

        elif value == 'last':
            self.__time_step = self.times_length - 1
            self.control.time = self.control.times[-1]
        else:
            # raise error ?
            pass

        self.container['times'] = self.control.times
        self.context = "processing"

        print('TIME_STEP: ', self.time_step)
        print(self.control.times)

# FIXME: Not sure this is still needed
#    def disable_load_data(self):
#        self.menu.fileMenu.entryconfig(4, state=tkinter.DISABLED)
#        self.info.data_load.config(state=tkinter.DISABLED)
#
#    def disable_load_media(self):
#        self.menu.fileMenu.entryconfig(3, state=tkinter.DISABLED)
#        self.info.media_load.config(state=tkinter.DISABLED)
#
#    def disable_load_code(self):
#        self.menu.fileMenu.entryconfig(2, state=tkinter.DISABLED)
#        self.info.code_load.config(state=tkinter.DISABLED)
#
#    def enable_load_data(self):
#        self.menu.fileMenu.entryconfig(4, state=tkinter.NORMAL)
#        self.info.data_load.config(state=tkinter.NORMAL)
#
#    def freeze(self):
#        """ cannot change step
#        """
#        self.control.mode_check.configure(state=tkinter.DISABLED)
#        self.control.period_ent.configure(state=tkinter.DISABLED)
#        self.control.time_ent.configure(state=tkinter.DISABLED)

#    def get_mode_and_period(self, encoding):
#        period = encoding['period']
#
#        if period is None:
#            # self.player_mode.set("continuous")
## FIXME: est que player ne serait pa mieux que control?
#            self.control.mode = "continuous"
#            tkinter.messagebox.showinfo('Continuous not implemented',
#                                   'Irregular sampling not implemented')
#            raise NotImplementedError()
#        else:
#            #self.player_mode.set("regular")
#            self.control.mode = "regular"
#            # self.period_display.set(str(period))

    def notimplemented(self):
        tkinter.messagebox.showinfo('Not implemented', 'Not implemented')

if __name__ == "__main__":
    app = Application()
    app.title(\
    f'Codix - The Swiss knife for coding behaviors - version: {__version__}')
    app.mainloop()
