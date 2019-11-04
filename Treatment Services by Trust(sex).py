# -*- coding: utf-8 -*-
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

# Census of Drug and Alcohol Treatment Services in Northern Ireland:Table 4 – Breakdown by Trust

from gssutils import *
scraper = Scraper('https://www.health-ni.gov.uk/publications/census-drug-and-alcohol-treatment-services-northern-ireland-2017')
scraper

tab = next(t for t in scraper.distributions[1].as_databaker() if t.name == 'Table 4')

observations = tab.excel_ref('B6').expand(DOWN).expand(RIGHT).is_not_blank() - tab.excel_ref('B20').expand(DOWN).expand(RIGHT)  


observations = observations - tab.filter(contains_string('18')).expand(DOWN).is_number()

Service = tab.excel_ref('A5').expand(DOWN).is_not_blank()

Treatment = tab.excel_ref('B4').expand(RIGHT).is_not_blank()

sex = tab.excel_ref('B3').expand(RIGHT).is_not_blank()

Dimensions = [
            HDim(Treatment,'Treatment Type',DIRECTLY,ABOVE),
            HDim(Service,'Health and Social Care Trust',DIRECTLY,LEFT),
            HDim(sex,'Sex',CLOSEST,LEFT),
            HDimConst('Measure Type', 'Count'),
            HDimConst('Unit','People'),
            HDimConst('Period','1 March 2017'),
            HDimConst('Age','All')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table = new_table[new_table['Value'] !=  0 ]

new_table['Treatment Type'].fillna('Total', inplace = True)

new_table.drop(new_table[new_table['Health and Social Care Trust'].isin(['Prison', 'Prison (%)'])].index, inplace = True)

new_table['Service Type'] = 'All'
new_table['Residential Status'] = 'All'
# new_table['Health and Social Care Trust']  = 'All'

new_table = new_table[['Period', 'Sex', 'Age', 'Service Type', 'Residential Status', 'Treatment Type', 'Health and Social Care Trust', 'Measure Type', 'Unit', 'Value']]

new_table['Treatment Type'].unique()


