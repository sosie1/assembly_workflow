# This is a sample Python script.
import subprocess
import sys

from DataFilter import filter_data, bwa_and_separate
from DataProcess import DataProcessUtil
import GraphicalProcess
import argparse
import os

from all_demo import Barcode_info
from MatrixGeneration import back_info, barcode_info, F_B, B_F
from all_demo_ff import  front_info
from Utils import Feature_extract

def processArgs():
    parser = argparse.ArgumentParser(description='SeriesAnalysis_1.0')
    parser.add_argument('--coincidenceThreshold', type=float, default=99, help='序列有效重合比例阈值')
    parser.add_argument('--coincidenceThreshold_1', type=float, default=99, help='短-长序列有效重合比例阈值')
    parser.add_argument('--lengthThreshold', type=int,  default=5000,help='序列长度阈值')
    parser.add_argument('--workingSpace',type=str,help='工作路径')
    parser.add_argument('--outputSpace',type=str,default='.',help='输出路径')
    parser.add_argument('--batch',type=bool,default=False)
    parser.add_argument('--repeatSeriesSpace', type=str, default='/Users/yangweiyi/Desktop/liyutongFiles/旧样本重复序列',help='可重复长序列信息路径')
    parser.add_argument('--plasmids', type=bool, default=False)
    parser.add_argument('--i1', type=str, default='i1.fastq', help='i1_fastq文件名（需要放在工作路径下')
    parser.add_argument('--r1', type=str, default='r1.fastq', help='r1_fastq文件名')
    parser.add_argument('--r2', type=str, default='r2.fastq', help='r2_fastq文件名')
    #todo help信息补齐
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--num', type=int, default=1)
    parser.add_argument('--c1', type=int, default=1)
    parser.add_argument('--c2',type=int, default=1)
    # parser.add_argument('--output', type=str, default='output.txt', help='输出文件路径（默认：output.txt）')
    # parser.add_argument('--flag', action='store_true', help='一个布尔标志')
    args = parser.parse_args()
    return args

