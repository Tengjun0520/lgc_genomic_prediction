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

def gv_to_snpeff(bfile, gvfile, ginvfile, outfile, part):
    ##read bed
    snp = Bed('{}'.format(bfile), count_A1 = False)
    num_snp = snp.sid_count
    
    ##snp_index
    snp_index = []
    for i in range(part):
        snp_index.append(int(num_snp/part) * i)
    snp_index.append(num_snp)

    ##read gv
    df = pd.read_csv('{}'.format(gvfile), sep='\s+')
    df_gv = df[df['type'] == 3]
    gv = df_gv['effect'].values
    gv = gv.reshape(-1, 1)
    
    ##read ginv
    ginv = np.loadtxt('{}'.format(ginvfile))
    
    ##cal snp_eff
    scale = 0
    snp_eff = np.empty((0, 1))
    for i in tqdm(range(part)):
        snp_mat = snp[:, snp_index[i]:snp_index[i+1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        freq = np.sum(snp_mat, axis = 0) / (2 * snp.iid_count)
        scale += np.sum(2 * freq * (1 - freq))
        Z = snp_mat - 2 * freq
        gg = np.dot(Z.T, ginv)
        snp_eff_b = np.dot(gg, gv)
        snp_eff = np.concatenate((snp_eff, snp_eff_b))
    snp_eff = snp_eff/scale
    res = pd.DataFrame(snp_eff)
    res.to_csv('{}'.format(outfile), index=None, header=None)
    
for tr in ['tr1', 'tr2']:
    bfile = 'train' #plink file
    ginvfile = 'train.inv.mat_fmt' #ginv file
    part = 30 #partition all SNPs into n parts
    gvfile = '{}.sln'.format(tr)
    outfile = '{}.snp.eff'.format(tr)
    gv_to_snpeff(bfile, gvfile, ginvfile, outfile, part)