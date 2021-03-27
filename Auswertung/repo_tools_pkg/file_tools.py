import os
import re
from datetime import date

def find_latest_file(searchpath, file_pattern=None):
    iso_date_re = '([0-9]{4})(-?)(1[0-2]|0[1-9])\\2(3[01]|0[1-9]|[12][0-9])'
    path=searchpath
    file_list=os.listdir(path)
    date_max=date(1900,1,1)
    file_max=None
    search_filename=False
    if file_pattern:
        search_filename=True
    for file in file_list:
        file_path_full=os.path.join(path,file)
        if not os.path.isdir(file_path_full):
            filename=os.path.basename(file)
            if search_filename:
                re_filename=re.search(file_pattern,filename)
            else:
                re_filename=True
            re_search=re.search(iso_date_re, filename)
            if re_search and re_filename:
                test_date=date(int(re_search.group(1)), int(re_search.group(3)), int(re_search.group(4)))
                if test_date>date_max:
                    date_max=test_date
                    file_max=file_path_full
    if file_max:
        file_max=os.path.normpath(file_max)
    return (file_max, date_max)