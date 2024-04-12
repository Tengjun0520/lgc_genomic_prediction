# LGC genomic prediction

## Model summary

We presented three novel models for incorporating local genetic correlations into multi-trait genomic prediction and compared our models with the conventional multi-trait genomic prediction model (MTGBLUP) and single trait model (STGBLUP). The models is as follows,
![](https://github.com/Tengjun0520/lgc_genomic_prediction/blob/main/model.png)

## Requirements

- [GMAT](https://github.com/chaoning/GMAT)
- [PLINK](https://www.cog-genomics.org/plink/)
- [Python 3.11](https://www.python.org/)

## Example data

There are genotype and phenotype data for 500 individuals as example data, which can be used to run all scripts.

## How to run script

Taking LGC-model-1 as an example,

### Step 1: calculate the genomic relationship matrix (GRM)

python3 1.make.GRM.py

### Step 2: run LGC-model-1

bash 2.run.LGC-model-1.sh

## About

If you want to know more details about the model, please read this paper

Jun Teng, Tingting Zhai,  Xinyi Zhang, Changheng Zhao, Wenwen Wang, Hui Tang, Chao Ning, Yingli Shang, Dan Wang* and Qin Zhang*. Improving multi-trait genomic prediction by incorporating local genetic correlations. in press.
