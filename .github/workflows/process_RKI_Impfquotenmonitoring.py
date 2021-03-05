#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
from datetime import datetime
import pandas as pd
import numpy as np

DATAPATH     = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Impfquotenmonitoring' + os.sep + 'raw_data' + os.sep
PARSED_CSV   = '..' + os.sep + 'RKI_COVID19_Impfquotenmonitoring.csv'
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

isodate_pattern = re.compile(r"([\d]{4})-([\d]{2})-([\d]{2})")
        
# generate CSVs
for r, d, f in os.walk(DATAPATH, topdown=True):
    for file in f:
        filename = os.path.join(r, file)
        if filename.endswith('.xlsx'):
            csv_file = filename.replace('.xlsx', '.csv')
                        
            # if not os.path.isfile(csv_file):
            if True:
            
                pm_date = re.findall(isodate_pattern, csv_file)
                if (len(pm_date) < 1) or (len(pm_date[0]) < 3):
                    continue
                date = datetime(year=int(pm_date[0][0]), month=int(pm_date[0][1]), day=int(pm_date[0][2]))
                
                # check for different formats
                if date < datetime(year=2021, month=1, day=18):
                    
                    # 1st format
                    df = pd.read_excel(filename, sheet_name=1, nrows=17, engine='openpyxl')
                    
                    columns = list(df.columns)
                    for column in columns:
                        fixed_name = column.replace(' ', '').replace('*', '').replace('-', '')
                        df.rename(columns={column:fixed_name}, inplace=True)
                    
                    df = df.fillna(0)
                    df.to_csv(csv_file, sep=',', decimal='.', encoding='utf-8', float_format='%.0f', index=False)
                    
                else:
                    
                    #2nd format
                    
                    # read first sheet
                    df_a = pd.read_excel(filename, header=[0, 1, 2], sheet_name=1, nrows=17, engine='openpyxl')
                    df_a = df_a.fillna(0)
                    
                    major_col_vac = 'Erstimpfung'
                    major_col_vac_2nd = 'Zweitimpfung'
                    
                    idx_id = -1
                    idx_state = -1
                    idx_vac_sum = -1
                    idx_vac_inc = -1
                    idx_vac_biontec = -1
                    idx_vac_moderna = -1
                    idx_vac_rate = -1
                    idx_vac_2nd_sum = -1
                    idx_vac_2nd_inc = -1
                    
                    for i, column in enumerate(df_a.columns):
                        column_str = ''
                        for c in column:
                            column_str += c + ' '
                        
                        if 'RS ' in column_str:
                            idx_id = i
                        if 'Bundesland' in column_str:
                            idx_state = i
                        if major_col_vac in column_str and 'Gesamt' in column_str:
                            idx_vac_sum = i
                        if major_col_vac in column_str and 'Vortag' in column_str:
                            idx_vac_inc = i
                        if major_col_vac in column_str and 'BioNTech' in column_str:
                            idx_vac_biontec = i
                        if major_col_vac in column_str and 'Moderna' in column_str:
                            idx_vac_moderna = i
                        if major_col_vac in column_str and 'quote' in column_str:
                            idx_vac_rate = i
                        if major_col_vac_2nd in column_str and 'kumulativ' in column_str and idx_vac_2nd_sum == -1:
                            idx_vac_2nd_sum = i
                        if major_col_vac_2nd in column_str and 'Vortag' in column_str and idx_vac_2nd_inc == -1:
                            idx_vac_2nd_inc = i

                    # read 2nd sheet
                    df_b = pd.read_excel(filename, header=[0, 1], sheet_name=2, nrows=17, engine='openpyxl')
                    df_b = df_b.fillna(0)
                    
                    idx_vac_by_age = -1
                    idx_vac_by_job = -1
                    idx_vac_by_med = -1
                    idx_vac_by_ret = -1
                    
                    for i, column in enumerate(df_b.columns):
                        column_str = ''
                        for c in column:
                            column_str += '{} '.format(c)
                            
                        if major_col_vac in column_str and 'Alter' in column_str:
                            idx_vac_by_age = i
                        if major_col_vac in column_str and 'Beruf' in column_str:
                            idx_vac_by_job = i
                        if major_col_vac in column_str and 'Medizin' in column_str:
                            idx_vac_by_med = i
                        if major_col_vac in column_str and 'Pflege' in column_str:
                            idx_vac_by_ret = i
                    
                    # merge the sheets
                    dtypes = np.dtype([
                        ('RS', int),
                        ('Bundesland', str),
                        ('Impfungenkumulativ', int),
                        ('DifferenzzumVortag', int),
                        ('Impfungenpro1.000Einwohner', float),
                        ('IndikationnachAlter', int),
                        ('BeruflicheIndikation', int),
                        ('MedizinischeIndikation', int),
                        ('PflegeheimbewohnerIn', int),
                        ('ImpfungenkumulativBiontec', int),
                        ('ImpfungenkumulativModerna', int),
                        ('ZweiteImpfungkumulativ', int),
                        ('ZweiteImpfungDifferenzzumVortag', int)
                    ])
                    
                    df = pd.DataFrame( np.empty(0, dtype=dtypes) )
                                        
                    for i, row in df_a.iterrows():                        
                        row2 = df_b.iloc[i]      
                        
                        # skip other lines
                        if 'Bund' in str(row2['Bundesland']):
                            continue
                        
                        data_row = {
                                'RS':                              int(row[idx_id])          if idx_id >= 0 else 0,
                                'Bundesland':                      row[idx_state]            if idx_state >= 0 else 0,
                                'Impfungenkumulativ':              int(row[idx_vac_sum])     if idx_vac_sum >= 0 else 0,
                                'DifferenzzumVortag':              int(row[idx_vac_inc])     if idx_vac_inc >= 0 else 0,
                                'Impfungenpro1.000Einwohner':      float(row[idx_vac_rate])*10.0 if idx_vac_rate >= 0 else 0,
                                'IndikationnachAlter':             int(row2[idx_vac_by_age]) if idx_vac_by_age >= 0 else 0,
                                'BeruflicheIndikation':            int(row2[idx_vac_by_job]) if idx_vac_by_job >= 0 else 0,
                                'MedizinischeIndikation':          int(row2[idx_vac_by_med]) if idx_vac_by_med >= 0 else 0,
                                'PflegeheimbewohnerIn':            int(row2[idx_vac_by_ret]) if idx_vac_by_ret >= 0 else 0,
                                'ImpfungenkumulativBiontec':       int(row[idx_vac_biontec]) if idx_vac_biontec >= 0 else 0,
                                'ImpfungenkumulativModerna':       int(row[idx_vac_moderna]) if idx_vac_moderna >= 0 else 0,
                                'ZweiteImpfungkumulativ':          int(row[idx_vac_2nd_sum]) if idx_vac_2nd_sum >= 0 else 0,
                                'ZweiteImpfungDifferenzzumVortag': int(row[idx_vac_2nd_inc]) if idx_vac_2nd_inc >= 0 else 0
                        }                        
                        df = df.append(data_row, ignore_index=True)
                        
                        
                    df = df.fillna(0)                    
                    df.to_csv(csv_file, sep=',', decimal='.', encoding='utf-8', float_format='%.3f', index=False)
        
