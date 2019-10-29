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

# Census of Drug and Alcohol Treatment Services in Northern Ireland

from gssutils import *
scraper = Scraper('https://www.health-ni.gov.uk/publications/census-drug-and-alcohol-treatment-services-northern-ireland-2017')
scraper

tabs = {tab.name: tab for tab in scraper.distribution(
    title='Data from Census of Drug and Alcohol Treatment Services').as_databaker()}
tabs.keys()
tabs

tables = []
for tab_name, script in [
    ('Table 1', 'Treatment Services by Age and Gender.ipynb'),
    ('Table 2', 'Treatment Services by Service Type(Age).py'),
    ('Table 2', 'Treatment Services by Service Type(sex).py'),
    ('Table 3', 'Treatment Services by Residential status(Age).py'),
    ('Table 3', 'Treatment Services by Residential Status(sex).py'),
    ('Table 4', 'Treatment Services by Trust(Age).py'),
    ('Table 4', 'Treatment Services by Trust(sex).py'),
    ('Table 5', 'Treatment Services by Comparison table.py')
]:
    tab = tabs[tab_name]
    %run "$script"
    tables.append(new_table)

tidy = pd.concat(tables)
#tidy.to_csv('testCompare.csv', index = False)

tidy['Treatment Type'].fillna('Total', inplace = True)

# +
#tidy = tidy[tidy['Treatment Type'] == 'Alcohol Only']

# +
#tidy['Sex'].unique()
#tidy.to_csv('testCompare.csv', index = False)
# -

tidy.drop(tidy[tidy.Sex.isin(['% of Total', '% of all Males ','% of all Females'])].index, inplace = True)

from datetime import datetime

tidy.Period = pd.to_datetime(tidy.Period).dt.strftime('%Y-%m-%d')

tidy['Period'] = str('day/') + tidy['Period']

# +
#tidy['Age'].unique()
#tidy.to_csv('testCompare.csv', index = False)
# -

tidy['Age'] = tidy['Age'].map(
    lambda x: {
        'Under 18 ' : 'under-18', 
        '18 and over' : '18-plus',
        'All years': 'all' ,
        'All': 'all',
        'All Ages': 'all'
        }.get(x, x))


# +
#tidy['Treatment Type'] = 'alcohol'
#tidy.to_csv('testCompare.csv', index = False)

# +
def user_perc(x,y):
    
    if ( (str(x) == 'Statutory (%)')) | ((str(x) == 'Non-statutory (%)')) | ((str(x) == 'Prison (%)')): 
        
        return 'Percentage'
    else:
        return y
    
tidy['Measure Type'] = tidy.apply(lambda row: user_perc(row['Service Type'], row['Measure Type']), axis = 1)



# +
def user_perc(x,y):
    
    if ( (str(x) == 'Residential (%)')) | ((str(x) == 'Non-residential (%)')) | ((str(x) == 'Mixed (%)')): 
        
        return 'Percentage'
    else:
        return y
    
tidy['Measure Type'] = tidy.apply(lambda row: user_perc(row['Residential Status'], row['Measure Type']), axis = 1)



# +
#tidy['Health and Social Care Trust'].unique()

# +
def user_perc(x,y):
    
    if ( (str(x) == 'Belfast (%)')) | ((str(x) == 'Northern (%)')) | ((str(x) == 'South Eastern (%)')) | ((str(x) == 'Southern (%)')) | ((str(x) == 'Western (%)')) | ((str(x) == 'Emergency admissions (HIS) (%)')) : 
        
            return 'Percentage'
    else:
            return y
    
tidy['Measure Type'] = tidy.apply(lambda row: user_perc(row['Health and Social Care Trust'], row['Measure Type']), axis = 1)


# +
def user_perc(x,y):
    
    if  ((str(x) == 'Emergency admissions (HIS)  (%)')) : 
        
            return 'Percentage'
    else:
            return y
    
tidy['Measure Type'] = tidy.apply(lambda row: user_perc(row['Health and Social Care Trust'], row['Measure Type']), axis = 1)
# -

