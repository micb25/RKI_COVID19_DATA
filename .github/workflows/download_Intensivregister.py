#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download_pkg import DownloadFile
import os


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Intensivregister', 'raw_data')
filename_tagesdaten = 'DIVI_Intensivregister_Auszug_pro_Landkreis.csv'
url_tagesdaten = "https://diviexchange.blob.core.windows.net/%24web/DIVI_Intensivregister_Auszug_pro_Landkreis.csv"
filename_zeitreihe = 'bundesland-zeitreihe.csv'
url_zeitreihe = "https://diviexchange.blob.core.windows.net/%24web/bundesland-zeitreihe.csv"

#download Tagedaten
a = DownloadFile(url=url_tagesdaten, filename=filename_tagesdaten, download_path=data_path, compress=True,add_date=True,add_latest=True)
a.write_file()

#download Zeitreihe
b = DownloadFile(url=url_zeitreihe, filename=filename_zeitreihe, download_path=data_path, compress=True,add_date=True,add_latest=True)
b.write_file()