# merge CSVs
                
columns = [ 
        'timestamp', 'ISODate', 'IdBundesland', 'Bundesland', 
        'Impfungenkumulativ', 'DifferenzzumVortag', 'IndikationnachAlter', 'BeruflicheIndikation', 'MedizinischeIndikation', 'PflegeheimbewohnerIn',
        'ZweiteImpfungkumulativ', 'ZweiteImpfungDifferenzzumVortag'
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
                            'Impfungenkumulativ': row['Impfungenkumulativ'] if 'Impfungenkumulativ' in row else 0,
                            'DifferenzzumVortag': row['DifferenzzumVortag'] if 'DifferenzzumVortag' in row else 0,
                            'IndikationnachAlter': row['IndikationnachAlter'] if 'IndikationnachAlter' in row else 0,
                            'BeruflicheIndikation': row['BeruflicheIndikation'] if 'BeruflicheIndikation' in row else 0,
                            'MedizinischeIndikation': row['MedizinischeIndikation'] if 'MedizinischeIndikation' in row else 0,
                            'PflegeheimbewohnerIn': row['PflegeheimbewohnerIn'] if 'PflegeheimbewohnerIn' in row else 0,
                            'ZweiteImpfungkumulativ': row['ZweiteImpfungkumulativ'] if 'ZweiteImpfungkumulativ' in row else 0,
                            'ZweiteImpfungDifferenzzumVortag': row['ZweiteImpfungDifferenzzumVortag'] if 'ZweiteImpfungDifferenzzumVortag' in row else 0
                    }
                                        
                    df_export = df_export.append(row_data, ignore_index=True)
                    
# fill n/a data
df_export = df_export.fillna(0);

# sort by timestamp and state
df_export.sort_values(by=['timestamp', 'IdBundesland'], ascending=True, axis=0, inplace=True)

# export parsed CSV
df_export.to_csv(DATAPATH + PARSED_CSV, sep=',', decimal=".", encoding='utf-8', float_format='%.0f', index=False)