# Press the green button in the gutter to run the script.
def generateSeries(args):
    if (args.batch == False):
        a = DataProcessUtil(args.workingSpace)
        a.readPlasmids()
        a.readRepeat(args.workingSpace)
        a.readDepthTable(args.lengthThreshold)
        a.readDirection(False)
        a.readGenome()
        a.extendSeries(args.coincidenceThreshold, args.coincidenceThreshold_1)
        b = GraphicalProcess.GraphicalProcessUtil(a)
        b.showCommandLineGraphics(a.contigs)
        b.showCommandLineGraphics_Extend(a.contigs, args.outputSpace)
        b.generateSvg(a.contigs, args.outputSpace)
        a.writeFastA(args.outputSpace, True)
        print('段数:' + str(a.writeFastA(args.outputSpace, False)))
        a.encodeFastA(args.outputSpace)

        if (args.plasmids == True):
            folder = os.path.exists(args.outputSpace + '/plasmid')
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(args.outputSpace + '/plasmid')  # makedirs 创建文件时如果路径不存在会创建这个路径

            a1 = DataProcessUtil(args.workingSpace)
            a1.readPlasmids()
            a1.readDepthTable_Plasmid(args.lengthThreshold)
            a1.readDirection(True)
            a1.readGenome()
            a1.extendSeries(args.coincidenceThreshold, args.coincidenceThreshold_1)
            b1 = GraphicalProcess.GraphicalProcessUtil(a1)
            b1.showCommandLineGraphics(a1.contigs)
            b1.showCommandLineGraphics_Extend(a1.contigs, args.outputSpace + '/plasmid')
            b1.generateSvg(a1.contigs, args.outputSpace + '/plasmid')
            a1.writeFastA(args.outputSpace + '/plasmid', True)
            print('plasmid:段数:' + str(a1.writeFastA(args.outputSpace + '/plasmid', False)))
            a1.encodeFastA(args.outputSpace + '/plasmid')


    else:
        for root, dirs, files in os.walk(args.workingSpace):
            # for name in files:
            #     print(os.path.join(root, name))
            for name in dirs:
                space = os.path.join(root, name)
                print(space)

                a = DataProcessUtil(space)
                a.readPlasmids()
                a.readRepeat(args.repeatSeriesSpace + '/' + name)
                a.readDepthTable(args.lengthThreshold)
                a.readDirection(False)
                a.readGenome()
                b = GraphicalProcess.GraphicalProcessUtil(a)
                b.showCommandLineGraphics(a.contigs)
                a.extendSeries(args.coincidenceThreshold, args.coincidenceThreshold_1)
                b.showCommandLineGraphics_Extend(a.contigs, space)
                b.generateSvg(a.contigs, space)
                a.writeFastA(space, True)
                print('段数:' + str(a.writeFastA(space, False)))
                print('延伸后断裂位点总数量:', str(a.encodeFastA(space)))
                if (args.plasmids == True):
                    folder = os.path.exists(space + '/plasmid')

                    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                        os.makedirs(space + '/plasmid')  # makedirs 创建文件时如果路径不存在会创建这个路径

                    a1 = DataProcessUtil(space)
                    a1.readPlasmids()
                    a1.readDepthTable_Plasmid(args.lengthThreshold)
                    a1.readDirection(True)
                    a1.readGenome()
                    a1.extendSeries(args.coincidenceThreshold, args.coincidenceThreshold_1)
                    b1 = GraphicalProcess.GraphicalProcessUtil(a1)
                    b1.showCommandLineGraphics(a1.contigs)
                    b1.showCommandLineGraphics_Extend(a1.contigs, space + '/plasmid')
                    b1.generateSvg(a1.contigs, space + '/plasmid')
                    a1.writeFastA(space + '/plasmid', True)
                    print('plasmid:段数:' + str(a1.writeFastA(space + '/plasmid', False)))
                    print('plasmid:延伸后断裂位点总数量:', str(a1.encodeFastA(space + '/plasmid')))
            break


def unique_reads(path, i1, r1, r2):
    I1_1 = open(path + i1, "r").readlines()
    R1_1 = open(path + r1, "r").readlines()
    R2_1 = open(path + r2, "r").readlines()

    #output_integration = open(path + 'integration.fastq', 'w')
    map={}
    i=0
    while(i<len(R1_1)):
        list=[]
        index = R1_1[i]
        list.append(index)

        i=i+1
        line = R1_1[i][:-1] + R2_1[i][:-1] + I1_1[i]

        i=i+2
        # signal = R1_1[i]
        # list.append(signal)
        lines = R1_1[i][:-1] + R2_1[i][:-1] + I1_1[i]
        list.append(lines)
        i=i+1
        map[line]=list
    unique_fa_R1 = open(path + "unique_R1.fastq", "w")
    unique_fa_R2 = open(path + "unique_R2.fastq", "w")
    unique_fa_I1 = open(path + "unique_I1.fastq", "w")
    for key in map:
        list=map[key]

        unique_fa_R1.writelines(list[0])
        unique_fa_R2.writelines(list[0])
        unique_fa_I1.writelines(list[0])

        seq_R1 = key[0:150]
        seq_R2 = key[150:300]
        seq_I1 = key[300:318]
        unique_fa_R1.writelines(seq_R1 + "\n")
        unique_fa_R2.writelines(seq_R2 + "\n")
        unique_fa_I1.writelines(seq_I1 + "\n")

        unique_fa_R1.writelines("+"+"\n")
        unique_fa_R2.writelines("+" + "\n")
        unique_fa_I1.writelines("+" + "\n")

        score_R1 = list[1][0:150]
        score_R2 = list[1][150:300]
        score_I1 = list[1][300:318]
        unique_fa_R1.writelines(score_R1 + "\n")
        unique_fa_R2.writelines(score_R2 + "\n")
        unique_fa_I1.writelines(score_I1 + "\n")
    unique_fa_R1.close()
    unique_fa_R2.close()
    unique_fa_I1.close()
