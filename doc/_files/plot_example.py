#!/usr/bin/python
# -*- coding: utf-8

scenario = 'lk_wittenberg_reegis'
#scenario = 104
#scenario = 67

import logging
import dblib as db
import outputlib as out


db.define_logging()
logging.info('Pahesmf plot started!')
main_dc = db.get_basic_dc()

main_dc['basic']['res_schema'] = 'pahesmf_dev_res'

out.read_results(scenario, main_dc)

main_dc['res'] = out.restructure_results_generation_demand(main_dc)

# Define the plot interval using the hours of the year
# The plot interval should not exceed the result intervall.
# This intervall is optional. If not set,
# the result intervall will be plotted.
main_dc['res']['info']['plotstart'] = 3192
main_dc['res']['info']['plotend'] = 3384
main_dc['res']['xlabel'] = 'Hour of the Year (6. April - 20. April)'


#out.test_plot(db.get_basic_dc())
out.multiplot(main_dc, main_dc['res']['info']['regions'],
    ['elec', 'heat'])
#plot.singleplot(main_dc, main_dc['res']['info']['regions'],
    #['elec', 'heat'])