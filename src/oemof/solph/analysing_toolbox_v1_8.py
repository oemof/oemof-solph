# -*- coding: utf-8 -*-
'''
General description
-------------------
This is the blackbox function. The aim of this function is to monitor inputs and outputs
of an locationsystem (more explanation in the example) in oemof.

Installation requirements
-------------------------
This example depends on an installation of oemof

20.03.2019 - philipp.gradl@stud.unileoben.ac.at
'''


from oemof.solph.custom import *
import oemof.solph as solph
import pandas as pd




def blackbox(results, locationsystem, get_inputs=False, get_outputs=False, get_innerflows=False, get_capacities=False, get_potentials=False, get_allpotentials=False):
    i=1

    input_data=get_input(results, locationsystem)
    output_data=get_output(results, locationsystem)
    innerflow_data=get_innerflow(results, locationsystem)
    capacity_data=get_capacity(results, locationsystem)
    potential_data=get_potential(results, locationsystem)
    allpotential_data = get_allpotential(results)
    combined_dataframe = pd.concat([input_data, output_data, innerflow_data, capacity_data, potential_data, allpotential_data], axis=1, sort=False)

    results=combined_dataframe

    if get_inputs==True:
        results=results,input_data

    if get_outputs==True:
        if type(results)==type(tuple()):
            results=results+tuple([output_data])

        if type(results)!=type(tuple()):
            results=results,get_outputs

    if get_innerflows==True:
        if type(results) == type(tuple()):
            results = results + tuple([innerflow_data])

        if type(results) != type(tuple()):
            results = results, innerflow_data

    if get_capacities == True:
        if type(results) == type(tuple()):
            results = results + tuple([capacity_data])

        if type(results) != type(tuple()):
            results = results, capacity_data

    if get_potentials==True:
        if type(results)==type(tuple()):
            results=results+tuple([potential_data])

        if type(results)!=type(tuple()):
            results=results,potential_data

    if get_allpotentials==True:
        if type(results) == type(tuple()):
            results = results + tuple([allpotential_data])

        if type(results) != type(tuple()):
            results = results, allpotential_data
    return results





###################################################################################
def res_key(results):
    result_keys=[]
    for key in results.keys():
        result_keys.append(key)
    return result_keys


###################################################################################
def get_input(results, locationsystem):
    in_data=pd.DataFrame()
    result_keys=res_key(results)
    for key in result_keys:
        if hasattr(key[0], 'label') and hasattr(key[1], 'label'):
            if type(key[0]) != type(solph.Source()) and type(key[1]) != type(solph.Source()) and type(key[0]) != type(solph.Sink()) and type(key[1]) != type(solph.Sink()):
                if hasattr(key[0].label, 'location')==True and hasattr(key[1].label, 'location')==True:
                    if key[0].label.location != '' and key[1].label.location != '':
                        if key[0].label.location not in locationsystem:
                            if key[1].label.location in locationsystem:
                                put_data_ob=pd.DataFrame(results[key]['sequences'])
                                column=put_data_ob.columns[0]
                                label = label_function(results, key)
                                put_data_ob=put_data_ob.rename(columns={column:label})
                                in_data=pd.concat([in_data,put_data_ob], axis=1)

                if hasattr(key[1].label, 'location')==True:
                    if hasattr(key[0].label, 'location')==False:
                        if key[1].label.location in locationsystem:
                            overlap=ob_location_test(key[0])
                            if overlap==False:
                                put_data_ob = pd.DataFrame(results[key]['sequences'])
                                column=put_data_ob.columns[0]
                                label = label_function(results, key)
                                put_data_ob = put_data_ob.rename(columns={column: label})
                                in_data = pd.concat([in_data, put_data_ob], axis=1)

                    if hasattr(key[0].label, 'location')==True:
                        if key[0].label.location == '':
                            if key[1].label.location in locationsystem:
                                overlap = ob_location_test(key[0])
                                if overlap == False:
                                    put_data_ob = pd.DataFrame(results[key]['sequences'])
                                    column = put_data_ob.columns[0]
                                    label = label_function(results, key)
                                    put_data_ob = put_data_ob.rename(columns={column: label})
                                    in_data = pd.concat([in_data, put_data_ob], axis=1)

                    if type(key[0]) == type(Link()):
                        if hasattr(key[1].label, 'location'):
                            if key[1].label.location in locationsystem:
                                put_data_ob = pd.DataFrame(results[key]['sequences'])
                                column = put_data_ob.columns[0]
                                label = label_function(results, key)
                                put_data_ob = put_data_ob.rename(columns={column: label})
                                in_data = pd.concat([in_data, put_data_ob], axis=1)

            if type(key[0]) == type(solph.Source()):
                if hasattr(key[1].label, 'location'):
                    if key[1].label.location in locationsystem:
                        put_data_ob = pd.DataFrame(results[key]['sequences'])
                        column = put_data_ob.columns[0]
                        label = label_function(results, key)
                        put_data_ob = put_data_ob.rename(columns={column: label})
                        in_data = pd.concat([in_data, put_data_ob], axis=1)





    return in_data

