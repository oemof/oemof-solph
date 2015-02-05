#!/usr/bin/python
# -*- coding: utf-8

import os
import numpy as np
from os.path import expanduser
import pylatex
import logging


def dict2table(main_dt, key):
    '''
    Creates a table from a numpy array using the tabular environment of
    pylatex.

    Parameters
    ----------
    main_dt : dictionary
        Main dictionary as described below.
    key: string
        Name of the key where the definition of the table can be found.

    See Also
    --------
    dict2table_asterisk

    Examples
    --------
    Definition of a table from the branch:
    main_dt['comp']['region']['transformer']['heat']

    .. code:: python

        import outputlib as out

        # Define the key of the table
        main_dt['latex']['table']['transheat'] = {}

        # Set the branch you want to print to a table
        main_dt['latex']['table']['transheat']['branch_ls'] = [
            'comp', 'region', 'transformer', 'heat']

        # Set 'inconsistent' to True if you want add missing keys
        main_dt['latex']['table']['transheat']['inconsistent'] = True

        # Pass your own tabular string to define the width of the columns
        # '{p{0.17\textwidth}|p{0.11\textwidth}p{0.11\textwidth}p{0.11...}}'
        main_dt['latex']['table']['transheat']['tabular_str'] = (
            'p{0.17\\textwidth}|' + 6 * 'p{0.11\\textwidth}')

        out.dict2table(main_dt, 'transheat')
    '''
    # Gets the part of the main_dt that should be printed to the latex table.
    data_branch2table_branch(main_dt, key)

    # Fetches the number of columns
    col_num = np.shape(main_dt['latex']['table'][key]['array'])[1]
    # Sets the typical table structure if nothing else is set before.
    main_dt['latex']['table'][key].setdefault(
        'tabular_str', 'r|' + col_num * 'c')

    # Creating the table from the array. See the pylatex doc for more details.
    table = pylatex.Table(main_dt['latex']['table'][key]['tabular_str'])
    table.add_hline()
    for i in range(np.shape(main_dt['latex']['table'][key]['array'])[0]):
        t_row = []
        for j in range(col_num):
            t_row.append(
                main_dt['latex']['table'][key]['array'][i, j])
        table.add_row(eval(str(t_row)))
        if i == 0:
            table.add_hline()
    table.add_hline()
    main_dt['latex']['table'][key]['tex'] = table
    return table


def dict2table_asterisk(main_dt, key):
    '''
    Creates a table from a numpy array using the tabular* environment of
    latex.

    Use main_dt['latex']['table'][key]['width'] to set the width of the table.
    The value 1 means 100% of the text width, 0.5 means 50%.

    See: :py:func:`dict2table <outputlib.pdf_report_file.dict2table>`
    for more details.
    '''
     # Gets the part of the main_dt that should be printed to the latex table.
    data_branch2table_branch(main_dt, key)

    # Fetches the number of columns
    col_num = np.shape(main_dt['latex']['table'][key]['array'])[1]

    # Creating the table from the array using tabular* without pylatex.
    t = ''
    t += '\\begin{{tabular*}}{{{0}\\textwidth}}{{{1}}}'.format(
        main_dt['latex']['table'][key]['width'], 'r|' + col_num * 'c')
    t += '\\hline \n'
    for i in range(np.shape(main_dt['latex']['table'][key]['array'])[0]):
        t_row = ''
        for j in range(col_num):
            t_row += main_dt['latex']['table'][key]['array'][i, j] + '&'
        t += t_row[:-1] + ' \\\\ \n'
        if i == 0:
            t += '\\hline \n'
    t += '\\hline \n'
    t += '\\end{tabular*}'
    main_dt['latex']['table'][key]['tex'] = t
    return t