def qualityAssessment(output_path):
    #todo 原始文件名？
    subprocess.run(
        'fastqc -o '+ output_path +' '+output_path+'output_re_I1_T500.fastq.gz -t 10'
        , shell=True)
    subprocess.run(
        'fastqc -o ' + output_path + ' ' + output_path + 'output_re_R1_T500.fastq.gz -t 10'
        , shell=True)
    subprocess.run(
        'fastqc -o ' + output_path + ' ' + output_path + 'output_re_R2_T500.fastq.gz -t 10'
        , shell=True)
    subprocess.run(
        'fastqc -o ' + output_path + ' ' + output_path + 'fastp_i1.fastq -t 10'
        , shell=True)
    subprocess.run(
        'fastqc -o ' + output_path + ' ' + output_path + 'fastp_r1.fastq -t 10'
        , shell=True)
    subprocess.run(
        'fastqc -o ' + output_path + ' ' + output_path + 'fastp_r2.fastq -t 10'
        , shell=True)


def rename_assembly(out_path):
    data = open(out_path + "spades_result_unique_new/scaffolds.fasta", "r").readlines()
    data_out = open(out_path + "spades_result_unique_new/assembly.fasta", "w")
    count = 1
    for i in range(len(data)):
        if data[i][0] == ">":
            data_out.writelines(">" + str(count) + "\n")
            count += 1
        else:
            data_out.writelines(data[i])
    data_out.close()

    with open(out_path + "spades_result_unique_new/assembly.fasta") as f:
        Dict = {}
        for line in f:
            line = line.strip()
            if line[0] == ">":
                key = line
                Dict[key] = []
            else:
                Dict[key].append(line)

        with open(out_path + "spades_result_unique_new/output_with_depth_table_1.txt", 'w') as table:
            with open(out_path + "spades_result_unique_new/outfile_genome.txt", 'w') as genome:
                #table.write("\tBase(bp)\tGC%\tStructure\n")
                for key, value in Dict.items():
                    if key[0] == ">":
                        name = key[1:]
                        seq = ''.join(value)
                        genome.write("{}\n{}\n".format(key, seq))
                        # write table
                        length = len(seq)
                        gc_percent = format((seq.count("G") + seq.count("C")) / length * 100, '0.2f')
                        # print("\033[32m{}\t{}\033[0m".format(key, length))
                        table.write("contig_{}\t{}\t{}\tChromosome\n".format(name, length, gc_percent))
     
    subprocess.run("sort -t $'\t' -k2,2nr "+ out_path + "/spades_result_unique_new/output_with_depth_table_1.txt > "+ out_path+ "/spades_result_unique_new/output_with_depth_table.txt", shell=True)
    data_new = open(out_path+"/spades_result_unique_new/output_with_depth_table.txt","r").readlines()       
    data_new.insert(0,"\tBase(bp)\tGC%\tStructure\n")
    with open(out_path+"/spades_result_unique_new/output_with_depth_table.txt", 'w', encoding='utf-8') as file:  
        file.writelines(data_new)
    '''
      output_file = open(out_path + "spades_result_unique_new/output_with_depth_table_1.txt","r").readlines()
      headLine=output_file[0]
      outresult=output_file[1:]
      output_file_sort = out_path + "spades_result_unique_new/output_with_depth_table.txt"
      
      with open(output_file_sort, 'w') as writersort:
          writersort.write(headLine)
          writersort.write(''.join(sorted(outresult, key=lambda s: int(s.split("\t")[1]))))
    '''
    data = open(out_path + "spades_result_unique_new/scaffolds.fasta", "r").readlines()
    data_out = open(out_path + "spades_result_unique_new/coverage.txt", "w")
    for line in data:
        if line[0] == ">":
            data_out.writelines(line)
    data_out.close()
    
