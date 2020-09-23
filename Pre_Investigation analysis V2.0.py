# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:26:18 2019

@author: arsene gasana
"""

import pandas as pd 
import xlsxwriter as xwt
import numpy as np
import os

SeasonClients = pd.read_excel(r'E:\Users\One Acre Fund\Desktop\GAB Analysis\gab_scc.xlsx')
VeriticalRepayment = pd.read_excel(r'E:\Users\One Acre Fund\Desktop\GAB Analysis\gab_vr.xlsx')

NeededSitesInput = input('Enter a list of Sites you want separated by comma(,)')
NeededSites = NeededSitesInput.split(',')
NeededSiteDf_sc = SeasonClients[SeasonClients['SiteName'].isin(NeededSites)]
NeededSiteDf_vr = VeriticalRepayment[VeriticalRepayment['Site'].isin(NeededSites)]

print('Sites data frames have been built')

#Site identification information

SiteName =  NeededSiteDf_sc['SiteName'].tolist()[0]
DistrictName = NeededSiteDf_sc['DistrictName'].tolist()[0]
RegionName = NeededSiteDf_sc['RegionName'].tolist()[0]
SeasonName = NeededSiteDf_sc['SeasonName'].tolist()[0]
FOName = NeededSiteDf_sc['FieldOfficer'].tolist()[0]

save_name= SiteName +'Analysis'+'.xlsx'
writer = pd.ExcelWriter(save_name, engine='xlsxwriter')
Template = pd.DataFrame()
Template.to_excel(writer, header=False, sheet_name=SiteName, index=False)
workbook = writer.book
workbook.formats[0].set_font_size(12)
worksheet = writer.sheets[SiteName]

#Format the heading row

worksheet.set_row(0, 32)
worksheet.insert_image('F1', 
                       r'E:\Personal folder\Coding\Python 3\tuburaimages.PNG',
                       {'x_scale': 0.5, 
                        'y_scale': 0.5})
title_format = workbook.add_format({'bold': True,
	                                        'text_wrap':True, 
	                                        'border':5,
	                                        'font_size':12}) 
title_format.set_align('left')
title_format.set_align('vcenter')
worksheet.merge_range('A1:E1',
                      'PRE-INVESTIGATION SITE ANALYSIS_CLIENTS OF INTEREST',
                      title_format)

#worksheet.set_column('A',20)

worksheet.write('B2',SeasonName)
worksheet.write('B3',SiteName)
worksheet.write('B4',DistrictName)
worksheet.write('B5',RegionName)
worksheet.write('B6',FOName)
worksheet.write('A2','Season Name')
worksheet.write('A3','Site Name')
worksheet.write('A4','District Name')
worksheet.write('A5','Region Name')
worksheet.write('A6','FO Name')

#Sites basic data

NumberofClients = NeededSiteDf_sc['OAFID'].count()
TotalCredit = NeededSiteDf_sc['TotalCredit'].sum()
TotalRepaid = NeededSiteDf_sc['TotalRepaid'].sum()
RemainingCredit = NeededSiteDf_sc['RemainingCredit'].sum()
Repaid = NeededSiteDf_sc['% Repaid'].mean()
NewClients = len(NeededSiteDf_sc.loc[NeededSiteDf_sc['NewMember']==True])
ExistingClients = len(NeededSiteDf_sc.loc[NeededSiteDf_sc['NewMember']==False])
NumberOfGroups = len(NeededSiteDf_sc['GroupName'].unique())

worksheet.write('B9',NumberofClients)
worksheet.write('B10',TotalCredit)
worksheet.write('B11',TotalRepaid)
worksheet.write('B12',RemainingCredit)
worksheet.write('B13',Repaid)
worksheet.write('B14',NewClients)
worksheet.write('B15',ExistingClients)
worksheet.write('B16',NumberOfGroups)
worksheet.write('A9','NumberofClients')
worksheet.write('A10','TotalCredit')
worksheet.write('A11','TotalRepaid')
worksheet.write('A12','RemainingCredit')
worksheet.write('A13','Repaid')
worksheet.write('A14','New Clients')
worksheet.write('A15','Existing Clients')
worksheet.write('A16','Number Of Groups')

worksheet.set_column('A:B',15)

#List of top 10 clients with highest credit a
ListTitlesFormat = workbook.add_format({'bold': True,
	                                        'text_wrap':False,
	                                        'font_size':12}) 
worksheet.write('A18','List of top 10 clients with highest credit',ListTitlesFormat)
ClientsWithHighCredit = NeededSiteDf_sc.nlargest(10, 
                                                 ['TotalCredit'])[['LastName',
                                                 'FirstName',
                                                 'OAFID',
                                                 'GroupName',
                                                 'TotalCredit',
                                                 '% Repaid']]
ClientsWithHighCredit['Defrauded?']=''
ClientsWithHighCredit.to_excel(writer, header=True, 
                               sheet_name=SiteName, 
                               index=False, startrow=19)

HCtoDataBase = ClientsWithHighCredit[['LastName',
                                      'FirstName',
                                      'OAFID',
                                      'GroupName']]
HCtoDataBase['Category'] = 'High Credit'


#List of top 10 clients low credit clients 
worksheet.write('A32','List of top 10 clients with Lowest credit',ListTitlesFormat)
ClientsWithLowCredit = NeededSiteDf_sc.nsmallest(10, 
                                                 ['TotalCredit'])[['LastName',
                                                 'FirstName',
                                                 'OAFID',
                                                 'GroupName',
                                                 'TotalCredit',
                                                 '% Repaid']]
ClientsWithLowCredit['Defrauded']=''
ClientsWithLowCredit.to_excel(writer, header=True, sheet_name=SiteName, 
                              index=False, startrow=33)
LCtoDataBase = ClientsWithLowCredit[['LastName',
                                     'FirstName',
                                     'OAFID',
                                     'GroupName']]
LCtoDataBase['Category'] = 'low Credit'

#List of clients below repayment target
worksheet.write('A46','List of top 10 clients Below Repayment goal',ListTitlesFormat)
ClientsBelowRepaymentGoal = NeededSiteDf_sc[NeededSiteDf_sc['% Repaid']<100][['LastName',
                                           'FirstName',
                                           'OAFID',
                                           'GroupName',
                                           'TotalCredit',
                                           '% Repaid']]

TopClientsBelowRepaymentGoal = ClientsBelowRepaymentGoal.nsmallest(10, ['% Repaid'])
TopClientsBelowRepaymentGoal['Defrauded']=''
TopClientsBelowRepaymentGoal.to_excel(writer, header=True, 
                                   sheet_name=SiteName, 
                                   index=False, startrow=47)
BRGtoDataBase = ClientsWithLowCredit[['LastName',
                                      'FirstName',
                                      'OAFID',
                                      'GroupName']]
BRGtoDataBase['Category'] = 'Below Repayment Goal'

#Top 10 payments that are not cash, mobile money or auditor
worksheet.write('A60','List of top 10 Repayments that are not cash, mobilemoney ',ListTitlesFormat)

ClientsWithOtherRepayments = VeriticalRepayment[~VeriticalRepayment['Type'].isin(['Receipt',
                                                'MobileMoney',
                                                'Auditor',
                                                'Repayment Write Off'])]

TopClientsWithOtherRepayments = ClientsWithOtherRepayments.nlargest(10,
                                                                    ['Amount'])[['LastName',
                                                                    'FirstName',
                                                                    'OAFID',
                                                                    'Group',
                                                                    'Amount',
                                                                    'Type']]
                                                                    

TopClientsWithOtherRepayments['Defrauded']=''                 
TopClientsWithOtherRepayments.to_excel(writer, header=True, 
                                       sheet_name=SiteName, 
                                       index=False, startrow=61)
OtherReptoDataBase = ClientsWithOtherRepayments[['LastName',
                                                 'FirstName',
                                                 'OAFID',
                                                 'Group']]
OtherReptoDataBase['Category'] = 'Other Rep Type'

#Clients who finished their in one payment
worksheet.write('A74','List of top 10 clients who finished their credit in one payment',ListTitlesFormat)
ClientsWhoPaidAllOnce = NeededSiteDf_sc[(NeededSiteDf_sc['NbOfRepayments']==1)&(NeededSiteDf_sc['% Repaid']==100)]
TopClientsWhoPaidAllOnce = ClientsWhoPaidAllOnce.nlargest(10,
                                                          ['TotalCredit'])[['LastName'
                                                          ,'FirstName',
                                                          'OAFID',
                                                          'TotalCredit',
                                                          'FirstRepayment',
                                                          '% Repaid']]
TopClientsWhoPaidAllOnce['Defrauded']=''
TopClientsWhoPaidAllOnce.to_excel(writer, 
                                  header=True, 
                                  sheet_name=SiteName, 
                                  index=False, 
                                  startrow=75)
OnePaytoDataBase = TopClientsWhoPaidAllOnce[['LastName',
                                             'FirstName',
                                             'OAFID']]
OnePaytoDataBase['Category'] = 'Finished in one pay'

writer.save()

DataBase = pd.concat([HCtoDataBase, 
                      LCtoDataBase, 
                      BRGtoDataBase, 
                      OtherReptoDataBase, 
                      OnePaytoDataBase ])

DataBase.to_excel('Final DataBase.xlsx')

#SITE LEVEL KPIs ANALYSIS





