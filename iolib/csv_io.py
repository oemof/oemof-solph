"""
This Module provides ready to go csv2object creation for (hopefully) every object type.

TODO: Nope, it doesn't.

"""
import csv
import oemof.iolib.config as cfg

print("/iolib/csv_io.py imported")

DELIMITER = ','
ROOT = ''



def load_dict_from_csv(file_name):
    """
    loads a list of dicts from a csv file.
    :param file_name: the filename.
    :return:the list of dicts.
    """
    _load_config()
    with open(ROOT + file_name) as f:
        reader = csv.DictReader(f, delimiter=DELIMITER)
        d = []
        i=0
        for line in reader:
            d.append(dict(line))
            i+=1
    return d


def write_dict_to_csv(file_name, dict):
    """
    writes a dict of dicts to a csv file.
    use with care or better not at all!
    :param file_name: the filename.
    :param dict: the dict of dicts.
    """
    _load_config()

    with open(ROOT + file_name, 'wf') as f:
        d = dict.values()
        writer = csv.DictWriter(f, delimiter=DELIMITER, fieldnames=d[0].keys())
        writer.writeheader()
        writer.writerows(d)


def _load_config():
    """
    loads the config
    :return:
    """
    global DELIMITER
    global ROOT
    #DELIMITER = cfg.get('csv', 'delimiter')
    ROOT = cfg.get('csv', 'root')
