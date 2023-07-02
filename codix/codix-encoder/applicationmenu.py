import tkinter

class ApplicationMenu(tkinter.Menu):

    def __init__(self, master=None):

        tkinter.Menu.__init__(self, master)
       
        # Actions Menu
        self.actionMenu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label='Actions', menu=self.actionMenu)

        self.new_code = self.actionMenu.add_command(label='Define a new code', 
                                                  command=master.new_code)

        self.start_session = self.actionMenu.add_command(label='Start a new session', 
                                                       command=master.start_session)

        self.retrieve_session = self.actionMenu.add_command(label='Retrieve a session', 
                                                          command=master.retrieve_session)

#        self.retrieve_session = self.actionMenu.add_command(label='Free viewing', 
#                                                          command=master.free_view)

        self.actionMenu.add_separator()

        self.actionMenu.add_command(label='Reset', command=master.reset,
                                  state=tkinter.NORMAL)

#        self.actionMenu.add_separator()
#        self.actionMenu.add_command(label='Save', command=master.save,
#                                  state=tkinter.DISABLED)
#        self.actionMenu.add_command(label='Save as', command=master.save_as,
#                                  state=tkinter.DISABLED)

        self.actionMenu.add_separator()

        self.actionMenu.add_command(label='Quit', command=master.quit)
        
        # Help Menu
        # FIXME: not implemented...
        helpMenu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label='Help', menu=helpMenu)
        helpMenu.add_command(label='Help', command=master.help_browser)
        helpMenu.add_command(label='About', command=master.aboutHandler)

    def disable_actions(self):
        # for idx in [0,1,2,3,5]:
        for idx in [0,1,2,4]:
            self.actionMenu.entryconfigure(idx, state=tkinter.DISABLED)
