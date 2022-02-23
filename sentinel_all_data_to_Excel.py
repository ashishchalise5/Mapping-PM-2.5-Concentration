# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 22:07:42 2020

@author: ashis
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:31:36 2020

@author: ashis
"""

from netCDF4 import Dataset
import numpy as np
import sys
import csv
name='S5P_OFFL_L2__AER_AI_20191001T062830_20191001T080959_10185_01_010302_20191007T055114.nc'
f = Dataset(name)
nc=f.groups['PRODUCT']
SDS_NAME1='aerosol_index_340_380'
SDS_NAME2='aerosol_index_340_380_precision'
SDS_NAME3='aerosol_index_354_388'
SDS_NAME4='aerosol_index_354_388_precision'
sds1=nc['aerosol_index_340_380']
sds2=nc['aerosol_index_340_380_precision']
sds3=nc['aerosol_index_354_388']
sds4=nc['aerosol_index_354_388_precision']
latitude=nc['latitude'][:][0,:,:]
longitude=nc['longitude'][:][0,:,:]
min_lat=latitude.min()
max_lat=latitude.max()
min_lon=longitude.min()
max_lon=longitude.max()
qa=nc['qa_value']
scale_factor=qa.scale_factor
fillvalue=sds1._FillValue
time=nc['time_utc'][:]
aerosol1=sds1[:][0,:,:]
aerosol2=sds2[:][0,:,:]
aerosol3=sds3[:][0,:,:]
aerosol4=sds4[:][0,:,:]
min_aerosol1=aerosol1.min()
min_aerosol2=aerosol2.min()
min_aerosol3=aerosol3.min()
min_aerosol4=aerosol4.min()
max_aerosol1=aerosol1.max()
max_aerosol2=aerosol2.max()
max_aerosol3=aerosol3.max()
max_aerosol4=aerosol4.max()
lat=list()
lon=list()
utc_time=list()
n_time=list()
e_date=list()
#aerosol value
a1=list()
a2=list()
a3=list()
a4=list()
#aerosol_name
sdsname1=list()
sdsname2=list()
sdsname3=list()
sdsname4=list()
#total number of valid pixel in 3*3
a1_3=list()
a2_3=list()
a3_3=list()
a4_3=list()
#total number of valid pixel in 5*5
a1_5=list()
a2_5=list()
a3_5=list()
a4_5=list()
#average value in 3*3
a3_av1=list()
a3_av2=list()
a3_av3=list()
a3_av4=list()
#median value in 3*3
a3_md1=list()
a3_md2=list()
a3_md3=list()
a3_md4=list()
#sd value in 3*3
a3_sd1=list()
a3_sd2=list()
a3_sd3=list()
a3_sd4=list()
#average value in 5*5
a5_av1=list()
a5_av2=list()
a5_av3=list()
a5_av4=list()
#average value in 5*5
a5_md1=list()
a5_md2=list()
a5_md3=list()
a5_md4=list()
#average value in 5*5
a5_sd1=list()
a5_sd2=list()
a5_sd3=list()
a5_sd4=list()

print('The range of latitude in this file is: ',min_lat,' to ',max_lat, 'degrees \nThe range of longitude in this file is: ',min_lon, ' to ',max_lon,' degrees')
a=int(input('please enter the total number of coordinates to be checked in this images: '))
count=range(a)
for items in count:
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
    lat.append(latitude[x,y])
    lon.append(longitude[x,y])
    
    utc1_time=time[0,x]
    
    a=utc1_time.split('T')
    e=a[0].lstrip()
    e_date.append(a[0])
    e_date=e_date
    print('The date of the capture is: ',a[0])
    utc_time.append(a[1])
    nepali=a[1].split(':')
    hour=int(nepali[0])+5
    minute=int(nepali[1])+45
    if minute>60:
        minute=minute-60
        hour=hour+1
    hour=str(hour)
    minute=str(minute)
    ne_time=hour+':'+minute+':'+nepali[2]
    n_time.append(ne_time)
    
    print('The time of the capture is: ',a[1],'UTC')
    print('The capture time according to  nepali clock:',ne_time)
    
    def aerosols(aerosol,SDS_NAME,p,q):
        global nnan1, nnan2, three_by_three_average, three_by_three_median, three_by_three_std, five_by_five_average, five_by_five_median, five_by_five_std 
        
        
        if aerosol[p,q]==fillvalue:
            print('The value of ',SDS_NAME,'at this pixel is',fillvalue,',(No Value)\n')
        else:
            print('\nThe value of ', SDS_NAME,'at this pixel is ',(aerosol[x,y]*scale_factor))
        if p < 1:
            p+=1
        if p > aerosol.shape[0]-2:
            p-=2
        if q < 1:
            q+=1
        if q > aerosol.shape[1]-2:
            q-=2
        three_by_three=aerosol[p-1:p+2,q-1:q+2]
        three_by_three=three_by_three.astype(float)
        three_by_three[three_by_three==float(fillvalue)]=np.nan
        nnan1=np.count_nonzero(~np.isnan(three_by_three))
        if nnan1 == 0:
            print ('\nThere are no valid pixels in a 3x3 grid centered at your entered location.')
        else:
            three_by_three=three_by_three*scale_factor
            three_by_three_average=np.mean(three_by_three)            
            three_by_three_std=np.std(three_by_three)            
            three_by_three_median=np.median(three_by_three)
            if nnan1 == 1:
                npixels='is'
                mpixels='pixel'
            else:
                npixels='are'
                mpixels='pixels'
            print('\nThere',npixels,nnan1,'valid',mpixels,'in a 3x3 grid centered at your entered location.')
            print('\nThe average value in this grid is: ',(three_by_three_average),' \nThe median value in this grid is: ',(three_by_three_median),'\nThe standard deviation in this grid is: ',(three_by_three_std))                               
        if p < 2:
            p+=1
        if p > aerosol.shape[0]-3:
            p-=1
        if q < 2:
            q+=1
        if q > aerosol.shape[1]-3:
            q-=1
        five_by_five=aerosol[p-2:p+3,q-2:q+3]
        five_by_five=five_by_five.astype(float)
        five_by_five[five_by_five==float(fillvalue)]=np.nan
        nnan2=np.count_nonzero(~np.isnan(five_by_five))
        if nnan2 == 0:
            print ('There are no valid pixels in a 5x5 grid centered at your entered location. \n')
        else:
            five_by_five=five_by_five*scale_factor
            five_by_five_average=np.mean(five_by_five)
            five_by_five_std=np.std(five_by_five)
            five_by_five_median=np.median(five_by_five)
            if nnan2 == 1:
                npixels='is'
                mpixels='pixel'
            else:
                npixels='are'
                mpixels='pixels'
            print('\nThere',npixels,nnan2,' valid',mpixels,' in a 5x5 grid centered at your entered location. \n')
            print('The average value in this grid is: ',(five_by_five_average),' \nThe median value in this grid is: ',(five_by_five_median),'\nThe standard deviation in this grid is: ',(five_by_five_std))
    aerosols(aerosol1,SDS_NAME1,x,y)
    a1.append(aerosol1[x,y]*scale_factor)
    sdsname1.append(SDS_NAME1)
    a1_3.append(nnan1)
    a1_5.append(nnan2)
    a3_av1.append(three_by_three_average)
    a3_md1.append(three_by_three_median)
    a3_sd1.append(three_by_three_std)
    a5_av1.append(five_by_five_average)
    a5_md1.append(five_by_five_median)
    a5_sd1.append(five_by_five_std)
    aerosols(aerosol2,SDS_NAME2,x,y)
    a2.append(aerosol2[x,y]*scale_factor)
    sdsname2.append(SDS_NAME2)
    a2_3.append(nnan1)
    a2_5.append(nnan2)
    a3_av2.append(three_by_three_average)
    a3_md2.append(three_by_three_median)
    a3_sd2.append(three_by_three_std)
    a5_av2.append(five_by_five_average)
    a5_md2.append(five_by_five_median)
    a5_sd2.append(five_by_five_std)
    
    aerosols(aerosol3,SDS_NAME3,x,y)
    a3.append(aerosol3[x,y]*scale_factor)
    sdsname3.append(SDS_NAME3)
    a3_3.append(nnan1)
    a3_5.append(nnan2)
    a3_av3.append(three_by_three_average)
    a3_md3.append(three_by_three_median)
    a3_sd3.append(three_by_three_std)
    a5_av3.append(five_by_five_average)
    a5_md3.append(five_by_five_median)
    a5_sd3.append(five_by_five_std)
    
    aerosols(aerosol4,SDS_NAME4,x,y)
    a4.append(aerosol4[x,y]*scale_factor)
    sdsname4.append(SDS_NAME4)
    a4_3.append(nnan1)
    a4_5.append(nnan2)
    a3_av4.append(three_by_three_average)
    a3_md4.append(three_by_three_median)
    a3_sd4.append(three_by_three_std)
    a5_av4.append(five_by_five_average)
    a5_md4.append(five_by_five_median)
    a5_sd4.append(five_by_five_std)
    print(aerosol4[x,y])

row3=['Date', 'UTC_Time','Nepali_time','Latitude','Longitude','Aerosol1 value','Valid Pixel A1','3*3 average A1','3*3 median A1','3*3 STD A1','Aerosol2 value','Valid Pixel A2','3*3 average A2','3*3 median A2','3*3 STD A2','Aerosol3 value','Valid Pixel A3','3*3 average A3','3*3 median A3','3*3 STD A3','Aerosol4 value','Valid Pixel A4','3*3 average A4','3*3 median A4','3*3 STD A4']
row5=['Date', 'UTC_Time','Nepali_time','Latitude','Longitude','Aerosol1 value','Valid Pixel A1','5*5 average A1','5*5 median A1','5*5 STD A1','Aerosol2 value','Valid Pixel A2','5*5 average A2','5*5 median A2','5*5 STD A2','Aerosol3 value','Valid Pixel A3','5*5 average A3','5*5 median A3','5*5 STD A3','Aerosol4 value','Valid Pixel A4','5*5 average A4','5*5 median A4','5*5 STD A4']
rows3 = zip(e_date,utc_time,n_time,lat,lon,a1,a1_3,a3_av1,a3_md1,a3_sd1,a2,a2_3,a3_av2,a3_md2,a3_sd4,a3,a3_3,a3_av3,a3_md3,a3_sd3,a4,a4_3,a3_av4,a3_md4,a3_sd4)
rows5=zip(e_date,utc_time,n_time,lat,lon,a1,a1_5,a5_av1,a5_md1,a5_sd1,a2,a2_5,a5_av2,a5_md2,a5_sd2,a3,a3_5,a5_av3,a5_md3,a5_sd3,a4,a4_5,a5_av4,a5_md4,a5_sd4)
with open('1.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(row3)
    writer.writerows(rows3)
with open('2.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(row5)
    writer.writerows(rows5)

  
    
    



 
        
            
            



    
    










    
    

    
    