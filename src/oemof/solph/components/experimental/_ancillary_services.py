# -*- coding: utf-8 -*-

"""
In-development component for ancillary services demand

SPDX-FileCopyrightText: Ekaterina Zolotarevskaia (e-zolotarevskaya)

SPDX-License-Identifier: MIT

"""
from oemof.solph.components._sink import Sink
import random

class AncillaryServices(Sink):
    """
    request
    timeindex
    price
    """
    def __init__(self, request, timeindex, price):
        self.request = request # timeseries of ancillary services request
        self.timeindex = timeindex
        self.price = price

    #julia-style draft
    def createAncServScen(self,nominal_value,request_number, timeindex):
        s_xi = random.choice([1,-1])
        recovery_time = 12
        if s_xi == 1:
            #Sink
        else:
            #Source
        t_xi = [0 for i in range(request_number)]
        for i in range(request_number):
            t_xi[i] = random.randrange(24)
        flow = [0. for i in range(recovery_time)]
        for t in t_xi:
            flow[t] = nominal_value


"""
constraint (model or model components/constraints/objectives, stage_index, anc_nominal_value, request_number = 1):
    create_scenario function (oemof model, realization of stoc vars)

"""
