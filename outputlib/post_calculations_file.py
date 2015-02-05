#!/usr/bin/python  # lint:ok
# -*- coding: utf-8


def post_calculations(main_dc):
    if main_dc['energy_system']['transmission']:
        transmission_line_power = {}
        for k in list(main_dc['lp']['trline_transfer']['data']['pos'].keys()):
            transmission_line_power[k] = {t: (
                main_dc['lp']['trline_transfer']['data']['neg'][k][t].varValue -
                main_dc['lp']['trline_transfer']['data']['pos'][k][t].varValue)
                for t in list(
                    main_dc['lp']['trline_transfer']['data']['pos'][k].keys())}
        if main_dc['energy_system']['transmission']:
            main_dc['lp']['trline_transfer']['data'] = transmission_line_power