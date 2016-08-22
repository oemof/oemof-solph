"""
writes a csv-file to a database specified in `~/.oemof/config.ini`-
run as `python write_results_to_db_py tablename file.csv`.

does need a section in ~/.oemof/config.ini with:

    [renpassgis results]
        username = 
        database = 
        host     = 
        port     = 
        pw       = 
        schema   = 
"""

import sys
import os.path as path
from configparser import ConfigParser
import pandas as pd
from sqlalchemy import create_engine

try:
    tablename = sys.argv[1]
except:
    raise Exception("Please specify tablename as first and csv-file as second argument")

try:
    csv_file = sys.argv[2]
except:
    raise Exception("Please specify csv-file as second argument")

print("Writing", csv_file, "into table", tablename)

cfg = ConfigParser()
cfg.read(path.join(path.expanduser("~"), '.oemof', 'config.ini'))

section = "renpassgis results"

uri = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(
        user=cfg.get(section, "username"),
        passwd=cfg.get(section, "pw"),
        host=cfg.get(section, "host"),
        db=cfg.get(section, "database"),
        port=cfg.get(section, "port"))

schema = cfg.get(section, "schema")

print("Using database connection")
print(uri)
print("with schema", schema)

df = pd.read_csv(csv_file)
df.columns = [c.lower() for c in df.columns]

engine = create_engine(uri)

print("Writing to Database")

df.to_sql(tablename, engine, schema=schema)

print("Finished")

