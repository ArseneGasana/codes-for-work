#Import modules to use
import pandas as pd
import os
from datetime import datetime
version = '2_0'

#Set main directory where to store your output
while True:
    try:
        main_dir = input ('Where do you want to store out put?(Enter full dir name):')
        os.chdir(main_dir)
        break
    except FileNotFoundError:
        print('YOU ENTERED A WRONG VALUE! TRY AGAIN:')

time = datetime.now()
datestring_for_file = '%04d%02d%02d%02d%02d%02d' % (time.year, time.month, time.day, time.hour,time.minute, time.second)

#Import season client and vertical repayment in .xlsx format
while True:
    try:
        SCPath = input('Enter season clients Path')
        SCdata = pd.read_excel(SCPath)
        break
    except FileNotFoundError:
        print('YOU ENTERED A WRONG VALUE! TRY AGAIN:')

while True:
    try:
        VRPath = input('Enter Vertical Repayment')
        VRdata = pd.read_excel(VRPath)
        break
    except FileNotFoundError:
        print('YOU ENTERED A WRONG VALUE! TRY AGAIN:')

#Insert new columns, do some cleaning and melt the inputs columns to show them in horizontal format
SCdata['NationalID'] = SCdata['NationalID'].astype(str)
SCdata.insert(0, 'UID', SCdata['DistrictName']+'_'+SCdata['OAFID'].astype('str'))
SCdata.insert(1, 'SiteID', SCdata['DistrictName']+'_'+SCdata['SiteName'])
VRdata.insert(0, 'UID', VRdata['District']+'_'+VRdata['OAFID'].astype('str'))
VRdata.insert(1, 'SiteID', VRdata['District']+'_'+VRdata['Site'])
inputsdf =SCdata[SCdata.iloc[:,[0,1]].columns.to_list()+SCdata.iloc[:,43:].columns.to_list()]
MeltInputs=inputsdf.melt(['UID','SiteID'],SCdata.iloc[:,43:].columns.to_list(),'Input','Quantity')
Finalinputdf =MeltInputs[MeltInputs['Quantity']>0].sort_values(by='UID')

#Print the list of sites & districts present in the dataframe
SiteIDList = SCdata['SiteID'].unique().tolist()
counter = 0
for i,SiteID in enumerate(SiteIDList, start=0):
    print(i,':',SiteID)

#Make a list of selected sites and print them
while True:
    try:
        IDsNumbers = [int(SiteID) for SiteID in input("Select number corresponding to sites you need:").split()] 
        break
    except ValueError:
        print('The list should only contain numbers separated by a single space, no other character should be between numbers')
        
ListOfSitesUID = [SiteIDList[i] for i in IDsNumbers]
print('You have selected the following sites:',ListOfSitesUID)


#Make site data frames for each category and rename index columns
#save the output
for site in ListOfSitesUID:

    #Make directory for each site
    dir_name = '%s-%s-%s' % (site,version, datestring_for_file)
    os.chdir(main_dir)
    os.mkdir(dir_name)
    os.chdir(main_dir +'\\'+ dir_name)

    #Make dataframes for each site
    identity = SCdata[SCdata['SiteID']==site][SCdata.iloc[:,[0,1,2,3,4,7,9,10,11,12,13,17,19,20,21,22,23,24,25,26,27,31,32]].columns.to_list()]
    inputs = Finalinputdf[Finalinputdf['SiteID']==site]
    inputs=inputs.drop(['SiteID'], axis=1)
    repayment = VRdata[VRdata['SiteID']==site][VRdata.iloc[:,[0,2,4,5,8,9,10,12,13,14,15,16,18,19]].columns.to_list()]

    #Rename index columns
    inputs.index.names = ['ID']
    repayment.index.names = ['ID']

    #Save files
    save_name= site +'.xlsx'
    identity.to_excel('identity'+ save_name, index=False)
    inputs.to_excel('inputs'+ save_name)
    repayment.to_excel('Repayment'+save_name)
    save_name= site +'.xlsx'
    identity.to_excel('identity'+ save_name, index=False)

print('OPERATION SUCCESSFUL!!')




