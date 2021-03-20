#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os
from datetime import datetime

VERBOSE = True
DATAPATH = os.path.dirname(os.path.abspath(
    __file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Nowcasting' + os.sep + 'raw_data' + os.sep
DATE_STR = datetime.now().date().strftime('%Y-%m-%d')
FILENAME = 'Nowcasting_Zahlen_csv_{date}.csv'.format(date=DATE_STR)
FULLNAME = DATAPATH + FILENAME
CSV_URL = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen_csv.csv?__blob=publicationFile"

# download latest data
if os.path.isfile(FULLNAME):

    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME))

else:

    if VERBOSE:
        print("The file '{}' does not exist.".format(FILENAME))

    headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

    r = requests.get(CSV_URL, headers=headers, allow_redirects=True, timeout=5.0)
    if r.status_code != 200:
        print("Download failed!")

    else:

        with open(FULLNAME, 'wb') as df:
            df.write(r.content)
            df.close()