####################################################################################

def ob_location_test(object):
    input_location_list=[]
    output_location_list=[]
    for input in object.inputs:
        if hasattr(input, 'label'):
            if hasattr(input.label, 'location'):
                input_location_list.append(input.label.location)
    for output in object.outputs:
        if hasattr(output, 'label'):
            if hasattr(output.label, 'location'):
                output_location_list.append(output.label.location)

    overlap=False

    for location_ob_in in input_location_list:
        for location_ob_out in output_location_list:
            if location_ob_in==location_ob_out:
                overlap=True

    return overlap


####################################################################################
def get_output(results, locationsystem):
    out_data=pd.DataFrame()

    result_keys=res_key(results)

    for key in result_keys:
        if hasattr(key[0], 'label') and hasattr(key[1], 'label'):
            if type(key[0]) != type(solph.Source()) and type(key[1]) != type(solph.Source()) and type(key[0]) != type(solph.Sink()) and type(key[1]) != type(solph.Sink()):
                if hasattr(key[0].label, 'location')==True and hasattr(key[1].label, 'location')==True:
                    if key[0].label.location != '' and key[1].label.location != '':
                        if key[0].label.location in locationsystem:
                            if key[1].label.location not in locationsystem:
                                put_data_ob=pd.DataFrame(results[key]['sequences'])
                                column=put_data_ob.columns[0]
                                label = label_function(results, key)
                                put_data_ob=put_data_ob.rename(columns={column:label})
                                out_data=pd.concat([out_data,put_data_ob], axis=1)

                if hasattr(key[0].label, 'location')==True:
                    if hasattr(key[1].label, 'location')==False:
                        if key[0].label.location in locationsystem:
                            overlap=ob_location_test(key[1])
                            if overlap==False:
                                put_data_ob = pd.DataFrame(results[key]['sequences'])
                                column=put_data_ob.columns[0]
                                label = label_function(results, key)
                                put_data_ob = put_data_ob.rename(columns={column: label})
                                out_data = pd.concat([out_data, put_data_ob], axis=1)

                    if hasattr(key[1].label, 'location')==True:
                        if key[1].label.location == '':
                            if key[0].label.location in locationsystem:
                                overlap = ob_location_test(key[1])
                                if overlap == False:
                                    put_data_ob = pd.DataFrame(results[key]['sequences'])
                                    column=put_data_ob.columns[0]
                                    label=label_function(results, key)
                                    put_data_ob = put_data_ob.rename(columns={column: label})
                                    out_data = pd.concat([out_data, put_data_ob], axis=1)

                if type(key[1])==type(Link()):
                    if hasattr(key[0].label, 'location'):
                        if key[0].label.location in locationsystem:
                            put_data_ob = pd.DataFrame(results[key]['sequences'])
                            column = put_data_ob.columns[0]
                            label = label_function(results, key)
                            put_data_ob = put_data_ob.rename(columns={column: label})
                            out_data = pd.concat([out_data, put_data_ob], axis=1)

            if type(key[1]) == type(solph.Sink()):
                if hasattr(key[0].label, 'location'):
                    if key[0].label.location in locationsystem:
                        put_data_ob = pd.DataFrame(results[key]['sequences'])
                        column = put_data_ob.columns[0]
                        label = label_function(results, key)
                        put_data_ob = put_data_ob.rename(columns={column: label})
                        out_data = pd.concat([out_data, put_data_ob], axis=1)


    return out_data
####################################################################################
def get_innerflow(results, locationsystem):
    innerflow_data=pd.DataFrame()
    result_keys=res_key(results)
    key_list=[]
    for key in result_keys:
        if type(key[0])!=type(solph.Source()) and type(key[1])!=type(solph.Source()) and type(key[0])!=type(solph.Sink()) and type(key[1])!=type(solph.Sink()):
            if type(key[0])!=type(Link()) and type(key[1])!=type(Link()):
                if hasattr(key[0], 'label')and hasattr(key[1], 'label'):
                    if hasattr(key[0].label, 'location') and hasattr(key[1].label, 'location'):
                        if key[0].label.location in locationsystem and key[1].label.location in locationsystem:
                            key_list.append(key)

                        if key[0].label.location=='' and key[1].label.location in locationsystem:
                            overlap=ob_location_test(key[0])
                            if overlap==True:
                                key_list.append(key)

                        if key[1].label.location=='' and key[0].label.location in locationsystem:
                            overlap=ob_location_test(key[1])
                            if overlap==True:
                                key_list.append(key)

                if hasattr(key[0], 'label')and hasattr(key[1], 'label'):
                    if hasattr(key[0].label, 'location')==False or hasattr(key[1].label, 'location')==False:
                        if hasattr(key[0].label, 'location'):
                            if key[0].label.location in locationsystem:
                                overlap=ob_location_test(key[1])
                                if overlap==True:
                                    key_list.append(key)

                        if hasattr(key[1].label, 'location'):
                            if key[1].label.location in locationsystem:
                                overlap=ob_location_test(key[0])
                                if overlap==True:
                                    key_list.append(key)

    for key in key_list:
            put_data_ob = pd.DataFrame(results[key]['sequences'])
            column = put_data_ob.columns[0]
            label = label_function(results, key)
            put_data_ob = put_data_ob.rename(columns={column: label})
            innerflow_data = pd.concat([innerflow_data, put_data_ob], axis=1)

    return innerflow_data
