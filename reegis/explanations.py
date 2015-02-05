#!/usr/bin/python
# -*- coding: utf-8

'''
Erklärungen zu den Variablen:
    hourly_heat_demand -- Matrix (8760, 5)
                Spalte 0 -- Ölheizung
                Spalte 1 -- Gasheizung
                Spalte 2 -- Biomasseheizung
                Spalte 3 -- Fernwärme
                Spalte 4 -- Kohleheizung
    hourly_el_demand -- Spaltenvektor (8760, )
    hourly_wind_potential -- Spaltenvektor (8760, )
    hourly_pv_potential -- Spaltenvektor (8760, )
    hourly_biogas_potential -- Spaltenvektor (8760, )

    annual_biomass_potential -- Biomasse für Kraftwerke und Heizungen
'''