#!/bin/sh

gmat2 \
    --mvlmm \
    --mgrm lgc_pos.agrm lgc_neg.agrm lgc_res.agrm \
    --data ../0.example_data/all.pheno \
    --random id id id \
    --trait tr1 tr2 \
    --out tr1_tr2 \
    --threads 30 \
    --predict
