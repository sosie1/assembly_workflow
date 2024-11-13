import subprocess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import math


class bwa_and_separate:
    def __init__(self, out_path, n):
        self.out_path = out_path
        self.n = n

    def bwa_result(self):
        subprocess.run(
            'sh ./scripts/bwa_and_separate.sh ' + self.out_path
            , shell=True)

    def separate_and_clear(self,args,n):
        import matplotlib
        matplotlib.use('Agg')
        data_in = open(self.out_path + "spades_result_unique_new/coverage.txt", "r").readlines()
        data_out = open(self.out_path + "spades_result_unique_new/coverage_pair_info.txt", "w")
        for line in data_in:
            name = line.split("_")[1]
            cov = line.split("_")[5]
            data_out.writelines(name + "\t" + cov)
        data_out.close()

        data = open(self.out_path + "spades_result_unique_new/coverage_pair_info.txt", "r").readlines()
        cov_whole = 0
        index = 0
        while index < 9:
            cov_whole += float(data[index].split("\t")[1][:-1])
            index += 1

        cov_list = []
        for i in range(0, 10):
            cov_list.append(float(data[index].split("\t")[1][:-1]))
        # add_new_content
        x = []
        y = []
        for line in data:
            x.append(int(line.split("\t")[0]))
            y.append(float(line.split("\t")[1][:-1]) + 0.00000001)

        logy = np.log10(y)
        avg = np.mean(logy)
        std = np.std(logy)
        print(avg, std)
        dirn = {}
        for i in range(len(x)):
            dirn[x[i]] = logy[i]

        sns.kdeplot(logy)
        plt.savefig(self.out_path + 'spades_result_unique_new/cov_new.png')

        gmm = GaussianMixture(n_components=2)
        gmm.fit(logy.reshape(-1, 1))
        means = gmm.means_
        standard_deviations = gmm.covariances_ ** 0.5
        weights = gmm.weights_
        # print(f"Means: {means}, Standard Deviations: {standard_deviations},Weights:{weights}")
        means = list(np.concatenate(means.reshape((-1, 1), order="F")))
        standard_deviations = list(np.concatenate(standard_deviations.reshape((-1, 1), order="F")))
        dir_gauss = {}
        for i in range(2):
            dir_gauss[i] = [means[i] - 1, standard_deviations[i]]
        # print(dir_gauss)

        length = open(self.out_path + "spades_result_unique_new/output_with_depth_table.txt", "r").readlines()
        length_list = []
        sum_length = 0
        for i in range(1, 11):
            length_list.append(int(length[i].split("\t")[1]))
            sum_length += int(length[i].split("\t")[1])
        min_length = min(length_list)
        jiaquan_mean = 0
        for i in range(len(logy)):
            jiaquan_mean += logy[i] * length_list[i] / sum_length

        jiaquan_mean_new = 0
        for i in range(len(length_list)):
            jiaquan_mean_new += length_list[i] * ((logy[i] - jiaquan_mean) ** 2)

        import math
        std0 = math.sqrt(jiaquan_mean_new / (sum_length * 9 / 10))
        std1 = math.sqrt(min_length / int(args.lengthThreshold))

        low = jiaquan_mean - std0 * 1.96 * std1
        high = jiaquan_mean + std0 * 1.96 * std1

        # low = cov_whole//20
        # high = cov_whole*3//20

        print("low_coverage_threshold:" + str(low), "high_coverage_threshold:" + str(high))

        name_list = []
        duplication_list = []
        for i in range(len(data)):
            name = data[i].split()[0]
            cov = data[i].split()[1]
            if float(low) < float(cov):
                name_list.append(name)

        for i in range(len(data)):
            name = data[i].split()[0]
            cov = data[i].split()[1]
            if float(cov) >= float(high):
                duplication_list.append(name)

        name_dir = {}
        for k, v in enumerate(name_list):
            name_dir[v] = k

        out_duplication_txt = open(self.out_path + "duplication_name_list.txt", "w")
        for index in duplication_list:
            out_duplication_txt.writelines(str(index) + "\n")
        out_duplication_txt.close()

        efficient_id = open(self.out_path + "efficient_id.txt", "w")
        for e in name_list:
            efficient_id.writelines(str(e) + "\n")
        efficient_id.close()

        length = open(self.out_path + "spades_result_unique_new/output_with_depth_table.txt", "r").readlines()
        # this step need file(prediction_plasmid_plasflow.txt)--so we need run plasflow
        # new_code
        large_contig_name = []
        for i in range(1, n):
            large_contig_name.append(length[i].split("\t")[0].split("_")[1])
        print(large_contig_name)

        plasmids_data = open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow.txt",
                             "r").readlines()
        data_out = open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow_bak.txt", "w")
        for line in plasmids_data:
            lastD = line.split("_")[-1]
            x = float(lastD)
            if x>=low :
                data_out.writelines(line)
        data_in = open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow_bak.txt",
                             "r").readlines()
        with open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow.txt", 'w') as file:
            pass
        data_out = open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow.txt", "w")
        for line in data_in:
            data_out.writelines(line)
        plasmids_data = open(self.out_path + "spades_result_unique_new/prediction_plasmid_plasflow.txt",
                             "r").readlines()
        plasmids_name = []
        for line in plasmids_data:
            plasmids_name.append(line.split("_")[1])

        name_interaction = list(set(duplication_list) & set(large_contig_name))
        name_inter_final = list(set(name_interaction) - set(plasmids_name))
        print(name_interaction)
        print(name_inter_final)

        large_contig_txt = open(self.out_path + "duplicated_long_contigs_name.txt", "w")
        for name in name_inter_final:
            large_contig_txt.writelines(name + "\n")
        large_contig_txt.close()

        data = open(self.out_path + "spades_result_unique_new/full_final_unique_out.info.txt", "r").readlines()
        j = 1
        while j < n:
            if str(j) in name_dir:
                data_out = open(
                    self.out_path + "spades_result_unique_new/get_bam_info/final_out_" + str(j) + ".info.txt", "w")
                for i in range(len(data)):
                    if int(data[i].split("\t")[2]) == j:
                        data_out.writelines(data[i])
                data_out.close()
                j += 1
            else:
                data_out = open(
                    self.out_path + "spades_result_unique_new/get_bam_info/final_out_" + str(j) + ".info.txt", "w")
                data_out.writelines("")
                data_out.close()
                j += 1


