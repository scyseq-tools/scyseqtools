import re
import os
import json
import tkinter
import tkinter.messagebox
import tkinter.filedialog

from functools import partial
from datetime import datetime

import utils as U
import htmlreport as H

ITEMSEP = ' |,|-|;|:|/'

class NewCode(tkinter.LabelFrame):

    def __init__(self, parent):
        tkinter.LabelFrame.__init__(self, parent)

        # Project
        projectframe = tkinter.LabelFrame(self, text="Project")
        projectframe.grid(sticky=U.sticky_all)

        self.project_name = tkinter.StringVar()

        name_label = tkinter.Label(projectframe, text='Name: ')
        name_label.grid(row=0, column=0)
        name_entry = tkinter.Entry(projectframe, textvariable=self.project_name)
        name_entry.grid(row=0, column=2)
        
        description_label = tkinter.Label(projectframe, text='Description: ')
        description_label.grid(row=1, column=0)
        self.description_text = tkinter.Text(projectframe)
        self.description_text.grid(row=1, column=2)

        # specifications
        specframe = tkinter.LabelFrame(self, text='Specifications')
        specframe.grid(sticky=U.sticky_all)

        self.regular = tkinter.BooleanVar()
        self.regular.set(False)
        self.period = tkinter.StringVar()

        reg_check = tkinter.Checkbutton(specframe, text='Regular sampling',
                                                   variable=self.regular,
                                                   onvalue=True,
                                                   offvalue=False,
                                                   command=self.toggle_specs)
        reg_check.grid(row=0, column=0)
        period_label = tkinter.Label(specframe, text='Interval: ')
        period_label.grid(row=0, column=2)
        self.period_entry = tkinter.Entry(specframe, 
                                       textvariable=self.period,
                                       state=tkinter.DISABLED)
        self.period_entry.grid(row=0, column=3)
        unit = tkinter.Label(specframe, text='Seconds')
        unit.grid(row=0, column=4)

        # codes
        codeframe = tkinter.LabelFrame(self, text='Coding definitions')
        codeframe.grid(sticky=U.sticky_all)

        self.tmpcode = tkinter.StringVar()
        self.tmpitems = tkinter.StringVar()
        self.codes_container = {}

        cname = tkinter.Label(codeframe, text='Code name: ')
        cname.grid(row=0, column=0)
        centry = tkinter.Entry(codeframe, textvariable=self.tmpcode)
        centry.grid(row=0, column=1)
        itemlabel = tkinter.Label(codeframe, text='List of items: ')
        itemlabel.grid(row=0, column=2)
        itementry = tkinter.Entry(codeframe, textvariable=self.tmpitems)
        itementry.grid(row=0, column=3)
        code_button = tkinter.Button(codeframe, text='Record',
                                                command=self.record_code)
        code_button.grid(row=0, column=5, sticky=tkinter.E)

        self.recorded_codes = tkinter.LabelFrame(codeframe, text='Recorded codes')
        self.recorded_codes.grid(row=1, column=0, columnspan=6, sticky=U.sticky_all)

        # sites
        siteframe = tkinter.LabelFrame(self, text='Recording sites')
        siteframe.grid(sticky=U.sticky_all)
     
        self.listcode = tkinter.StringVar()
        self.tmpsite = tkinter.StringVar()
        self.sites_container = {}

        sitename = tkinter.Label(siteframe, text='Recording site: ')
        sitename.grid(row=0, column=0, sticky=tkinter.N)
        siteentry = tkinter.Entry(siteframe, textvariable=self.tmpsite)
        siteentry.grid(row=0, column=1, sticky=tkinter.N)
        codelabel = tkinter.Label(siteframe, text='Available codes : ')
        codelabel.grid(row=0, column=2, sticky=(tkinter.N, tkinter.W))
        yscroll = tkinter.Scrollbar(siteframe, orient=tkinter.VERTICAL)
        yscroll.grid(row=0, column=4, 
                     sticky=(tkinter.N, tkinter.S, tkinter.W))
        self.codelist = tkinter.Listbox(siteframe, listvariable=self.listcode,
                                        selectmode=tkinter.MULTIPLE,
                                        height=5, # nb of lines
                                        width=15, # default=20
                                        yscrollcommand=yscroll.set)
        self.codelist.grid(row=0, column=3, sticky=(tkinter.N, tkinter.E)) 
        yscroll['command'] = self.codelist.yview
        site_button = tkinter.Button(siteframe, text='Record',
                                                command=self.record_site)
        site_button.grid(row=0, column=5, sticky=(tkinter.N, tkinter.E))
        self.recorded_sites = tkinter.LabelFrame(siteframe, text='Recorded sites')
        self.recorded_sites.grid(row=1, column=0, columnspan=6, sticky=U.sticky_all)

        # save all specs
        savebutton = tkinter.Button(self, text='Save all specifications and quit',
                                          command = self.record_all )
        savebutton.grid(sticky=U.sticky_all)

    def toggle_specs(self):
        if self.regular.get():
            self.period_entry.configure(state=tkinter.NORMAL)
        else:
            self.period.set('')
            self.period_entry.configure(state=tkinter.DISABLED)

    def record_code(self):
        name = self.tmpcode.get().strip()
        items = self.tmpitems.get().strip()

        if name == '' or items == '':
            tkinter.messagebox.showinfo('Bad code', 
                                        'You cannot record empty codes')
        elif name in self.codes_container.keys():
            tkinter.messagebox.showinfo('Bad code', 
                                        'Code name already exists')
        else:
            # split items according to chars in ITEMSEP
            listofitems = [s for s in re.split(ITEMSEP, items) if s != '']
            self.codes_container.update({name: listofitems})
            rec = RecordedCode(self,  # application
                               name, listofitems,
                               len(self.codes_container))
            self.tmpcode.set('')
            self.tmpitems.set('')
            self.listcode.set(' '.join(list(self.codes_container.keys())))

    def record_site(self):
        site_name = self.tmpsite.get()
        selected_codes = self.codelist.curselection()
        list_of_codes = self.listcode.get()
        if len(selected_codes) == 0:
            tkinter.messagebox.showinfo('Bad selection', 
                                        'You should select at least one code.')
        elif site_name == '':
            tkinter.messagebox.showinfo('Bad selection', 
                                        'You should give a site name.')
        else:
            list_of_codes = [c for c in re.split("\(|,|'| |\)", list_of_codes) if c!='']
            list_of_selected_codes = [list_of_codes[i] for i in selected_codes]
            self.sites_container.update({site_name: list_of_selected_codes})
            site_rec = RecordedSite(self, 
                                    site_name, list_of_selected_codes, len(self.sites_container))
            self.tmpsite.set('')
            for line in selected_codes: 
                self.codelist.selection_clear(line)

    def record_all(self):

        all_specs = {'date': datetime.now().strftime('%c')}

        pname = self.project_name.get()
        if pname == '':
            tkinter.messagebox.showerror('You forgot something...', 
                             'Enter the name of the project.')
            pass
        else:
            all_specs.update({"project": pname})

        description = self.description_text.get("1.0", "end-1c")
        if description == '':
            tkinter.messagebox.showerror('You forgot something...', 
                             'Enter the description of the project.')
            pass
        else:
            all_specs.update({"description": description})

        regular = self.regular.get()
        if regular:
            period = self.period.get()
            if period == '':
                tkinter.messagebox.showerror('You forgot something...', 
                                 'Enter the period of regular coding.')
                pass
            else:
                try:
                    period = float(period)
                except:
                    tkinter.messagebox.showerror('Something went wrong...', 
                                     'Interval is wrong.')
                    pass
            all_specs.update({'period': period})
        else:
            all_specs.update({'period': None})

        if len(self.codes_container) == 0:
            tkinter.messagebox.showerror('You forgot something...', 
                             'Enter at least one code.')
            pass
        else:
            all_specs.update({'codes': self.codes_container})
       
        if len(self.sites_container) == 0:
            tkinter.messagebox.showerror('You forgot something...', 
                             'Enter at least one recording site.')
            pass
        else:
            all_specs.update({'sites': self.sites_container})

        print(all_specs)

        html_report = H.to_html_report(all_specs)
        print(html_report)

        filename = tkinter.filedialog.asksaveasfilename(
                                      initialdir=os.path.expanduser('~'),
                                      initialfile=pname+'.jod')

        # FIXME: does not work if file already exists
        if U.is_valid_filename(filename):
            if not filename.endswith('.jod'):
                filename += '.jod'
            datafile = open(filename, 'w')
            json.dump(all_specs, datafile)
            datafile.close()

            dirname, fname = os.path.split(filename)
            html_file = os.path.join(dirname, fname.replace('.jod', '.html'))
            htmlfile = open(html_file, 'w')
            htmlfile.write(html_report)
            htmlfile.close()
            
            print('data: ', all_specs)
            print('Saved in %s and %s' % (filename, html_file))
            self.saved = True
            self.destroy()
        else:
            tkinter.messagebox.showinfo('File not saved', 'File has not been saved')
            pass

