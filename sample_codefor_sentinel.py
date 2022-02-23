# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:45:24 2020

@author: ashis
"""


from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import sys
name='S5P_OFFL_L2__AER_AI_20190901T055336_20190901T073505_09759_01_010302_20190907T051728.nc'
f = Dataset(name)
nc=f.groups['PRODUCT']
latitude=nc['latitude'][:][0,:,:]
longitude=nc['longitude'][:][0,:,:]
min_lat=latitude.min()
x=min_lat
print(type(x))
max_lat=latitude.max()
min_lon=longitude.min()
max_lon=longitude.max()
SDS_NAME='aerosol_index_354_388-precision'
sds=nc['aerosol_index_354_388']
aerosol=nc['aerosol_index_354_388'][:][0,:,:]

min_aerosol=aerosol.min()
max_aerosol=aerosol.max()
qa=nc['qa_value']
scale_factor=qa.scale_factor
valid_data=aerosol.ravel()

valid_data=[x for x in valid_data if x>=min_aerosol]
valid_data=[x for x in valid_data if x<=max_aerosol]
valid_data=np.asarray(valid_data)
valid_data=valid_data*scale_factor
average=sum(valid_data)/len(valid_data)
stdev=np.std(valid_data)
print('\nThe valid range of values is: ',round(min_aerosol*scale_factor,3), ' to ',round(max_aerosol*scale_factor,3),'\nThe average is: ',round(average,3),'\nThe standard deviation is: ',round(stdev,3))
print('The range of latitude in this file is: ',min_lat,' to ',max_lat, 'degrees \nThe range of longitude in this file is: ',min_lon, ' to ',max_lon,' degrees')
fillvalue=sds._FillValue
fv=fillvalue
aerosol=aerosol.astype(float)
aerosol[aerosol == fv] = np.nan
aerosol = np.ma.masked_array(aerosol, np.isnan(aerosol))
m = Basemap(projection='cyl', resolution='l', llcrnrlat=min_lat, urcrnrlat = 31, llcrnrlon=81, urcrnrlon = 88)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(10., 60., 10.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(80., 120., 10.), labels=[0, 0, 0, 1])
x, y = m(longitude, latitude)
m.pcolormesh(x, y, aerosol, cmap=plt.cm.jet)
plt.autoscale()
cb = m.colorbar()
cb.set_label('AOD')
plotTitle=name[:-4]
plt.title('{0}\n {1}'.format(plotTitle, SDS_NAME))
fig = plt.gcf()
plt.show()


			




