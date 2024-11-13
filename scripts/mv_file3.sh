path=$1
for i in `seq 1 "$2"`;do
  cd ${path}/new_info_${i}/
  mkdir compare_to_contig
  mv ${path}/new_info_${i}/front_*compare_to_back_* ${path}/new_info_${i}/compare_to_contig/
done

for i in `seq 1 "$2"`;do
  mv ${path}/new_info_${i}/compare_to_contig/front_${i}compare_to_back_${i}.txt ${path}/new_info_${i}/
done

path=$3
for i in `seq 1 "$2"`;do
  cd ${path}/new_info_${i}/
  mkdir compare_to_contig
  mv ${path}/new_info_${i}/back_*compare_to_front_* ${path}/new_info_${i}/compare_to_contig/
done

for i in `seq 1 "$2"`;do
  mv ${path}/new_info_${i}/compare_to_contig/back_${i}compare_to_front_${i}.txt ${path}/new_info_${i}/
done
