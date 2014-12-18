#!/usr/bin/python
# -*- coding: utf-8

scenario = 'lk_wittenberg_reegis'
#scenario = 104
#scenario = 67

import logging
import time
import dblib as db
import solph
import dinput as indb
import outputlib as out

overwrite = True
failsafe = False
#scenario = 'lk_wittenberg_reegis'
scenario = 104
#scenario = 67

# Starts pahesmf and initialises the logger
main_dt = {}
main_dt['switch'] = {}
main_dt['switch']['read_re_data'] = True
main_dt['switch']['read_demand_data'] = True
main_dt['start'] = time.time()
db.define_logging()

if failsafe is True:
    logging.info('Pahesmf started in failsafe-mode!')
else:
    logging.info('Pahesmf started!')

# Checks and loggs the git version
db.check_git_branch(main_dt)

# Reads the input data and writes it into a dictionary
indb.read_pahesmf.parameter_from_db(scenario, main_dt, overwrite, failsafe)

# Creates an LP-Model and solves it
solph.start(scenario, main_dt, debug=False)

# Writes results into the pgsql-database
logging.info(('Writing results into database'))
main_dt.update(db.get_basic_dc())
main_dt['basic']['res_schema'] = 'pahesmf_dev_res'

out.write_all(main_dt, overwrite=overwrite)

db.time_logging(main_dt['start'], 'Pahesmf finished.', 'info')