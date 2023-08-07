"""
Menu for codix encoder
"""
import tkinter

class ApplicationMenu(tkinter.Menu):
    """
    The menu with very few actions...
    """

    def __init__(self, master=None):

        tkinter.Menu.__init__(self, master)
        # Actions Menu
        self.action_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label='Actions', menu=self.action_menu)

        self.action_menu.add_command(label='Define a new code',
                                     command=master.new_code)
        self.action_menu.add_command(label='Start a new session',
                                     command=master.start_session)
        self.action_menu.add_command(label='Retrieve a session',
                                     command=master.retrieve_session)
        self.action_menu.add_separator()
        self.action_menu.add_command(label='Reset',
                                     command=master.reset,
                                     state=tkinter.NORMAL)
        self.action_menu.add_separator()
        self.action_menu.add_command(label='Quit', command=master.quit)

        # Help Menu
        # FIXME: not implemented...
        help_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Help', command=master.help_browser)
        help_menu.add_command(label='About', command=master.about_handler)

    def disable_actions(self):
        """
        When an action starts they are all disabled
        """
        for idx in [0,1,2,4]:
            self.action_menu.entryconfigure(idx, state=tkinter.DISABLED)
