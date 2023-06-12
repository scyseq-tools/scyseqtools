#! == encoding:utf8 ==
"""
Module to deal with the methods exposed by json-wsp server
"""
import tkinter
import tkinter.filedialog
import os
import json
from parameters import Parameter
import utils as U

class Method(object):
    """
    Main class to represent the methods exposed by json-wsp server
    """
    # def __init__(self, name, client, page):
    def __init__(self, name, parent):
        """
        Define the method with its tab and own method
        """
        self.name = name
        self.tab = parent.notebook.add(self.name.replace('_', ' ').title())
        self.parent = parent

        self.client = parent.json_client
        method_info = self.client.method_info(self.name)
        ret_info = method_info['ret_info']
        self.rtype = ret_info['type']
        params_info = method_info['params_info']
        doc_lines = method_info['doc_lines']
        # Documentation
        doc_frame = tkinter.LabelFrame(self.tab, text='Documentation')
        tkinter.Label(doc_frame, text='\n'.join(doc_lines)).grid()
        doc_frame.grid(column=0, row=0)
        # Inputs
        self.gdata = {}
        self.selected_files = []
        self.parameters = []

        for param, status in params_info.items():
        # status in: ['def_order', 'doc_lines', 'type', 'optional']
            par = Parameter(param, status, self)
            par.frame.grid(column=int(status['optional']),
                           row=status['def_order']+2)
            self.parameters.append(par)
        
        launch_but = tkinter.Button(self.tab, text='Launch',
                                    command=self.launch)
        launch_but.grid(sticky=tkinter.W)

    def launch(self):
        """
        Launches the method of the service
        """
        method = self.name
        in_params = {}
        for param in self.parameters:
            if param.ptype in ['number', 'string', 'float']: #, 'Correspondance']:
                in_params[param.name] = param.get()
            elif param.ptype.startswith('listof'):
                in_params[param.name] = param.get().split(', ')

                print(in_params[param.name])

            elif param.ptype == 'Data':
                outval = param.get()
                s_site, s_code = outval['site'], outval['code']
                retval = []
                for fichier in self.selected_files:
                    dico = self.gdata[fichier][s_site][s_code]['dico']
                    d = []
                    for nb in range(len(dico)):
                        d.append(dico[str(nb)]) # so we get it in order
                    s = self.gdata[fichier][s_site][s_code]['seq']
                    retval.append({'filename': os.path.basename(fichier),
                                   'sitename': s_site,
                                   'codename': s_code,
                                   'sequence': {'svalues': s,
                                                'alphabet': d}})
                in_params[param.name] = retval

#         print in_params

        output = self.client.call_method(method, **in_params)
        try:
            result = output.response_dict['result']
        except KeyError:
            print(output.response_body)

        # save the results
        if type(result) is list:
            # choose a directory
            outdir = tkinter.filedialog.askdirectory()
            if outdir is not None:
                if not os.path.exists(outdir):
                    os.mkdir(outdir)

                for ffile in result:
                    fname = os.path.join(outdir, ffile['name'])
                    ofid = open(fname, 'wb')
                    ofid.write(ffile['data'].read())
                    ofid.close()

        elif type(result) is dict:
            # save file as
            outfile = tkinter.filedialog.asksaveasfilename(initialfile=result['name'],
                                                     initialdir=self.parent.ddir)
            if outfile is not None:
                ofid = open(outfile, 'wb')
                ofid.write(result['data'].read())
                ofid.close()
        else:
            raise ValueError("Do not know the type of the result")
        
    def update_state(self, state):
    # def update_state(self):
        """
        Update the interface on the basis of application changes
        """
        # FIXME: this could certainly use self.parent.selected_files etc. but
        # need to change parameters
        self.selected_files = state['files']
        self.gdata = state['data']
        for param in self.parameters:
            param.update(state)
