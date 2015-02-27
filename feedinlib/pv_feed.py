from base_feed import Feed
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('/home/caro/rlihome/Git/pahesmf')
import src.output.write_file as out # vorrübergehend importiert für Output,
#sollte ausgelagert werden
sys.path.append('/home/caro/rlihome/Git/PVLIB_Python')
import pvlib
from matplotlib import cm # vorrübergehend importiert für Output
from mpl_toolkits.mplot3d.axes3d import Axes3D # vorrübergehend importiert für
#Output


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

        # 3. Fetch module parameter from Sandia Database
        module_data = (pvlib.pvl_retrieveSAM('SandiaMod')[site['module_name']])
        module_data['Area'] = 1.7

        # Determines the postion of the sun
        (data['SunAz'], data['SunEl'], data['AppSunEl'], data['SolarTime'],
            data['SunZen']) = pvlib.pvl_ephemeris(Time=data.index, Location=site)


        #date = data.index
        #h, az = pv.position_sun(site['latitude'], site['longitude'], year,
                #date.month, date.day, date.hour)
        #h[h < 0] = 0

        beam_hrz = data['GHI'] - data['DHI']

        data['HExtra'] = pvlib.pvl_extraradiation(doy=data.index.dayofyear)
        data['AM'] = pvlib.pvl_relativeairmass(z=data['SunZen'])

        #azimuth = np.array([
                #-180., -170., -160., -150., -140., -130., -120., -110., -100.,
                #-90., -80., -70., -60., -50., -40., -30., -20., -10., 0.,
                #10., 20., 30., 40., 50., 60., 70., 80., 90.,
                #100., 110., 120., 130., 140., 150., 160., 170., 180.])

        ##azimuth = np.arange(0, 370, 10)
        ##print(azimuth)

        #tilt = np.array([0., 10., 20., 30., 40., 50., 60., 70., 80., 90.])

        #results = np.zeros(((len(azimuth), len(tilt))))

        #for i in range(len(azimuth)):
            #site['azimuth'] = azimuth[i]
            #for j in range(len(tilt)):
                #site['tilt'] = tilt[j]

        data['AOI'] = pvlib.pvl_getaoi(SunAz=data['SunAz'], SunZen=data['SunZen'],
            SurfTilt=site['tilt'], SurfAz=site['azimuth'])

        #theta = np.degrees(np.arccos(np.cos(np.radians(data['SunEl'])) * -1
            #* np.sin(np.radians(site['tilt']))
            #* np.cos(np.radians(data['SunAz']) - np.radians(180))
            #+ np.sin(np.radians(data['SunEl'])) * np.cos(np.radians(site['tilt']))))

        #plt.figure(1)
        #plt.plot(data['AOI'], 'b.')

        #plt.figure(2)
        #plt.plot(theta, 'r.')

        plt.figure(3)
        plt.plot(data['SunAz'], '.')

        plt.show()

        #data['AOI'][data['AOI'] > 90] = 90

        # ??
        # Direktnormalstrahlung? AOI = 0?
        data['DNI'] = (beam_hrz) / np.cos(np.radians(data['SunZen']))
        #data['DNI'] = (data['GHI'] - data['DHI']) / np.sin(h)

        data['DNI'][data['SunZen'] > 88] = beam_hrz

        print(sum(data['GHI']))
        print(sum(data['DHI']))
        print(sum(beam_hrz))
        print(sum(data['DNI']))


        #plt.plot(data['DNI'])
        #plt.plot(beam_hrz)
        ##plt.plot(np.degrees(h)[2160:2180] * 10)
        #plt.plot((90 - data['SunZen']) * 10)
        ##plt.plot((data['GHI']))
        ##plt.plot((data['GHI'] - data['DHI']))
        ###plt.plot((data['GHI']))
        ###plt.plot((data['DHI']))
        ###plt.plot((data['SunZen']))
        ###plt.plot((np.cos(data['SunZen'] / 180 * np.pi) * 100))

        #plt.show()

        # Klucher oder Perez, Schalter notwendig
        data['In_Plane_SkyDiffuseP'] = pvlib.pvl_perez(SurfTilt=site['tilt'],
                                                    SurfAz=site['azimuth'],
                                                    DHI=data['DHI'],
                                                    DNI=data['DNI'],
                                                    HExtra=data['HExtra'],
                                                    SunZen=data['SunZen'],
                                                    SunAz=data['SunAz'],
                                                    AM=data['AM'])

        # ??
        data['In_Plane_SkyDiffuseP'][pd.isnull(data['In_Plane_SkyDiffuseP'])] = 0

        data['In_Plane_SkyDiffuse'] = pvlib.pvl_klucher1979(site['tilt'],
            site['azimuth'], data['DHI'], data['GHI'], data['SunZen'], data['SunAz'])

        #plt.plot(data['In_Plane_SkyDiffuse'])
        #plt.plot(data['In_Plane_SkyDiffuseP'])
        #plt.plot(data['DHI'])
        #plt.show()

        data['GR'] = pvlib.pvl_grounddiffuse(GHI=data['GHI'], Albedo=site['albedo'],
            SurfTilt=site['tilt'])

        #print data['DNI'][data['DNI'] < 0]
        #print 'GR'
        #print data['GR'][data['GR'] < 0]
        #print 'dif'
        #print data['In_Plane_SkyDiffuse'][data['In_Plane_SkyDiffuse'] < 0]
        #print 'res'

        data['E'], data['Eb'], data['EDiff'] = pvlib.pvl_globalinplane(AOI=data['AOI'],
                                        DNI=data['DNI'],
                                        In_Plane_SkyDiffuse=data['In_Plane_SkyDiffuse'],
                                        GR=data['GR'],
                                        SurfTilt=site['tilt'],
                                        SurfAz=site['azimuth'])

        #results[i, j] = sum(data['E'])

        #print data['AOI'][data['E'] < 0]

        #plt.plot(data['GHI'])
        #plt.plot(data['temp'])
        #plt.show()


        data['Tcell'], data['Tmodule'] = pvlib.pvl_sapmcelltemp(E=data['E'],
                                    Wspd=data['v_wind'],
                                    Tamb=data['temp'],
                                    modelt='Open_rack_cell_polymerback')


        DFOut = pvlib.pvl_sapm(Eb=data['Eb'],
                            Ediff=data['EDiff'],
                            Tcell=data['Tcell'],
                            AM=data['AM'],
                            AOI=data['AOI'],
                            Module=module_data)


        data['Pmp'] = DFOut['Vmp'] * DFOut['Imp']


        #print sum(data['E'])
        #print sum(data['GHI'])
        #print sum(data['Pmp'])
        #Data['Imp']=DFOut['Imp']*meta['parallelStrings']
        #Data['Voc']=DFOut['Voc']
        #Data['Vmp']=DFOut['Vmp']*meta['seriesModules']
        #Data['Pmp']=Data.Imp*Data.Vmp
        #Data['Ix']=DFOut['Ix']
        #Data['Ixx']=DFOut['Ixx']


        ## Wenn die Sonne untergegangen ist entstehen NaN-Werte im Diffus-Vektor
        ## Entweder auf Null setzen oder in der entsprechenden Funktion korrigieren.
        #blubb = Data.as_blocks()['float64'].as_blocks()['float64']['Imp'].values
        #bla = Data.as_blocks()['float64'].as_blocks()['float64']['Vmp'].values

        #blubber = blubb * bla

        #print blubb

        #plt.plot(data['Pmp'])
        ##plt.plot(data['E'])
        ##plt.plot(bla)
        ##plt.plot(blubber)
        #plt.show()

        # Einfallswinkel
        out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        '04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'aoi.csv',
        data['AOI'])

        # Direktstrahlung auf geneigte Ebene
        out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        '04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'eb.csv',
        data['Eb'])


        # Diffusstrahlung auf geneigte Ebene (gesamt)
        out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        '04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'ediff.csv',
        data['EDiff'])

        # Globalstrahlung auf geneigte Ebene
        out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        '04-Projektinhalte/PV_Modell_Vergleich/2015_PV_Modell_Vergleich_3/PVLIB_Python/results', 'e.csv',
        data['E'])

        #out.write_csv('/home/caro/rliserver/04_Projekte/026_Berechnungstool/' +
        #'04-Projektinhalte/PV_Modell_Vergleich/PVLIB_Python/results', 'pmp.csv',
        #data['Pmp'])

        #print(module_data['Area'])


        #results = db.read_data_from_file('3d_3.csv',
            #'/home/likewise-open/RL-INSTITUT/birgit.schachler')

        #fig = plt.figure()

        #tilt, azimuth = np.meshgrid(tilt, azimuth)
        #print(results)

        #fig = plt.figure()
        #ax = Axes3D(fig)

        #surf = ax.plot_surface(tilt, azimuth, results,
            #rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
        #fig.colorbar(surf)

        #plt.show()