def readN(path,length_threshold):
    if os.path.exists(path + '/spades_result_unique_new/output_with_depth_table.txt'):
        with open(path + '/spades_result_unique_new/output_with_depth_table.txt', 'r') as file:
            # 按行读取文件内容
            lines = file.readlines()
            lines.pop(0)
            list=[]
            # 打印每一行的内容
            for line in lines:
                nums = line.split('\t')
                length = int(nums[1])
                idStr = nums[0].replace(" ","").split('_')[1]
                #map[idStr]=length
                a=[]
                a.append(int(idStr))
                a.append(length)
                list.append(a)
            list=sorted(list,key=lambda x: x[1], reverse=True)
            for line in list:
                if line[1] < length_threshold:
                    return line[0]            
    return -1    
    
def filt(args):
    file_r1 = args.workingSpace + "unique_R1.fastq"
    file_r2 = args.workingSpace + "unique_R2.fastq"
    file_i1 = args.workingSpace + "unique_I1.fastq"
    file_w = args.workingSpace + 'file_w.txt'
    out_path = args.workingSpace
    my_class = filter_data(args.workingSpace, args.workingSpace + "unique_R1.fastq",
                           args.workingSpace + "unique_R2.fastq", args.workingSpace + "unique_I1.fastq",
                           args.workingSpace + 'file_w.txt')
    my_class.summary_barcode(file_r1, file_w)
    my_class.re_get_reads(file_r1, file_r2, file_i1, out_path)
    my_class.remove_wrong_barcode(out_path)
    my_class.cut_adapter_and_fastp(out_path)
    my_class.get_final_corrected_reads(out_path)
    my_class.add_index(out_path)
def spadesRun(args):
    subprocess.run(
        './SPAdes-3.15.5-Linux/bin/spades.py -1 ' + args.workingSpace + '/fastp_r1.fastq -2 ' + args.workingSpace + '/fastp_r2.fastq -o ' +
        args.workingSpace + '/spades_result_unique_new/ -k 21 25 33 55 71 77 115'
        , shell=True)
def bwaAndSeparate(args,n):
    my_class1 = bwa_and_separate(args.workingSpace, n)
    #my_class1.bwa_result()
    get_plasmids(args)
    my_class1.separate_and_clear(args,n)
def Barcode_info_run(path_bam, file_path, start, n, num, c, file_compare):
    my_class0 = Barcode_info(path_bam, file_path, start, n, num, c, file_compare)
    my_class0.create_file(file_path, n)
    my_class0.get_front_barcode_info(path_bam, file_path, start, n, num)
    my_class0.get_back_barcode_info(path_bam, file_path, start, num)
    my_class0.design_file_intbar(file_path, n, start, num)
    my_class0.barcode_bwa_set(file_path, n, start)
    my_class0.barcode_bwa_number(file_path, n, start)
    my_class0.barcode_bwa_set_few(file_path, n, start)
    my_class0.auto_barcode_intersection_sort(file_path, n, start)
    my_class0.auto_intersection_count_sort(file_path, n, start)
    my_class0.mv_file(file_compare, n)
    my_class0.remove_occur_once(file_path, n, start)
    my_class0.remove_more_than_k(file_path, n, c)
    my_class0.get_int_barcode_set(file_path, n, start)
    my_class0.get_dir_barcode_set(file_path, n, start)
    my_class0.auto_barcode_intersection(file_path, n, start)
    my_class0.auto_intersection_count(file_path, n, start)
    my_class0.auto_barcode_union(file_path, n, start)
    my_class0.barcode_intersection_len(file_path, n, start)
    my_class0.barcode_union_len(file_path, n, start)
    my_class0.get_jaccard_corr(file_path, n, start)
    my_class0.all_count_of_contig_each(file_path, n, start)
    my_class0.barcode_total_number(file_path, n, start)
    my_class0.get_sorensen_dice(file_path, n, start)
