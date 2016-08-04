renpassG!S is an easy-to-use application designed to model energy systems.

.. contents:: `Table of contents`
    :depth: 1
    :local:
    :backlinks: top
.. sectnum::

Introduction
============

renpassG!S is developed and maintained at the Center for Sustainable Energy Systems (Zentrum für nachhaltige Energysysteme (ZNES)) in Flensburg. The application is closely linked to the Open-Energy-Modeling-Framework. An energy system represented as a bipartite graph of 


Energy system scenarios are defined using two CSV files.  


variable cost fix cost
planning perspective
minimizing cost



Scenario Data
=============

Status Quo 2014
---------------

Regions
~~~~~~~

AT, BE, CH, CZ, DE, DK, FR, LU, NL, NO, PL, SE

Fuel prices & CO2 costs
~~~~~~~~~~~~~~~~~~~~~~~

European Countries 
~~~~~~~~~~~~~~~~~~

+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|Fuel        |Fuel price €2014/GJ          |Source         |Emission tCO2/GJ  |Source     |Fuel price including CO2 cost €2014/MWh|
+============+=============================+===============+==================+===========+=======================================+
|gas         |6.71                         |BMU-DLR2012_   |0.0559            |UBA2015_   | 24.486369                             |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|hard_coal   |3.61                         |"              |0.0934            |          "| 13.547994                             |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|oil         |12.24                        |"              |0.0733            |          "| 44.497203                             |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|waste       |1.86                         |"              |0.0917            |IPCC2006_  | 12.78                                 |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|biomass     |5.56                         |PROGNOS2013_   |0.0020            |DEFRA2012_ | 20.02782                              |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|lignite     |1.15                         |ISI2011_       |0.1051            |UBA2015_   | 4.761141                              |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|uranium     |1.11                         |"              |0.0088            |OEKO2007_  | 4.048008                              |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|mixed_fuels |1.86                         |nan            |0.0917            |nan        | 7.237947                              |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+

with CO2 price = 18.43 €2014/t (BMU-DLR2012_) (Anmerkung Cord: VIEL ZU HOCH! Für 2014 lag der Wert laut EEX-Daten im Durchschnitt bei 5.91 EUR/tCO2. Ich habe die Preise in der o. g. Tabelle dahingehend aktualisiert)
with 3.6 GJ ~ 1 MWh

Manipulations: 
* BMU-DLR2012_: Linear interpolated in the timeframe from 2010 to 2015, inflation - adjusted 
* mixed fuels same values as waste

Variable costs
~~~~~~~~~~~~~~

+-----------+----------+---------------+
|Type       | €/MWh    |Source         |
+===========+==========+===============+
|gas        | 2.0      |IER2010_       |
+-----------+----------+---------------+
|hard_coal  | 4.0      |"              |
+-----------+----------+---------------+
|oil        | 1.5      |DIW2013_       |
+-----------+----------+---------------+
|waste      | 23.0     |Energynet2012_ |
+-----------+----------+---------------+
|biomass    | 3.9      |"              |
+-----------+----------+---------------+
|lignite    | 4.4      |IER2010_       |
+-----------+----------+---------------+
|uranium    | 0.5      |"              |
+-----------+----------+---------------+
|mixed_fuels| 23.0     |nan            |
+-----------+----------+---------------+

Fixed costs
~~~~~~~~~~~

+-----------+----------+---------------+
|Type       | €/MW     | Source        |
+===========+==========+===============+
|gas        | 19,000   |IER2010_       |
+-----------+----------+---------------+
|hard_coal  | 35,000   |"              |
+-----------+----------+---------------+
|oil        |  6,000   |DIW2013_       |
+-----------+----------+---------------+
|waste      | 16,500   |Energynet2012_ |
+-----------+----------+---------------+
|biomass    | 29,000   |"              |
+-----------+----------+---------------+
|lignite    | 39,000   |IER2010_       |
+-----------+----------+---------------+
|uranium    | 55,000   |"              |
+-----------+----------+---------------+
|mixed_fuels| 16,500   |nan            |
+-----------+----------+---------------+

Efficiencies
~~~~~~~~~~~~

