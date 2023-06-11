"""
parser for interactive behavior file
"""
# from externals.scikits.symbolic.sequence import Sequence
# from ..sequence import Sequence

class ib:

    def __init__(self, filename):
        try:
            f = open(filename, 'r')
        except:
            raise IOError('File does not exist')

        self.text = f.read()

    def read(self):
        """
        Convert a file in InteractiveBehavior (ib) format to a dictionary
        of sequences or one single sequence
        """

        text = self.text

        specif = {}
        seqs = []
        no_indiv = -1 # FIXME: this is not very elegant...
        bool_part = False
        state = "init"

        for no_line, line in enumerate(text.splitlines()):
            # print no_line

            line = line.expandtabs(1)
            line = line.lstrip() 

            try:
                first_char = line[0]
            except IndexError:
                first_char = ''

            if first_char in ('#', '\n', ''):  # no commentary or blank line
                continue
            
            elif first_char == '%':
                if state == "init":
                    state = "specs"
                elif state == "specs":
                    state = "data"
                    # data_line = 0
                continue
            
            else:

                if state == "specs":

                    if first_char == ':':
                        lk = line.split()
                        k = lk[0].replace(':','') # delete the ':'
                        if k == 'regular':
                            specif.update({k : eval(lk[1])})
                            continue
                        elif k == 'participants':
                            bool_part = True
                            continue
                        else:
                            specif.update({k : lk[1]})
                            continue

                    elif first_char == '[' and bool_part:
                        no_indiv += 1
                        no_seq = 0
                        indiv = line.replace('[','').replace(']','')
                        seqs.append({"name" : indiv, "seq" : [] })
                    
                    else:
                        wordlist = line.split()
                        type_name = wordlist.pop(0)
                        seqs[no_indiv]['seq'].append({'code_name' : type_name, 'dico': {}, 'locseq' : []})

                        code = {}
                        for word in wordlist:
                            keyval = word.split(':')
                            code.update({int(keyval[0]): keyval[1]})

                        seqs[no_indiv]['seq'][no_seq]['dico'].update(code)
                        no_seq += 1

                
                if state == "data":

                    decoupe = line.split()

                    for no_indiv, code in enumerate(decoupe):
                    
                        for no_code, val in enumerate(code):
                        
                            if int(val) in seqs[no_indiv]['seq'][no_code]['dico']:
                                seqs[no_indiv]['seq'][no_code]['locseq'].append(int(val))
                            else:
                                raise ValueError("Error in coding in line %s for indiv %s and code %s" \
                                        %  (str(no_line + 1), str(no_indiv), str(no_code)))
        
#        retval = []
#
#        for d in seqs:
#            for sd in d['seq']:
#                retval.append(Sequence(s = sd['locseq'], a = sd['dico'],\
#                              regular = specif['regular'], period = float(specif['period']),\
#                              t_unit = specif['t_unit'], rec_site = d['name'],\
#                              code = sd['code_name']))

#        return retval
        return specif, seqs

if __name__ == '__main__':

    """  test """

    test = ib('ib.txt')
    lseq = test.read()
    print(lseq)
    test = ib('ib.cod')
    lseq = test.read()
    print(lseq)

#    for seq in lseq:
#        print seq.rec_site
#        print seq.period
#        print seq.t_unit
#        print seq.d
#        print seq.s
#        print seq.regular
#        print seq.code
#        print
#    """
#    test = ib('examples/single.ib')
#    lseq = test.read()
#
#    for seq in lseq:
#        print seq.rec_site
#        print seq.period
#        print seq.t_unit
#        print seq.d
#        print seq.s
#        print seq.regular
#        print seq.code
#        print
#    """