def front_info_run(file_path, file_path_in, n, start, c, file_compare):
    my_class2 = front_info(file_path, file_path_in, n, start, c, file_compare)
    my_class2.create_file(file_path_in, n)
    my_class2.design_file_intbar(file_path, file_path_in, n, start)
    my_class2.barcode_bwa_set(file_path_in, n, start)
    my_class2.barcode_bwa_number(file_path_in, n, start)
    my_class2.barcode_bwa_set_few(file_path_in, n, start)
    my_class2.auto_barcode_intersection_sort(file_path_in, n, start)
    my_class2.auto_intersection_count_sort(file_path_in, n, start)
    my_class2.mv_file(file_compare, n)
    my_class2.combine_file(file_path_in, n, start)
    my_class2.sort_useful_info(file_path_in, c)
    my_class2.get_int_barcode_set(file_path_in, n, start)
    my_class2.get_dir_barcode_set(file_path_in, n, start)
    my_class2.auto_barcode_intersection(file_path_in, n, start)
    my_class2.auto_intersection_count(file_path_in, n, start)
    my_class2.all_count_of_contig_each(file_path_in, n, start)
    my_class2.barcode_total_number(file_path_in, n, start)
    my_class2.get_sorensen_dice(file_path_in, n, start)
    my_class2.auto_barcode_union(file_path_in, n, start)
    my_class2.barcode_intersection_len(file_path_in, n, start)
    my_class2.barcode_union_len(file_path_in, n, start)
    my_class2.get_jaccard(file_path_in, n, start)
def back_info_run(file_path, file_path_in, n, start, c, file_compare):
    my_class3 = back_info(file_path, file_path_in, n, start, c, file_compare)
    my_class3.create_file(file_path_in, n)
    my_class3.design_file_intbar(file_path, file_path_in, n, start)
    my_class3.barcode_bwa_set(file_path_in, n, start)
    my_class3.barcode_bwa_number(file_path_in, n, start)
    my_class3.barcode_bwa_set_few(file_path_in, n, start)
    my_class3.auto_barcode_intersection_sort(file_path_in, n, start)
    my_class3.auto_intersection_count_sort(file_path_in, n, start)
    my_class3.mv_file(file_compare, n)
    my_class3.combine_file(file_path_in, n, start)
    my_class3.sort_useful_info(file_path_in, c)
    my_class3.get_int_barcode_set(file_path_in, n, start)
    my_class3.get_dir_barcode_set(file_path_in, n, start)
    my_class3.auto_barcode_intersection(file_path_in, n, start)
    my_class3.auto_intersection_count(file_path_in, n, start)
    my_class3.all_count_of_contig_each(file_path_in, n, start)
    my_class3.barcode_total_number(file_path_in, n, start)
    my_class3.get_sorensen_dice(file_path_in, n, start)
    my_class3.auto_barcode_union(file_path_in, n, start)
    my_class3.barcode_intersection_len(file_path_in, n, start)
    my_class3.barcode_union_len(file_path_in, n, start)
    my_class3.get_jaccard(file_path_in, n, start)
def barcode_info_run(file_path, file_path_in, n, num, start):
    my_class4 = barcode_info(file_path, file_path_in, n, num, start)
    my_class4.create_file(file_path_in, n)
    my_class4.get_front_barcode_info(file_path, file_path_in, n, num, start)
    my_class4.get_back_barcode_info(file_path, file_path_in, start, n, num)
    my_class4.barcode_bwa_set(file_path_in, n, start)
    my_class4.barcode_bwa_set_1(file_path_in, n, start)
    my_class4.barcode_bwa_number(file_path_in, n, start)
    my_class4.barcode_bwa_number_1(file_path_in, n, start)
    my_class4.barcode_bwa_set_few(file_path_in, n, start)
    my_class4.barcode_bwa_set_few_1(file_path_in, n, start)
    my_class4.auto_barcode_intersection_sort(file_path_in, n, start)
    my_class4.auto_intersection_count_sort(file_path_in, n, start)
    my_class4.auto_barcode_intersection_sort_1(file_path_in, n, start)
    my_class4.auto_intersection_count_sort_1(file_path_in, n, start)
