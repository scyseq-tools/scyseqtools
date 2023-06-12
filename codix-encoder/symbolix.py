#!== encoding:utf8 ==
"""
Module used to serve the symbolic routines in the context of behaviorla studies
"""
import itertools
import io
import json
import numpy as np

from .ladon.ladonizer import ladonize
from .ladon.types.ladontype import LadonType
from .ladon.types.attachment import attachment
from .ladon.compat import PORTABLE_STRING

from .scikits.symbolic import sequence as S
from .scikits.symbolic import information as I
from .scikits.symbolic import algorithmic as A
from .scikits.symbolic import stochastic as T

SEQ_EXT = '.json'
TABLE_EXT = '.csv'
SEP = ';'

class Sequence(LadonType):
    """
    A usable representation of a symbolic sequence
    """
    alphabet = {'type': [PORTABLE_STRING],
                'doc': 'List of coding items'}
    svalues = {'type': [int], 
               'doc': 'The sequence itself, ie a list of integers'}

class Data(LadonType):
    """
    Information about data surrounding the symbolic sequence.
    """
    filename = {'type': PORTABLE_STRING,
                'doc': 'Filename where data come from'}
    sitename = {'type': PORTABLE_STRING,
                'doc': 'Name of the recording site'}
    codename = {'type': PORTABLE_STRING,
                'doc': 'Name of the encoding framework'}
    sequence = {'type': Sequence,
                'doc': 'The sequence and its alphabet'}

class File(LadonType):
    """
    A file object with a name and a data buffer
    """
    name = PORTABLE_STRING
    data = attachment
    
def get_symbolic(sequence):
    """
    Get the symbolic sequence from a data.sequence
    """
    return S.Sequence(sequence.svalues, sequence.alphabet)
            
def sequence_to_file(filename, sitename, codename, sequence):
    """
    Gathers all information to pack in a file for a symbolic sequence
    """
    retfile = File()
    retfile.name = filename
    strio = io.StringIO()
    res_dict = {'data': {\
                sitename: {\
                codename: {\
                'seq': [int(sval) for sval in sequence.svalues],
                'dico': dict((str(nos), sym) 
                        for nos, sym in enumerate(sequence.alphabet))}}}}

    json.dump(res_dict, strio)
    strio.seek(0) # otherwise strio.read returns an empty string
    retfile.data = attachment(strio)
    return retfile

def table_to_file(filename, headers, table_rows):
    """
    Gathers all the information to pack in a file for a table of results
    """
    retfile = File()
    retfile.name = filename
    
    strio = io.StringIO() 
    strio.write(SEP.join(headers) + '\n')
    for row in table_rows:
        strio.write(SEP.join([str(item) for item in row]) + '\n')
    strio.seek(0) # otherwise strio.read returns an empty string
    retfile.data = attachment(strio)
    return retfile

class Symbolix(object):
    """
    Main class for our Behavior server
    """
    
    # numpy.float64 and numpy.int16 not in Ladon safe_conversion 