tidy['Health and Social Care Trust'] = tidy['Health and Social Care Trust'].str.rstrip(' (%)')

tidy['Health and Social Care Trust'] = tidy['Health and Social Care Trust'].str.lower()

# +
#tidy['Health and Social Care Trust'].unique()
# -

tidy['Health and Social Care Trust'] = tidy['Health and Social Care Trust'].map(
    lambda x: {
        'south eastern' : 'south-eastern', 
        'emergency admissions (his)' : 'emergency-admissions',
        'emergency admissions (his' : 'emergency-admissions'
        }.get(x, x))

tidy['Measure Type'] = tidy['Measure Type'].map(
    lambda x: {
        'Headcount' : 'Count', 
        'Percentage of Headcount' : 'Percentage',
        }.get(x, x))


# +
#tidy['Sex'].unique()

# +
def user_perc(x,y):
    
    if ( (str(x) == 'Male (%)')) | ((str(x) == 'Female (%)')): 
        
        return 'Percentage'
    else:
        return y
    
tidy['Measure Type'] = tidy.apply(lambda row: user_perc(row['Sex'], row['Measure Type']), axis = 1)


# -

tidy['Sex'] = tidy['Sex'].map(
    lambda x: {
        'Female' : 'F', 
        'Male' : 'M',
        'Persons' : 'T',
        'Female  ' : 'F',
        'Male (%)' : 'M',
        'Female (%)': 'F'
        }.get(x, x))

tidy['Sex'] = tidy['Sex'].str.rstrip('(%)')

tidy['Service Type'].unique()

tidy['Service Type'] = tidy['Service Type'].map(
    lambda x: {
        'Total' : 'all',
        'total' : 'all'
        }.get(x, x))

tidy['Service Type'] = tidy['Service Type'].str.rstrip(' (%)')

tidy['Service Type'] = tidy['Service Type'].str.lower()

tidy['Residential Status'] = tidy['Residential Status'].str.rstrip(' (%)')

tidy['Residential Status'] = tidy['Residential Status'].str.lower()

tidy['Health and Social Care Trust'] = tidy['Health and Social Care Trust'].map(
    lambda x: {
        'total' : 'all' 
        }.get(x, x))

tidy['Residential Status'] = tidy['Residential Status'].map(
    lambda x: {
        'total' : 'all' 
        }.get(x, x))

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
tidy.to_csv(out / 'observations.csv', index = False)
#tidy.to_csv('testCompare.csv', index = False)
#tidy['Treatment Type'].unique()

# +
# tidy[tidy['Measure Type'] != 'Percentage'].to_csv(out / 'observations-no-percentages.csv', index=False)
# -

# There's a metadata tab in the spreadsheet with abstract and contact details. **Todo: extract these and also figure out what the license should really be.**

md_tab = tabs['Metadata']
md_heading = md_tab.filter('Metadata')
md_heading.assert_one()
properties = md_heading.fill(DOWN).is_not_whitespace()
values = properties.fill(RIGHT).is_not_whitespace()
headings = properties - values.fill(LEFT)
properties = properties - headings
cs = ConversionSegment(values, [
    HDim(properties, "Property", DIRECTLY, LEFT),
    HDim(headings, "Heading", CLOSEST, UP)
], includecellxy=True)
#savepreviewhtml(cs)

# +
from gssutils.metadata import THEME

for i, row in cs.topandas().iterrows():
    v = md_tab.get_at(row.__x, row.__y).value.strip()
    if row.Property == 'Abstract':
        scraper.dataset.description = v
    elif row.Property == 'National Statistics Theme':
        scraper.dataset.theme = THEME[pathify(v)]
    elif row.Property == 'Keyword':
        scraper.dataset.keyword = map(lambda x: x.strip(), v.split(' '))
    elif row.Property == 'Email Address':
        scraper.dataset.contactEmail = f'mailto:{v}'

# +
scraper.dataset.family = 'health'
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
schema = CSVWMetadata('https://gss-cogs.github.io/ref_alcohol/')
schema.create(out / 'observations.csv', out / 'observations.csv-schema.json')

# +
# tidy.to_csv('testCompare.csv', index = False)
