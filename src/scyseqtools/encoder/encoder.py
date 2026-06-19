"""
Main application module

.. todo:: All the "print" should be moved to some logging process...

We need doc
"""

import os
# import json
#import time

import tkinter
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog

# tk colors : https://www.tcl.tk/man/tcl/TkCmd/colors.html

# from datetime import datetime # datetime.now().strftime('%c')

import scyseqtools.encoder.utils as U
from scyseqtools.encoder.infoframe import InfoFrame
from scyseqtools.encoder.playercontrol import PlayerControl
from scyseqtools.encoder.applicationmenu import ApplicationMenu
from scyseqtools.encoder.codingframe import FrameworkFrame
from scyseqtools.encoder.config import (
    get_cwd_file_path,
    get_encoder_layout,
    load_encoder_config,
)
from scyseqtools.encoder.newcode import NewCode

__version__ = '0.9'
__author__ = 'L. Pezard'
__licence__ = 'GPL'

class Application(tkinter.Tk):
    """
    Main ScySeqTools application class
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
        self.info = None
        self.control = None
        self.framework = None
        self._control_window = None
        self._coding_window = None
        self.cwd = self.__set_cwd()
        self.encoder_layout = get_encoder_layout(self.cwd)
        print('Current working directory set to :', self.cwd)
        print('Encoder layout set to :', self.encoder_layout)
        self.protocol("WM_DELETE_WINDOW", self.quit_session)
        # FIXME: this is related to coding framework.
        # self.recorded_steps = []
        self.recorded_steps = set()
        self.coding_workspace = None

# Working directory

    def __set_cwd(self):
        """
        Reads initial cwd from file or from default value and set cwd to the one
        provided through filedialog.
     
        Also make sure that the folder "data" is present. Create it if it is
        lacking.
        """
        config = load_encoder_config(required_sections=("application",))
        cwd_filename = get_cwd_file_path(config)
        default_cwd = config["application"]["default_cwd"]

        if cwd_filename.exists():
            with cwd_filename.open('r', encoding='utf-8') as cwdfile:
                initdir = os.path.expanduser(cwdfile.readline())
                # print('initdir from file: ', initdir)
        else:
            initdir = os.path.expanduser(default_cwd)
            # print('initdir default: ', initdir)

        cwd = ''
        while cwd == '':
            cwd = filedialog.askdirectory(title="Choose working directory",
                                          initialdir=initdir, mustexist=True)
        with cwd_filename.open('w', encoding='utf-8') as cwdfile:
            cwdfile.write(cwd)

        U.ensure_subdirectory(cwd, "data")

        return cwd

# Menu related functions
#-----------------------

    def new_code(self):
        """Application for defining a new coding framework.
        """
        self.newcode = NewCode(parent=self)
        self.newcode.grid(row=1, column=1, sticky=U.sticky_all)
        self.menu.disable_actions()
        self.after_idle(self.newcode.focus_first_field)

    def finish_new_code(self):
        """Return to the main action menu after defining a new code.
        """
        self.newcode = None
        self.menu.enable_actions()

    def start_session(self):
        """Starting a new coding session
        """
        self.info = InfoFrame(parent=self,
                              states=(tkinter.NORMAL,    # load media
                                      tkinter.DISABLED,  # load code
                                      tkinter.DISABLED)) # load data
        self.__grid_information_frame()
        if not self.detached_layout:
            self.__make_coding_workspace()
        self.menu.disable_actions()

    def retrieve_session(self):
        """Resume an interrupted coding session
        """
        self.info = InfoFrame(parent=self,
                              states=(tkinter.DISABLED, # load code
                                      tkinter.DISABLED, # load media
                                      tkinter.NORMAL))  # load data
        self.__grid_information_frame()
        if not self.detached_layout:
            self.__make_coding_workspace()
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
        """Gives some information about ScySeqTools
        """
        self.notimplemented()

    @property
    def detached_layout(self):
        """Whether encoder content should be split into separate windows."""
        return self.encoder_layout == "detached"

    def __grid_information_frame(self):
        """
        Put the information frame in the root window.
        """
        if self.detached_layout:
            self.title(f'ScySeqTools - Information - version: {__version__}')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.info.grid(row=0, column=0, sticky=U.sticky_all)
        else:
            self.info.grid(row=1, column=1, sticky=U.sticky_all)

    def __detached_window(self, attr_name, title):
        """
        Return an application-managed detached content window.
        """
        window = getattr(self, attr_name)
        if window is not None and window.winfo_exists():
            window.deiconify()
            window.lift()
            return window

        window = tkinter.Toplevel(self)
        window.title(f'ScySeqTools - {title} - version: {__version__}')
        window.resizable(tkinter.TRUE, tkinter.TRUE)
        window.protocol("WM_DELETE_WINDOW", self.__refocus_information_window)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        setattr(self, attr_name, window)
        return window

    def __refocus_information_window(self):
        """
        Keep detached content windows open and return focus to Information.
        """
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
        except tkinter.TclError:
            pass

    def __control_parent(self):
        if self.detached_layout:
            return self.__detached_window("_control_window", "Control")
        return self

    def __coding_parent(self):
        if self.detached_layout:
            return self.__detached_window("_coding_window", "Coding framework")
        return self

    def quit_session(self):
        """
        Close the encoder session and shut down playback cleanly.
        """
        if self.control is not None and self.control.winfo_exists():
            self.control.shutdown()

        for window in (self._control_window, self._coding_window):
            if window is not None and window.winfo_exists():
                window.destroy()

        self.destroy()

# Functions related to infoframe
#-------------------------------

    def make_media_player(self, fname):
        """
        create a player control frame
        """
        parent = self.__control_parent()
        self.control = PlayerControl(
            parent=parent,
            file_name=fname,
            application=self,
        )
        if self.detached_layout:
            self.control.grid(row=0, column=0, sticky=U.sticky_all)
            parent.lift()
        else:
            self.control.grid(row=1, column=0, sticky=U.sticky_all)
        self.state['media_loaded'] = True

    def make_coding_frame(self, fname):
        """
        creates the coding frame
        """
        self.__make_coding_workspace()
        self.framework = FrameworkFrame(
            parent=self.coding_workspace,
            filename=fname,
            application=self,
        )
        self.framework.grid(row=0, column=0, sticky=U.sticky_all,
                            padx=20, pady=20)
        self.state['code_loaded'] = True

    def __make_coding_workspace(self):
        """
        Create the lower yellow area that holds coding widgets.
        """
        if self.coding_workspace is not None and self.coding_workspace.winfo_exists():
            return

        config = load_encoder_config(
            self.cwd, required_sections=("codingframework",)
        )
        coding_config = config["codingframework"]
        parent = self.__coding_parent()

        if self.detached_layout:
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_rowconfigure(0, weight=1)
        else:
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=1)

        self.coding_workspace = tkinter.LabelFrame(parent)
        self.coding_workspace.configure(
            background=coding_config["background"],
            borderwidth=coding_config.getint("borderwidth"),
            padx=20,
            pady=20,
            relief=coding_config["relief"],
            text='Coding framework: ',
            font=('bold',),
        )
        if self.detached_layout:
            self.coding_workspace.grid(row=0, column=0, sticky=U.sticky_all)
            parent.lift()
        else:
            self.coding_workspace.grid(row=2, column=0, columnspan=2,
                                       sticky=U.sticky_all)
        self.coding_workspace.grid_columnconfigure(0, weight=1)
        self.coding_workspace.grid_columnconfigure(1, weight=1)
        self.coding_workspace.grid_rowconfigure(0, weight=1)

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

            self.time_step = 'last_recorded'
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
            if self.control.times:
                self.control.time = self.control.times[-1]
        elif value == 'last_recorded':
            if self.recorded_steps:
                self.__time_step = max(self.recorded_steps)
            else:
                self.__time_step = max(0, self.times_length - 1)
            if self.control.times:
                time_index = min(self.__time_step, self.times_length - 1)
                self.control.time = self.control.times[time_index]
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
    f'ScySeqTools - The Swiss knife for coding behaviors - version: {__version__}')
    app.mainloop()
