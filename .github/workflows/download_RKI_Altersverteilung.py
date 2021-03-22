#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download_pkg import DownloadFile
import os

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Altersverteilung', 'raw_data')
filename = 'Altersverteilung.xlsx'
url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Altersverteilung.xlsx?__blob=publicationFile"

a = DownloadFile(url=url, filename=filename, download_path=data_path, compress=False,add_date=True,add_latest=True)
a.write_file()
