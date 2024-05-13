path=$1
mkdir ${path}/bwa_original_barcode_name ${path}/back_barcode ${path}/bwa_dir_and_set ${path}/set_remove_few ${path}/compare_before ${path}/remove_occur_once ${path}/final_int_barcode ${path}/final_dir_barcode ${path}/compara_file_final_int ${path}/compara_file_final_dir ${path}/union_file_final_int
for i in `seq 1 "$2"`;do
  mkdir ${path}/compare_before/new_info_${i}
  mkdir ${path}/compara_file_final_int/new_info_${i}
  mkdir ${path}/compara_file_final_dir/new_info_${i}
  mkdir ${path}/union_file_final_int/new_info_${i}
done