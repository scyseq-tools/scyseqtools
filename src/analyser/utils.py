"""
Some common utils
"""
import tkinter

def listbox(upper, title, choice_list, multiple):
    """
    Utils for listbox
    """
    selectmode = tkinter.BROWSE # default
    if multiple:
        selectmode = tkinter.MULTIPLE
    master = tkinter.Frame(upper)
    label = tkinter.Label(master, text=title)
    label.grid(row=0, column=0, sticky=(tkinter.N, tkinter.W))

    yscroll = tkinter.Scrollbar(master, orient=tkinter.VERTICAL)
    yscroll.grid(row=1, column=1,
                 sticky=(tkinter.N, tkinter.S, tkinter.W))
    xscroll = tkinter.Scrollbar(master, orient=tkinter.HORIZONTAL)
    xscroll.grid(row=2, column=0,
              sticky=(tkinter.E, tkinter.S, tkinter.W))

# NB: exportselection=False means that you can select for each listbox
# independently see:
# http://stackoverflow.com/questions/756662/using-multiple-listboxes-in-python-tkinter
# It took me some times to figure out what happened...
    choice = tkinter.Listbox(master, listvariable=choice_list,
                                    selectmode=selectmode,
                                    height=5, # nb of lines
                                    width=15, # default=20
                                    yscrollcommand=yscroll.set,
                                    xscrollcommand=xscroll.set,
                                    exportselection=False)
    choice.grid(row=1, column=0, sticky=(tkinter.N, tkinter.E))
    yscroll['command'] = choice.yview
    xscroll['command'] = choice.xview

    return master, choice
