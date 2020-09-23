# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 19:43:36 2018

@author: Arsene Gasana
"""

import pandas as pd
import numpy as np
import os
import xlsxwriter as xwt
os.chdir(r'E:\Personal folder\Coding')

def getData():
    data=pd.read_excel('Distribution point.xlsx')
    return data

def getDistList():
    data=getData()
    dist_list=np.unique(data['DistrictFrom'].values)
    return(dist_list)
    
def distDataFrame(dist_selected):
    data=getData()
    distDF=data.loc[data['DistrictFrom']==dist_selected]
    return (distDF)
    
def getSiteList(dist_selected):
    data = distDataFrame(dist_selected)
    site_list=np.unique(data['DropFrom'].values)
    return(site_list)
    
def makeSiteDataFrame(df,site_selected):
    
    siteDF=df.loc[df['DropFrom']==site_selected]
    IDP_dataframe=pd.DataFrame(siteDF, columns=['DistrictFrom','DropFrom','InputName','MovementSummaryString','Quantity'])
    table=pd.pivot_table(IDP_dataframe, values='Quantity', index=['DistrictFrom','DropFrom','InputName'], columns=['MovementSummaryString'], aggfunc=np.sum)
    table['Total_Difference']=table['Distributed to clients']+table['Reloaded onto truck']+table['Unloaded from truck']
    return(table)

def main():
    DistList = getDistList()

    counter=0
    for d in DistList:
        print(str(counter) +':'+ d)
        counter+=1
    select_dist=input('choose a district number above:')
    dist_selected=DistList[int(select_dist)]
    print('you have selected',dist_selected, 'District and it has the following sites:')
    df = distDataFrame(dist_selected)
        
    siteList = getSiteList(dist_selected)
    counter=0
    for site in siteList:
        print(str(counter) +':'+ site)
        counter+=1
    
    select_site=input('choose a site number above:')
    site_selected=siteList[int(select_site)]
    print ('you have selected:', site_selected, 'site')
    dataframe =makeSiteDataFrame(df,site_selected)
    save_name=dist_selected + site_selected + '.xlsx'
    directory = os.getcwd()
    writer = pd.ExcelWriter(save_name, engine = 'xlsxwriter')
    dataframe.to_excel(writer, header=False, sheet_name='Sheet1', startrow=3)
    
    workbook = writer.book
    workbook.formats[0].set_font_size(9)
    worksheet = writer.sheets['Sheet1']
    cell_format = workbook.add_format({'bold': True,
                                       'text_wrap':True, 
                                       'border':1,
                                       'font_size':9})
    cell_format.set_align('top')
    cell_format.set_align('center')
    
    worksheet.merge_range('A1:G1','2019A IDS & TMS RECONCILIATION',cell_format)
    worksheet.write('A3', 'Akarere',cell_format)
    worksheet.write('B3', 'Akagali',cell_format)
    worksheet.write('C3', 'Inyongeramusaruro',cell_format)
    worksheet.write('D3', 'Ibyahawe abahinzi',cell_format)
    worksheet.write('E3', 'Ibyagaruwe',cell_format)
    worksheet.write('F3', 'Ibyapakuruwe',cell_format)
    worksheet.write('G3', 'Ikinyuranyo',cell_format)
    worksheet.write('F2', 'Abura:')
    worksheet.write('G2', '=sum(G5:G18)')
    
    col_format = workbook.add_format({'font_size':9})
    
    worksheet.set_row(0, 30,)
    worksheet.set_column('A:B',15)
    worksheet.set_column('A:C',15,col_format)

    
    
    print('DONE!!!', save_name, 'file have been successfully saved in,', directory)


main()