def data_branch2table_branch(main_dt, key):
    '''
    Creates a latex table from datatree branch
    using the ['latex']['table'] branch of the main_dt.
    '''
    main_dt['latex']['table'][key].setdefault(
        'firstvalue2row', main_dt['latex']['layout']['firstvalue2row'])
    main_dt['latex']['table'][key].setdefault(
        'inconsistent', main_dt['latex']['layout']['inconsistent'])
    main_dt['latex']['table'][key].setdefault(
        'width', main_dt['latex']['layout']['width'])

    dt_str = 'main_dt'
    for i in range(len(main_dt['latex']['table'][key]['branch_ls'])):
        dt_str += "['{0}']".format(
            main_dt['latex']['table'][key]['branch_ls'][i])
    tmp_branch = eval(dt_str)

    if main_dt['latex']['table'][key]['inconsistent']:
        add_missing_keys(tmp_branch)
    key1_ls = list(tmp_branch.keys())
    key2_ls = list(tmp_branch[key1_ls[0]].keys())

    if main_dt['latex']['table'][key]['firstvalue2row']:
        rows = key1_ls
        columns = key2_ls
        main_dt['latex']['table'][key]['array'] = values2array(
            tmp_branch, key1_ls, key2_ls, key)
    else:
        rows = key2_ls
        columns = key1_ls
        main_dt['latex']['table'][key]['array'] = values2array(
            tmp_branch, key1_ls, key2_ls, key).transpose()
    addname2data(main_dt, key, rows, columns)


def addname2data(main_dt, key, rows, columns):
    '''
    Adds the keys to the numpy table.
    '''
    main_dt['latex']['table'][key]['array'][0, 0] = ''
    i = 1
    for col in columns:
        main_dt['latex']['table'][key]['array'][0, i] = col.replace('_', ' ')
        i += 1
    i = 1
    for row in rows:
        main_dt['latex']['table'][key]['array'][i, 0] = row.replace('_', ' ')
        i += 1


def values2array(tmp_dt, key1_ls, key2_ls, key):
    '''
    Adds the values to the numpy table.
    '''
    new_ary = np.ones_like((np.zeros((len(key1_ls) + 1, len(key2_ls) + 1))),
                           dtype='S20')
    i = 1
    for key1 in key1_ls:
        j = 1
        for key2 in key2_ls:
            value = tmp_dt[key1][key2]
            if value is None:
                value = '-'
            if isinstance(value, list):
                value = str(value).replace('[]', '-')
            if isinstance(value, np.ndarray):
                value = sum(value)
            if not isinstance(value, str):
                if value > 1:
                    value = round(float(value), 2)
                if value > 10:
                    value = int(round(float(value)))
                if value > 1000000:
                    value = format(value, '.2e')
                new_ary[i, j] = value
            else:
                new_ary[i, j] = value
            j += 1
        i += 1
    return new_ary


