# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 11:11:31 2020

@author: Arsene Gasana
"""

import pandas as pd
import os
from datetime import datetime
version = '1_0'

main_dir = (r'C:\Users\user\Desktop\Analysis\Access App Uploads')
os.chdir(main_dir)
time = datetime.now()
datestring_for_file = '%04d%02d%02d%02d%02d%02d' % (time.year, time.month, time.day, time.hour,time.minute, time.second)


SCdata = pd.read_excel(r'')
VRdata = pd.read_excel(r'')
SCdata.insert(0, 'UID', SCdata['DistrictName']+SCdata['OAFID'].astype('str'))
VRdata.insert(0, 'UID', VRdata['District']+VRdata['OAFID'].astype('str'))
ListOfSites = SCdata['SiteName'].unique().tolist()

for site in ListOfSites:
    dir_name = '%s-%s-%s' % (site,version, datestring_for_file)
    os.chdir(main_dir)
    os.mkdir(dir_name)
    os.chdir(main_dir +'\\'+ dir_name)
    identity = SCdata[['UID',
                     'RegionName',
                     'DistrictName',
                     'SiteName',
                     'FieldOfficer',
                     'GroupName',
                     'LastName',
                     'FirstName',
                     'OAFID',
                     'NationalID', 
                     'NewMember',
                     'Facilitator',
                     'TotalCredit',
                     'TotalRepaid',
                     'RemainingCredit', 
                     '% Repaid', 
                     'FirstRepayment', 
                     'NbOfRepayments',
                     'LastRepayment', 
                     'TotalRepaid_IncludingOverpayments',
                     'ClientPhone', 
                     'AccountNumber']]
    inputs = SCdata.drop(['SeasonName', 'RegionName', 'DistrictName', 'SectorName','FieldManager', 'SiteName', 'FieldOfficer', 'GroupName', 'LastName',
                        'FirstName', 'OAFID', 'NationalID', 'FirstSeasonDataEntry','FieldOfficerPayrollID', 'FieldManagerPayrollID', 'NewMember',
                        'TotalEnrolledSeasons', 'Facilitator', 'TotalCredit', 'TotalRepaid','RemainingCredit', '% Repaid', 'FirstRepayment', 'NbOfRepayments',
                        'LastRepayment', 'TotalRepaid_IncludingOverpayments', 'Dropped','Deceased', 'DataEntry', 'ClientPhone', 'AccountNumber',
                        'ValidationCode', 'GovLocationGrandParent', 'GovLocationParent','GovLocationChild', 'GovLocationGrandChild', 'SiteProjectCode',
                        'GlobalClientID', '2020A_CycleCredit', '2020B_CycleCredit'], axis=1)
    repayment = VRdata[['UID','District','Site', 'Group','LastName', 'FirstName', 'OAFID','Amount', 'ReceiptID', 'Type', 'RepaymentDate','RepaymentPhoneNumber', 'AccountNumber']]
    inputs.index.names = ['ID']
    repayment.index.names = ['ID']
    save_name= site +'.xlsx'
    identity.to_excel('identity'+ save_name, index=False)
    inputs.to_excel('inputs'+ save_name)
    repayment.to_excel('Repayment'+save_name)
    
print('Data have been successfully exported')