####################################################################################
def label_function(results, key):
    data=pd.DataFrame(results[key]['sequences'])
    column=data.columns[0]

    if hasattr(key[0], 'label') and hasattr(key[1], 'label'):
        if type(key[0].label)!=str and type(key[1].label)!=str:
            label = tuple(key[0].label) + tuple(key[1].label) + tuple([column])

    if hasattr(key[0], 'label')==False or hasattr(key[1], 'label')==False:
        ob=find_the_ob(key)
        label_0=ob.label
        if type(label_0)==str:
            label_0=[label_0]
        label=tuple(label_0)+ tuple([column])

    if hasattr(key[0], 'label') and hasattr(key[1], 'label'):
        if type(key[0].label)==str:
            label_key_0=tuple([key[0].label])

        if type(key[1].label)==str:
            label_key_1=tuple([key[1].label])

        if type(key[0].label) != str:
            label_key_0 = tuple(key[0].label)

        if type(key[1].label) != str:
            label_key_1 = tuple(key[1].label)

        label=label_key_0+label_key_1

    return label
####################################################################################
def find_the_ob(key):
    if hasattr(key[0], 'label')==True:
        ob=key[0]
    if hasattr(key[1], 'label')==True:
        ob=key[1]

    return ob
####################################################################################
def get_capacity(results, locationsystem):
    capacity_dataframe=pd.DataFrame()
    key_list=res_key(results)
    for key in key_list:
        if hasattr(key[0], 'label')==False or hasattr(key[1], 'label')==False:
            relevant=False
            if hasattr(key[0], 'inputs'):
                for input in key[0].inputs:
                    if hasattr(input, 'label'):
                        if hasattr(input.label, 'location'):
                            if input.label.location in locationsystem:
                                relevant=True

            if hasattr(key[0], 'outputs'):
                for output in key[0].outputs:
                    if hasattr(output, 'label'):
                        if hasattr(output.label, 'location'):
                            if output.label.location in locationsystem:
                                relevant=True

            if hasattr(key[1], 'inputs'):
                for input in key[1].inputs:
                    if hasattr(input, 'label'):
                        if hasattr(input.label, 'location'):
                            if input.label.location in locationsystem:
                                relevant = True

            if hasattr(key[1], 'outputs'):
                for output in key[1].outputs:
                    if hasattr(output, 'label'):
                        if hasattr(output.label, 'location'):
                            if output.label.location in locationsystem:
                                relevant = True

            if relevant==True:
                cap_frame=results[key]['sequences']
                column = cap_frame.columns[0]
                label = label_function(results, key)
                cap_frame = cap_frame.rename(columns={column: label})
                capacity_dataframe = pd.concat([capacity_dataframe, cap_frame], axis=1)

    return capacity_dataframe


def get_potential(results, locationsystem):
    potential_data=pd.DataFrame()
    res_list=res_key(results)
    key_list=[]
    for key in res_list:
        if key[0]!=None and key[1]==None:
            if hasattr(key[0], 'label'):
                if hasattr(key[0].label, 'location'):
                    if key[0].label.location in locationsystem:
                        key_list.append(key)


    for key in key_list:
        put_data_ob = pd.DataFrame(results[key]['sequences'])
        column = put_data_ob.columns[0]
        label = key[0].label
        put_data_ob = put_data_ob.rename(columns={column: label})
        potential_data = pd.concat([potential_data, put_data_ob], axis=1)

    return potential_data

def get_allpotential(results):
    potential_data=pd.DataFrame()
    res_list=res_key(results)
    key_list=[]
    for key in res_list:
        if key[0]!=None and key[1]==None:
            if hasattr(key[0], 'label'):
                key_list.append(key)


    for key in key_list:
        put_data_ob = pd.DataFrame(results[key]['sequences'])
        column = put_data_ob.columns[0]
        label = key[0].label
        put_data_ob = put_data_ob.rename(columns={column: label})
        potential_data = pd.concat([potential_data, put_data_ob], axis=1)

    return potential_data
