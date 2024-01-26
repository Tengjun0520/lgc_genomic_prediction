#!/bin/bash

##Step 1: calculate the genomic relationship matrix (input file: train.bed train.bim train.fam)
gmat2 \
	--make-grm \
	--bfile ../0.example_data/train \
	--out train \
	--threads 30

##Step 2: calculate the inverse of GRM (out-fmt 0, matrix format)
gmat2 --process-grm \
	--make-inv \
	--grm train.agrm \
	--out-fmt 0 \
	--out train.inv

##Step 3: run STGBLUP
gmat2 \
    --uvlmm \
    --grm train \
    --data ../0.example_data/train.pheno \
    --trait tr1 \
    --out tr1 \
    --threads 30 \
    --predict
	
gmat2 \
    --uvlmm \
    --grm train \
    --data ../0.example_data/train.pheno \
    --trait tr2 \
    --out tr2 \
    --threads 30 \
    --predict