def add_rli_header(d):
    '''
    This function adds the layout of a typical rli report to the document
    '''
    logopath = os.path.join(expanduser("~"), 'oemof', 'RLI_Logo.png')
    d.packages.append(pylatex.Package('fontenc', options='T1'))
    d.packages.append(pylatex.Package('inputenc', options='utf8'))
    d.packages.append(pylatex.Package('geometry', options='a4paper'))
    d.preamble.append('\\geometry{verbose,tmargin=2cm,bmargin=3.5cm,')
    d.preamble.append('lmargin=2cm,rmargin=2cm}')
    d.preamble.append('\\setlength{\\parskip}{\\smallskipamount}')
    d.preamble.append('\\setlength{\\parindent}{0pt}')
    d.packages.append(pylatex.Package('array', options=''))
    d.packages.append(pylatex.Package('float', options=''))
    d.packages.append(pylatex.Package('fancyhdr', options=''))
    d.preamble.append('\\pagestyle{fancy}')
    d.packages.append(pylatex.Package('textcomp', options=''))
    d.packages.append(pylatex.Package('amsbsy', options=''))
    d.packages.append(pylatex.Package('color', options=''))
    d.preamble.append(
        '\\definecolor{lgrau}{rgb}{0.655, 0.659, 0.667} % Lemoine-Grau')
    d.preamble.append(
        '\\definecolor{lblau}{rgb}{0, 0.173, 0.322} % Lemoine-Blau')
    d.packages.append(pylatex.Package('totpages'))
    d.preamble.append('\\fancypagestyle{plain}{%')
    d.preamble.append('\\fancyhf{}%')
    d.preamble.append('\\fancyhead[RO, LE]{\\resizebox{1.2in}{!}{')
    d.preamble.append('\\includegraphics{' + logopath + '}}}')
    d.preamble.append('\\fancyhead[LO, RE]{\\textcolor{lgrau}{\\textsf{')
    d.preamble.append('\\textbf{')
    d.preamble.append('\\small Scenario Report - oemof\\\~\\\~\\\~\\\}}}}')
    d.preamble.append('\\fancyfoot[LO, RE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize © RLI gGmbH}}')
    d.preamble.append('\\fancyfoot[CO, CE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize \\today}}')
    d.preamble.append('\\fancyfoot[RO, LE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize Seite \\thepage /\pageref{TotPages}}}\n')
    d.preamble.append('}')
    d.preamble.append('%%Alle anderen Seiten werden hier definiert')
    d.preamble.append('\\fancyhf{}')
    d.preamble.append('\\fancyhead[RO, LE]{\\resizebox{1.2in}{!}{')
    d.preamble.append('\\includegraphics{' + logopath + '}}}')
    d.preamble.append('\\fancyhead[LO, RE]{\\textcolor{lgrau}{\\textsf{')
    d.preamble.append('\\textbf{')
    d.preamble.append('\\small Scenario Report - oemof\\\~\\\~\\\~\\\}}}}')
    d.preamble.append('\\fancyfoot[LO, RE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize © RLI gGmbH}}')
    d.preamble.append('\\fancyfoot[CO, CE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize \\today}}')
    d.preamble.append('\\fancyfoot[RO, LE]{\\textcolor{lgrau}{')
    d.preamble.append('\\footnotesize Seite \\thepage /\pageref{TotPages}}}')
    d.preamble.append('%\\fancyheadoffset [RO,LE]{0pt}')
    d.preamble.append('%\\fancyfootoffset [RO,LE]{0pt}')
    d.preamble.append('%\\fancyhfoffset[RO,LE]{0pt}')
    d.preamble.append('%%Vergrößerung der Kopfzeile gemäß der Größe des Logos')
    d.preamble.append('\\addtolength{\\headheight}{2\\baselineskip}')
    d.preamble.append('\\addtolength{\\headheight}{0.61pt}')
    d.packages.append(pylatex.Package(
        'hyperref', options=[
            'unicode=true', 'pdfusetitle', 'bookmarks=true',
            'bookmarksnumbered=false', 'bookmarksopen=false',
            'breaklinks=false', 'pdfborder={0 0 0}', 'backref=false',
            'colorlinks=false']))
    return d


def set_default_values(main_dt):
    '''
    Use this function to make sure that parameters are set to their default
    values .
    '''
    main_dt['latex'].setdefault('layout', {})
    main_dt['latex']['layout'].setdefault('rli', 'False')
    main_dt['latex']['layout'].setdefault('info', 'True')
    main_dt['latex']['layout'].setdefault('clean', 'False')
    main_dt['latex']['layout'].setdefault('all_tables', 'True')
    main_dt['latex']['layout'].setdefault('firstvalue2row', False)
    main_dt['latex']['layout'].setdefault('inconsistent', False)
    main_dt['latex']['layout'].setdefault('width', 1)
    main_dt['latex']['layout'].setdefault('asterisk', True)


def add_info_table(main_dt):
    '''
    Adds some information of the info table of the results data tree to a
    section named 'info of the given document.
    '''
    section = pylatex.Section('General information')
    section.append('\\begin{tabular}{>{\\raggedright}p{')
    section.append('0.5\\textwidth}>{\\raggedright}p{0.5\\textwidth}}')
    section.append('\\begin{description}')
    section.append('\\item [{{Used~git~branch:}}] {0}'.format(
        main_dt['res']['info']['name_branch'].replace('_', ' ')))
    section.append('\\item [{{Objective~value:}}] {0:.3e}'.format(
        main_dt['res']['info']['objective_value']))
    section.append('\\item [{{Solver:}}] {0}'.format(
        main_dt['res']['info']['solver'].replace('_', '\\_')))
    section.append('\\item [{{Solver~status:}}] {0}'.format(
        main_dt['res']['info']['solver_status']))
    section.append('\\item [{{Simulation~periode:}}] {0} to {1} hoy '.format(
        main_dt['res']['info']['timestart'],
        main_dt['res']['info']['timeend']))
    section.append('\\item [{{Investment:}}] {0}'.format(
        main_dt['res']['info']['investment']))
    section.append('\\end{description}')
    section.append(' & \\begin{description}')
    section.append('\\item [{{Used~git~commit:}}] {0}'.format(
        main_dt['res']['info']['last_commit']))
    section.append('\\item [{{Operating~system:}}] {0}'.format(
        main_dt['res']['info']['os_system']))
    section.append('\\item [{{Optimisation~target:}}] {0}'.format(
        main_dt['res']['info']['opt_target'].replace('_', ' ')))
    section.append('\\item [{{Solver~time:}}] {0}'.format(
        main_dt['res']['info']['solver_time_minutes']))
    section.append('\\item [{{Simulated~year:}}] {0}'.format(
        main_dt['res']['info']['sim_year']))
    section.append('\\item [{{Renewable~share:}}] {0}'.format(
        main_dt['res']['info']['re_share']))
    section.append('\end{description}')
    section.append('\\end{tabular}')

    return section


