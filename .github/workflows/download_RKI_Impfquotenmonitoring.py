#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re, sys
from datetime import datetime
import pandas as pd

VERBOSE      = True
DATAPATH     = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Impfquotenmonitoring' + os.sep
DATE_STR     = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d')
FILENAME     = 'RKI_COVID19_Impfquotenmonitoring_{}.xlsx'.format(DATE_STR)
PARSED_CSV   = 'RKI_COVID19_Impfquotenmonitoring.csv'
FULLNAME     = DATAPATH + FILENAME
CSV_URL      = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile"
ONE_DAY_IN_S = 86400

states = {
    "Gesamt": 0,
    "Schleswig-Holstein": 1,
    "Hamburg": 2,
    "Niedersachsen": 3,
    "Bremen": 4,
    "Nordrhein-Westfalen": 5,
    "Hessen": 6,
    "Rheinland-Pfalz": 7,
    "Baden-Württemberg": 8,
    "Bayern": 9,
    "Saarland": 10,
    "Berlin": 11,
    "Brandenburg": 12,
    "Mecklenburg-Vorpommern": 13,
    "Sachsen": 14,
    "Sachsen-Anhalt": 15,
    "Thüringen": 16
}

# download latest data
if os.path.isfile(FULLNAME):

    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME))
            
else:
    
    if VERBOSE:
        print("The file '{}' does not exist.".format(FILENAME))
        
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    r = requests.get(CSV_URL, headers=headers, allow_redirects=True, timeout=5.0)
    if r.status_code != 200:
        print("Download failed!")
    
    else:
        
        with open(FULLNAME, 'wb') as df:
            df.write(r.content)
            df.close()  
        
        
# generate CSVs
for r, d, f in os.walk(DATAPATH, topdown=True):
    for file in f:
        filename = os.path.join(r, file)
        if filename.endswith('.xlsx'):
            csv_file = filename.replace('.xlsx', '.csv')
            
            if not os.path.isfile(csv_file):
            
                df = pd.read_excel(filename, sheet_name=1, nrows=17)
                
                columns = list(df.columns)
                for column in columns:
                    fixed_name = column.replace(' ', '').replace('*', '').replace('-', '')
                    df.rename(columns={column:fixed_name}, inplace=True)
                
                df = df.fillna(0)
                
                df.to_csv(csv_file, sep=',', decimal='.', encoding='utf-8', float_format='%.0f', index=False)

# merge CSVs
                
columns = [ 
        "timestamp", "ISODate", "IdBundesland", "Bundesland", 
        "Impfungenkumulativ", "DifferenzzumVortag", "IndikationnachAlter", "BeruflicheIndikation", "MedizinischeIndikation", "PflegeheimbewohnerIn" 
]

df_export = pd.DataFrame(columns=columns)

csv_pattern = re.compile(r"RKI_COVID19_Impfquotenmonitoring_([\d]{4})-([\d]{2})-([\d]{2}).csv")
for r, d, f in os.walk(DATAPATH, topdown=True):
    for file in f:
        filename = os.path.join(r, file)
        pm = re.match(csv_pattern, file)
        if pm and len(pm.groups()) == 3:
            
            timestamp = int(datetime(year=int(pm.group(1)), month=int(pm.group(2)), day=int(pm.group(3))).timestamp()/ONE_DAY_IN_S)*ONE_DAY_IN_S
            isodate   = '{}-{}-{}'.format(pm.group(1), pm.group(2), pm.group(3))
            
            df = pd.read_csv(filename, sep=',', decimal='.', encoding='utf-8')
            for i, row in df.iterrows():
                
                state_name = row['Bundesland'].replace('*', '').replace(' ', '')
                
                if state_name in states:
                    idBundesland = states[state_name]
                    
                    row_data = { 
                            'timestamp': timestamp, 
                            'ISODate': isodate, 
                            'IdBundesland': idBundesland, 
                            'Bundesland': state_name,
                            'Impfungenkumulativ': row['Impfungenkumulativ'] if row['Impfungenkumulativ'] is not None else 0,
                            'DifferenzzumVortag': row['DifferenzzumVortag'] if row['DifferenzzumVortag'] is not None else 0,
                            'IndikationnachAlter': row['IndikationnachAlter'] if row['IndikationnachAlter'] is not None else 0,
                            'BeruflicheIndikation': row['BeruflicheIndikation'] if row['BeruflicheIndikation'] is not None else 0,
                            'MedizinischeIndikation': row['MedizinischeIndikation'] if row['MedizinischeIndikation'] is not None else 0,
                            'PflegeheimbewohnerIn': row['PflegeheimbewohnerIn'] if row['PflegeheimbewohnerIn'] is not None else 0
                    }
                                        
                    df_export = df_export.append(row_data, ignore_index=True)
                    
# fill n/a data
df_export = df_export.fillna(0);

# sort by timestamp and state
df_export.sort_values(by=['timestamp', 'IdBundesland'], ascending=True, axis=0, inplace=True)

# export parsed CSV
df_export.to_csv(DATAPATH + PARSED_CSV, sep=',', decimal=".", encoding='utf-8', float_format='%.0f', index=False)
