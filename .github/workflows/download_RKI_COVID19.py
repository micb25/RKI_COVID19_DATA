#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download_pkg import DownloadFile
import os

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
filename = "RKI_COVID19.csv"
url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"

a = DownloadFile(url=url, filename=filename, download_path=data_path, compress=True,add_date=True,add_latest=True)
a.write_file()
