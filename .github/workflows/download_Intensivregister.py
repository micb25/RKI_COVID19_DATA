#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os
from datetime import datetime

VERBOSE = True
DATAPATH = os.path.dirname(os.path.abspath(
    __file__)) + os.sep + '..' + os.sep + '..' + os.sep + 'Intensivregister' + os.sep + 'raw_data' + os.sep
DATE_STR = datetime.now().date().strftime('%Y-%m-%d')
FILENAME_TAGESDATEN = 'DIVI_Intensivregister_Auszug_pro_Landkreis_{date}.csv'.format(date=DATE_STR)
FILENAME_ZEITREIHE = 'bundesland-zeitreihe_{date}.csv'.format(date=DATE_STR)
FULLNAME_TAGESDATEN = DATAPATH + FILENAME_TAGESDATEN
FULLNAME_ZEITREIHE = DATAPATH + FILENAME_ZEITREIHE
URL_TAGESDATEN = "https://diviexchange.blob.core.windows.net/%24web/DIVI_Intensivregister_Auszug_pro_Landkreis.csv"
URL_ZEITREIHE = "https://diviexchange.blob.core.windows.net/%24web/bundesland-zeitreihe.csv"

# download latest data
if os.path.isfile(FULLNAME_TAGESDATEN):
    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME_TAGESDATEN))

elif os.path.isfile(FULLNAME_ZEITREIHE):
    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME_ZEITREIHE))

else:

    if VERBOSE:
        print("The files '{0},{1}' does not exist.".format(FILENAME_TAGESDATEN, FILENAME_ZEITREIHE))

    headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

    r = requests.get(URL_TAGESDATEN, headers=headers, allow_redirects=True, timeout=5.0)
    if r.status_code != 200:
        print("Download failed!")

    else:

        with open(FULLNAME_TAGESDATEN, 'wb') as df:
            df.write(r.content)
            df.close()

    r2 = requests.get(URL_ZEITREIHE, headers=headers, allow_redirects=True, timeout=5.0)
    if r2.status_code != 200:
        print("Download failed!")

    else:

        with open(FULLNAME_ZEITREIHE, 'wb') as df:
            df.write(r2.content)
            df.close()
