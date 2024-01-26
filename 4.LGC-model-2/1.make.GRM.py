import pandas as pd
import sys
import os
import subprocess
import multiprocessing

def process_line(line):
    b = line.split()
    bim_chr = bim[bim[0] == int(b[0])]
    bim_chr = bim_chr[bim_chr[3].between(int(b[1]), int(b[2]))]
    return bim_chr

def lgc(rg_thre):
    lgc = pd.read_csv('../0.example_data/tr1.tr2.7.bivar.lava', sep='\s+')
    lgc_pos = lgc[lgc['rho'] >= rg_thre]
    lgc_neg = lgc[lgc['rho'] <= -rg_thre]
    lgc_pos[['chr','start','stop']].to_csv('lgc_pos.pos', index=None, header=None, sep='\t')
    lgc_neg[['chr','start','stop']].to_csv('lgc_neg.pos', index=None, header=None, sep='\t')
    
    res = pd.DataFrame()
    with open('lgc_pos.pos') as f:
        lines = f.readlines()
    with multiprocessing.Pool() as pool:
        results = pool.map(process_line, lines)
    res = pd.concat(results)
    res[1].to_csv('lgc_pos.snp', index=None, header=None)
    
    res = pd.DataFrame()
    with open('lgc_neg.pos') as f:
        lines = f.readlines()
    with multiprocessing.Pool() as pool:
        results = pool.map(process_line, lines)
    res = pd.concat(results)
    res[1].to_csv('lgc_neg.snp', index=None, header=None)
    
    os.system('cat lgc_pos.snp lgc_neg.snp > lgc_res.snp')
    os.system('plink --bfile ../0.example_data/all --extract lgc_pos.snp --make-bed --out lgc_pos')
    os.system('plink --bfile ../0.example_data/all --extract lgc_neg.snp --make-bed --out lgc_neg')
    os.system('plink --bfile ../0.example_data/all --exclude lgc_res.snp --make-bed --out lgc_res')

rg_thre = 0.5
bim = pd.read_csv('../0.example_data/all.bim', sep='\s+', header=None)
lgc(rg_thre)
run_script='gmat2 --make-grm --bfile lgc_pos --out lgc_pos --threads 30'
subprocess.run(run_script, shell=True)
run_script='gmat2 --make-grm --bfile lgc_neg --out lgc_neg --threads 30'
subprocess.run(run_script, shell=True)
run_script='gmat2 --make-grm --bfile lgc_res --out lgc_res --threads 30'
subprocess.run(run_script, shell=True)