def fb_run(file_path_in, n, start, file_compare1, file_compare2, c):
    my_class5 = F_B(file_path_in, n, start, file_compare1, file_compare2, c)
    my_class5.mv_file(file_compare1, n, file_compare2)
    my_class5.combine_file(file_path_in, n, start)
    my_class5.sort_useful_info(file_path_in, n, c)
    my_class5.get_int_barcode_set(file_path_in, n, start)
    my_class5.get_dir_barcode_set(file_path_in, n, start)
    my_class5.get_useful_back_file(file_path_in, n, start)
    my_class5.sort_useless_back_info(file_path_in, c)
    my_class5.get_new_final_barcode_set(file_path_in, n, start)
    my_class5.get_new_dir_barcode_set(file_path_in, n, start)
    my_class5.auto_barcode_intersection_sort(file_path_in, n, start)
    my_class5.auto_intersection_count_sort(file_path_in, n, start)
    my_class5.auto_barcode_union(file_path_in, n, start)
    my_class5.barcode_intersection_len(file_path_in, n, start)
    my_class5.barcode_union_len(file_path_in, n, start)
    my_class5.get_jaccard(file_path_in, n, start)
    my_class5.all_count_of_contig_each(file_path_in, n, start)
    my_class5.barcode_total_number(file_path_in, n, start)
    my_class5.get_sorensen_dice(file_path_in, n, start)
def bf_run(file_path_in, n, start, c):
    my_class6 = B_F(file_path_in, n, start, c)
    my_class6.combine_file(file_path_in, n, start)
    my_class6.sort_useful_info(file_path_in, n, c)
    my_class6.get_int_barcode_set(file_path_in, n, start)
    my_class6.get_dir_barcode_set(file_path_in, n, start)
    my_class6.get_useful_back_file(file_path_in, n, start)
    my_class6.sort_useless_back_info(file_path_in, c)
    my_class6.get_new_final_barcode_set(file_path_in, n, start)
    my_class6.get_new_dir_barcode_set(file_path_in, n, start)
    my_class6.auto_barcode_intersection_sort(file_path_in, n, start)
    my_class6.auto_intersection_count_sort(file_path_in, n, start)
    my_class6.auto_barcode_union(file_path_in, n, start)
    my_class6.barcode_intersection_len(file_path_in, n, start)
    my_class6.barcode_union_len(file_path_in, n, start)
    my_class6.get_jaccard(file_path_in, n, start)
    my_class6.all_count_of_contig_each(file_path_in, n, start)
    my_class6.barcode_total_number(file_path_in, n, start)
    my_class6.get_sorensen_dice(file_path_in, n, start)
def get_label_list(file_path, start):
    my_class7 = Feature_extract(file_path, start)
    my_class7.get_pair_info(file_path, start)
    my_class7.feature_extract(file_path)
    my_class7.get_label(file_path)
def get_blast(args):
    #process = subprocess.Popen(['sh', shell_script_path])  # 如果shell_script_path是可执行的，可以直接使用它
    # 等待shell脚本执行完成
    process = subprocess.Popen(
        'sh ./scripts/generateBlastResult.sh ' + args.workingSpace + "/spades_result_unique_new/assembly.fasta "
        + args.workingSpace + "/spades_result_unique_new/get_different_contig "
        + args.workingSpace + "/blast_connection "
        + args.workingSpace
        , shell=True)
    print('get_blast ................')
    process.wait()
    print('get_blast finish')

