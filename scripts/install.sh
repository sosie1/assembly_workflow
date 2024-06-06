#!/bin/bash

# 检查conda是否可用
if command -v conda &> /dev/null
then
    echo "conda可用. 尝试使用conda安装依赖工具"
    conda install -c bioconda cutadapt -y
    conda install -c bioconda fastp -y
    conda install -c bioconda fastqc -y
    conda install -c bioconda bwa -y
    conda install -c bioconda samtools -y

    conda install -c jjhelmus tensorflow=0.10.0rc0 -y
    conda install -c smaegol plasflow -y

    conda install -c bioconda blast
# 安装python包
pip3 install svglib
pip3 install svgwrite
pip3 install numpy
pip3 install pandas