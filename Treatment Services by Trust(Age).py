# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Census of Drug and Alcohol Treatment Services in Northern Ireland:Breakdown by Service Type

from gssutils import *
if is_interactive():
    import requests
    from cachecontrol import CacheControl
    from cachecontrol.caches.file_cache import FileCache
    from cachecontrol.heuristics import LastModified
    from pathlib import Path

    session = CacheControl(requests.Session(),
                           cache=FileCache('.cache'),
                           heuristic=LastModified())

    sourceFolder = Path('in')
    sourceFolder.mkdir(exist_ok=True)

    inputURL = 'https://www.health-ni.gov.uk/sites/default/files/publications/dhssps/data-census-drug-alcohol-treatment-services.xlsx'
    inputFile = sourceFolder / 'data-census-drug-alcohol-treatment-services.xlsx'
    response = session.get(inputURL)
    with open(inputFile, 'wb') as f:
      f.write(response.content)
    tab = loadxlstabs(inputFile, sheetids='Table 4')[0]

observations = tab.excel_ref('B24').expand(DOWN).expand(RIGHT).is_not_blank() - tab.excel_ref('B38').expand(DOWN).expand(RIGHT)  


observations

Service = tab.excel_ref('A23').expand(DOWN).is_not_blank()
Service

Treatment = tab.excel_ref('B22').expand(RIGHT)
Treatment

age = tab.excel_ref('B21').expand(RIGHT).is_not_blank()
age

Dimensions = [
            HDim(Treatment,'Treatment Type',DIRECTLY,ABOVE),
            HDim(Service,'Health and Social Care Trust',DIRECTLY,LEFT),
            HDim(age,'Age',CLOSEST,LEFT),
            HDimConst('Measure Type', 'Count'),
            HDimConst('Unit','People'),
            HDimConst('Period','1 March 2017'),
            HDimConst('Sex','Persons')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
# savepreviewhtml(c1)

new_table = c1.topandas()
new_table.loc[new_table['Age'] == 'Treatment Type', 'Age'] = 'All Ages'
new_table.loc[new_table['Age'] == 'Overall Total', 'Age'] = 'All Ages'
new_table.loc[new_table['Treatment Type'] == '', 'Treatment Type'] = 'Total'
new_table

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table = new_table[new_table['Value'] !=  0 ]

new_table = new_table[new_table['Value'] !=  '' ]

new_table.dtypes

new_table.tail(5)

new_table.count()

new_table = new_table[new_table['Value'] !=  '-' ]

new_table.count()


# +
def user_perc(x):
    
    if str(x) == 'Treatment Type':
        return 'All years'
    else:
        return x
    
new_table['Age'] = new_table.apply(lambda row: user_perc(row['Age']), axis = 1)
# -

new_table['Treatment Type'].fillna('Total', inplace = True)

new_table.drop(new_table[new_table['Health and Social Care Trust'].isin(['Prison', 'Prison (%)'])].index, inplace = True)

new_table['Service Type'] = 'All'
new_table['Residential Status'] = 'All'
# new_table['Health and Social Care Trust']  = 'All'

new_table = new_table[['Period', 'Sex', 'Age', 'Service Type', 'Residential Status', 'Treatment Type', 'Health and Social Care Trust', 'Measure Type', 'Unit', 'Value']]

new_table.head(5)

new_table.count()


