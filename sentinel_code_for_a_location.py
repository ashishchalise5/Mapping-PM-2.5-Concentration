# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:31:36 2020

@author: ashis
"""

from netCDF4 import Dataset
import numpy as np
import sys
name='S5P_OFFL_L2__AER_AI_20200129T053326_20200129T071456_11887_01_010302_20200201T072459.nc'
f = Dataset(name)
nc=f.groups['PRODUCT']
SDS_NAME='aerosol_index_354_388-precision'
sds=nc['aerosol_index_354_388']
latitude=nc['latitude'][:][0,:,:]
longitude=nc['longitude'][:][0,:,:]
min_lat=latitude.min()
max_lat=latitude.max()
min_lon=longitude.min()
max_lon=longitude.max()
qa=nc['qa_value']
scale_factor=qa.scale_factor
fillvalue=sds._FillValue
time=nc['time_utc'][:]
aerosol=nc['aerosol_index_354_388'][:][0,:,:]
min_aerosol=aerosol.min()
max_aerosol=aerosol.max()
print('The range of latitude in this file is: ',min_lat,' to ',max_lat, 'degrees \nThe range of longitude in this file is: ',min_lon, ' to ',max_lon,' degrees')
user_lat=float(input('\nPlease enter the latitude you would like to analyze (Deg. N): '))
user_lon=float(input('Please enter the longitude you would like to analyze (Deg. E): '))
while user_lat < min_lat or user_lat > max_lat:
    user_lat=float(input('The latitude you entered is out of range. Please enter a valid latitude: '))
while user_lon < min_lon or user_lon > max_lon:
    user_lon=float(input('The longitude you entered is out of range. Please enter a valid longitude: '))
R=6371000#radius of the earth in meters
lat1=np.radians(user_lat)
lat2=np.radians(latitude)
delta_lat=np.radians(latitude-user_lat)
delta_lon=np.radians(longitude-user_lon)
a=(np.sin(delta_lat/2))*(np.sin(delta_lat/2))+(np.cos(lat1))*(np.cos(lat2))*(np.sin(delta_lon/2))*(np.sin(delta_lon/2))
c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
d=R*c
x,y=np.unravel_index(d.argmin(),d.shape)
print('\nThe nearest pixel to your entered location is at: \nLatitude:',latitude[x,y],' Longitude:',longitude[x,y])

if aerosol[x,y]==fillvalue:
    print('The value of ',SDS_NAME,'at this pixel is',fillvalue,',(No Value)\n')
else:
    print('The value of ', SDS_NAME,'at this pixel is ',(aerosol[x,y]*scale_factor))
if x < 1:
    x+=1
if x > aerosol.shape[0]-2:
    x-=2
if y < 1:
    y+=1
if y > aerosol.shape[1]-2:
    y-=2
three_by_three=aerosol[x-1:x+2,y-1:y+2]
three_by_three=three_by_three.astype(float)
three_by_three[three_by_three==float(fillvalue)]=np.nan
nnan=np.count_nonzero(~np.isnan(three_by_three))
if nnan == 0:
    print ('\nThere are no valid pixels in a 3x3 grid centered at your entered location.')
else:
    three_by_three=three_by_three*scale_factor
    three_by_three_average=np.mean(three_by_three)
    three_by_three_std=np.std(three_by_three)
    three_by_three_median=np.median(three_by_three)
    if nnan == 1:
        npixels='is'
        mpixels='pixel'
    else:
        npixels='are'
        mpixels='pixels'
    print('\nThere',npixels,nnan,'valid',mpixels,'in a 3x3 grid centered at your entered location.')
    print('\nThe average value in this grid is: ',(three_by_three_average),' \nThe median value in this grid is: ',(three_by_three_median),'\nThe standard deviation in this grid is: ',(three_by_three_std))
if x < 2:
    x+=1
if x > aerosol.shape[0]-3:
    x-=1
if y < 2:
    y+=1
if y > aerosol.shape[1]-3:
    y-=1
five_by_five=aerosol[x-2:x+3,y-2:y+3]
five_by_five=five_by_five.astype(float)
five_by_five[five_by_five==float(fillvalue)]=np.nan
nnan=np.count_nonzero(~np.isnan(five_by_five))
if nnan == 0:
    print ('There are no valid pixels in a 5x5 grid centered at your entered location. \n')
else:
    five_by_five=five_by_five*scale_factor
    five_by_five_average=np.mean(five_by_five)
    five_by_five_std=np.std(five_by_five)
    five_by_five_median=np.median(five_by_five)
    if nnan == 1:
        npixels='is'
        mpixels='pixel'
    else:
        npixels='are'
        mpixels='pixels'
    print('\nThere',npixels,nnan,' valid',mpixels,' in a 5x5 grid centered at your entered location. \n')
    print('The average value in this grid is: ',(five_by_five_average),' \nThe median value in this grid is: ',(five_by_five_median),'\nThe standard deviation in this grid is: ',(five_by_five_std))
utc_time=time[0,x]
a=utc_time.split('T')
print('The data of the capture is: ',a[0])
nepali=a[1].split(':')
hour=int(nepali[0])+5
minute=int(nepali[1])+45
if minute>60:
    minute=minute-60
    hour=hour+1
hour=str(hour)
minute=str(minute)
print('The time of the capture is: ',a[1],'UTC')
print('The capture time according to  nepali clock: '+hour+':'+minute+':'+nepali[2])
    
    










    
    

    
    