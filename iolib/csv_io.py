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
    _load_config()
    with open(ROOT + file_name) as f:
        reader = csv.DictReader(f, delimiter=DELIMITER)
        d = {}
        i=0
        for line in reader:
            try:
                d[line["id"]] = dict(line)
            except:
                d[i] = dict(line)
                i+=1
    return d


def write_dict_to_csv(file_name, dict):
    _load_config()

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
