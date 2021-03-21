import requests, os, gzip
from datetime import datetime
from shutil import copyfile

class DownloadFile():
    def __init__(self,url,filename,download_path,compress=True,add_date=True,add_latest=False):
        self.url=url
        self.filename=filename
        self.download_path=os.path.normpath(download_path)
        self.compress=compress
        self.add_date=add_date
        self.add_latest=add_latest
        self._file_name_root, self._file_extension =os.path.splitext(self.filename)

    @property
    def full_path(self):
        path = os.path.join(self.download_path,self._file_name_root)
        if self.add_date:
            DATE_STR = datetime.now().date().strftime('%Y-%m-%d')
            path=path+"_"+DATE_STR
        path = path+self._file_extension
        if self.compress:
            path = path+".gz"
        return path

    @property
    def full_path_latest(self):
        path = os.path.join(self.download_path,self._file_name_root+"_latest"+self._file_extension)
        if self.compress:
            path = path + ".gz"
        return path

    @property
    def content(self):
        headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
        r = requests.get(self.url, headers=headers, allow_redirects=True, timeout=10.0)
        if r.status_code != 200:
            print("Download failed!")
            raise ValueError(f'Download failed! File {self.full_path} was not created!')
        else:
            return r.content
        
    def write_file(self):
        if self.compress:
            with gzip.open(self.full_path, 'wb') as file:
                file.write(self.content)
                file.close()
        else:
            with open(self.full_path, 'wb') as file:
                file.write(self.content)
                file.close()
        print(f"File {self.full_path} created.")
        if self.add_latest:
            copyfile(self.full_path, self.full_path_latest)
            print(f"File {self.full_path_latest} created.")