def get_plasmids(args):
    
    subprocess.run(
        './pkgs/PlasFlow/filter_sequences_by_length.pl -input ' + args.workingSpace + "/spades_result_unique_new/scaffolds.fasta -output " +
        args.workingSpace + "/spades_result_unique_new/filter_scaffolds.fasta -thresh 1000"
        , shell=True)
    subprocess.run(
        "./pkgs/PlasFlow/PlasFlow.py --input " + args.workingSpace + "/spades_result_unique_new/filter_scaffolds.fasta --output " + args.workingSpace + "/spades_result_unique_new/plasflow_prediction.tsv --threshold 0.7"
        , shell=True)
    
    data_in = open(args.workingSpace +"/spades_result_unique_new/plasflow_prediction.tsv_plasmids.fasta" , "r").readlines()
    data_out = open(args.workingSpace +"/spades_result_unique_new/prediction_plasmid_plasflow.txt", "w")
    for line in data_in:
        if "NODE" in line:
            data_out.writelines(line)
    data_out.close()
if __name__ == '__main__':
    # 解析参数
    args=processArgs()   
    # 去重
    unique_reads(args.workingSpace+'/', args.i1, args.r1,args.r2)
    # 过滤
    filt(args)
    #质量评估
    qualityAssessment(args.workingSpace+'/')
    
    
    #spades
    spadesRun(args)
    #整理spades得到初步组装的结果
    rename_assembly(args.workingSpace+'/')
    
    #解析contig边界
    n=0
    n=readN(args.workingSpace,args.lengthThreshold)
    if(n==-1):
        print("generate n error")
        sys.exit()
    else:
        print('n='+str(n))
    
    #BWA比对并分别获取每个contig对应的比对信息，去除低质量的contigs：
    bwaAndSeparate(args,n)
    #确定contigs之间的配对信息和方向信息：
    #1)得到整体contigs之间的相似度度量矩阵
    Barcode_info_run(args.workingSpace+'/spades_result_unique_new/', args.workingSpace+'/spades_result_unique_new/', args.start, n, args.num, args.c1, args.workingSpace+'/spades_result_unique_new/compare_before_(file_4)')
    #2)得到前端方向信息的相似度度量矩阵
    front_info_run(args.workingSpace+'/spades_result_unique_new/', args.workingSpace+'/spades_result_unique_new/ff_list/', n, args.start, args.c2, args.workingSpace+'/spades_result_unique_new/ff_list/compare_before/')
    #3)得到后端方向信息的相似度度量矩阵
    back_info_run(args.workingSpace+'/spades_result_unique_new/', args.workingSpace+'/spades_result_unique_new/bb_list/', n, args.start, args.c2, args.workingSpace+'/spades_result_unique_new/bb_list/compare_before/')
    #得到前端—后端方向信息的相似度度量矩阵和后端—前端方向信息的相似度度量矩阵
    barcode_info_run(args.workingSpace+'/spades_result_unique_new/', args.workingSpace+'/spades_result_unique_new/fb_and_bf_list/', n, args.num, args.start)
    #F_B
    fb_run(args.workingSpace+'/spades_result_unique_new/fb_and_bf_list/', n, args.start, args.workingSpace+'/spades_result_unique_new/fb_and_bf_list/compare_before(f-b)', args.workingSpace+'/spades_result_unique_new/fb_and_bf_list/compare_before(b-f)', args.c1)
    #b_f
    bf_run(args.workingSpace+'/spades_result_unique_new/fb_and_bf_list/', n, args.start, args.c1)
    #得到label_list(jaccard).txt：
    get_label_list(args.workingSpace+'/spades_result_unique_new/', args.start)
    
    #得到延申需要的blast结果：  # todo 并行
    get_blast(args)
    
    #拼接、延伸、生成序列图及信息
    generateSeries(args)
