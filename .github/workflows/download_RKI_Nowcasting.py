#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download_pkg import DownloadFile
import os

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Nowcasting', 'raw_data')
filename = 'Nowcasting_Zahlen_csv.csv'
url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen_csv.csv?__blob=publicationFile"

a = DownloadFile(url=url, filename=filename, download_path=data_path, compress=True,add_date=True,add_latest=False)
a.write_file()
