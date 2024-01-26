#!/bin/sh

gmat2 \
    --mvlmm \
    --grm all \
    --data ../0.example_data/all.pheno \
    --trait tr1 tr2 \
    --out tr1_tr2 \
    --threads 30 \
    --predict
	