+-----------+-------+----------------+
|Type       |eta    |Source          |
+===========+=======+================+
|gas        | 47.1  |ECOFYS2014_     |
+-----------+-------+----------------+
|hard_coal  | 38.5  | "              |
+-----------+-------+----------------+
|oil        | 36.8  |"               |
+-----------+-------+----------------+
|waste      | 26.0  |own assumption  |
+-----------+-------+----------------+
|biomass    | 38.0  |own assumption  |
+-----------+-------+----------------+
|lignite    | 36.0  | own assumption |
+-----------+-------+----------------+
|uranium    | 36.0  |IER2010_        |
+-----------+-------+----------------+
|mixed_fuels| 26.0  |nan             |
+-----------+-------+----------------+

* Mixed fuels same values as waste

Installed capacities
~~~~~~~~~~~~~~~~~~~~

Source: "140602_SOAF 2014_dataset.zip ":http://vernetzen.uni-flensburg.de/redmine/attachments/download/850/140602_SOAF%202014_dataset.zip
Description: 19:00pm values, Scenario B (Best estimate) based on the expectations of the TSO, See "Source". Original Data has been provided by ENTSO-E.
Year: 2014
Manipulations: None

Detailed Scenario
~~~~~~~~~~~~~~~~~

OPSD BNetzA list of power plants...

Demand
~~~~~~

Source: http://data.open-power-system-data.org/datapackage_timeseries/
Description: See "Source". Original Data has been provided by ENTSO-E.
Year: 2014
Manipulations: Normalised by dividing the values of the respective country by their annual maximum.

Transshipment - Net Transfer Capacities (NTC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Source: "Electricity Without Borders - The need for cross-border transmission investment in Europe":http://ses.jrc.ec.europa.eu/sites/ses.jrc.ec.europa.eu/files/documents/thesis_brancucci_electricity_without_borders.pdf (p.149 ff)
Description: See "Source". Original Data has been provided by ENTSO-E (NTC Matrix)
Year: 2010
Manipulations: None

Wind Timeseries
~~~~~~~~~~~~~~~

Source: https://beta.renewables.ninja/downloads
Description: See "Source" and respective journal articles on the dataset. Original Data has been provided by MERRA.
Year: 2014
Manipulations: None

Solar Timeseries
~~~~~~~~~~~~~~~~

Source: https://beta.renewables.ninja/downloads
Description: See "Source" and respective journal articles on the dataset. Original Data has been provided by MERRA-2.
Year: 2014
Manipulations: None


Sources
~~~~~~~

* BMU-DLR2012_
* ISI2011_
* IPCC2006_
* DEFRA2012_
* OEKO2007_
* PROGNOS2013_
* ECOFYS2014_
* IER2010_
* DIW2013_
* Energynet2012_

.. _ISI2011: http://www.isi.fraunhofer.de/isi-wAssets/docs/x/de/publikationen/Final_Report_EU-Long-term-scenarios-2050_FINAL.pdf
.. _UBA2015: https://www.umweltbundesamt.de/themen/klima-energie/treibhausgas-emissionen
.. _IPCC2006: http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf
.. _DEFRA2012: https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/69554/pb13773-ghg-conversion-factors-2012.pdf
.. _OEKO2007: http://www.oeko.de/oekodoc/318/2007-008-de.pdf
.. _PROGNOS2013: http://www.prognos.com/uploads/tx_atwpubdb/131010_Prognos_Belectric_Studie_Freiflaechen_Solarkraftwerke_02.pdf
.. _ECOFYS2014: http://www.ecofys.com/files/files/ecofys-2014-international-comparison-fossil-power-efficiency.pdf
.. _IER2010: http://www.ier.uni-stuttgart.de/publikationen/arbeitsberichte/downloads/Arbeitsbericht_08.pdf
.. _DIW2013: https://www.diw.de/documents/publikationen/73/diw_01.c.424566.de/diw_datadoc_2013-068.pdf
.. _Energynet2012: https://www.energinet.dk/SiteCollectionDocuments/Danske%20dokumenter/Forskning/Technology_data_for_energy_plants.pdf
.. _BMU-DLR2012: http://www.dlr.de/dlr/Portaldata/1/Resources/bilder/portal/portal_2012_1/leitstudie2011_bf.pdf