#    @ladonize(int, int, rtype=int)
#    def add(self, a,b):
#        return a+b

    @ladonize([Data], rtype=File)
    def statistics(self, lod):
        """
        Returns the length of each sequence and the symbols with their
        frequencies

        @param lod: list of data
        @rtype: a file with a table with the length of the sequences and the frequency of each symbol.
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0].sitename, lod[0].codename, \
                             'statistics']) + TABLE_EXT
        headers = ['Filename', 'N']
        seq = get_symbolic(lod[0].sequence)
        headers.extend(['%s_%s' % (str(item), str(nb)) 
                                   for nb, item in enumerate(seq.alphabet)])
        rows = []
        for data in lod:
            retlist = [data.filename]
            seq = get_symbolic(data.sequence)
            retlist.append(len(seq))
            retlist.extend(seq.frequency())
            rows.append(retlist)
        return table_to_file(filename, headers, rows)

    @ladonize([Data], [Data], rtype=File)
    def mutual_information(self, lod1, lod2):
        """
        Returns the mutual information between two sequences

        @param lod1: First list of data
        @param lod2: Second list of data
        @rtype: Table with mutual information between sequences in lod1 and sequences in lod2
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod1[0].sitename, lod1[0].codename, \
                             lod2[0].sitename, lod2[0].codename, \
                             'mutual_information']) + TABLE_EXT
        headers = ['Filename', 'MI']
        rows = []
        for dat1, dat2 in zip(lod1, lod2):
            retlist = ['-'.join([dat1.filename, dat2.filename])]
            seq1 = get_symbolic(dat1.sequence)
            seq2 = get_symbolic(dat2.sequence)
            retlist.append(I.mutual_information(seq1, seq2))
            rows.append(retlist)
        return table_to_file(filename, headers, rows)

    @ladonize([Data], rtype=File)
    def complexity(self, lod):
        """
        Returns the normalized Lempel-Ziv Complexity

        @param lod: List of data.
        @rtype: Table with Lempel-Ziv complexity
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0].sitename, lod[0].codename, \
                             'lz_complexity']) + TABLE_EXT
        headers = ['Filename', 'LZ']
        rows = []
        for dat in lod:
            retlist = [dat.filename]
            seq = get_symbolic(dat.sequence)
            retlist.append(A.lempel_ziv(seq))
            rows.append(retlist)
        return table_to_file(filename, headers, rows)

    @ladonize([Data], int, rtype=File)
    def transition_probability(self, lod, step):
        """
        Compute the transition matrix for a sequence for step time step ahead

        @param lod: List of data
        @param step: time step ahead to compute the influence.
        @rtype: Table with transition probabilities
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod[0].sitename, lod[0].codename, \
                             'transition+%s' % str(step)]) + TABLE_EXT
        headers = ['Filename']
        seq = get_symbolic(lod[0].sequence)
        headers.extend(['%s-%s' % (sfrom, sto) for sfrom, sto in \
                                  itertools.product(seq.alphabet, repeat=2)])
        rows = []
        for dat in lod:
            retlist = [dat.filename]
            seq = get_symbolic(dat.sequence)
            retlist.extend(np.array(T.transition_matrix(seq, step)).flatten())
            rows.append(retlist)
        return table_to_file(filename, headers, rows)

    @ladonize([Data], [Data], int, rtype=File)
    def influence_probability(self, lod1, lod2, step):
        """
        Computes the influence of sequence one to sequence two for certain time
        step
        
        @param lod1: First list of data
        @param lod2: Second list of data
        @param step: time step ahead to compute the influence.
        @rtype: Table with influence probabilities from first to second.
        """
        # assume that site, code and alphabet are the same for all the sequences
        filename = '_'.join([lod1[0].sitename, lod1[0].codename, \
                             lod2[0].sitename, lod2[0].codename, \
                             'influence+%s' % str(step)]) + TABLE_EXT
        headers = ['Filename']
        seq1 = get_symbolic(lod1[0].sequence)
        seq2 = get_symbolic(lod2[0].sequence)
        headers.extend(['%s-%s' % (sfrom, sto) for sfrom, sto in \
                              itertools.product(seq1.alphabet, seq2.alphabet)])
        rows = []
        for dat1, dat2 in zip(lod1, lod2):
            retlist = ['-'.join([dat1.filename, dat2.filename])]
            seq1 = get_symbolic(dat1.sequence)
            seq2 = get_symbolic(dat2.sequence)
            arr = np.array(T.influence_matrix(seq1, seq2, step))
            retlist.extend(arr.flatten())
            rows.append(retlist)
        return table_to_file(filename, headers, rows)
    
    @ladonize([Data], [Data], rtype=[File])
    def join(self, lod1, lod2):
        """
        Joins two sequences
        
        @param lod1: First list of data
        @param lod2: Second list of data
        @rtype: A list of data with symbolic sequence joined from lod1 and lod2
        """
        retlist = []
        for dat1, dat2 in zip(lod1, lod2):
            seq1 = get_symbolic(dat1.sequence)
            seq2 = get_symbolic(dat2.sequence)
            retseq = S.recode([seq1, seq2], new_dict=True)
            retseq.alphabet = ['+'.join(coding) for coding in retseq.alphabet] 

            cod1 = '-'.join([dat1.sitename, dat1.codename])
            cod2 = '-'.join([dat2.sitename, dat2.codename])
            if '.' in dat1.filename:
                filename = '_'.join(\
                    (dat1.filename.rpartition('.')[0], cod1, cod2)) + SEQ_EXT
            else:
                filename = '_'.join((dat1.filename, cod1, cod2)) + SEQ_EXT

            sitename = '+'.join((dat1.sitename, dat2.sitename))
            codename = '+'.join((dat1.codename, dat2.codename))

            retfile = sequence_to_file(filename, sitename, codename, retseq)
            retlist.append(retfile)
        return retlist

    @ladonize([Data], PORTABLE_STRING, [int], [PORTABLE_STRING], rtype=[File])
    def change_code(self, lod, name, correspondance, alphabet):
        """
        Change the code according to a correspondance given as a list of
        integers.

        @param lod: List of data
        @rtype: A list of data with symbolic sequence recoded.
        """
        retlist = []
        for dat in lod:
            
            seq = get_symbolic(dat.sequence)
            newseq = S.transform(seq, correspondance, new_d=alphabet)

            cod = '-'.join((dat.sitename, name))
            if '.' in dat.filename:
                filename = '_'.join(\
                    (dat.filename.rpartition('.')[0], cod)) + SEQ_EXT
            else:
                filename = '_'.join((dat.filename, cod)) + SEQ_EXT

            retfile = sequence_to_file(filename, dat.sitename, name, newseq)
            retlist.append(retfile)
        return retlist
