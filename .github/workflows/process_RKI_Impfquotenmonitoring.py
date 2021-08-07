#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
from datetime import datetime
import pandas as pd
import numpy as np

DATAPATH     = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Impfquotenmonitoring' + os.sep + 'raw_data' + os.sep
PARSED_CSV   = '..' + os.sep + 'RKI_COVID19_Impfquotenmonitoring.csv'
THURINGIA_CSV= '..' + os.sep + 'RKI_COVID19_Impfquotenmonitoring_Thuringia.csv'
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
                    
RKI_population = {
        8: 11100394, 
        9: 13124737, 
        11: 3669491, 
        12: 2521893, 
        4:   681202, 
        2:  1847253, 
        6:  6288080, 
        13: 1608138, 
        3:  7993608, 
        5: 17947221, 
        7:  4093903, 
        10:  986887, 
        14: 4071971, 
        15: 2194782, 
        1:  2903773, 
        16: 2133378,
        0: 83166711
}

# Thuringia
pop_TH_all     = 2133378 / 100
pop_TH_A00_A17 =  324465 / 100
pop_TH_A60p    =  730456 / 100
pop_TH_A18_A59 = pop_TH_all - pop_TH_A00_A17 - pop_TH_A60p
pop_TH_A00_A59 = pop_TH_all - pop_TH_A60p
pop_TH_A12_A17 =  104207 / 100

