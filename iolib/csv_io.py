"""
This Module provides ready to go csv2object creation for (hopefully) every object type.

TODO: Nope, it doesn't.

"""
import csv
import oemof.iolib.config as cfg

print("/iolib/csv_io.py imported")

DELIMITER = ','
ROOT = ''


def load_from_csv(file_name):
    reader = csv.DictReader(open(ROOT + file_name), delimiter=DELIMITER)
    return reader


def _load_config():
    global DELIMITER
    global ROOT
    #DELIMITER = cfg.get('csv', 'delimiter')
    ROOT = cfg.get('csv', 'root')
