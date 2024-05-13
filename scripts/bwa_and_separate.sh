path=$1
r1="R1_with_barcode_new.fastq"
r2="R2_with_barcode_new.fastq"

bwa index ${path}/spades_result_unique_new/assembly.fasta
bwa mem ${path}/spades_result_unique_new/assembly.fasta ${path}/${r1} ${path}/${r2} | samtools view -q 20 -bS > ${path}/spades_result_unique_new/full_contig_blast.bam 
samtools view -q 1 ${path}/spades_result_unique_new/full_contig_blast.bam > ${path}/spades_result_unique_new/full_final_unique_out.info.txt
samtools view ${path}/spades_result_unique_new/full_contig_blast.bam > ${path}/spades_result_unique_new/full_final_out.info.txt

mkdir ${path}/spades_result_unique_new/get_bam_info/