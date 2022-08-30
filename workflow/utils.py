'''Utilities.'''


import gzip
import os
from os import makedirs, symlink
from os.path import abspath, exists, join
import pandas as pd
import shutil


# --- Workflow functions --- #


def calc_read_lens(sp, st, fqs, fo): # A list of FastQ files
    # Extract read sequences and their lengths
    seqs = []
    for fq in fqs:
        f = gzip.open(fq, 'rt') if 'gz' in fq else open(fq, 'r')
        lines = f.readlines()
        f.close()
        for i,l in enumerate(lines):
            if i % 4 == 1:
                seqs.append(l.strip())
    seq_lens = [len(s) for s in seqs]
    line = "%s,%s,%d,%d,%.2f" % (sp, st, len(seq_lens), sum(seq_lens), float(sum(seq_lens)/len(seq_lens)))
    with open(fo, 'w') as f_out:
        f_out.write(line + '\n')


# --- Workflow setup --- #


def extract_from_gzip(p, out):
    if open(ap, 'rb').read(2) == b'\x1f\x8b': # If the input is gzipped
        with gzip.open(ap, 'rb') as f_in, open(out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    else: # Otherwise, symlink
        symlink(ap, out)


def ingest_samples(samples, tmp):
    df = pd.read_csv(samples, header = 0, index_col = 0) # name, fwd, rev
    s = list(df.index)
    lst = df.values.tolist()
    for f in os.listdir(tmp):
        os.remove(join(tmp, f))
    for i,l in enumerate(lst):
        symlink(abspath(l[0]), join(tmp, s[i] + '_1.fastq.gz'))
        symlink(abspath(l[1]), join(tmp, s[i] + '_2.fastq.gz'))
        calc_read_lens(s[i], '0_begin', [abspath(l[0]), abspath(l[1])], join(tmp, s[i] + '_read_stats.csv'))
    return s


class Workflow_Dirs:
    """Management of the working directory tree."""
    OUT = ''
    TMP = ''
    LOG = ''

    def __init__(self, work_dir, module):
        self.OUT = join(work_dir, module)
        self.TMP = join(work_dir, 'tmp') 
        self.LOG = join(work_dir, 'logs') 
        if not exists(self.OUT):
            makedirs(self.OUT)
            makedirs(join(self.OUT, '0_lowqual_removal'))
            makedirs(join(self.OUT, '1_adapter_removal'))
            makedirs(join(self.OUT, '2_host_removal'))
            makedirs(join(self.OUT, '3_error_removal'))
            makedirs(join(self.OUT, '4_summary'))
            makedirs(join(self.OUT, 'final_reports'))
        if not exists(self.TMP):
            makedirs(self.TMP)
        if not exists(self.LOG):
            makedirs(self.LOG)
            makedirs(join(self.LOG, 'lowqual_removal'))
            makedirs(join(self.LOG, 'adapter_removal'))            
            makedirs(join(self.LOG, 'host_removal'))
            makedirs(join(self.LOG, 'error_removal'))

            