#!/bin/bash

# 检查conda是否可用
if command -v conda &> /dev/null
then
    echo "conda可用. 尝试使用conda安装依赖工具"
    conda install -c bioconda cutadapt
    conda install -c bioconda fastp
    conda install -c bioconda fastqc
    conda install -c bioconda bwa
    conda install -c bioconda samtools
    conda install -c bioconda blast
# 安装python包
pip3 install svglib
pip3 install svgwrite
pip3 install numpy
pip3 install pandas