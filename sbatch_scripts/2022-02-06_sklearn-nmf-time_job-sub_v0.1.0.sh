#!/bin/bash
#SBATCH --job-name="2022-02-06_sklearn-nmf-time_v0.1.0"
#SBATCH --output="2022-02-06_sklearn-nmf-time_v0.1.0.%j.%N.out"
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=2G
#SBATCH --export=ALL
#SBATCH --account=ddp242
#SBATCH --chdir=/expanse/lustre/scratch/atwenzel/temp_project/msigdb_decomp/2022-02_work/2022-02-06_sklearn-nmf-time_v0.1.0
#SBATCH -t 48:00:00

module load anaconda3/2020.11

python /home/atwenzel/msigdb_decomp/2022-02_work/2022-02-06_sklearn-nmf-time_v0.1.0/2022-02-06_sklearn-nmf-time_v0.1.0.py BRCA_DESeq2_normalized_19307x40.preprocessed.gct 2022-02-07_sklearn-nmf-time_19307x40_v0.1.0.json
