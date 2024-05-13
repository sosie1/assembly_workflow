path=$1
for i in `seq 1 "$2"`;do
  cd ${path}/new_info_${i}/
  mkdir ./compara_to_contig/
  mv ${path}/new_info_${i}/barcode_set_of_contig_* ${path}/new_info_${i}/compara_to_contig/
done

for i in `seq 1 "$2"`;do
  mv ${path}/new_info_${i}/compara_to_contig/barcode_set_of_contig_${i}compare_to_contig_${i}.txt ${path}/new_info_${i}/
done