def add_missing_keys(tmp_dt):
    'Adds missing keys if the data tree has a inconsistent structure'
    item_ls = []
    for key in list(tmp_dt.keys()):
        for item in list(tmp_dt[key].keys()):
            if not item in item_ls:
                item_ls.append(item)
    for key in list(tmp_dt.keys()):
        for item in item_ls:
            if item not in tmp_dt[key]:
                tmp_dt[key][item] = '-'


def scenario_report(main_dt):
    r"""Prints a basic pdf document with some scenario results.

    The function uses pylatex. [1]_

    Parameters
    ----------
    main_dt : dictionary
        Main dictionary as described below.

    Other Parameters
    ----------------
    main_dt['latex'] : dictionary
        Dictionary with some layout and table definitions.
        All the other values will get the default value.
    main_dt[latex]['table'][table_key]['branch_ls'] : list
        For all tables with the identifier table_key one has to define a list
        to describe the way to the data:
        ['a', 'b', 'c'] means main_dt['a']['b']['c']
    main_dt[latex]['table'][table_key]['firstvalue2row'] : boolean
        If this value is True the first keys will be the row indicators,
        otherwise the first keys will be the column indicators.


    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    out.restructure_results_generation_demand

    Notes
    -----
    Please note ....

    References
    ----------
    .. [1] `JelteF's PyLaTeX <https://github.com/JelteF/PyLaTeX>`_

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    .. code:: python

        SCENARIO = 'lk_wittenberg_reegis'

        import dblib as db
        import outputlib as out

        MAIN_DT = db.get_basic_dc()
        MAIN_DT['basic']['res_schema'] = 'oemof_res'

        # Reading results
        out.read_results(SCENARIO, MAIN_DT)

        # Restructure Results
        MAIN_DT['res'] = out.restructure_results_generation_demand(MAIN_DT)

        MAIN_DT['latex'] = {}
        MAIN_DT['latex']['table'] = {}

        # Electrical demand
        MAIN_DT['latex']['table']['edemand'] = {}
        MAIN_DT['latex']['table']['edemand']['branch_ls'] =
        ['res', 'elec', 'demand']

        # Electrical generation
        MAIN_DT['latex']['table']['egen'] = {}
        MAIN_DT['latex']['table']['egen']['branch_ls'] =
        ['res', 'elec', 'generation']
        MAIN_DT['latex']['table']['egen']['firstvalue2row'] = True

        MAIN_DT['latex']['layout'] = {}

        # Add all tables to document
        MAIN_DT['latex']['layout']['all_tables'] = 'True'

        # Don't remove the .tex, .aux... files after the pdf file is created.
        MAIN_DT['latex']['layout']['clean'] = False

        out.scenario_report(MAIN_DT)
    """
    # Creates a basic latex document.
    doc = basic_report(main_dt)

    # Adds some basic information of the info table to the document
    # if info= True
    if main_dt['latex']['layout']['info']:
        doc.append(add_info_table(main_dt))

    # Writes all defined tables to a section named "Tables" if all_tables=True
    if main_dt['latex']['layout']['all_tables']:
        doc.append(all_tables2doc(main_dt, doc))
    generate_pdf_from_doc(main_dt, doc)


