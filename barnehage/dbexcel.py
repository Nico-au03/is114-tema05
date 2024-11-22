# dbexcel module
import pandas as pd

kgdata = pd.ExcelFile('/users/filip/desktop/is114-tema05/barnehage/kgdata.xlsx', engine='openpyxl')
barnehage = pd.read_excel(kgdata, 'barnehage', index_col=0)
forelder = pd.read_excel(kgdata, 'foresatt', index_col=0)
barn = pd.read_excel(kgdata, 'barn', index_col=0)
soknad = pd.read_excel(kgdata, 'soknad', index_col=0)


"""
Referanser
[] https://www.geeksforgeeks.org/list-methods-python/
"""

print(barnehage.head())
print(forelder.head())
print(barn.head())
print(soknad.head())