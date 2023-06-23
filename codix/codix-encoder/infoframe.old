import tkinter
import tkinter.font
from tkinter.colorchooser import askcolor

bd = 2 # borderwidth
info_bg = 'yellow' # information background
disabled_bg = 'light grey' # disabled background
relief = 'groove'
filename_width = 50
# relief in ['flat', 'raised', 'sunken', 'solid', 'ridge', 'groove']

class InfoFrame(tkinter.LabelFrame):

    def __init__(self, parent, states=[None, None, None]):
        tkinter.LabelFrame.__init__(self, parent)
        self.configure(background=info_bg, 
                       borderwidth=bd, 
                       padx=20, pady=20, 
                       relief=relief,
                       text='Information: ', font=(tkinter.font.BOLD,))
        # Code File
        self.code_label = tkinter.Label(self, text='Code file: ', 
                                         background=info_bg)
        self.code_label.grid(row=1, column=0, sticky=tkinter.W)
        code_msg = tkinter.Entry(self, textvariable=parent.code_file,
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg)
        code_msg.grid(row=1, column=1, sticky=tkinter.W)
        self.code_load = tkinter.Button(self, text='Load',
                                        state=states[0],
                                        command=parent.ask_code)
        self.code_load.grid(row=1, column=2, sticky=tkinter.W)

        # Media File
        self.media_label = tkinter.Label(self, text='Media file: ', 
                                          background=info_bg)
        self.media_label.grid(row=2, column=0, sticky=tkinter.W)
        media_msg = tkinter.Entry(self, textvariable=parent.media_file, 
                                        state=tkinter.DISABLED,
                                        width=filename_width, 
                                        disabledbackground=disabled_bg)
        media_msg.grid(row=2, column=1, sticky=tkinter.W)
        self.media_load = tkinter.Button(self, text='Load',
                                         state=states[1],
                                         command=parent.ask_media)
        self.media_load.grid(row=2, column=2, sticky=tkinter.W)

        # Data File
        self.data_label = tkinter.Label(self, text='Data file: ', 
                                         background=info_bg)
        self.data_label.grid(row=3, column=0, sticky=tkinter.W)
        data_msg = tkinter.Entry(self, textvariable=parent.data_file, 
                                       state=tkinter.DISABLED, 
                                       width=filename_width, 
                                       disabledbackground=disabled_bg) 
        data_msg.grid(row=3, column=1, sticky=tkinter.W)
        self.data_load = tkinter.Button(self, text='Load',
                                        state=states[2],
                                        command=parent.ask_data)
        self.data_load.grid(row=3, column=2, sticky=tkinter.W)
        self.data_save = tkinter.Button(self, text='Save',
                                        command=parent.save_data,
                                        state=tkinter.DISABLED)
        self.data_save.grid(row=3, column=3, sticky=tkinter.W)

        self.bind('<Button-3>', self.change_color)

    def change_color(self, event):
        colortuple = askcolor()
        # print colortuple
        self.configure(background=colortuple[1]) 
        self.code_label.configure(background=colortuple[1])
        self.media_label.configure(background=colortuple[1])
        self.data_label.configure(background=colortuple[1])
