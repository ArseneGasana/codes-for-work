# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:01:19 2019

@author: One Acre Fund
"""
#import modules
import pandas as pd 
import xlsxwriter as xwt
import numpy as np
import os
from datetime import datetime
version = '1_0'

main_dir = r'E:\Personal folder\Coding\pandas output'
os.chdir(main_dir)
time = datetime.now()
datestring_for_file = '%04d%02d%02d%02d%02d%02d' % (time.year, time.month, time.day, time.hour,time.minute, time.second)

#import excel database and organize it
df = pd.read_excel(r'E:\Users\One Acre Fund\Desktop\final database for notices.xlsx')

#get a list of districts and make directories per district & get a list of sites
GetDistrictList = np.unique(df['DistrictFrom'].values)
for dist in GetDistrictList:
    dir_name = '%s-%s-%s' % (dist,version, datestring_for_file)
    os.chdir(main_dir)
    os.mkdir(dir_name)
    os.chdir(main_dir +'\\'+ dir_name)
    DistrictDF = df.loc[df['DistrictFrom']==dist]
    site_list=np.unique(DistrictDF['UID'].values)
    
    #get values to use in identity information from site dataframes
    for site in site_list :
        mydf = df.loc[df['UID']==site]
        Akarere = mydf['DistrictFrom'].tolist()[0]
        Akagali = mydf['Site'].tolist()[0]
        Site_yitanga = mydf['DropFrom'].tolist()[0]
        FM_witanga = mydf['FM Distributor'].tolist()[0]
        payroll_ID = mydf['Distributor Payroll code'].tolist()[0]
        distribution_date = mydf['Distribution date'].tolist()[0]
        uid = mydf['UID'].tolist()[0]
        
        #final data frame containing data values
        finaldf = mydf[['InputName',
               'Unloaded from truck',
               'Reloaded onto truck',
               'Distributed to clients',
               'should have been distributed',
               'Difference(missing)',
               'Price per unit/Kg',
               'Total cost']]
        
        #save the data frame
        save_name= FM_witanga + uid +'.xlsx'
        writer = pd.ExcelWriter(save_name, engine='xlsxwriter')
        finaldf.to_excel(writer, header=False, sheet_name=site, startrow=8, index=False)
        
#EXCEL SHEET FORMATTING SECTION
#==============================================================================
        #make a workbook and its global size    
        workbook = writer.book
        workbook.formats[0].set_font_size(12)
        worksheet = writer.sheets[site]
        
        #set roow sizes for the first 3 rows containing headings common for each notice
        worksheet.set_row(0, 32)
        worksheet.set_row(1, 49)
        worksheet.set_row(2, 160)
        
        #set column size for all columns
        worksheet.set_column('A:H',9)
        
        #insert an image - TUBURA - in the notice heading
        worksheet.insert_image('G1', r'E:\Personal folder\Coding\tuburaimages.PNG',{'x_scale': 0.5, 'y_scale': 0.5})
        
        
        #NOTICE TITLE
        #======================================================================
        #Title and its format
        title_format = workbook.add_format({'bold': True,
	                                        'text_wrap':True, 
	                                        'border':5,
	                                        'font_size':18}) 
        
        title_format.set_align('center')
        title_format.set_align('vcenter')
        worksheet.merge_range('A2:H2','IHUZAMAKURU RYA IDS NA TMS RYA 2019 A\n KUMENYESHA INYONGERAMUSARURO ZABUZE',title_format)
        
        
        # NOTICE COMM
        #======================================================================
        #comm and its format
        comm_format = workbook.add_format({'text_wrap':True,
	                                       'font_size':12})
    
        comm_format.set_align('justify')
        
        comm_format.set_align('vcenter')
        worksheet.merge_range('A3:H3',"Nkuko bigaragazwa n’amakuru ya IDS na TMS wakoresheje mu ifata kandi wasinyeho, biragaragara ko urebwa n’inyongeramusaruro zabuze mu ifata ry’ igihembwe cya 2019 A. Dukurikije amategeko n’amabwiriza ku ibura ry’ inyongeramusaruro kandi wayashyizeho umukono mbere y’ifata rya 2019A, ugomba kwishyura igiciro cy’izo nyongeramusaruro wabuze kugirango hagarurwe amafaranga zari kuzishyurwa iyo zitabura. Icyakora hari amafaranga 10,000 Rwf wababariwe yagabanijwe kuyo ugomba kwishyura yose bityo ayo uzishyura ni make kuyo wagombaga kwishyura. Amafaranga uzishyuzwa azakurwa ku mushahara wawe kandi ntihazarenzwa 20% y’umushahara wawe wa buri kwezi. Kubera iyi mpamvu rero, turakumenyeshako uzishyura aya mafaranga buri kwezi kugeza ashizemo",comm_format)
        
        
        #IDENTITY INFORMATION SECTION
        #======================================================================
        #identity Format
        id_format = workbook.add_format({'bold': True,
	                                     'text_wrap':True, 
	                                     'font_size':12})
        id_format.set_align('top')
        id_format.set_align('left')
        
        #identity titles and their cell locations
        worksheet.merge_range('A4:B4', 'Akarere',id_format)
        worksheet.merge_range('A5:B5', 'Akagali',id_format)
        worksheet.merge_range('A6:B6', "Site y'ifata",id_format)
        worksheet.merge_range('E4:F4', "FM w'ifata",id_format)
        worksheet.merge_range('E5:F5', 'Numero imuranga',id_format)
        worksheet.merge_range('E6:F6', "Taliki y'ifata",id_format)
        
        #identity values and their cell locations
        worksheet.merge_range('C4:D4',Akarere, id_format)
        worksheet.merge_range('C5:D5',Akagali, id_format)
        worksheet.merge_range('C6:D6',Site_yitanga, id_format)
        worksheet.merge_range('G4:I4',FM_witanga,id_format)
        worksheet.merge_range('G5:I5',payroll_ID,id_format)
        worksheet.merge_range('G6:I6',distribution_date,id_format)
        
        #INPUTS TABLE SECTION
        #======================================================================
        #table headings format
        heading_format = workbook.add_format({'bold': True,
	                                       'text_wrap':True, 
	                                       'border':1,
	                                       'font_size':12})
        heading_format.set_align('top')
        heading_format.set_align('center')
        
        #table headings, their cell location and format
        worksheet.write('A8', 'Inyongeramusaruro',heading_format)
        worksheet.write('B8', '1.Ibyapakuruwe\n(TMS)',heading_format)
        worksheet.write('C8', '2.Ibyongeye gupakirwa\n(TMS)',heading_format)
        worksheet.write('D8', '3.Ibyahawe abahinzi\n(IDS)',heading_format)
        worksheet.write('E8', '4.Ibyagombaga guhabwa abahinzi\n(1-2)',heading_format)
        worksheet.write('F8', 'Ibibura\n(3-4)',heading_format)
        worksheet.write('G8', 'Agaciro ka kimwe',heading_format)
        worksheet.write('H8', 'Agaciro kose',heading_format)
        
        #add borders to the table
        border_format = workbook.add_format({'border':1})
        bor_last_row = str(len(mydf['InputName'])+8)
        bor_range = 'A9' + ':' + 'H'+ bor_last_row
        worksheet.conditional_format(bor_range, {'type':'no_blanks',
	                                            'format':border_format})
    
        #TOTAL AMOUNT TO BE CHARGED SECTION
        #======================================================================
        
        #format
        col3_format = workbook.add_format({'font_size':13,
	                                       'bold':True})
        col3_format.set_num_format('#,##0'+ 'Rwf')
        
        #build ranges for total values of missing input, title and values
        tot_charg_row = str(len(mydf['InputName'])+10)
        col1 = 'A' + tot_charg_row
        col2 = 'E' + tot_charg_row
        col3 = 'F' + tot_charg_row
        col4 = 'G' + tot_charg_row
        range1 = col1 + ':' + col2
        range2 = col3 + ':' + col4
        worksheet.merge_range(range1,"Agaciro k'inyongera musaruro zibura mu kagali",col3_format)
        
        #range for summation of missing cash
        
        sum_miss_range = 'H9'+ ':' + 'H'+ str(len(mydf['InputName'])+8)
        TotalMissing = '=SUM('+ sum_miss_range + ')'
        worksheet.merge_range(range2,TotalMissing,col3_format)
        
        #build ranges for total values of missing input minus buffer, title and values
        tot_charg_buffer_row = str(len(mydf['InputName'])+11)
        col5 = 'A' + tot_charg_buffer_row
        col6 = 'E' + tot_charg_buffer_row
        col7 = 'F' + tot_charg_buffer_row
        col8 = 'G' + tot_charg_buffer_row
        range3 = col5 + ':' + col6
        range4 = col7 + ':' + col8
        worksheet.merge_range(range3,"Agaciro k'inyongera musaruro uzishyura",col3_format)
        missing_buffer = TotalMissing +'- 10000'
        worksheet.merge_range(range4,missing_buffer,col3_format)
        
        #SIGNATURE SECTION
        #======================================================================
        sign_format = workbook.add_format({'text_wrap':True,
	                                       'font_size':12})
        sign_format.set_align('justify')
        
        #buld range for declaration column -jyewe...- and add its value
        dcl_row = str(len(mydf['InputName'])+14)
        dcl_col1 = 'A'+ dcl_row
        dcl_col2 = 'H'+ dcl_row
        dcl_range = dcl_col1 + ':' + dcl_col2
        num_dcl_row = int(dcl_row)-1
        worksheet.set_row(num_dcl_row,30)
        worksheet.merge_range(dcl_range, "Njyewe .................................................................... nemeyeko amafaranga avuzweho haruguru azakurwa ku umusharahara wange kugeze arangiye.",sign_format)
        
        #build range for where to write data - Italiki... - and add its value
        date_row = str(len(mydf['InputName'])+16)
        date_col1 = 'A'+ date_row
        date_col2 = 'E'+ date_row
        date_range = date_col1 + ':' + date_col2
        worksheet.merge_range(date_range, "Taliki: ……………………………………………………………………………",sign_format)
        
        #build range for where to actually sign - umukono..... - add its value
        sign_row = str(len(mydf['InputName'])+18)
        sign_col1 = 'A'+ sign_row
        sign_col2 = 'E'+ sign_row
        sign_range = sign_col1 + ':' + sign_col2
        worksheet.merge_range(sign_range,"Umukono w’umukozi: …………………………………………………………",sign_format)
        writer.save()
        del writer
#save the workbook

print ('Success!')



