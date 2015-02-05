#!/usr/bin/python
# -*- coding: utf-8

import os
import plot_lists
import database as db


def tex_file(filename, input_data, p_set,
    dep_var_components, dep_var_dict,
    total_co2_emissions, sum_var_co2_emissions,
    total_costs, sum_var_costs,
    components_dict, full_load_hours_dict,
    pv_area, number_wka, cap_pv,
    cap_wind, cap_gas_power, cap_dh_gas_heat, cap_dh_excess_heat, max_el_import,
    annual_biomass_potential, hourly_biogas_potential,
    comment_1, comment_2, storage_losses, storage_energy, biomass_used):
    '''
    Creates a tex file with all important input and output data of the
    optimization.
    '''

    dep_var_components['DH Biomass Cog'] = 0
    # dictionary for legend
    legend_dict = plot_lists.legend_dictionary_output()
    if p_set['optimize_for'] == 'Costs':
        opt_var = 'Kosten'
    else:
        opt_var = 'CO2'
    opfile = filename + '.tex'
    #opfile = output_dir + '/' + filename + '.tex'
    outfile = open(opfile, 'w')

    # Usepackages
    p = []
    p.append('\\documentclass[ngerman]{scrartcl}\n')
    p.append('\\usepackage[T1]{fontenc}\n')
    p.append('\\usepackage[utf8]{inputenc}\n')
    p.append('\\usepackage[a4paper]{geometry}\n')
    p.append('''\\geometry{verbose,tmargin=2cm,bmargin=2cm,
            lmargin=2cm,rmargin=2cm}\n''')
    p.append('\\setlength{\\parskip}{\\smallskipamount}\n')
    p.append('\\setlength{\\parindent}{0pt}\n')
    p.append('\\usepackage{babel}\n')
    p.append('\\usepackage{array}\n')
    p.append('\\usepackage{float}\n')
    p.append('\\usepackage{color}\n')
    p.append('\\usepackage{textcomp}\n')
    p.append('\\usepackage{amsbsy}\n')
    p.append('\\usepackage{graphicx}\n')
    p.append('''\\usepackage[unicode=true,pdfusetitle,
     bookmarks=true,bookmarksnumbered=false,bookmarksopen=false,
     breaklinks=false,pdfborder={0 0 1},backref=false,colorlinks=false]
     {hyperref}\n''')
    p.append('\\makeatletter\n')
    p.append('\\providecommand{\\tabularnewline}{\\\\}\n')
    p.append('\\makeatother\n')

    # Titel
    p.append('\\begin{document}\n')
    p.append('\\title{Ausgabefile der Simulation}\n')
    p.append('\\date{Erstellt am: \\today}\n')
    p.append('\\maketitle\n')

    # Allgemeines
    p.append('''\\section*{Simulationsdaten (Eingaben /
        \\textcolor{red}{Ausgaben})}\n''')
    p.append('\\begin{table}[H]\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}l>{\\raggedright}p{0.2\\textwidth}>
        {\\raggedright}p{0.7\\textwidth}}\n''')
    p.append('''\\textbf{ID} & \\textbf{Name} &
        \\textbf{Ort}\\tabularnewline\n''')
    p.append('''%d & %s & %s\\tabularnewline\n'''
        % (input_data['ProjectID'], input_data['Name'], input_data['district']))
    p.append('\\noalign{\\vskip1em}\n')
    p.append('''\\multicolumn{3}{l}
        {\\textbf{Optimierung nach: } %s}
        \\tabularnewline\n'''
        % opt_var)
    p.append('''\\multicolumn{3}{l}
        {\\textbf{Gesamtemissionen: } \\textcolor{red}{%.0f t}}
        \\tabularnewline\n'''
        % (total_co2_emissions / 1000))
    p.append('''\\multicolumn{3}{l}
        {\\textbf{Direkte Emissionen: } \\textcolor{red}{%.0f t}}
        \\tabularnewline\n'''
        % (sum_var_co2_emissions / 1000))
    p.append('''\\multicolumn{3}{l}
        {\\textbf{Gesamtkosten: } \\textcolor{red}{%.0f T€}}
        \\tabularnewline\n'''
        % (total_costs / 1000))
    p.append('''\\multicolumn{3}{l}
        {\\textbf{Brennstoffkosten: } \\textcolor{red}{%.0f T€}}
        \\tabularnewline\n'''
        % (sum_var_costs / 1000))
    p.append('\\noalign{\\vskip1em}\n')
    p.append('\\multicolumn{3}{l}{\\textbf{Solver: }%s}\\tabularnewline\n'
        % input_data['Solver'].replace('_', '\\_'))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')

    # Kraftwerke
    p.append('\\begin{table}[H]\n')
    p.append('\\subsubsection*{Definition der Kraft- und Wärmeanlagen}\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}lccccc}\n''')
        # Tabellenkopf
        # Tabellenkopf Kosten
    if p_set['optimize_for'] == 'Costs':
        p.append('''\\textbf{Kraftwerk} &
            \\textbf{Kapazität} &
            \\textbf{$\\boldsymbol{\\eta}$} &
            \\textbf{VLS} &
            \\textbf{var. Kosten} &
            \\textbf{fixe Kosten}
            \\tabularnewline\n''')
        p.append('''\\ &
            \\ [MW] &
            \\ [-] &
            \\ [h] &
            \\ [Euro/MWh] &
            \\ [T€/a]
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
        # Tabellenkopf CO2
    else:
        p.append('''\\textbf{Kraftwerk} &
            \\textbf{Kapazität} &
            \\textbf{$\\boldsymbol{\\eta}$} &
            \\textbf{VLS} &
            \\textbf{var. $\\boldsymbol{CO}_{\\boldsymbol{2}}$ Em.} &
            \\textbf{fixe $\\boldsymbol{CO}_{\\boldsymbol{2}}$ Em.}
            \\tabularnewline\n''')
        p.append('''\\ &
            \\ [MW] &
            \\ [-] &
            \\ [h] &
            \\ [kg/MWh] &
            \\ [t/a]
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
        # Tabelleneinträge
            # Power Sources
    if 'PV' in components_dict['Power Sources']:
        p.append('''PV & %.1f & -- & \\textcolor{red}{(%r)} &
            -- & \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (cap_pv,
            int(full_load_hours_dict['PV']),
            dep_var_components['PV'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'Wind' in components_dict['Power Sources']:
        p.append('''Wind & %.1f & -- & \\textcolor{red}{(%r)} &
         -- & \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (cap_wind,
            int(full_load_hours_dict['Wind']),
            dep_var_components['Wind'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'Hydropower' in components_dict['Power Sources']:
        p.append('''Wasserkraft & %.3f & -- & \\textcolor{red}{(%.0f)} &
            -- & \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (p_set['cap_hydropower'],
            (p_set['hourly_hydropower_pot'] * 8760 / p_set['cap_hydropower']),
            dep_var_components['Hydropower'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'Gas Power' in components_dict['Power Sources']:
        p.append('''Erdgas-Kraftwerk & \\textcolor{red}{%.1f} & %.2f &
            \\textcolor{red}{%r} & \\textcolor{red}{%1.3e} &
            \\textcolor{red}{%.1f}\\tabularnewline\n'''
            % (cap_gas_power,
            input_data['eta Gas Power'],
            int(full_load_hours_dict['Gas Power']),
            dep_var_dict['Gas Power'],
            dep_var_components['Gas Power'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'Biomass Power' in components_dict['Power Sources']:
        p.append('''Biomasse-Kraftwerk & %.1f & %.2f & \\textcolor{red}{%r} &
            \\textcolor{red}{%1.3e} & \\textcolor{red}{%.1f}
            \\tabularnewline\n'''
            % (input_data['cap Biomass Power'],
            input_data['eta Biomass Power'],
            int(full_load_hours_dict['Biomass Power']),
            dep_var_dict['Biomass Power'],
            dep_var_components['Biomass Power'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'El Import' in components_dict['Power Sources']:
        p.append('''Stromimport & %.1f & -- & \\textcolor{red}{%r} &
            \\textcolor{red}{%1.3e} & --
            \\tabularnewline\n'''
            % (max_el_import,
            int(full_load_hours_dict['El Import']),
            dep_var_dict['El Import']))
        p.append('\\noalign{\\vskip0.4em}\n')
            # Heat Sources
    for i in components_dict['Heat Sources']:
        if i == 'DH Gas Heat':
            p.append('''%s & \\textcolor{red}{%.1f} & %.2f &
                \\textcolor{red}{%r} & \\textcolor{red}{%1.3e} &
                \\textcolor{red}{%.1f} \\tabularnewline\n'''
                % (legend_dict[i], cap_dh_gas_heat,
                input_data['eta ' + i],
                int(full_load_hours_dict[i]),
                dep_var_dict[i],
                dep_var_components[i] / 1000))
        elif i == 'DH Excess Heat':
            p.append('''%s & \\textcolor{red}{%.1f} & - & - &
                \\textcolor{red}{%1.3e} & - \\tabularnewline\n'''
                % (legend_dict[i],
                cap_dh_excess_heat,
                dep_var_dict[i]))
        else:
            p.append('''%s & %.1f & %.2f & \\textcolor{red}{%r} &
                \\textcolor{red}{%1.3e} & \\textcolor{red}{%.1f}
                \\tabularnewline\n'''
                % (legend_dict[i], input_data['cap ' + i],
                input_data['eta ' + i],
                int(full_load_hours_dict[i]),
                dep_var_dict[i],
                dep_var_components[i] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
            # Cogeneration
    for i in components_dict['Cog Sources']:
                # Power
        p.append('''%s & %.1f & %.2f & \\textcolor{red}{%r} &
            \\textcolor{red}{%1.3e} & \\textcolor{red}{%.1f}
            \\tabularnewline\n'''
            % (legend_dict[i + ' Power'], input_data['cap ' + i + ' Power'],
            input_data['eta ' + i + ' Power'],
            int(full_load_hours_dict[i + ' Power']),
            dep_var_dict[i + ' Power'],
            dep_var_components[i] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
                # Heat
        p.append('''%s & -- & \\textcolor{red}{%r} & -- &
            \\textcolor{red}{%1.3e} & --
            \\tabularnewline\n'''
            % (legend_dict[i + ' Heat'],
            input_data['eta ' + i + ' Heat'],
            dep_var_dict[i + ' Heat']))
        p.append('\\noalign{\\vskip0.4em}\n')
             # Heating Systems
    for i in components_dict['Heating Systems']:
        p.append('''%s & %.1f & %.2f & -- & \\textcolor{red}{%1.3e} &
            \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (legend_dict[i],
            p_set['max_heat_' + (i.replace(' Heat', '')).lower()],
            input_data['eta ' + i],
            dep_var_dict[i],
            dep_var_components[i] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
            # ST Heat
    if 'ST Heat' in components_dict['Solarthermal System']:
        p.append('''%s & -- & -- & -- & -- &
            \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (legend_dict['ST Heat'],
            dep_var_components['ST Heat'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')
    if 'ST Heat supp Gas' in components_dict['Solarthermal System']:
            # ST Heat supp Gas
        p.append('''%s & %.1f & %.2f & -- & \\textcolor{red}{%1.3e} &
            \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (legend_dict['ST Heat supp Gas'],
            p_set['max_heat_st'],
            input_data['eta ST Heat supp Gas'],
            dep_var_dict['ST Heat supp Gas'],
            dep_var_components['ST Heat supp Gas'] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')

              # el Heating in Heating Systems
    for i in components_dict['el Heating']:
        p.append('''%s & %.1f & 1 & -- & -- & \\textcolor{red}{%.1f}
            \\tabularnewline\n'''
            % (legend_dict[i], input_data['cap ' + i],
            dep_var_components[i] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')

            # Heat Pump Mono
    for i in components_dict['Heat Pump Mono']:
        p.append('''%s & %.1f & -- & \\textcolor{red}{%r} & -- &
            \\textcolor{red}{%.1f} \\tabularnewline\n'''
            % (legend_dict[i], input_data['cap ' + i],
            int(full_load_hours_dict[i]),
            dep_var_components[i] / 1000))
        p.append('\\noalign{\\vskip0.4em}\n')

            # dec. Cog units
    for i in components_dict['dec Cog units']:
        if i == 'Gas Cog unit Boiler' or i == 'Biogas Cog unit Boiler':
            p.append('''%s & %.1f & %.2f & \\textcolor{red}{%.0f} &
                 \\textcolor{red}{%1.3e} &
                \\textcolor{red}{%.1f} \\tabularnewline\n'''
                % (legend_dict[i], input_data['cap ' + i],
                input_data['eta ' + i],
                int(full_load_hours_dict[i]),
                dep_var_dict[i],
                dep_var_components[i] / 1000))
            p.append('\\noalign{\\vskip0.4em}\n')
        else:
                # Power
            p.append('''%s & %.1f & %.2f & \\textcolor{red}{%r} &
                \\textcolor{red}{%1.3e} & \\textcolor{red}{%.1f}
                \\tabularnewline\n'''
                % (legend_dict[i + ' Power'], input_data['cap ' + i + ' Power'],
                input_data['eta ' + i + ' Power'],
                int(full_load_hours_dict[i + ' Power']),
                dep_var_dict[i + ' Power'],
                dep_var_components[i] / 1000))
            p.append('\\noalign{\\vskip0.4em}\n')
                # Heat
            p.append('''%s & -- & %.2f & \\textcolor{red}{%r} &
                \\textcolor{red}{%1.3e} & \\textcolor{red}{%.1f}
                \\tabularnewline\n'''
                % (legend_dict[i + ' Heat'],
                input_data['eta ' + i + ' Heat'],
                int(full_load_hours_dict[i + ' Heat']),
                dep_var_dict[i + ' Heat'],
                dep_var_components[i] / 1000))
            p.append('\\noalign{\\vskip0.4em}\n')

         # Tabellenende
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')

    # Batteriespeicher und thermische Speicher (1)
    if len(components_dict['Storages']) > 0:
        p.append('\\begin{table}[H]\n')
        p.append('''\\subsubsection*{Definition des Batteriespeichers und der
            thermischen Speicher}\n''')
        p.append('''\\begin{tabular*}{0.95\\textwidth}{@{\\extracolsep
            {\\fill}}lccc}\n''')
            # Tabellenkopf
        p.append('''\\textbf{Speicher} &
            \\textbf{Kapazität} &
            \\textbf{Entladerate} &
            \\textbf{Speicher-}
            \\tabularnewline\n''')
        p.append('''\\textbf{} &
            \\textbf{} &
            \\textbf{} &
            \\textbf{verluste}
            \\tabularnewline\n''')
        p.append(''' &
            \\ [MWh] &
            \\ [MWh/h] &
            \\ [1/h]
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
            # Tabelleneinträge
        for i in components_dict['Storages']:
            if i == 'Storage Battery' or i == 'DH Storage Thermal':
                p.append('%s & %.1f & %.1f & %.3f \\tabularnewline\n'
                    % (legend_dict[i],
                    input_data['cap ' + i],
                    input_data['Discharge rate ' + i],
                    input_data['Loss ' + i]))
                p.append('\\noalign{\\vskip0.4em}\n')
            else:
                p.append('%s & %.1f & %.1f & %.3f \\tabularnewline\n'
                    % (legend_dict[i],
                    input_data['cap ' + i],
                    input_data['Discharge rate ' + i],
                    input_data['Loss Storage Thermal Building']))
                p.append('\\noalign{\\vskip0.4em}\n')
            # Tabellenende
        p.append('\\end{tabular*}\n')
        p.append('\\end{table}\n')

        # Batteriespeicher und thermische Speicher (2)
        p.append('\\begin{table}[H]\n')
        p.append('''\\begin{tabular*}{0.95\\textwidth}{@{\\extracolsep
            {\\fill}}lccc}\n''')
            # Tabellenkopf
        p.append('''\\textbf{Speicher} &
            \\textbf{$\\boldsymbol{CO}_{\\boldsymbol{2}}$-} &
            \\textbf{Gesamt-} &
            \\textbf{Aufgenommene}
            \\tabularnewline\n''')
        p.append('''\\textbf{} &
            \\textbf{Emissionen} &
            \\textbf{verluste} &
            \\textbf{Energie}
            \\tabularnewline\n''')
        p.append(''' &
            \\ [t/a] &
            \\ [MW] &
            \\ [MWh]
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
            # Tabelleneinträge
        for i in components_dict['Storages']:
            if i == 'Storage Battery' or i == 'DH Storage Thermal':
                p.append('''%s & \\textcolor{red}{%.0f} &
                    \\textcolor{red}{%.0f} &
                    \\textcolor{red}{%.0f} \\tabularnewline\n'''
                    % (legend_dict[i],
                    dep_var_components[i] / 1000,
                    storage_losses[i],
                    storage_energy[i]))
                p.append('\\noalign{\\vskip0.4em}\n')
            else:
                p.append('''%s & \\textcolor{red}{%.0f} &
                    \\textcolor{red}{%.0f} &
                    \\textcolor{red}{%.0f} \\tabularnewline\n'''
                    % (legend_dict[i],
                    dep_var_components[i] / 1000,
                    storage_losses[i],
                    storage_energy[i]))
                p.append('\\noalign{\\vskip0.4em}\n')
            # Tabellenende
        p.append('\\end{tabular*}\n')
        p.append('\\end{table}\n')

    # Biomassespeicher
    key_dict = {'Storage Biogas': 'central',
                'Storage Biogas dec': 'dec'}
    p.append('\\begin{table}[H]\n')
    p.append('''\\subsubsection*{Definition der Biomassespeicher}\n''')
    p.append('''\\begin{tabular*}{0.95\\textwidth}{@{\\extracolsep
        {\\fill}}lccc}\n''')
        # Tabellenkopf
    p.append('''\\textbf{Speicher} &
        \\textbf{Kapazität} &
        \\textbf{eingesetzte} &
        \\textbf{jährliches}
        \\tabularnewline\n''')
    p.append('''\\textbf{} &
        \\textbf{} &
        \\textbf{Biomasse} &
        \\textbf{Potenzial}
        \\tabularnewline\n''')
    p.append(''' &
        \\ [MWh] &
        \\ [MW] &
        \\ [MWh/a]
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
        # Tabelleneinträge
    for storage in biomass_used.keys():
        if storage == 'Storage Biogas' or storage == 'Storage Biogas dec':
            p.append('''%s & \\textcolor{red}{%.0f} & \\textcolor{red}{%.0f} &
                \\textcolor{red}{%.0f} \\tabularnewline\n'''
                % (legend_dict[storage],
                input_data['cap ' + storage],
                biomass_used[storage],
                hourly_biogas_potential[key_dict[storage]] * 8760))
            p.append('\\noalign{\\vskip0.4em}\n')
        else:
            p.append('''%s & \\textcolor{red}{%.0f} & \\textcolor{red}{%.0f} &
                \\textcolor{red}{%.0f} \\tabularnewline\n'''
                % (legend_dict[storage],
                annual_biomass_potential,
                biomass_used[storage],
                annual_biomass_potential))
            p.append('\\noalign{\\vskip0.4em}\n')
        # Tabellenende
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')

    # Winddaten
    p.append('\\subsubsection*{Windkraftanlagendaten}\n')
    p.append('Anzahl von Windkraftanlagen: %.0f \\tabularnewline \n'
        % number_wka)
    p.append('\\begin{table}[H]\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}ccccc}\n''')
    p.append('''\\textbf{Typ} &
        \\textbf{Rotordurchmesser} &
        \\textbf{Nabenhöhe} &
        \\textbf{Höhe Standort} &
        \\textbf{Rauhigkeitslänge}\\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('''%s & %d m & %d m & %d m & %r m \\tabularnewline \n'''
        % (input_data['type_wka'], input_data['h_hub'], input_data['d_rotor'],
        input_data['h_windmast'], input_data['z_0']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')
    # PV-Daten
    p.append('\\subsubsection*{PV-Daten}\n')
    p.append('Gesamte PV-Fläche: %r m² \\tabularnewline \n' % pv_area)
    p.append('\\begin{table}[H]\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}ccc}\n''')
    p.append('''\\textbf{Typ} &
        \\textbf{Performance Ratio} &
        \\textbf{Wirkungsgrad}
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('''%s & %r & %r \\tabularnewline\n'''
        % (input_data['PV cell type'],
        input_data['PR'],
        input_data['eta PV']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')

    # weitere PV-Daten
    p.append('\\begin{table}[H]\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}cccccc}\n''''')
    p.append('''\\textbf{Ausrichtung} &
        \\textbf{Aufstellwinkel} &
        \\textbf{Albedo} &
        \\textbf{Grenzwinkel} &
        \\textbf{Mobilisierung} &
        \\textbf{Eignungsfaktor}
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('%r° & %r° & %r & %r° & %r & %r \\tabularnewline\n'
        % (input_data['a_module'],
        input_data['h_module'],
        input_data['albedo'],
        input_data['h_limit [m]'],
        input_data['mob_fac'],
        input_data['E_F']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')
    # Wärmelastangaben
    p.append('\\begin{table}[H]\n')
    p.append('\\subsubsection*{Wärmelastparameter}\n')
    p.append('''\\begin{tabular*}{0.5\\textwidth}
        {@{\\extracolsep{\\fill}}cc}\n''')
    p.append('''\\textbf{Gebäudeklasse} &
        \\textbf{Windklasse}
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('''%r & %r \\tabularnewline\n'''
        % (input_data['building_class'],
            input_data['wind_class']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')
    # Fernwärmeangaben
    p.append('\\begin{table}[H]\n')
    p.append('\\subsubsection*{Fernwärmeparameter}\n')
    p.append('''\\begin{tabular*}{0.95\\textwidth}
        {@{\\extracolsep{\\fill}}cccccc}\n''')
    p.append('''\\textbf{$\\boldsymbol{T}_{\\boldsymbol{VL, max}}$} &
        \\textbf{$\\boldsymbol{T}_{\\boldsymbol{VL, min}}$} &
        \\textbf{$\\boldsymbol{T}_{\\boldsymbol{RL}}$} &
        \\textbf{$\\boldsymbol{T}_{\\boldsymbol{Speicher}}$} &
        \\textbf{$\\boldsymbol{AT}_{\\boldsymbol{Heizperiode}}$} &
        \\textbf{$\\boldsymbol{AT}_{\\boldsymbol{Design}}$}
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('''%r °C & %r °C & %r °C & %r °C & %r °C & %r °C
        \\tabularnewline\n'''
        % (input_data['DH T_sup_max'],
        input_data['DH T_sup_min'],
        input_data['DH T_return'],
        input_data['DH T_storage'],
        input_data['DH T_heat_period'],
        input_data['DH T_amb_design']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')
    # Wärmepumpenangaben
    if input_data['Heat source HP Mono Air'] == 'yes' or \
    input_data['Heat source HP Mono Brine'] == 'yes':
        # Wärmepumpenangaben (1)
        p.append('\\begin{table}[H]\n')
        p.append('\\subsubsection*{Wärmepumpenparameter}\n')
        p.append('''\\begin{tabular*}{0.95\\textwidth}
            {@{\\extracolsep{\\fill}}cccccc}\n''')
        p.append('''\\textbf{$\\boldsymbol{\\eta}_{\\boldsymbol{Luft-WP}}$} &
            \\textbf{$\\boldsymbol{\\eta}_{\\boldsymbol{Sole-WP}}$} &
            \\textbf{$\\boldsymbol{x}_{\\boldsymbol{Sole-WP}}$} &
            \\textbf{$\\boldsymbol{x}_{\\boldsymbol{Heizstab}}$} &
            \\textbf{$\\boldsymbol{AT}_{\\boldsymbol{Heizperiode}}$} &
            \\textbf{$\\boldsymbol{AT}_{\\boldsymbol{Design}}$}
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
        p.append('''%r & %r & %r & %r & %r °C & %r °C
            \\tabularnewline\n'''
            % (input_data['eta_g_air'],
            input_data['eta_g_brine'],
            input_data['share_brine_hp'],
            input_data['share el heating HP'],
            input_data['Heat Pump T_heat_period'],
            input_data['Heat Pump T_amb_design']))
        p.append('\\end{tabular*}\n')
        p.append('\\end{table}\n')
        # Wärmepumpenangaben (2)
        p.append('\\begin{table}[H]\n')
        p.append('''\\begin{tabular*}{0.95\\textwidth}
            {@{\\extracolsep{\\fill}}cccccc}\n''')
        p.append('''\\textbf{$\\boldsymbol{T}_{\\boldsymbol{FBH, max}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{FBH, min}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{Rad., max}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{Rad. min}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{WW, EFH}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{WW, MFH}}$}
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
        p.append('''%r °C & %r °C & %r °C & %r °C & %r °C & %r °C
            \\tabularnewline\n'''
            % (input_data['T FBH max'],
            input_data['T FBH min'],
            input_data['T radiator max'],
            input_data['T radiator min'],
            input_data['T WW EFH'],
            input_data['T WW MFH']))
        p.append('\\end{tabular*}\n')
        p.append('\\end{table}\n')
        # Wärmepumpenangaben (3)
        p.append('\\begin{table}[H]\n')
        p.append('''\\begin{tabular*}{0.95\\textwidth}
            {@{\\extracolsep{\\fill}}ccccccc}\n''')
        p.append('''\\textbf{$\\boldsymbol{x}_{\\boldsymbol{WW, Haus.}}$} &
            \\textbf{$\\boldsymbol{x}_{\\boldsymbol{WW, GHD}}$} &
            \\textbf{$\\boldsymbol{x}_{\\boldsymbol{WW, Ind.}}$} &
            \\textbf{$\\boldsymbol{t}_{\\boldsymbol{WSp, Heiz}}$} &
            \\textbf{$\\boldsymbol{t}_{\\boldsymbol{WSp, WW}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{WSp, max}}$} &
            \\textbf{$\\boldsymbol{T}_{\\boldsymbol{WSp, min}}$}
            \\tabularnewline\n''')
        p.append('\\hline \n')
        p.append('\\noalign{\\vskip0.4em}\n')
        p.append('''%.1f & %.1f & %.1f & %r h & %r h & %r °C & %r °C
            \\tabularnewline\n'''
            % (1 - input_data['share heating res'],
            1 - input_data['share heating com'],
            1 - input_data['share heating ind'],
            input_data['t_st_heating'],
            input_data['t_st_ww'],
            input_data['TS HP Heating hot'],
            input_data['TS HP Heating cold']))
        p.append('\\end{tabular*}\n')
        p.append('\\end{table}\n')
    # Sonstige Angaben
    p.append('\\begin{table}[H]\n')
    p.append('\\subsubsection*{Sonstige Parameter}\n')
    p.append('''\\begin{tabular*}{0.5\\textwidth}
        {@{\\extracolsep{\\fill}}ccc}\n''')
    p.append('''\\textbf{Jahr} &
        \\textbf{$\\boldsymbol{\\eta}_{\\boldsymbol{ref, th}}$} &
        \\textbf{$\\boldsymbol{\\eta}_{\\boldsymbol{ref, el}}$}
        \\tabularnewline\n''')
    p.append('\\hline \n')
    p.append('\\noalign{\\vskip0.4em}\n')
    p.append('''%r & %r & %r\\tabularnewline\n'''
        % (input_data['Year'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical']))
    p.append('\\end{tabular*}\n')
    p.append('\\end{table}\n')

    p.append('\\pagebreak{}\n')
    # Ergebnisse
    p.append('\\section*{Ergebnisgrafiken}\n')

    # Strom Pie
    p.append('\\begin{figure}[H]\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1\\textwidth]{%s}\n'
        % (p_set['output_dir'] + '/' + p_set['pie_p_name'] + '.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Anteile der Erzeugungsanlagen an der Stromerzeugung}\n')
    p.append('\\end{figure}\n')
    # Wärme Pie
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1\\textwidth]{%s}\n'
        % (p_set['output_dir'] + '/' + p_set['pie_h_name'] + '.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Anteile der Erzeugungsanlagen an der Wärmeerzeugung}\n')
    p.append('\\end{figure}\n')
    # Stack Winter
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.3\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/' + p_set['stackplot_name_winter'] + '.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Last- und Erzeugungszeitreihe Winterwoche}\n')
    p.append('\\end{figure}\n')
    # Stack Sommer
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.3\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/' + p_set['stackplot_name_summer'] + '.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Last- und Erzeugungszeitreihe Sommerwoche}\n')
    p.append('\\end{figure}\n')
    # Share Wind and PV of total power demand
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.0\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/' + 'share_FEE_power_demand.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Anteil der FEE am Stromverbrauch}\n')
    p.append('\\end{figure}\n')
    # Share Wind and PV of end energy demand
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.0\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/' + 'share_FEE_end_energy_demand.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Anteil der FEE am Endenergieverbrauch}\n')
    p.append('\\end{figure}\n')
    # Surplus FEE
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.0\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/' + 'surplus_fee.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Stündliche Überschussleistung der FEE}\n')
    p.append('\\end{figure}\n')
    # Jahresdauerlinie El Import
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/load_curve_El Import.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Jahresdauerlinie Stromimport}\n')
    p.append('\\end{figure}\n')
    # Jahresdauerlinie Gas Power
    if input_data['Power source Gas Power'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_Gas Power.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Gaskraftwerk}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie DH Gas Heat
    if input_data['Heat source DH Gas Heat'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_DH Gas Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Gas-Spitzenkessel}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie Biomasse KWK
    if input_data['Cog source DH Biomass Cog'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_DH Biomass Cog Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Biomasse-HKW}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie DH Biogas BHKW
    if input_data['Cog source DH Biogas Cog unit'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_DH Biogas Cog unit Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie zentrale Biogas-BHKW}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie DH Gas BHKW
    if input_data['Cog source DH Gas Cog unit'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_DH Gas Cog unit Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie zentrale Gas-BHKW}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie Biogas BHKW
    if input_data['Heat source Biogas Cog unit'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_Biogas Cog unit Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Biogas-BHKW}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie Gas BHKW
    if input_data['Heat source Gas Cog unit'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/load_curve_Gas Cog unit Heat.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Gas-BHKW}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie KWK
    p.append('\\begin{figure}\n')
    p.append('\\begin{centering}\n')
    p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
        % (p_set['output_dir'] + '/load_curve_Sum Cog.png'))
    p.append('\\par\\end{centering}\n')
    p.append('\\caption{Jahresdauerlinie KWK (gesamt)}\n')
    p.append('\\end{figure}\n')
    # Jahresdauerlinie Batteriespeicher
    if input_data['Storage Battery'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] +
            '/load_curve_Storage Battery Discharge.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Batteriespeicher (Entladung)}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie Gas-BHKW Wärmespeicher
    if input_data['Gas Cog unit Storage Thermal'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] +
            '/load_curve_Gas Cog unit Storage Thermal Discharge.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Wärmespeicher (Gas-BHKW)}\n')
        p.append('\\end{figure}\n')
    # Jahresdauerlinie Biogas-BHKW Wärmespeicher
    if input_data['Biogas Cog unit Storage Thermal'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] +
            '/load_curve_Biogas Cog unit Storage Thermal Discharge.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Jahresdauerlinie Wärmespeicher (Gas-BHKW)}\n')
        p.append('\\end{figure}\n')

    # Fernwärmespeicher Speicherstand
    if input_data['DH Storage Thermal'] == 'yes':
        p.append('\\begin{figure}\n')
        p.append('\\begin{centering}\n')
        p.append('\\includegraphics[width=1.1\\textwidth,angle=90]{%s}\n'
            % (p_set['output_dir'] + '/thermal_storage_soc.png'))
        p.append('\\par\\end{centering}\n')
        p.append('\\caption{Speicherstand des Fernwärmespeichers}\n')
        p.append('\\end{figure}\n')

    # Check
    p.append('\\pagebreak{}\n')
    p.append('\\section*{Check}\n')
    #p.append('\\tabularnewline\n')
    p.append('%s \\tabularnewline\n' % comment_1)
    p.append('%s \\tabularnewline\n' % comment_2)
    # Dokumentende
    p.append('\\end{document}\n')

    for i in p:
        outfile.writelines(i)
    outfile.close()
    os.system(('pdflatex --output-directory=%s ' % p_set['output_dir']) +
        opfile)

    return


def text_file(p_set, data, colnames, list_p, list_h, list_h_DH,
    el_demand, end_energy_demand, pv_pot, wind_pot, fee,
    output_dir, filename, sum_var_co2, total_emissions,
    sum_var_costs, total_costs,
    storage_losses, efficiency_heat_pump, max_el_demand_hp,
    components_dict, full_load_hours_dict):

        ######################### Power ############################

    sumdata = ((data.sum(axis=0)))

    component_power = []

    nc_p = []
    for j in list_p:
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                component_power.append(j[0])

    energy_comp = (sumdata[nc_p])

    # write produced energy of each component to .txt-file
    out = open(output_dir + '/' + filename + '.txt', 'w')
    for i in range(len(component_power)):
        out.write(str(component_power[i]) + ' [MWh/a]; ')
        out.write(str(energy_comp[i]))
        out.write('\n')

        ########################## Heat ############################

    component_heat = []

    nc_p = []
    for j in (list_h + list_h_DH):
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                component_heat.append(j[0])

    energy_comp = (sumdata[nc_p])

    # write produced energy of each component to .txt-file
    for i in range(len(component_heat)):
        out.write(str(component_heat[i]) + ' [MWh/a]; ')
        out.write(str(energy_comp[i]))
        out.write('\n')

        ######################## other values #########################

    # emissions
    out.write('Direkte Emissionen [t]; ' + str(int(sum_var_co2 / 1000)))
    out.write('\n')
    out.write('Gesamtemissionen [t]; ' + str(int(total_emissions / 1000)))
    out.write('\n')

    # electricity import
    el_import_tmp = ([i for i, x in enumerate(colnames) if x == 'El Import'])
    el_import = data[:, el_import_tmp[0]]
    out.write('Max. Backup-Leistung (Stromimport) [MW]; ' +
        str(max(el_import)))
    out.write('\n')

    # Gesamtstromverbrauch
    out.write('Gesamtstromverbrauch [MWh/a]; ' + str(el_demand))
    out.write('\n')

    # theoretical and actual share of wind and pv
    out.write('Theo. Anteil Wind (Gesamtstromverbrauch) [%]; ' +
        str(100 * sum(wind_pot) / el_demand))
    out.write('\n')
    out.write('Theo. Anteil PV  (Gesamtstromverbrauch) [%]; ' +
        str(100 * sum(pv_pot) / el_demand))
    out.write('\n')
    out.write('Realer Anteil FEE  (Gesamtstromverbrauch) [%]; ' +
        str(100 * fee / el_demand))
    out.write('\n')

    out.write('Theo. Anteil Wind (Endenergieverbrauch) [%]; ' +
        str(100 * sum(wind_pot) / end_energy_demand))
    out.write('\n')
    out.write('Theo. Anteil PV  (Endenergieverbrauch) [%]; ' +
        str(100 * sum(pv_pot) / end_energy_demand))
    out.write('\n')
    out.write('Realer Anteil FEE  (Endenergieverbrauch) [%]; ' +
        str(100 * fee / end_energy_demand))
    out.write('\n')

    # storage losses
    for i in storage_losses:
        out.write('Speicherverlust [MWh/a] ' + i + '; ')
        out.write(str(storage_losses[i]))
        out.write('\n')

    # battery discharge
    if 'Storage Battery Discharge' in colnames:
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Storage Battery Discharge'])
        battery_discharge = sum(data[:, tmp[0]])

        out.write('Battery Discharge [MWh]' + '; ')
        out.write(str(battery_discharge))
        out.write('\n')

    # air heat pump electricity use
    if 'HP Mono Air Heating' in colnames:
        hp_heating = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air Heating'])
        hp_heating_el_demand = sum(data[:, hp_heating] /
            efficiency_heat_pump['HP Mono Air Heating'])[0]
        hp_el_heating = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air Heating el Heating'])
        hp_el_heating_el_demand = sum(data[:, hp_el_heating])[0]
        out.write('Luft-WP (Heizung) Strombedarf [MWh/a]; ' +
            str(hp_heating_el_demand + hp_el_heating_el_demand))
        out.write('\n')
        JAZ_heating = ((sum(data[:, hp_heating]) + sum(data[:, hp_el_heating]))
         / (hp_heating_el_demand + hp_el_heating_el_demand))
        out.write('JAZ Luft-WP (Heizung); ' + str(JAZ_heating[0]))
        out.write('\n')
    if 'HP Mono Air WW' in colnames:
        hp_water = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air WW'])
        hp_water_el_demand = sum(data[:, hp_water] /
            efficiency_heat_pump['HP Mono Air WW'])[0]
        hp_el_water = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air WW el Heating'])
        hp_el_water_el_demand = sum(data[:, hp_el_water])[0]
        out.write('Luft-WP (WW) Strombedarf [MWh/a]; ' +
            str(hp_water_el_demand + hp_el_water_el_demand))
        out.write('\n')
        JAZ_water = ((sum(data[:, hp_water]) + sum(data[:, hp_el_water]))
        / (hp_water_el_demand + hp_el_water_el_demand))
        out.write('JAZ Luft-WP (WW); ' + str(JAZ_water[0]))
        out.write('\n')

    # brine heat pump electricity use
    if 'HP Mono Brine Heating' in colnames:
        hp_heating = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Brine Heating'])
        hp_heating_el_demand = sum(data[:, hp_heating] /
            efficiency_heat_pump['HP Mono Brine Heating'])[0]
        out.write('Sole-WP (Heizung) Strombedarf [MWh/a]; ' +
            str(hp_heating_el_demand))
        out.write('\n')
        JAZ_heating = sum(data[:, hp_heating]) / hp_heating_el_demand
        out.write('JAZ Sole-WP (Heizung); ' + str(JAZ_heating[0]))
        out.write('\n')
    if 'HP Mono Brine WW' in colnames:
        hp_water = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Brine WW'])
        hp_water_el_demand = sum(data[:, hp_water] /
            efficiency_heat_pump['HP Mono Brine WW'])[0]
        out.write('Sole-WP (WW) Strombedarf [MWh/a]; ' +
            str(hp_water_el_demand))
        out.write('\n')
        JAZ_water = sum(data[:, hp_water] / hp_water_el_demand)
        out.write('JAZ Sole-WP (WW); ' + str(JAZ_water[0]))
        out.write('\n')

    # Costs
    out.write('Variable Kosten [t Euro]; ' + str(int(sum_var_costs / 1000)))
    out.write('\n')
    out.write('Gesamtkosten [t Euro]; ' + str(int(total_costs / 1000)))
    out.write('\n')

    # Wind and PV potential and used energy
    out.write('PV Potential [MWh/a]; %.1f' % (sum(pv_pot)))
    out.write('\n')
    out.write('Wind Potential [MWh/a]; %.1f' % (sum(wind_pot)))
    out.write('\n')
    pv_used = sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['output_table'], 'PV'))
    out.write('PV genutzt [MWh/a]; %.1f' % pv_used)
    out.write('\n')
    wind_used = sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['output_table'], 'Wind'))
    out.write('Wind genutzt [MWh/a]; %.1f' % wind_used)
    out.write('\n')
    out.close

    # Max. elec. demand of heat pumps
    out.write('Max. Strombedarf WP [MW]; %.1f' % max_el_demand_hp)
    out.write('\n')

    # FLH Cog units
    if 'Gas Cog unit Boiler' in colnames:
        out.write('VLS Gas-Spitzenkessel [h/a]; %.0f' %
        full_load_hours_dict['Gas Cog unit Boiler'])
        out.write('\n')
    if 'Gas Cog unit Power' in colnames:
        out.write('VLS Gas-BHKWs Strom [h/a]; %.0f' %
        full_load_hours_dict['Gas Cog unit Power'])
        out.write('\n')
        out.write('VLS Gas-BHKWs Wärme [h/a]; %.0f' %
        full_load_hours_dict['Gas Cog unit Heat'])
        out.write('\n')
    if 'Biogas Cog unit Boiler' in colnames:
        out.write('VLS Biogas-Spitzenkessel [h/a]; %.0f' %
        full_load_hours_dict['Biogas Cog unit Boiler'])
        out.write('\n')
    if i == 'Biogas Cog unit Power' in colnames:
        out.write('VLS Biogas-BHKWs Strom [h/a]; %.0f' %
        full_load_hours_dict['Biogas Cog unit Power'])
        out.write('\n')
        out.write('VLS Biogas-BHKWs Wärme [h/a]; %.0f' %
        full_load_hours_dict['Biogas Cog unit Heat'])
        out.write('\n')

    return
