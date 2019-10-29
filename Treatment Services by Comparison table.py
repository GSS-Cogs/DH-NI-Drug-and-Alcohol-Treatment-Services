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

# Census of Drug and Alcohol Treatment Type Services in Northern Ireland:Table 5 Comparison table

from gssutils import *
import numpy
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
    inputFile = sourceFolder / 'data-census-drug-alcohol-Treatment Type-services.xlsx'
    response = session.get(inputURL)
    with open(inputFile, 'wb') as f:
      f.write(response.content)
    tab = loadxlstabs(inputFile, sheetids='Table 5')[0]

observations = tab.excel_ref('B6').expand(DOWN).expand(RIGHT).is_not_blank() - tab.excel_ref('J8').expand(DOWN).expand(RIGHT)  


Service = tab.excel_ref('A').expand(DOWN).by_index([6,7,10,13,17,21,24])

TreatmentType = tab.excel_ref('A').expand(DOWN).is_not_blank() - tab.excel_ref('A').expand(DOWN).by_index([6,7,10,13,17,21,24])


month = tab.excel_ref('B3').expand(RIGHT).is_not_blank()


year = tab.excel_ref('B4').expand(RIGHT).is_not_blank()


mt = tab.excel_ref('B5').expand(RIGHT).is_not_blank()


Dimensions = [
            HDim(TreatmentType,'Treatment Type',CLOSEST,ABOVE),
            HDim(Service,'Category',CLOSEST,ABOVE),
            HDim(month,'month',CLOSEST,LEFT),
            HDim(year,'Year',CLOSEST,LEFT),
            HDim(mt,'Measure Type',DIRECTLY,ABOVE),
            HDimConst('Unit','People'),
            HDimConst('Age','All'),
            HDimConst('Sex','Persons')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table['Year'] = pd.to_numeric(new_table['Year'], errors='coerce').fillna(0)

new_table['Year'] = new_table['Year'].astype(int)

new_table['Year'] = new_table['Year'].astype(str)

new_table['Period'] = new_table['month'] + new_table['Year']

new_table['Measure Type'] = new_table['Measure Type'].map(
    lambda x: {
        '%' : 'Percentage of Headcount'
        }.get(x, x))


new_table = new_table[new_table['Value'] !=  0 ]

new_table['Treatment Type'].unique()
new_table['Treatment Type'] = new_table['Treatment Type'].str.strip() #Get rid of extra spce at end of Under 18

new_table['Treatment Type'].fillna('All', inplace = True)

# +
new_table['Service Type'] = 'All'
new_table['Residential Status'] = 'All'
new_table['Health and Social Care Trust']  = 'All'

# All Categories are in the Treatment Type column at the moment when they need to be put into the relevant columns
# Put the Age categories into the Age column
new_table['Age'] = numpy.where(new_table['Category'] == 'Age', new_table['Treatment Type'], 'All')

# Put the Gender categories into the Sex column and then change to M/F/T as defined in the schema file
new_table['Sex'] = numpy.where(new_table['Category'] == 'Gender', new_table['Treatment Type'], 'All')
#new_table['Sex'] = numpy.where(new_table['Sex'] == 'Male', 'M', new_table['Sex'])
#new_table['Sex'] = numpy.where(new_table['Sex'] == 'Female', 'F', new_table['Sex'])
#new_table['Sex'] = numpy.where(new_table['Sex'] == 'all', 'T', new_table['Sex'])

# Put the Service type categories into the Service Type column (Lower t for the value, upper T for the Colum name)
new_table['Service Type'] = numpy.where(new_table['Category'] == 'Service type', new_table['Treatment Type'], 'All')

# Put the Residential Status into the Residential Status column
new_table['Residential Status'] = numpy.where(new_table['Category'] == 'Residential Status', new_table['Treatment Type'], 'All')

# Put the Trust value into the Health and Social Care Trust column
new_table['Health and Social Care Trust'] = numpy.where(new_table['Category'] == 'Trust', new_table['Treatment Type'], 'All')

# Set all the values in the Treatment Type column that you have just copied over to All
new_table['Treatment Type'] = numpy.where(new_table['Category'] == 'Treatment type', new_table['Treatment Type'], 'Total')
new_table['Treatment Type'] = numpy.where(new_table['Treatment Type'] == 'All', 'Total', new_table['Treatment Type'])

# Merged cell (B25) over 5 rows for 1st March 2007, equals total for a few trusts rather than just one. Need to change Trust
new_table['Health and Social Care Trust'] = numpy.where((new_table['Category'] == 'Trust') & 
                (new_table['Period'] == '1st March 2007') &
                (new_table['Health and Social Care Trust'] == 'Belfast'), 
                'Belfast + Northern + South Eastern + Southern + Western', new_table['Health and Social Care Trust'])
# Output to folder for testing
#new_table.to_csv('testCompare.csv', index = False)
new_table
# -

new_table = new_table[['Period', 'Sex', 'Age', 'Service Type', 'Residential Status', 'Treatment Type', 'Health and Social Care Trust', 'Measure Type', 'Unit', 'Value']]
