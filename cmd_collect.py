import pandas as pd
import os, glob
from datetime import datetime

class collectCommand:
    
    track_df = pd.DataFrame()
    command_list = list()
    curr_d = str(datetime.now().date())

    def __init__(self):
        fname = glob.glob('tracks*')[0]
        self.track_df = pd.read_csv(fname, index_col=0)
    
    def get_gff_proc(self, fname, ftype, match):
        cmd= "./bin/flatfile-to-json.pl -gff " + fname
        cmd= cmd + " --trackLabel " + fname + " --trackType CanvasFeatures --out data --mem 16384000000 "
        if match == "mRNA":
            cmd += "--type mRNA"
        elif match == "gene":
            cmd += "--type gene"
        else:
            cmd += "--type match"
        return cmd
    
    def update_command(self):
        for index, row in self.track_df.iterrows():
            command = ""
            if row['ftype'] == "gff":
                command = get_gff_proc(row['fname'], row['ftype'], row['match'])
                command_list.append(command)
    
    def set_cmd_file(self):
        fname = "command_" + curr_d + ".txt"
        with open(fname, 'w') as f:
            for item in command_list:
                f.write("%s\n" % item)