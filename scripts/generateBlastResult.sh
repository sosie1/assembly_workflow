#获取结果
ref_full=$1
path=$2
path_1=$3
root=$4
#ref_full="/bios-store5/lyt/D1_L31/D1/spades_result_unique/assembly.fasta"
mkdir ${path}/
#path="/bios-store5/lyt/D1_L31/D1/spades_result_unique_new/get_different_contig"
mkdir ${path_1}/
#path_1='/bios-store5/lyt/D1_L31/D1/blast_connection'
cd ${path_1}
cat ${root}/efficient_id.txt | while read line
do
   echo ${line}
   samtools faidx ${ref_full} ${line} > ${path}/assembly_${line}.fasta
   mkdir blast_${line}
   makeblastdb -in ${path}/assembly_${line}.fasta -dbtype nucl -parse_seqids -out ${path}/contig_${line}_index
done


cat ${root}/efficient_id.txt | while read a
do
    cat ${root}/efficient_id.txt | while read b
    do
        {
            blastn -query ${path}/assembly_${b}.fasta -db ${path}/contig_${a}_index -outfmt 6 -evalue 1e-6 -num_threads 6 -out ${path_1}/blast_${a}/blastoutfile_${b}_to_${a}.txt -word_size 7
        } 
    done
done
# for ((i=0;i<${job_num};i++));do # 任务数量
#     # 一个read -u6命令执行一次，就从fd6中减去一个回车符，然后向下执行，
#     # fd6中没有回车符的时候，就停在这了，从而实现了线程数量控制
#     read -u6
#
#     #可以把具体的需要执行的命令封装成一个函数
#     {
#         my_cmd
#     } &
#
#     echo >&6 # 当进程结束以后，再向fd6中加上一个回车符，即补上了read -u6减去的那个
# done


#cat ${root}/efficient_id.txt | while read a
#do
#    cat ${root}/efficient_id.txt | while read b
#    do
#        blastn -query ${path}/assembly_${b}.fasta -db ${path}/contig_${a}_index -outfmt 6 -evalue 1e-6 -num_threads 6 -out ${path_1}/blast_${a}/blastoutfile_${b}_to_${a}.txt -word_size 7
#    done
#done



cat ${root}/efficient_id.txt | while read a
do
    cat ${root}/efficient_id.txt | while read b
    do
        if [[ -f ${path_1}/blast_${a}/blastoutfile_${b}_to_${a}.txt && -s ${path_1}/blast_${a}/blastoutfile_${b}_to_${a}.txt ]];then
          echo "the file is not none"
        else
          rm -f ${path_1}/blast_${a}/blastoutfile_${b}_to_${a}.txt
        fi
    done
done

mkdir ${root}/blast_connection/blast_all_info/
cat ${root}/efficient_id.txt | while read line
do
   echo ${line}
   cat ${path_1}/blast_${line}/*.txt > ${path_1}/blast_all_info/all_${line}.txt
done