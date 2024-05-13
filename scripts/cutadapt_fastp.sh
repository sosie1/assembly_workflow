path=$1
./bin/cutadapt -a TGAAGCGGCGCACGAAAAACGCGAAAGCGTTTCAC -a TGGTCATGTGGAGACGCTGGG -a ATCACGGACTGCCCATAGAGAGGCTCTGG -j 10 -O 5 -o ${path}/R1.cutadapt.fastq ${path}/correct_R1.fastq
./bin/cutadapt -a TGGGCCGGTGCAGTTAATGTAGGGAAAGAGTGT -j 10 -O 5 -o ${path}/R2.cutadapt.fastq ${path}/correct_R2.fastq

#todo fastp
#cd /bios-store1/home/yutongli/
#./fastp -Q 30 -i ${path}/R1.cutadapt.fastq -o ${path}/fastp_r1.fastq -I ${path}/R2.cutadapt.fastq -O ${path}/fastp_r2.fastq