"""
Module to deal with the methods exposed by symbolix
"""
import tkinter
import tkinter.filedialog

import pathlib

import copy
from datetime import datetime
import json
import os
# import inspect
import sys

from scyseqtools.analyser.parameters import Parameter
# import utils as U
# import symbolix

# SEQ_EXT = '.json'
TABLE_EXT = '.csv'
SEP = ';'


def _as_codix_writer_sequences(dico_seqs):
    """
    Adapt analyser sequence mappings to the shape accepted by write_codix.
    """
    return {
        site: list(codes.items()) if hasattr(codes, 'items') else codes
        for site, codes in dico_seqs.items()
    }


def _sequence_values(sequence):
    return sequence.ivals.tolist()


def _sequence_alphabet(sequence):
    return list(sequence.alphabet.svals)


def _codix_container(source_metadata, dico_seqs):
    """
    Build a Codix record for analyser-generated sequence outputs.
    """
    container = copy.deepcopy(source_metadata) if source_metadata else {}
    container.setdefault('history', [])
    container.setdefault('media', '')
    container.setdefault('times', [])
    container.setdefault('comments', [])
    container.setdefault('version', '0.9')

    code = copy.deepcopy(container.get('code', {}))
    code['codes'] = {}
    code['sites'] = {}

    data = {}
    for site, code_sequences in _as_codix_writer_sequences(dico_seqs).items():
        data[site] = {}
        code['sites'][site] = []
        for codename, sequence in code_sequences:
            code['sites'][site].append(codename)
            code['codes'][codename] = _sequence_alphabet(sequence)
            data[site][codename] = _sequence_values(sequence)

    container['code'] = code
    container['data'] = data
    container['history'].append(
        (datetime.now().strftime('%c'), 'cdx-analyzer', '')
    )
    return container


def write_codix_export(fname, dico_seqs, source_metadata=None):
    """
    Write analyser-generated Codix data while preserving source metadata.
    """
    container = _codix_container(source_metadata, dico_seqs)
    with open(fname, 'w', encoding='utf-8') as datafile:
        json.dump(container, datafile)


class Method():
    """
    Main class to represent the methods exposed by symbolix
    """
    def __init__(self, name, meth, parent):
        """
        Define the method with its tab and own method
        """
        # Inputs
        self.gdata = {}
        self.metadata = {}
        self.selected_files = []
        self.parameters = []

        self.name = name
        self.tab = parent.notebook.add(self.name.replace('_', ' ').title())
        self.parent = parent
        doc_lines = meth.__doc__
        self.method = meth
        annotations = meth.__annotations__
        # retval = annotations.pop('return')
        _ = annotations.pop('return')
        args = annotations

        # Documentation
        doc_frame = tkinter.LabelFrame(self.tab, text='Documentation')
        tkinter.Label(doc_frame, text=doc_lines).grid()
        doc_frame.grid(column=0, row=0)

        for param in args.items():
            par = Parameter(*param, self)
#            par.frame.grid(column=int(status['optional']),
#                           row=status['def_order']+2)
            par.frame.grid()
            self.parameters.append(par)

        launch_but = tkinter.Button(self.tab, text='Launch',
                                    command=self.launch)
        launch_but.grid(sticky=tkinter.W)

    def launch(self):
        """
        Launches the method of the service
        """
        in_params = {param.name: param.get() for param in self.parameters}

        print(in_params)
        # print(inspect.signature(self.method))
        output = self.method(self.method, **in_params)
        print(output)

#        output = self.client.call_method(method, **in_params)
#        try:
#            result = output.response_dict['result']
#        except KeyError:
#            print(output.response_body)

#       Save the results
        initialdir = os.path.join(self.parent.cwd, self.name)
        print('initial folder: ', initialdir)
        if not os.path.exists(initialdir):
            pathlib.Path(initialdir).mkdir()

        outdir = None
        while not outdir:
            outdir = tkinter.filedialog.askdirectory(initialdir=initialdir,
                                                     mustexist=True)
        if len(output) == 2:
        # FIXME: Suppose this is a table
            fname, table = output
            with open(os.path.join(outdir, fname), 'w', encoding='utf-8') as datafile:
                datafile.writelines(table)
        else:
        # FIXME: Suppose this is a list of sequences...
            for index, elem in enumerate(output):
                fname, dico_seqs = elem
                datafile = os.path.join(outdir, fname)
                source_metadata = self._source_metadata(index)
                write_codix_export(datafile, dico_seqs, source_metadata)

        # Not useful since either created or must exist...
#        if outdir is not None:
#            if not os.path.exists(outdir):
#                pathlib.Path(outdir).mkdir()

#        if type(output) is list:
#
#            for ffile in result:
#                fname = os.path.join(outdir, ffile['name'])
#                ofid = open(fname, 'wb')
#                ofid.write(ffile['data'].read())
#                ofid.close()
#
#        elif type(result) is dict:
#            # save file as
#            outfile = tkinter.filedialog.asksaveasfilename(initialfile=result['name'],
#                                                     initialdir=self.parent.ddir)
#            if outfile is not None:
#                ofid = open(outfile, 'wb')
#                ofid.write(result['data'].read())
#                ofid.close()
#        else:
#            raise ValueError("Do not know the type of the result")

    def update_state(self, state):
        """
        Update the interface on the basis of application changes
        """
        # FIXME: this could certainly use self.parent.selected_files etc. but
        # need to change parameters
        self.selected_files = state['files']
        self.gdata = state['data']
        self.metadata = state.get('metadata', {})
        for param in self.parameters:
            param.update(state)

    def _source_metadata(self, index):
        """
        Return metadata for the source file that produced an output row.
        """
        try:
            fname = self.selected_files[index]
        except (AttributeError, IndexError):
            return None
        return self.metadata.get(fname)
