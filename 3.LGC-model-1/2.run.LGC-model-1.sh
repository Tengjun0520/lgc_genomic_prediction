#!/bin/sh

gmat2 \
    --mvlmm \
    --mgrm sig.agrm non_sig.agrm \
    --data ../0.example_data/all.pheno \
	--random id id \
    --trait tr1 tr2 \
    --out tr1_tr2 \
    --threads 30 \
    --predict
