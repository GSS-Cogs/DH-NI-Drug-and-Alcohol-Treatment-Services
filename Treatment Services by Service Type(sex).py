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
    tab = loadxlstabs(inputFile, sheetids='Table 2')[0]

observations = tab.excel_ref('B6').expand(DOWN).expand(RIGHT).is_not_blank() - tab.excel_ref('B12').expand(DOWN).expand(RIGHT)  


observations

Service = tab.excel_ref('A5').expand(DOWN).is_not_blank()
Service

Treatment = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
Treatment

sex = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
sex

Dimensions = [
            HDim(Treatment,'Treatment Type',DIRECTLY,ABOVE),
            HDim(Service,'Service Type',DIRECTLY,LEFT),
            HDim(sex,'Sex',CLOSEST,LEFT),
            HDimConst('Measure Type', 'Count'),
            HDimConst('Unit','People'),
            HDimConst('Period','1 March 2017'),
            HDimConst('Age','All')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
# savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table.dtypes

new_table.tail(5)

new_table.count()

new_table = new_table[new_table['Value'] !=  0 ]

new_table.count()

new_table['Treatment Type'].fillna('All', inplace = True)
#new_table['Service Type'] = 'All'
new_table['Residential Status'] = 'All'
new_table['Health and Social Care Trust']  = 'All'
new_table['Service Type'].unique()

new_table = new_table[['Period', 'Sex', 'Age', 'Service Type', 'Residential Status', 'Treatment Type', 'Health and Social Care Trust', 'Measure Type', 'Unit', 'Value']]

new_table

new_table.tail()

new_table.to_csv('testCompare.csv', index = False)


