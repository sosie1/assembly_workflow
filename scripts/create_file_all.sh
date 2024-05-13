path=$1
mkdir ${path}/bwa_original_barcode_name_\(file_1\) ${path}/front_and_back_barcode_\(file_2\) ${path}/bwa_dir_of_int_\(file_3\) ${path}/int_set_remove_few_\(file_3\) ${path}/compare_before_\(file_4\) ${path}/remove_occur_once_\(file_5\) ${path}/final_int_barcode\(file_6\) ${path}/final_dir_barcode\(file_7\) ${path}/compara_file_final_int_\(file_8\) ${path}/compara_file_final_dir_\(file_9\) ${path}/union_file_final_int_\(file_10\) ${path}/ff_list ${path}/bb_list ${path}/fb_and_bf_list
for i in `seq 1 "$2"`;do
  mkdir ${path}/compare_before_\(file_4\)/new_info_${i}
  mkdir ${path}/compara_file_final_int_\(file_8\)/new_info_${i}
  mkdir ${path}/compara_file_final_dir_\(file_9\)/new_info_${i}
  mkdir ${path}/union_file_final_int_\(file_10\)/new_info_${i}
done