class filter_data:
    def __init__(self, out_path, file_r1, file_r2, file_i1, file_w):
        self.out_path = out_path
        self.file_r1 = file_r1
        self.file_r2 = file_r2
        self.file_i1 = file_i1
        self.file_w = file_w

    def summary_barcode(self, file_r1, file_w):
        data = open(self.file_r1, "r").readlines()
        print("total_number_of_read:" + str(len(data) // 4))
        file_write = open(self.file_w, "w")
        name_list = []
        for i in range(len(data)):
            if data[i][0] == "@":
                name_list.append(data[i + 1][:-1])
        from collections import Counter
        number_dir = Counter(name_list)

        number_sort = sorted(number_dir.items(), key=lambda x: x[1], reverse=True)
        print('reads_with_barcode_all_Gs:' + str(number_sort[0][1]))
        for i in range(len(number_sort)):
            line = number_sort[i][0] + "\t" + str(number_sort[i][1]) + "\n"
            file_write.writelines(line)
        file_write.close()

        index = data[0].split()[1].split(":")[3][:-1]

        data = open(self.file_w, "r").readlines()
        barcode_catagory_count = len(data)
        unique_barcode = 0
        more_than_three = 0
        read_with_more_than_three = 0
        all_reads = 0
        for line in data:
            name = line.split()[0]
            count = int(line.split()[1])
            all_reads += count
            if count == 1:
                unique_barcode += 1
            elif count >= 3:
                more_than_three += 1
                read_with_more_than_three += count
        print("all_reads:" + str(all_reads))
        print("unique_barcode:" + str(unique_barcode))
        print("more_than_three:" + str(more_than_three))
        print("read_with_more_than_three:" + str(read_with_more_than_three))
        print("barcode_catagory_count:" + str(barcode_catagory_count))

    def re_get_reads(self, file_r1, file_r2, file_i1, out_path):
        data_I1 = open(self.file_i1, "r").readlines()
        data_R1 = open(self.file_r1, "r").readlines()
        data_R2 = open(self.file_r2, "r").readlines()
        I1 = open(self.out_path + "reget_I1.fastq", "w")
        R1 = open(self.out_path + "reget_R1.fastq", "w")
        R2 = open(self.out_path + "reget_R2.fastq", "w")
        for i in range(len(data_I1)):
            if i % 4 == 0:
                name = data_I1[i].split()[0]
                I1.writelines(name + "\n" + data_I1[i + 1] + data_I1[i + 2] + data_I1[i + 3])
                R1.writelines(name + "\n" + data_R1[i + 1] + data_R1[i + 2] + data_R1[i + 3])
                R2.writelines(name + "\n" + data_R2[i + 1] + data_R2[i + 2] + data_R2[i + 3])
        I1.close()
        R1.close()
        R2.close()

    def remove_wrong_barcode(self, out_path):
        H = ['A', 'C', 'T']
        Y = ['C', 'T']
        R = ['A', 'G']
        I1 = open(self.out_path + "reget_I1.fastq", "r").readlines()
        R1 = open(self.out_path + "reget_R1.fastq", "r").readlines()
        R2 = open(self.out_path + "reget_R2.fastq", "r").readlines()
        correct_index = []
        i1 = open(self.out_path + "correct_I1.fastq", "w")
        r1 = open(self.out_path + "correct_R1.fastq", "w")
        r2 = open(self.out_path + "correct_R2.fastq", "w")
        one_mismatch_barcode_num = 0
        for i in range(len(I1)):
            if i % 4 == 1:
                position_1 = I1[i][2]
                position_2 = I1[i][5]
                position_3 = I1[i][6]
                position_4 = I1[i][11]
                position_5 = I1[i][12]
                position_6 = I1[i][15]
                if position_1 in H and position_6 in H and position_2 in Y and position_3 in R and position_4 in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                elif position_1 not in H and position_6 in H and position_2 in Y and position_3 in R and position_4 in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
                elif position_1 in H and position_6 not in H and position_2 in Y and position_3 in R and position_4 in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
                elif position_1 in H and position_6 in H and position_2 not in Y and position_3 in R and position_4 in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
                elif position_1 in H and position_6 in H and position_2 in Y and position_3 not in R and position_4 in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
                elif position_1 in H and position_6 in H and position_2 in Y and position_3 in R and position_4 not in Y and position_5 in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
                elif position_1 in H and position_6 in H and position_2 in Y and position_3 in R and position_4 in Y and position_5 not in R:
                    correct_index.append(i)
                    i1.writelines(I1[i - 1] + I1[i] + I1[i + 1] + I1[i + 2])
                    r1.writelines(R1[i - 1] + R1[i] + R1[i + 1] + R1[i + 2])
                    r2.writelines(R2[i - 1] + R2[i] + R2[i + 1] + R2[i + 2])
                    one_mismatch_barcode_num += 1
        i1.close()
        r1.close()
        r2.close()
        print(one_mismatch_barcode_num)

    def cut_adapter_and_fastp(self, out_path):

        subprocess.run(
            'sh ./scripts/cutadapt_fastp.sh ' +
            self.out_path, shell=True)

    def get_final_corrected_reads(self, out_path):
        original_i1 = open(self.out_path + 'reget_I1.fastq', "r").readlines()
        cut_r1_in = open(self.out_path + "fastp_r1.fastq", "r").readlines()
        cut_r2_in = open(self.out_path + "fastp_r2.fastq", "r").readlines()
        i1_in = open(self.out_path + 'correct_I1.fastq', "r").readlines()
        print("error_barcode_num:" + str(len(original_i1) // 4 - len(i1_in) // 4))
        name_list_before = []
        for line in i1_in:
            if line[0] == "@":
                name_list_before.append(line)
        name_list_after = []
        for line in cut_r1_in:
            if line[0] == "@":
                name_list_after.append(line)
        cut_i1_out = open(self.out_path + "fastp_i1.fastq", "w")
        name_intersection_list = list(set(name_list_before) & set(name_list_after))

        name_intersection_dir = {}
        for i, k in enumerate(name_intersection_list):
            name_intersection_dir[k] = i

        for i in range(len(i1_in)):
            if i % 4 == 0:
                if i1_in[i] in name_intersection_dir:
                    cut_i1_out.writelines(i1_in[i] + i1_in[i + 1] + i1_in[i + 2] + i1_in[i + 3])
        cut_i1_out.close()
        print("final_reads_num:" + str(len(cut_r1_in) // 4))

        data = open(self.out_path + "fastp_i1.fastq", "r").readlines()
        name_list = []
        for i in range(len(data)):
            if i % 4 == 1:
                name_list.append(data[i])
        set_name = set(name_list)
        print("final_correct_barcode_number:" + str(len(set_name)))

    def add_index(self, out_path):
        R1 = open(self.out_path + "fastp_r1.fastq", "r").readlines()
        R2 = open(self.out_path + "fastp_r2.fastq", "r").readlines()
        i1 = open(self.out_path + "fastp_i1.fastq", "r").readlines()

        for i in range(len(R1)):
            if i % 4 == 1:
                R1[i - 1] = R1[i - 1][:-1] + ":" + "index:" + i1[i]
                R2[i - 1] = R2[i - 1][:-1] + ":" + "index:" + i1[i]

        R1_with_index = open(self.out_path + "R1_with_barcode_new.fastq", "w")
        for line in R1:
            R1_with_index.writelines(line)
        R1_with_index.close()

        R2_with_index = open(self.out_path + "R2_with_barcode_new.fastq", "w")
        for line in R2:
            R2_with_index.writelines(line)
        R2_with_index.close()