class RecordedCode(tkinter.Label):

    def __init__(self, application, name, items, index):

        parent = application.recorded_codes
        self.name = name

        codelabel = name + ' = ' + ' / '.join(items)
        self.label = tkinter.Label(parent, text=codelabel)
        self.label.grid(column=1, row=index)
        self.but = tkinter.Button(parent, text='Delete',
                                          command=partial(self.delete, application))
        self.but.grid(sticky=U.sticky_all, row=index)

    def delete(self, app):
        app.codes_container = {key:val 
                        for key, val in app.codes_container.items() if key != self.name}
        app.listcode.set(' '.join(list(app.codes_container.keys())))
        self.label.destroy()
        self.but.destroy()

class RecordedSite(tkinter.Label):

    def __init__(self, application, name, items, index):

        parent = application.recorded_sites
        self.name = name

        sitelabel = name + ' = ' + ' | '.join(items)
        self.label = tkinter.Label(parent, text=sitelabel)
        self.label.grid(column=1, row=index)
        self.but = tkinter.Button(parent, text='Delete',
                                          command=partial(self.delete, application))
        self.but.grid(sticky=U.sticky_all, row=index)

    def delete(self, app):
        app.sites_container = {key:val 
                        for key, val in app.sites_container.items() if key != self.name}
        self.label.destroy()
        self.but.destroy()

if __name__ == '__main__':
    
    NewCode().mainloop()
