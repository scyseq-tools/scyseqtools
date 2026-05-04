"""
Module used to serve the symbolic routines in the context of behavioral studies
"""
# import io
# import json
import sys
import typing
import itertools

import numpy as np

# sys.path.append('/home/zarpe/scikits-symbolic/symbolic')
from scyseq import sequence as S
from scyseq import information as I
from scyseq import algorithmic as A
from scyseq import stochastic as T

SEQ_EXT = '.cdx'
TABLE_EXT = '.csv'
SEP = ';'

# class PORTABLE_STRING(object):
#    pass



#class Sequence(LadonType):
#class Sequence():
#    pass
#    """
#    A usable representation of a symbolic sequence
#    """
#    alphabet = {'type': [PORTABLE_STRING],
#                'doc': 'List of coding items'}
#    svalues = {'type': [int],
#               'doc': 'The sequence itself, ie a list of integers'}

Data = list[dict[str, typing.Any]]

#class Data(LadonType):
#class Data(object):
#    pass
#    """
#    Information about data surrounding the symbolic sequence.
#    """
#    filename = {'type': PORTABLE_STRING,
#                'doc': 'Filename where data come from'}
#    sitename = {'type': PORTABLE_STRING,
#                'doc': 'Name of the recording site'}
#    codename = {'type': PORTABLE_STRING,
#                'doc': 'Name of the encoding framework'}
#    sequence = {'type': Sequence,
#                'doc': 'The sequence and its alphabet'}

#class File(LadonType):
class File():
    """
    I'm not sure this is very useful...
    """
    pass
#    """
#    A file object with a name and a data buffer
#    """
#    name = PORTABLE_STRING
#    data = attachment

#def get_symbolic(sequence):
#    """
#    Get the symbolic sequence from a data.sequence
#    """
#    return S.Sequence(sequence.svalues, sequence.alphabet)

#def sequence_to_file(filename, sitename, codename, sequence):
#    """
#    Gathers all information to pack in a file for a symbolic sequence
#    """
#    retfile = File()
#    retfile.name = filename
#    strio = io.StringIO()
#    res_dict = {'data': {\
#                sitename: {\
#                codename: {\
#                'seq': [int(sval) for sval in sequence.svalues],
#                'dico': dict((str(nos), sym)
#                        for nos, sym in enumerate(sequence.alphabet))}}}}
#
#    json.dump(res_dict, strio)
#    strio.seek(0) # otherwise strio.read returns an empty string
#    retfile.data = attachment(strio)
#    return retfile
#
#def table_to_file(filename, headers, table_rows):
#    """
#    Gathers all the information to pack in a file for a table of results
#    """
##    retfile = File()
##    retfile.name = filename
#    strio = io.StringIO()
#    strio.write(SEP.join(headers) + '\n')
#    for row in table_rows:
#        strio.write(SEP.join([str(item) for item in row]) + '\n')
#    strio.seek(0) # otherwise strio.read returns an empty string
##    retfile.data = attachment(strio)
#    retfile = strio.getvalue()
#    return retfile

def to_table(headers, rows):
    """
    Convert headers and rows to a list of lines ready to write to a file
    """
    # rows.insert(0, headers)
    table = [SEP.join(headers) + '\n']
    for row in rows:
        table.append(SEP.join([str(item) for item in row]) + '\n')
    return table

