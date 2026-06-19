# import ib
import os
import tkinter
from pymediainfo import MediaInfo

sticky_all = (tkinter.W, tkinter.N, tkinter.S, tkinter.E)

# sec_abbrev = ('seconde', 'secondes', 'sec.', 'sec', 'second', 'seconds', 's', 's.')

def focus_widget(widget):
    """
    Give keyboard focus to a widget and bring its window to the front.
    """
    top_level = widget.winfo_toplevel()
    top_level.update_idletasks()
    top_level.lift()
    top_level.focus_force()
    widget.focus_set()

def ensure_subdirectory(parent, name):
    """
    Create a direct subdirectory if needed and return its path.
    """
    folder = os.path.join(os.path.expanduser(parent), name)
    os.makedirs(folder, exist_ok=True)
    return folder

def is_valid_media(fname):
    if is_valid_filename(fname):
        fileInfo = MediaInfo.parse(fname)
        track_types = [track.track_type for track in fileInfo.tracks]
        if "Video" in track_types or "Audio" in track_types:
            return True
#        else:
#            return False
    return False

#    for track in fileInfo.tracks:
#        if track.track_type == "Video" or track.track_type == "Audio":


def inverse_dict(d):
    rd = {}
    for k,v in d.items():
        rd.update({v:k})
    return rd

def is_valid_filename(fname, ext=None):
    if fname in ['', ()]:
        return False
    elif ext is not None and type(ext) == str:
        if not fname.endswith(ext):
            return False
    return True

def convert_jod(jdict):
    retval = {'specs':{}, 'codes': {}}

    if jdict['interval'] is None:
        retval['specs'].update({'period': None, 
                                't_unit': None, 
                                'regular': False})
    else:
        retval['specs'].update({'period': jdict['interval'], 
                                't_unit': 'second', 
                                'regular': True})

    base_codes = {}
    codes = jdict['codes']
    for k, v in codes.items():
        dcode = dict([(s,n) for n, s in enumerate(v)])
        base_codes.update({k: dcode}) 

    sites = jdict['sites']
    for k, v in sites.items():
        dsite = {}
        for code in v:
            dsite.update({code: base_codes[code]})
        retval['codes'].update({k: dsite})
    #print(retval)
    return retval

#def cod2jod(fname):
#    """convert into (with list so that order is constant): 
#
#    code = {'codes': {'recording_site':
#                       {'code': 
#                       {'symbol0':0, 'symbol1':1}}, ...},
#            'specs': {'period': 5, 't_unit': 'sec.', 'regular': True}}
#
#    CAUTION: dico for code is a reverse dico: 'symbol':int
#    """
#
#    ib_reader = ib.ib(fname)
#    specif, lseq = ib_reader.read()
#    # check that t_unit = second
#    assert(specif['t_unit'].lower() in sec_abbrev)
#
#    code =  {'specs': {'period': float(specif['period']),
#                         't_unit': specif['t_unit'], 
#                         'regular': specif['regular']}}
#    codelist = {}
#    for seq in lseq:
#        codelist.update({seq['name']: {}})
#        for cc in seq['seq']:
#            codelist[seq['name']].update({cc['code_name']: inverse_dict(cc['dico'])})
#
#    code.update({'codes': codelist})
#
#    return code

#if __name__ == '__main__':
#
#    fname = '../ib.cod'
#
#    print(cod2jod(fname))

