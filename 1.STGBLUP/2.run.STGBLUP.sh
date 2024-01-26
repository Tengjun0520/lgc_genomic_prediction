#!/bin/sh

## trait 1
gmat2 \
    --uvlmm \
    --grm all \
    --data ../0.example_data/all.pheno \
    --trait tr1 \
    --out tr1 \
    --threads 30 \
    --predict
	
## trait 2
gmat2 \
    --uvlmm \
    --grm all \
    --data ../0.example_data/all.pheno \
    --trait tr2 \
    --out tr2 \
    --threads 30 \
    --predict