class Symbolix():
    """
    Main class for our Behavior server
    """
    def statistics(self, lod:Data) -> File :
        """
        Returns the length of each sequence and the symbols with their
        frequencies

        @param lod: list of data
        @rtype: a file with a table with the length of the sequences and 
        the frequency of each symbol.
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0]['sitename'], lod[0]['codename'], \
                             'statistics']) + TABLE_EXT
        headers = ['Filename', 'N']
        seq = lod[0]['sequence']
        headers.extend([symb.strval for symb in seq.alphabet])
#        headers.extend(['%s_%s' % (str(item), str(nb))
#                                   for nb, item in enumerate(seq.alphabet)])
        rows = []
        for data in lod:
            retlist = [data['filename']]
            seq = data['sequence']
            retlist.append(len(seq))
            retlist.extend(seq.frequency())
            rows.append(retlist)

        return (filename, to_table(headers, rows))

    def mutual_information(self, lod1:Data, lod2:Data) -> File :
        """
        Returns the mutual information between two sequences

        @param lod1: First list of data
        @param lod2: Second list of data
        @rtype: Table with mutual information between sequences in lod1 and 
        sequences in lod2
        """
#        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod1[0]['sitename'], lod1[0]['codename'], \
                             lod2[0]['sitename'], lod2[0]['codename'], \
                             'mutual_information']) + TABLE_EXT
        headers = ['Filename', 'MI']

        rows = []
        for dat1, dat2 in zip(lod1, lod2):
            retlist = ['-'.join([dat1['filename'], dat2['filename']])]
            seq1 = dat1['sequence']
            seq2 = dat2['sequence']
            retlist.append(I.mutual_information(seq1, seq2))
            rows.append(retlist)

        return (filename, to_table(headers, rows))

    def complexity(self, lod:Data) -> File :
        """
        Returns the normalized Lempel-Ziv Complexity

        @param lod: List of data.
        @rtype: Table with Lempel-Ziv complexity
        """
#        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0]['sitename'], lod[0]['codename'], \
                             'lz_complexity']) + TABLE_EXT
        headers = ['Filename', 'LZ']

        rows = []
        for dat in lod:
            retlist = [dat['filename']]
            seq = dat['sequence']
            retlist.append(A.lempel_ziv(seq))
            rows.append(retlist)

        return (filename, to_table(headers,rows))

    def transition_probability(self, lod:Data, step:int) -> File :
        """
        Compute the transition matrix for a sequence for step time step ahead

        @param lod: List of data
        @param step: time step ahead to compute the influence.
        @rtype: Table with transition probabilities
        """
# FIXME - FIXME - FIXME - 
# FIXME: the direction of the influence is WRONG!!!
#        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0]['sitename'], lod[0]['codename'], \
                             f'transition{step}']) + TABLE_EXT
        headers = ['Filename']
        seq = lod[0]['sequence']
        headers.extend([f"{sfrom.strval}_{sto.strval}" \
                for sfrom, sto in itertools.product(seq.alphabet, repeat=2)])

        rows = []
        for dat in lod:
            retlist = [dat['filename']]
            seq = dat['sequence']
            retlist.extend(np.array(T.transition_matrix(seq, step)).flatten())
            rows.append(retlist)

        return (filename, to_table(headers, rows))

    def influence_probability(self, lod1:Data, lod2:Data, step:int) -> File :
        """
        Computes the influence of sequence one to sequence two for certain time
        step
        
        @param lod1: First list of data
        @param lod2: Second list of data
        @param step: time step ahead to compute the influence.
        @rtype: Table with influence probabilities from first to second.
        """
# FIXME - FIXME - FIXME - 
# FIXME: the direction of the influence is WRONG!!!
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod1[0]['sitename'], lod1[0]['codename'], \
                             lod2[0]['sitename'], lod2[0]['codename'], \
                             f"influence{step}"]) + TABLE_EXT
        headers = ['Filename']
        seq1 = lod1[0]['sequence']
        seq2 = lod2[0]['sequence']
        headers.extend([f'{sfrom.strval}-{sto.strval}' \
            for sfrom, sto in itertools.product(seq1.alphabet, seq2.alphabet)])

        rows = []
        for dat1, dat2 in zip(lod1, lod2):
            retlist = ['-'.join([dat1['filename'], dat2['filename']])]
            seq1 = dat1['sequence']
            seq2 = dat2['sequence']
            arr = np.array(T.influence_matrix(seq1, seq2, step))
            retlist.extend(arr.flatten())
            rows.append(retlist)

        return (filename, to_table(headers, rows))

    def join(self, lod1:Data, lod2:Data) -> File :
        """
        Joins two sequences
        
        @param lod1: First list of data
        @param lod2: Second list of data
        @rtype: A list of data with symbolic sequence joined from lod1 and lod2
        """
        retlist = []
        for dat1, dat2 in zip(lod1, lod2):
            # dicoseq = {}

            seq1 = dat1['sequence']
            seq2 = dat2['sequence']
            retseq = S.recode([seq1, seq2], new_alphabet=True)
            # retseq.alphabet = ['+'.join(coding.strval) for coding in retseq.alphabet]

            cod1 = '-'.join([dat1['sitename'], dat1['codename']])
            cod2 = '-'.join([dat2['sitename'], dat2['codename']])
            if '.' in dat1['filename']:
                filename = '_'.join(\
                    (dat1['filename'].rpartition('.')[0], cod1, cod2)) + SEQ_EXT
            else:
                filename = '_'.join((dat1['filename'], cod1, cod2)) + SEQ_EXT

            sitename = '+'.join((dat1['sitename'], dat2['sitename']))
            codename = '+'.join((dat1['codename'], dat2['codename']))

            #retfile = sequence_to_file(filename, sitename, codename, retseq)
            # retlist.append(retfile)
            retlist.append((filename, {sitename: {codename: retseq}}))

        return retlist

    def change_code(self, lod:Data, name:str,
                    correspondance:list[int], alphabet:list[str]) -> list[File] :
        """
        Change the code according to a correspondance given as a list of
        integers.

        @param lod: List of data
        @param correspondance: a list of integers
        @param: alphabet: a list of strings (in right order...)
        @rtype: A list of data with symbolic sequence recoded.
        """
        retlist = []

        for dat in lod:

            seq = dat['sequence']
            # new_alphabet = S.Alphabet(dict([(n,s) for n, s in enumerate(alphabet)]))
            new_alphabet = S.Alphabet(alphabet)
            newseq = S.transform(seq, correspondance, new_alphabet=new_alphabet)

            cod = '-'.join((dat['sitename'], name))
            if '.' in dat['filename']:
                filename = '_'.join(\
                    (dat['filename'].rpartition('.')[0], cod)) + SEQ_EXT
            else:
                filename = '_'.join((dat['filename'], cod)) + SEQ_EXT

#            retfile = sequence_to_file(filename, dat.sitename, name, newseq)
#            retlist.append(retfile)
            retlist.append((filename, {dat['sitename']: {name: newseq}}))

        return retlist
