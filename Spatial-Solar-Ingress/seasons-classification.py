#!/usr/bin/env python
# coding: utf-8

# In[18]:


import datetime
import math
from datetime import date
from geopy.geocoders import Nominatim
import pandas as pd
from time import sleep
import xlwt
from xlwt import Workbook
from geopy.exc import GeocoderTimedOut
import time
import geopy

def main():
    print('Hello World')
    initiate_data_ret()

## Returns the number of days completed till the given date from the starting of the year.
def numOfDays(date1, date2):
    return (date2-date1).days

## Compute whether NH / SH based on the input Date.
def compute_hemisphere(month,l_day):
        if month > 2 and month < 9:
            if month == 3 and l_day < 20:
                return 'SH'
            elif month == 9 and l_day < 20:
                return 'NH'
            elif month in (3,4,5,6,7,8):
                return 'NH'
            elif month in (1,2,9,10,11,12):
                return 'SH'
        else:
            return 'SH'

## Compute Declination based on the no.of days completed and NH/SH
def compute_declination(d_ct,hemi):
    if hemi == 'NH':
        return 0 - round(23.45 + math.cos(0.9863*(d_ct+10)),4)
    else:
        return round(23.45 + math.cos(0.9863*(d_ct+10)),4)
    
## Compute Sun's altitude based on the dates given
def compute_seasons_astro(p_place,declin,month,l_day):
    try:
        l_lat = p_place
        
        ## Spring and Autumnal Equinoxes
        if ((month == 3 and l_day >= 20) or (month == 9 and l_day >= 20) or (month in (4,5,10,11)) or (month == 6 and l_day < 20)):
            return round((90 - l_lat),0)
        ## Winter and Summer Solstices
        elif ((month == 3 and l_day < 20) or (month in (7,8,12,1,2)) or (month == 6 and l_day >= 20) or (month == 9 and l_day < 20)):
            return round((90 - l_lat + declin),0)
    except:
        return 0
    
    
## Driver Manager for the entire exercise    
def initiate_data_ret():
    date_time_str = '2018-10-21 08:15:27.243860'
    ##loc = 'Nellore Andhra Pradesh 524002'
    ##loc = 'Sydney Australia 2055'

    
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    # Calculate the no of days 'd' - a value req for Declination
    l_year = int(date_time_obj.year)
    l_month = int(date_time_obj.month)
    l_day = date_time_obj.day
    date2 = date(l_year, l_month,l_day)
    date1 = date(l_year, 1, 1)
    days = numOfDays(date1, date2)
    l_hem = compute_hemisphere(l_month,l_day)
    l_decl = compute_declination(days,l_hem)
    geocoder = Nominatim()
    df = pd.read_csv('latitudes-list-wd.csv')
    # Workbook is created
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'COUNTRY')
    sheet1.write(0, 1, 'LATITUDE')
    sheet1.write(0, 2, 'ALTITUDE')
    sheet1.write(0, 3, 'SEASON')
    wb.save('Seasons.xls')
    for index, row in df.iterrows():
        ##altitude = compute_seasons_astro(geocoder.geocode(row["country"], timeout=geopy.geocoders.base.DEFAULT_SENTINEL),l_decl)
        altitude = compute_seasons_astro(row["latitude"],l_decl,l_month,l_day)
        sheet1.write(index+1, 0, row["country"])
        sheet1.write(index+1, 1, row["latitude"])
        sheet1.write(index+1, 2, altitude)
        if altitude <= 100:
            sheet1.write(index+1, 3, 'Winter')
        elif altitude > 100:
            sheet1.write(index+1, 3, 'Summer')
        elif altitude == 0:
            sheet1.write(index+1, 3, 'None')
        wb.save('Seasons.xls')
            


# In[19]:


print(time.time())
initiate_data_ret()
print(time.time())

