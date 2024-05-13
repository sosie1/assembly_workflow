path=$1
mkdir ${path}/original_front_info ${path}/original_back_info ${path}/bwa_set_count_front ${path}/bwa_set_count_back ${path}/bwa_dir_of_int_front ${path}/bwa_dir_of_int_back ${path}/int_set_remove_few_front ${path}/int_set_remove_few_back ${path}/compare_before\(f-b\) ${path}/compare_before\(b-f\) ${path}/compare_after\(f-b\) ${path}/compare_after\(b-f\) ${path}/remove_occur_once\(f-b\) ${path}/final_int_barcode\(f-b\) ${path}/final_dir_barcode\(f-b\) ${path}/remove_occur_once\(b-f\) ${path}/final_int_barcode\(b-f\) ${path}/final_dir_barcode\(b-f\) ${path}/new_back_info_of_each ${path}/new_front_info_of_each ${path}/union_file_final_int\(f-b\) ${path}/union_file_final_int\(b-f\)
for i in `seq 1 "$2"`;do
  mkdir ${path}/compare_before\(f-b\)/new_info_${i}
  mkdir ${path}/compare_before\(b-f\)/new_info_${i}
  mkdir ${path}/compare_after\(f-b\)/new_info_${i}
  mkdir ${path}/compare_after\(b-f\)/new_info_${i}
  mkdir ${path}/union_file_final_int\(f-b\)/new_info_${i}
  mkdir ${path}/union_file_final_int\(b-f\)/new_info_${i}
done