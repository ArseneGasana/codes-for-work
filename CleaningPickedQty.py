import os
import pandas as pd
data = pd.read_excel(r'C:\Users\user\Desktop\Picked qty\Shingiro.xlsx',names=["District", "Sector", "Title", "Lot number","Bags","Kgs/ bag","Total picked","Total lost"])
dir = r'C:\Users\user\Desktop\Picked qty'

splitInputs = data.Title.str.split(" ",n=5,expand=True)
data['ProdName']= splitInputs[3]
dataFilled = data.fillna(method='ffill')

row1Index = dataFilled[dataFilled['Lot number']=='Lot number'].index
row2Index = dataFilled[dataFilled['Title'].str.contains('LOTS NUMBER')].index
RemoveRow1 = dataFilled.drop(row1Index)
RawDf = RemoveRow1.drop(row2Index).drop(['Title'], axis=1)

SplitTotalPicked = RawDf['Total picked'].str.split(" ", n=3, expand=True)
RawDf['Total qty picked']= SplitTotalPicked[0]
CleanDf = RawDf.drop(['Lot number', 'Bags', 'Kgs/ bag','Total picked', 'Total lost'], axis=1)
CleanDf['Total qty picked'] = CleanDf['Total qty picked'].replace(",","", regex=True).astype(int)
FinalDf = CleanDf.groupby(['District','Sector','ProdName'])['Total qty picked'].sum().reset_index()

DistricName = FinalDf['District'][0]
SectorName = FinalDf['Sector'][0]
SaveName = DistricName + SectorName +'.xlsx'

os.chdir(dir)
FinalDf.to_excel(SaveName, index=False)

print ('OPERATION SUCCESSFUL')