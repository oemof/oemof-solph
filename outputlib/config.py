# -*- coding: utf-8 -*-


def plot(main_dc):
    '''
    Adds the order list to the main_dc.
    The order-list is used to define the order of the components of the plot.
    '''
    main_dc['order'] = {}
    main_dc['order']['generation'] = [
        'tnuc', 'tlcp', 'thcp', 'tcpp',
        'rpvo', 'rpvr', 'rowi', 'rwin', 'twpp', 'tocg', 'topp', 'tgcb',
        'thoi', 'ahoi', 'dhoi',
        'thng', 'ahng', 'dhng',
        'twcb', 'awcb', 'dwcb', 'xwcb',
        'tbgc', 'tbbc', 'vbbc', 'tbga', 'thcc', 'tgac', 'vgac', 'tdhp', 'thdh',
        'tgbd', 'tbmc', 'vbmc', 'tccg', 'thxx',
        'sbat', 'sphs', 'trmi', 'txxx']
    main_dc['order']['demand'] = [
        'lele', 'sphs', 'sbat', 'tptg', 'trme',
        'rele', 'eexc', 'thoi', 'dhoi', 'thng', 'dhng', 'twcb', 'dwcb', 'tgcb',
        'dst0', 'hexc']