th_dtypes = np.dtype([
    ('Timestamp', int),
    ('RS', int),
    ('State', str),
    ('abs_1st_vac_A00-A17', int),
    ('abs_1st_vac_A18-A59', int),
    ('abs_1st_vac_A00-A59', int),
    ('abs_1st_vac_A60+', int),
    ('abs_2nd_vac_A00-A17', int),
    ('abs_2nd_vac_A18-A59', int),
    ('abs_2nd_vac_A00-A59', int),
    ('abs_2nd_vac_A60+', int)
])
df_th = pd.DataFrame( np.empty(0, dtype=th_dtypes) )

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
                ts = date.timestamp()
                
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
                    
                elif date < datetime(year=2021, month=4, day=8):
                    
                    # 2nd format
                    
                    # read first sheet
                    df_a = pd.read_excel(filename, header=[0, 1, 2], sheet_name=1, nrows=18, engine='openpyxl')
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
                    df_b = pd.read_excel(filename, header=[0, 1], sheet_name=2, nrows=18, engine='openpyxl')
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
                        
                        # skip empty lines
                        if str(row[idx_state]) == '0':
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
                    
                elif date < datetime(year=2021, month=6, day=7):
                    
                    # third format
                    
                    df_a = pd.read_excel(filename, header=[0, 1, 2, 3], sheet_name=2, nrows=18, engine='openpyxl')
                    df_a = df_a.fillna(0)
                    
                    idx_id = -1
                    idx_state = -1
                    idx_vac_sum = []
                    
                    idx_vac_sum_below_60 = []
                    idx_vac_sum_above_60 = []

                    idx_vac_BT_1st = []
                    idx_vac_MO_1st = []
                    idx_vac_AZ_1st = []
                    
                    idx_vac_1st = []
                    idx_vac_2nd = []
                    idx_vac_inc_1st = []
                    idx_vac_inc_2nd = []
                    
                    locations = ['Impfzentren', 'niedergelassen' ]
                    vacs = ['eine Impfung', 'begonnene Impfserie', 'vollständig geimpft']
                    types = ['Gesamt', 'Differenz', 'BioNTech', 'Moderna', 'AstraZeneca', 'Janssen']
                    
                    for i, column in enumerate(df_a.columns):
                        column_str = ''
                        for c in column:
                            column_str += c + ' '
                            
                        column_str = column_str.replace('*', '')
                            
                        if 'RS ' in column_str:
                            idx_id = i
                        if 'Bundesland' in column_str:
                            idx_state = i
                            
                        for t in types:
                            if t in column_str:
                                if t == types[0]:
                                    idx_vac_sum.append(i)
                                    if (vacs[0] in column_str) or (vacs[1] in column_str):
                                        idx_vac_1st.append(i)
                                    elif vacs[2] in column_str:
                                        idx_vac_2nd.append(i)
                                elif t == types[1]:
                                    if (vacs[0] in column_str) or (vacs[1] in column_str):
                                        idx_vac_inc_1st.append(i)
                                    elif vacs[2] in column_str:
                                        idx_vac_inc_2nd.append(i)
                                elif t == types[2]:
                                    if (vacs[0] in column_str) or (vacs[1] in column_str):
                                        idx_vac_BT_1st.append(i)
                                elif t == types[3]:
                                    if (vacs[0] in column_str) or (vacs[1] in column_str):
                                        idx_vac_MO_1st.append(i)
                                elif t == types[4]:
                                    if (vacs[0] in column_str) or (vacs[1] in column_str):
                                        idx_vac_AZ_1st.append(i)
                    
                    ############
                    # Thuringia
                    ############
                    if date >= datetime(year=2021, month=4, day=20):
                        df_c = pd.read_excel(filename, header=[3], sheet_name=1, nrows=18, engine='openpyxl')
                        df_c = df_c.fillna(0)
                        col = df_c.columns
                    
                        idx_bl = 15 # Thuringia
                    
                        vac_first_below_60_a = '<60 Jahre.2'
                        vac_first_above_60_a = '60+ Jahre.2'
                        vac_second_below_60_a = '<60 Jahre.3'
                        vac_second_above_60_a = '60+Jahre'
                        
                        vac_first_below_60_b = '<60 Jahre.4'
                        vac_first_above_60_b = '60+ Jahre.3'
                        vac_second_below_60_b = '<60 Jahre.5'
                        vac_second_above_60_b = '60+Jahre.1'
                        
                        vac_first_below_60 = df_c.iloc[idx_bl][vac_first_below_60_a] + df_c.iloc[idx_bl][vac_first_below_60_b]
                        vac_first_above_60 = df_c.iloc[idx_bl][vac_first_above_60_a] + df_c.iloc[idx_bl][vac_first_above_60_b]
                        vac_second_below_60 = df_c.iloc[idx_bl][vac_second_below_60_a] + df_c.iloc[idx_bl][vac_second_below_60_b]
                        vac_second_above_60 = df_c.iloc[idx_bl][vac_second_above_60_a] + df_c.iloc[idx_bl][vac_second_above_60_b]
                    
                        data_row = {
                            'Timestamp'          : int(ts),
                            'RS'                 : df_c.iloc[idx_bl][col[0]],
                            'State'              : df_c.iloc[idx_bl][col[1]].replace("*", ""),
                            'abs_1st_vac_A00-A17': -1,
                            'abs_1st_vac_A18-A59': -1,
                            'abs_1st_vac_A00-A59': int(vac_first_below_60),
                            'abs_1st_vac_A60+'   : int(vac_first_above_60),
                            'abs_2nd_vac_A00-A17': -1,
                            'abs_2nd_vac_A18-A59': -1,
                            'abs_2nd_vac_A00-A59': int(vac_second_below_60),
                            'abs_2nd_vac_A60+'    : int(vac_second_above_60)
                        }                        
                        df_th = df_th.append(data_row, ignore_index=True)
                                        
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
                        
                        # skip empty lines
                        if str(row[idx_state]) == '0':
                            continue
                        
                        # skip other lines
                        if 'Bund' in row[idx_state]:
                            continue
                        
                        data_row = {
                                'RS':                              int(row[idx_id])                if idx_id >= 0 else 0,
                                'Bundesland':                      row[idx_state].replace('*', '') if idx_state >= 0 else 0,
                        }
                        
                        data_row['Impfungenkumulativ'] = 0
                        for c in idx_vac_1st:
                            data_row['Impfungenkumulativ'] += int(row[c])
                            
                        data_row['Impfungenpro1.000Einwohner'] = data_row['Impfungenkumulativ'] / RKI_population[row[idx_id]] * 1000.0
                        
                        data_row['ZweiteImpfungkumulativ'] = 0
                        for c in idx_vac_2nd:
                            data_row['ZweiteImpfungkumulativ'] += int(row[c])
                                                
                        data_row['DifferenzzumVortag'] = 0
                        for c in idx_vac_inc_1st:
                            data_row['DifferenzzumVortag'] += int(row[c])
                            
                        data_row['ZweiteImpfungDifferenzzumVortag'] = 0
                        for c in idx_vac_inc_2nd:
                            data_row['ZweiteImpfungDifferenzzumVortag'] += int(row[c])
                        
                        data_row['ImpfungenkumulativBiontec'] = 0
                        for c in idx_vac_BT_1st:
                            data_row['ImpfungenkumulativBiontec'] += int(row[c])
                            
                        data_row['ImpfungenkumulativModerna'] = 0
                        for c in idx_vac_MO_1st:
                            data_row['ImpfungenkumulativModerna'] += int(row[c])
                        
                        # removed data types
                        data_row['IndikationnachAlter'] = -1
                        data_row['BeruflicheIndikation'] = -1
                        data_row['MedizinischeIndikation'] = -1
                        data_row['PflegeheimbewohnerIn'] = -1
                        
                        df = df.append(data_row, ignore_index=True)
                        
                    df = df.fillna(0)                    
                    df.to_csv(csv_file, sep=',', decimal='.', encoding='utf-8', float_format='%.3f', index=False)
                    
                else:
                    
                    # fourth format                    
                    df_a = pd.read_excel(filename, header=[0, 1, 2], sheet_name=2, nrows=18, engine='openpyxl')
                    df_a = df_a.fillna(0)
                    
                    col = df_a.columns
                    
                    idx_id = col[0]
                    idx_state = col[1]
                    idx_vac_1st_sum = col[2]
                    idx_vac_1st_diff = col[7]
                    
                    idx_vac_2nd_sum = col[8]
                    idx_vac_2nd_diff = col[13]

                    idx_vac_BT_1st = col[3]
                    idx_vac_MO_1st = col[4]
                    idx_vac_AZ_1st = col[5]
                    idx_vac_JJ_1st = col[6]
                                     
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
                                                
                        # skip other lines
                        if 'Bund' in row[idx_state]:
                            continue
                        
                        data_row = {}
                        data_row['RS'] = int(row[idx_id])
                        data_row['Bundesland'] = row[idx_state].replace('*', '')
                        data_row['Impfungenkumulativ'] = int(row[idx_vac_1st_sum])
                        data_row['Impfungenpro1.000Einwohner'] = data_row['Impfungenkumulativ'] / RKI_population[row[idx_id]] * 1000.0
                        data_row['ZweiteImpfungkumulativ'] = int(row[idx_vac_2nd_sum])
                        data_row['DifferenzzumVortag'] = int(row[idx_vac_1st_diff])
                        data_row['ZweiteImpfungDifferenzzumVortag'] = int(row[idx_vac_2nd_diff])
                        
                        data_row['ImpfungenkumulativBiontec'] = int(row[idx_vac_BT_1st])
                        data_row['ImpfungenkumulativModerna'] = int(row[idx_vac_MO_1st])
                        
                        # removed data types
                        data_row['IndikationnachAlter'] = -1
                        data_row['BeruflicheIndikation'] = -1
                        data_row['MedizinischeIndikation'] = -1
                        data_row['PflegeheimbewohnerIn'] = -1
                        
                        df = df.append(data_row, ignore_index=True)
                        
                    df = df.fillna(0)                    
                    df.to_csv(csv_file, sep=',', decimal='.', encoding='utf-8', float_format='%.3f', index=False)
                    
                    ##############
                    # Thuringia
                    ##############
                    df_c = pd.read_excel(filename, header=[0,1,2], sheet_name=1, nrows=18, engine='openpyxl')
                    df_c = df_c.fillna(0)                    
                    col = df_c.columns                
                    idx_bl = 15
                
                    idx_1st_vac_below_18   = col[6]
                    idx_1st_vac_below_60   = col[7]
                    idx_1st_vac_above_60   = col[8]
                    
                    idx_2nd_vac_below_18   = col[10]
                    idx_2nd_vac_below_60   = col[11]
                    idx_2nd_vac_above_60   = col[12]
                    
                    if int(ts) < 1627200000:
                        num_1st_vac_A00_A17   = int(pop_TH_A00_A17 * df_c.iloc[idx_bl][idx_1st_vac_below_18])
                        num_2nd_vac_A00_A17   = int(pop_TH_A00_A17 * df_c.iloc[idx_bl][idx_2nd_vac_below_18])
                    else:
                        num_1st_vac_A00_A17   = int(pop_TH_A12_A17 * df_c.iloc[idx_bl][idx_1st_vac_below_18])
                        num_2nd_vac_A00_A17   = int(pop_TH_A12_A17 * df_c.iloc[idx_bl][idx_2nd_vac_below_18])
                    
                    num_1st_vac_A18_A59   = int(pop_TH_A18_A59 * df_c.iloc[idx_bl][idx_1st_vac_below_60])
                    num_1st_vac_A00_A59   = num_1st_vac_A00_A17 + num_1st_vac_A18_A59
                    num_1st_vac_A60p      = int(pop_TH_A60p * df_c.iloc[idx_bl][idx_1st_vac_above_60])                    
                    
                    num_2nd_vac_A18_A59   = int(pop_TH_A18_A59 * df_c.iloc[idx_bl][idx_2nd_vac_below_60])
                    num_2nd_vac_A00_A59   = num_2nd_vac_A00_A17 + num_2nd_vac_A18_A59
                    num_2nd_vac_A60p      = int(pop_TH_A60p * df_c.iloc[idx_bl][idx_2nd_vac_above_60])
                    
                    data_row = {
                            'Timestamp'          : int(ts),
                            'RS'                 : df_c.iloc[idx_bl][col[0]],
                            'State'              : df_c.iloc[idx_bl][col[1]].replace("*", ""),
                            'abs_1st_vac_A00-A17': num_1st_vac_A00_A17,
                            'abs_1st_vac_A18-A59': num_1st_vac_A18_A59,
                            'abs_1st_vac_A00-A59': num_1st_vac_A00_A59,
                            'abs_1st_vac_A60+'   : num_1st_vac_A60p,
                            'abs_2nd_vac_A00-A17': num_2nd_vac_A00_A17,
                            'abs_2nd_vac_A18-A59': num_2nd_vac_A18_A59,
                            'abs_2nd_vac_A00-A59': num_2nd_vac_A00_A59,
                            'abs_2nd_vac_A60+'    : num_2nd_vac_A60p
                    }
                        
                    df_th = df_th.append(data_row, ignore_index=True)
            
# export TH age data
df_th.sort_values(by=['Timestamp'], ascending=True, axis=0, inplace=True)
df_th.to_csv(DATAPATH + THURINGIA_CSV, sep=',', decimal=".", encoding='utf-8', float_format='%.0f', index=False)
            
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
