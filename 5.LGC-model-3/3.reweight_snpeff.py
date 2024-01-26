import numpy as np
from pysnptools.snpreader import Bed
import pandas as pd
from tqdm import tqdm

def impute_geno(snp_mat):
    ind_na = np.where(np.isnan(snp_mat))
    col_na = set(ind_na[1])
    for i in col_na:
        snpi = snp_mat[:, i]
        code0 = np.sum(np.absolute(snpi - 0.0) < 1e-10)
        code1 = np.sum(np.absolute(snpi - 1.0) < 1e-10)
        code2 = np.sum(np.absolute(snpi - 2.0) < 1e-10)
        code_count = code0 + code1 + code2
        p_lst = [code0/code_count, code1/code_count, code2/code_count]
        icol_na = np.where(np.isnan(snpi))
        snpi[icol_na] = np.random.choice([0.0, 1.0, 2.0], len(icol_na[0]), p = p_lst)
        snp_mat[:, i] = snpi
    return snp_mat

def snpeff_to_gv(bfile, snp_eff, outfile, part):
    ##read bed
    snp = Bed('{}'.format(bfile), count_A1 = False)
    num_snp = snp.sid_count
    
    ##snp_index
    snp_index = []
    for i in range(part):
        snp_index.append(int(num_snp/part)*i)
    snp_index.append(num_snp)
    
    res = pd.DataFrame(snp.iid,columns=['fid','iid'])
    
    ##cal_gv
    gv = np.zeros((snp.iid_count,1))
    for i in tqdm(range(part)):
        snp_mat = snp[:, snp_index[i]:snp_index[i+1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        freq = np.sum(snp_mat,  axis = 0) / (2 * snp.iid_count)
        Z = snp_mat - 2 * freq
        gv_b = np.dot(Z, snp_eff[snp_index[i]:snp_index[i+1]])
        gv += gv_b
    res['gv'] = gv
    res.to_csv(outfile, index=None, sep='\t')

##get lgc
lgc_file = '../0.example_data/tr1.tr2.7.bivar.lava' ##local genetic correlation estimation using lava
sig_val = 0.05 ##P_threshold

df_lgc = pd.read_csv('{}'.format(lgc_file), sep = '\s+')
df_lgc['reg_index'] = df_lgc['chr'].map(str) + '_' + df_lgc['start'].map(str)
df_lgc_sig = df_lgc[df_lgc['p'] <= sig_val] ## sig lgc

lgc={}
for a in open(lgc_file):
    b=a.split()
    if len(b) > 8:
        lgc[b[1]+'_'+b[2]] = b[8]
    else:
        lgc[b[1]+'_'+b[2]] = '0'

for blocks in open('../0.example_data/block_snp_num.txt'):
    block = blocks.split()
    if block[0]+'_'+block[1] in df_lgc_sig['reg_index'].values:
        with open('tr1_tr2_weight.txt', 'a') as f:
            for i in range(0, int(block[3])):
                f.write(lgc[block[0]+'_'+block[1]]+'\n')
    else:
        with open('tr1_tr2_weight.txt', 'a') as f:
            for i in range(0, int(block[3])):
                f.write('0'+'\n')

bfile='../0.example_data/test'
part = 30 #partition all SNPs into n parts
snpeff1 = np.loadtxt('tr1.snp.eff')
snpeff2 = np.loadtxt('tr2.snp.eff')
rg = np.loadtxt('tr1_tr2_weight.txt')
snpeff1 = snpeff1.reshape(-1,1)
snpeff2 = snpeff2.reshape(-1,1)
rg = rg.reshape(-1,1)
snpeff_rw1 = snpeff1 + snpeff2 * rg
snpeff_rw2 = snpeff2 + snpeff1 * rg
snpeff_to_gv(bfile, snpeff_rw1, 'tr1.rw.gv', part)
snpeff_to_gv(bfile, snpeff_rw2, 'tr2.rw.gv', part)

