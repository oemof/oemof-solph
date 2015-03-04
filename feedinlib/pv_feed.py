from base_feed import Feed
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('/home/caro/rlihome/Git/pahesmf')
import src.output.write_file as out # temporarily imported for output
sys.path.append('/home/caro/rlihome/Git/PVLIB_Python')
import pvlib
from matplotlib import cm # temporarily imported for output
from mpl_toolkits.mplot3d.axes3d import Axes3D # temporarily imported for
#output


class PvFeed(Feed):

    def __init__(self, DIC, site, year, region):
        """
        private class for the implementation of a Phovoltaic Feed as timeseries
        :param DIC: database parameters
        :param site: site and plant parameters
        :param year: the year to get the data for
        :param region: the region to get the data for
        """
        super(PvFeed, self).__init__(DIC, site, year, region, ["WSS", "T"])

        self.DIC = DIC
        self.year = year
        self.region = region

    def _apply_model(self, DIC, site, year, region, data):
        """
        implementation of the model to generate the _timeseries data from the
        weatherdata
        :return:
        """
        self._timeseries = "pv timeseries"
        #TODO: setup the model, currently being done by caro

        # 1. Fetch module parameter from Sandia Database
        module_data = (pvlib.pvl_retrieveSAM('SandiaMod')[site['module_name']])

        # 2. Overwriting module area (better: switch on and off this option)
        module_data['Area'] = site['Area']

        # 3. Determine the postion of the sun
        (data['SunAz'], data['SunEl'], data['AppSunEl'], data['SolarTime'],
            data['SunZen']) = pvlib.pvl_ephemeris(Time=data.index,
            Location=site)

        # 4. Determine the global horizontal irradiation
        data['GHI'] = data['DirHI'] + data['DHI']

        # 5. Determine the extraterrestrial radiation
        data['HExtra'] = pvlib.pvl_extraradiation(doy=data.index.dayofyear)

        # 6. Determine the relative air mass
        data['AM'] = pvlib.pvl_relativeairmass(z=data['SunZen'])

        # 7. Determine the angle of incidence
        data['AOI'] = pvlib.pvl_getaoi(SunAz=data['SunAz'],
            SunZen=data['SunZen'], SurfTilt=site['tilt'],
            SurfAz=site['azimuth'])

##########################################################################
        #data['AOI'][data['AOI'] > 90] = 90


        # Direktnormalstrahlung? AOI = 0?
##########################################################################

        # 8. Determine direct normal irradiation
        data['DNI'] = (data['DirHI']) / np.cos(np.radians(data['SunZen']))
        #data['DNI'] = (data['GHI'] - data['DHI']) / np.sin(h)

        # what for??
        data['DNI'][data['SunZen'] > 88] = data['DirHI']

        print(sum(data['GHI']))
        print(sum(data['DHI']))
        print(sum(data['DirHI']))
        print(sum(data['DNI']))

        plt.plot(data['SunAz'], '.')
        plt.show()

        ## what is this??
        #plt.plot((90 - data['SunZen']) * 10)
        #plt.plot((data['SunZen']))
        #plt.plot((np.cos(data['SunZen'] / 180 * np.pi) * 100))
        #plt.show()

        # 9a. Determine the sky diffuse irradiation in plane
        # with model of Perez (switch would be good, see 9b)
        data['In_Plane_SkyDiffuseP'] = pvlib.pvl_perez(SurfTilt=site['tilt'],
                                                    SurfAz=site['azimuth'],
                                                    DHI=data['DHI'],
                                                    DNI=data['DNI'],
                                                    HExtra=data['HExtra'],
                                                    SunZen=data['SunZen'],
                                                    SunAz=data['SunAz'],
                                                    AM=data['AM'])

        # what for ??
        data['In_Plane_SkyDiffuseP'][pd.isnull(data['In_Plane_SkyDiffuseP'])] \
        = 0

        # 9b. Determine the sky diffuse irradiation in plane
        # with model of Perez (switch would be good)
        data['In_Plane_SkyDiffuse'] = pvlib.pvl_klucher1979(site['tilt'],
            site['azimuth'], data['DHI'], data['GHI'], data['SunZen'],
            data['SunAz'])

        #print(sum(data['In_Plane_SkyDiffuse']))
        #print(sum(data['In_Plane_SkyDiffuseP']))
        #print(sum(data['DHI']))

        # 10. Determine the diffuse irradiation from ground reflection in plane
        data['GR'] = pvlib.pvl_grounddiffuse(GHI=data['GHI'],
            Albedo=site['albedo'], SurfTilt=site['tilt'])

        # 11. Determine total in-plane irradiance
        data['E'], data['Eb'], data['EDiff'] = pvlib.pvl_globalinplane(
                                AOI=data['AOI'],
                                DNI=data['DNI'],
                                In_Plane_SkyDiffuse=data['In_Plane_SkyDiffuse'],
                                GR=data['GR'],
                                SurfTilt=site['tilt'],
                                SurfAz=site['azimuth'])

        # warum wird E negativ?
        #print(data['AOI'][data['AOI'] > 90])
        #print data['AOI'][data['E'] < 0]
        #plt.plot(data['E'])
        #plt.show()

        # 12. Determine module and cell temperature
        data['Tcell'], data['Tmodule'] = pvlib.pvl_sapmcelltemp(E=data['E'],
                                    Wspd=data['v_wind'],
                                    Tamb=data['temp'],
                                    modelt='Open_rack_cell_polymerback')

        # 13. Apply the Sandia PV Array Performance Model (SAPM) to get a
        # dataframe with all relevant electric output parameters
        DFOut = pvlib.pvl_sapm(Eb=data['Eb'],
                            Ediff=data['EDiff'],
                            Tcell=data['Tcell'],
                            AM=data['AM'],
                            AOI=data['AOI'],
                            Module=module_data)

##############################################################################
        # DIVERSE AUSWERTUNGEN

        #print sum(data['E'])
        #print sum(data['GHI'])
        #print sum(DFOut['Pmp'])

        #Data['Imp']=DFOut['Imp']*meta['parallelStrings']
        #Data['Voc']=DFOut['Voc']
        #Data['Vmp']=DFOut['Vmp']*meta['seriesModules']
        #Data['Pmp']=Data.Imp*Data.Vmp
        #Data['Ix']=DFOut['Ix']
        #Data['Ixx']=DFOut['Ixx']

        # Ist Outputleistung auf den Quadratmeter bezogen?
        return DFOut['Pmp']


        ## Einfallswinkel
        #out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        #'04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'aoi.csv',
        #data['AOI'])

        ## Direktstrahlung auf geneigte Ebene
        #out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        #'04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'eb.csv',
        #data['Eb'])


        ## Diffusstrahlung auf geneigte Ebene (gesamt)
        #out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        #'04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'ediff.csv',
        #data['EDiff'])

        ## Globalstrahlung auf geneigte Ebene
        #out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        #'04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'e.csv',
        #data['E'])

        ##out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        ##'04-Projektinhalte/PV_Modell_Vergleich/PVLIB_Python/results', 'pmp.csv',
        ##data['Pmp'])

        ##print(module_data['Area'])


        ##results = db.read_data_from_file('3d_3.csv',
            ##'/home/likewise-open/RL-INSTITUT/birgit.schachler')

        ##fig = plt.figure()

        ##tilt, azimuth = np.meshgrid(tilt, azimuth)
        ##print(results)

        ##fig = plt.figure()
        ##ax = Axes3D(fig)

        ##surf = ax.plot_surface(tilt, azimuth, results,
            ##rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
        ##fig.colorbar(surf)

        ##plt.show()
