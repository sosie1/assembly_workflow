#!/bin/bash

# 确保R和Rscript已安装
if ! command -v Rscript &> /dev/null
then
    echo "Rscript is not installed."
    exit
fi
# 确保R和Rscript已安装
if ! command -v conda &> /dev/null
then
    echo "conda is not installed."
    exit
fi
# 检查conda是否可用
if command -v conda &> /dev/null
then
    conda env create -f TELLBASE_environment.yaml
    pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp35-cp35m-linux_x86_64.whl
    pip install seaborn
    conda install -c bioconda cutadapt -y
    conda install -c bioconda fastp -y
    conda install -c bioconda fastqc -y
    conda install -c bioconda bwa -y
    conda install -c bioconda samtools -y

    pip3 install svglib
    pip3 install svgwrite
    pip install numpy pandas scipy rpy2 scikit-learn biopython
    conda install -c bioconda blast -y
    # 使用Rscript执行R命令
    Rscript -e "if (!requireNamespace('BiocManager', quietly = TRUE)) install.packages('BiocManager'); BiocManager::install('Biostrings', force = TRUE)"
    echo "Biostrings包及其依赖已安装。"

