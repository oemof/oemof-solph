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
    with open(ROOT + file_name) as f:
        reader = csv.DictReader(f, delimiter=DELIMITER)
        d = {}
        for line in reader:
            d[line["id"]] = dict(line)
    return d


def write_dict_to_csv(file_name, dict):
    with open(ROOT + file_name, 'wf') as f:
        d = dict.values()
        writer = csv.DictWriter(f, delimiter=DELIMITER, fieldnames=d[0].keys())
        writer.writeheader()
        writer.writerows(d)


def _load_config():
    global DELIMITER
    global ROOT
    #DELIMITER = cfg.get('csv', 'delimiter')
    ROOT = cfg.get('csv', 'root')
