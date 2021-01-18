#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os
from datetime import datetime

VERBOSE      = True
DATAPATH     = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Impfquotenmonitoring' + os.sep
DATE_STR     = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d')
FILENAME     = 'RKI_COVID19_Impfquotenmonitoring_{}.xlsx'.format(DATE_STR)
PARSED_CSV   = 'RKI_COVID19_Impfquotenmonitoring.csv'
FULLNAME     = DATAPATH + FILENAME
CSV_URL      = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile"

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