def basic_report(main_dt):
    '''
    Creates a basic latex document to make your own pdf report.
    See: :py:func:`scenario_report <outputlib.pdf_report_file.scenario_report>`
    for an example.
    '''

    # Loads default values
    set_default_values(main_dt)
    filename = ('Report_' + main_dt['res']['info']['name_set'])

    # Defines the basic header and title informations
    doc = pylatex.Document(
        filename=filename,
        documentclass='scrartcl',
        author=main_dt['res']['info']['user_name'].capitalize(),
        title=main_dt['res']['info']['name_set'].replace('_', ' '),
        date=main_dt['res']['info']['sim_end_time'].date().strftime(
            "%d. %B %Y"),
        )

    # Adds the basic packages
    doc.packages.append(pylatex.Package('graphicx'))
    doc.packages.append(pylatex.Package('babel', options=['ngerman']))

    # Adds more packages and layout descriptions for the rli layout if rli=True
    if main_dt['latex']['layout']['rli']:
        doc = add_rli_header(doc)

    # Creates the title section
    doc.append('\n\\maketitle')

    # Adds the basic description of the scenario
    doc.append('\\textsf{{\\textbf{{{0}}}}}'.format(
        main_dt['res']['info']['description']))
    return doc


def generate_pdf_from_doc(main_dt, doc):
    '''
    Creates the pdf document. If clean is True, all files except the pdf file
    will be removed after a successfull run.
    '''
    doc.generate_pdf(clean=main_dt['latex']['layout']['clean'])


def multi_dict2textable(main_dt):
    '''
    One can define output tables in the latex branch of the main_dt refering
    to the example of
    :py:func:`dict2table <outputlib.pdf_report_file.dict2table>`.
    This function will add the tex code for all defined tables to the main_dt.
    '''
    logging.debug('Writing all tables in latex format.')

    for key in list(main_dt['latex']['table'].keys()):
        # Sets the global value to the table value if not set before.
        main_dt['latex']['table'][key].setdefault(
            'asterisk', main_dt['latex']['layout']['asterisk'])

        # If a tabular string is set, it's not possible to use asterisk table.
        if 'tabular_str' in main_dt['latex']['table'][key]:
            main_dt['latex']['table'][key]['asterisk'] = False

        if main_dt['latex']['table'][key]['asterisk']:
            dict2table_asterisk(main_dt, key)
        else:
            dict2table(main_dt, key)


def float_table2section(main_dt, section, table_key):
    '''
    Adds a float environment to a tex table. The tex table can be created
    with the function
    :py:func:`dict2table <outputlib.pdf_report_file.dict2table>`.
    '''
    if 'caption' in main_dt['latex']['table'][table_key]:
        caption = main_dt['latex']['table'][table_key]['caption']
    else:
        caption = 'A table of {0}.'.format(table_key)
    section.append('\\begin{table}[h!]')
    section.append('\\begin{center}')
    section.append(main_dt['latex']['table'][table_key]['tex'])
    section.append('\\end{center}')
    section.append('\\caption{')
    section.append(caption)
    section.append('}')
    section.append('\\end{table}')
    return section


def dict_as_floattable2section(main_dt, key, section):
    '''
    Refering to the documentation of
    :py:func:`scenario_report <outputlib.pdf_report_file.scenario_report>`
    one can create their own document structure and add each table to the
    wanted section.

    Examples
    --------
    Bla, bala

    .. code:: python

        # Creates a basic latex document.
        doc = basic_report(main_dt)

        # First table in the first section
        section = pylatex.Section('First Table')
        doc.append(dict_as_floattable2section(main_dt, key_of_table1, section))

        # Second table in the second section
        section = pylatex.Section('Second Table')
        doc.append(dict_as_floattable2section(main_dt, key_of_table2, section))

        # Create pdf document.
        generate_pdf_from_doc(main_dt, doc)
    '''
    dict2table(main_dt, key)
    section = float_table2section(main_dt, section, key)
    return section


def all_tables2doc(main_dt, doc):
    '''
    Adds all tables defined in 'MAIN_DT['latex']['table']' to a section named
    'Table' of the given document.
    '''
    multi_dict2textable(main_dt)
    section = pylatex.Section('Tables')
    for table_key in list(main_dt['latex']['table'].keys()):
        section = float_table2section(main_dt, section, table_key)
    return section
