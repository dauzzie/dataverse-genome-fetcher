import requests as req
import json 
import pandas as pd
from pandas.io.json import json_normalize
import re
from pandas.util.testing import assert_frame_equal
import os, glob
from datetime import datetime
import sys
from pathlib import Path

class checkUpdate:
    dv_search = 'https://demo.dataverse.org/api/search?q=*&start=0&sort=date'
    dv_download = 'https://demo.dataverse.org/api/access/datafile/'
    dv_data = pd.DataFrame()
    track_data = pd.DataFrame()
    curr_fname = ""
    DATADIR = Path("./")
    curr_t = datetime.now().strftime("%d-%m-%Y_%H%M")
    
    def __init__(self):
        self.curr_fname = glob.glob('current_data*')[0]
        

    def get_response(self):
        dv_fetched = json.loads(req.get(dv_search).content.decode("utf-8")
        return json_normalize(dv_fetched['data']['items']
    
    def format_response(self, df):
        null_data, temp = dv_data.isna().sum(), df
        for x in null_data.index:
            if x.find("id") < 0 and null_data[x] >= len(df.index)/2 - 1:
                temp = temp.drop(columns={x})
        temp = temp.fillna(0)
        return temp
    
    def needs_update(self, curr, dv):
        null_data = dv.isna().sum()
        temp_df = dv
        for x in null_data.index:
            if x.find("id") < 0 and null_data[x] >= len(dv.index)/2 - 1:
        temp_df = temp_df.drop(columns={x})
        self.dv_data = temp_df.fillna(0)
        return dv.equals(curr)
    
    def set_files(self, curr):
        curr_f = curr.iloc[:, 6:7].values ## might fail
        file_req = list()
        for idx, r in dv_data.iterrows():
            if r['type'].find("file") >= 0 and r['name'] not in curr_f:
                if(r['name'].find("gff") > 0):
                    file_req.append(row['file_id'])
        return file_req
    
    def get_filename_from_cd(self, cd):
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]
        
    def download(self, res, fname):
        with open(fname, 'wb') as f:
            total = res.headers.get('content-length')

            if total is None:
                f.write(res.content)
        else:
            downloaded = 0
            total = int(total)
            for data in res.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')
                              
    def get_files(self, f_list):
        tracks = pd.DataFrame(columns=['fname', 'ftype', 'match'])
        for f in f_list:
            res = req.get(dv_download + f, stream=True)
            fname = get_filename_from_cd(res.headers.get('content-disposition'))
            fname = fname[1 :len(fname)-1]
            print('[*] Downloading the file ' + fname)
            self.download(res, fname)
            print('[*] Done!')
            tracks = tracks.append({'fname':fname,'ftype':'gff','match':'blat'},ignore_index=True)
        self.track_data = tracks
        return tracks
    
    def update_data(self):
        self.track_data.to_csv("tracks_" + curr_t + ".csv")
        os.remove(curr_fname)
        print(curr_fname + " removed")
        self.dv_data.to_csv("current_data_" + curr_t + ".csv")
        return "Success"
        
    
    def get_current(self):
        return pd.read_csv(curr_fname, index_col=0)
           