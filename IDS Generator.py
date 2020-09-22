# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:01:19 2019

@author: Arsene Gasana
"""
#import modules
import pandas as pd 
import xlsxwriter as xwt
import numpy as np
import os
from datetime import datetime
version = '1_0'

main_dir = r'D:\IDS PANDAS OUTPUT'
os.chdir(main_dir)
time = datetime.now()
datestring_for_file = '%04d%02d%02d%02d%02d%02d' % (time.year, time.month, time.day, time.hour,time.minute, time.second)

#import excel database and organize it
df = pd.read_csv(r'C:\Users\user\Desktop\chicken IDS tes.csv')

SiteID = df['DistrictName']+df['SiteName']
GroupID = df['SiteName'] + df['GroupName']

#get a list of districts and make directories per district & get a list of sites
GetDistrictList = np.unique(df['DistrictName'].values)
for dist in GetDistrictList:
    Dist_dir_name = '%s-%s-%s' % (dist,version, datestring_for_file)
    os.chdir(main_dir)
    os.mkdir(Dist_dir_name)
    os.chdir(main_dir +'\\'+ Dist_dir_name)
    DistrictDF = df.loc[df['DistrictName']==dist]
    site_list=np.unique(DistrictDF['SiteID'].values)

    for site in site_list:
        Site_dir_name = '%s-%s-%s' % (site,version, datestring_for_file)
        #os.chdir(main_dir)
        os.mkdir(Site_dir_name)
        os.chdir(Dist_dir_name +'\\'+Site_dir_name)
        SiteDF = df.loc[df['SiteName']==site]
        Group_list=np.unique(SiteDF['GroupID'].values)
        
        for group in Group_list :
            mydf = df.loc[df['GroupID']==group]
            Akarere = mydf['DistrictName'].tolist()[0]
            Akagali = mydf['SiteName'].tolist()[0]
            Itsinda = mydf['GroupName'].tolist()[0]
        
            #final data frame containing data values
            finaldf = mydf[['LastName','FirstName','2021A_Inkoko qty']]
            
            #save the data frame
            save_name= GroupID +'.xlsx'
            writer = pd.ExcelWriter(save_name, engine='xlsxwriter')
            finaldf.to_excel(writer, header=False, sheet_name=group, startrow=8, index=False)