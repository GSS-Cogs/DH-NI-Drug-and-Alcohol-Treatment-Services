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
scraper = Scraper('https://www.health-ni.gov.uk/publications/census-drug-and-alcohol-treatment-services-northern-ireland-2017')
scraper

tab = next(t for t in scraper.distributions[1].as_databaker() if t.name == 'Table 4')

observations = tab.excel_ref('B24').expand(DOWN).expand(RIGHT).is_not_blank() - tab.excel_ref('B38').expand(DOWN).expand(RIGHT)  


Service = tab.excel_ref('A23').expand(DOWN).is_not_blank()

Treatment = tab.excel_ref('B22').expand(RIGHT)

age = tab.excel_ref('B21').expand(RIGHT).is_not_blank()

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

new_table = new_table[new_table['Value'] !=  '-' ]


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


