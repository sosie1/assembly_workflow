import numpy as np
import pandas as pd
class front_info:
    def __init__(self, file_path, file_path_in, n, start, c, file_compare):
        self.file_path = file_path
        self.file_path_in = file_path_in
        self.n = n
        self.start = start
        self.c = c
        self.file_compare = file_compare

    def create_file(self, file_path_in, n):
        import subprocess
        subprocess.run(['sh', './scripts/create_file1.sh', self.file_path_in,
                        str(self.n - 1)])

    def design_file_intbar(self, file_path, file_path_in, n, start):
        path = self.file_path + "bwa_original_barcode_name_(file_1)/"
        path_out = self.file_path_in + "front_barcode/"
        count = self.start
        while count < self.n:
            full_path = path_out + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'w')
            full_path_read = path + "front_barcode_info_of_contig" + str(count) + '.txt'
            file_read = open(full_path_read, "r").readlines()
            for line in file_read:
                file.writelines(str(line[:-1]) + "\n")

            file.close()
            count += 1

    def barcode_bwa_set(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "front_barcode/"
        path_out = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()

            full_path_write = path_out + "final_barcode_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            barcode_set = set(file)

            for line in barcode_set:
                file_write.writelines(line)

            count += 1

    def barcode_bwa_number(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "front_barcode/"
        path_out = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
            full_path_write = path_out + "final_barcode_dir_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            number_dir = Counter(file)
            number_sort = sorted(number_dir.items(), key=lambda x: x[1], reverse=True)
            for i in range(len(number_sort)):
                line = number_sort[i][0][:-1] + "\t" + str(number_sort[i][1]) + "\n"
                # if the number of barcode is more than 2, it will be removed.
                if number_sort[i][1] >= 2:
                    file_write.writelines(line)

            count += 1

    def barcode_bwa_set_few(self, file_path_in, n, start):
        from collections import Counter
        path_out = self.file_path_in + "set_remove_few/"
        path = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_dir_info" + str(count) + '.txt'
            file_read = open(full_path, 'r').readlines()

            file_write = open(path_out + "barcode_set_of_contig_" + str(count) + ".txt", "w")

            for i in range(len(file_read)):
                barcode_name = file_read[i].split("\t")[0]
                file_write.writelines(barcode_name + "\n")

            count += 1

    def auto_barcode_intersection_sort(self, file_path_in, n, start):
        path_in = self.file_path_in + "set_remove_few/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "barcode_set_of_contig_" + str(count) + "compare_to_contig_" + str(
                    j) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count_sort(self, file_path_in, n, start):
        path_in = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before/new_info_" + str(j) + "/"
            while count < self.n:
                full_path = path_in + "final_barcode_dir_info" + str(count) + ".txt"
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "barcode_set_of_contig_" + str(count) + "compare_to_contig_" + str(j) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
                count += 1

            count = self.start
            j += 1

    # filter
    def mv_file(self, file_compare, n):
        import subprocess
        subprocess.run(
            ['sh', './scripts/mv_file1.sh', self.file_compare, str(self.n - 1)])

    def combine_file(self, file_path_in, n, start):
        import os
        import linecache
        i = self.start
        while i < self.n:
            root = self.file_path_in + "compare_before/new_info_" + str(i) + "/compara_to_contig"
            file_names = os.listdir(root)

            file_ob_list = []
            for file_name in file_names:
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

            data = []
            for file_ob in file_ob_list:
                line_num = 1
                length_file = len(open(file_ob, "r").readlines())
                while line_num <= length_file:
                    line = linecache.getline(file_ob, line_num)
                    data.append(line)
                    line_num = line_num + 1
                line_num = 1

            f = open(self.file_path_in + "remove_occur_once/sort_barcode_" + str(i) + ".txt", 'w')
            data_new = list(set(data))
            for k in data_new:
                f.write(k)
            i += 1
            f.close()

    def sort_useful_info(self, file_path_in, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "remove_occur_once/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            fileob = root + '/' + file_name
            file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if v <= self.c}

        f = open(self.file_path_in + "barcode_set_all.txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    def get_int_barcode_set(self, file_path_in, start):
        path = self.file_path_in + "remove_occur_once/"
        path_in = self.file_path_in + "barcode_set_all.txt"
        path_out = self.file_path_in + "final_int_barcode/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "sort_barcode_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "barcode_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode/"
        path_in = self.file_path_in + "bwa_dir_and_set/"
        path_out = self.file_path_in + "final_dir_barcode/"

        count = self.start
        while count < self.n:
            file_1 = open(path_in + "final_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "barcode_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path_out + "barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    def auto_barcode_intersection(self, file_path_in, n, start):
        path_in = self.file_path_in + "final_int_barcode/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compara_file_final_int/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count(self, file_path_in, n, start):
        path_in = self.file_path_in + "final_dir_barcode/"
        count = self.start
        j = self.start
        while j < self.n:
            while count < self.n:
                path_out = self.file_path_in + "compara_file_final_dir/new_info_" + str(j) + "/"
                path = self.file_path_in + "compara_file_final_int/new_info_" + str(j) + "/"

                full_path = path_in + "barcode_dir_contig_" + str(count) + ".txt"
                file = open(full_path, 'r').readlines()

                full_path_1 = path + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])

                count += 1

            count = self.start
            j += 1

    # get_matrix
    def all_count_of_contig_each(self, file_path_in, n, start):
        path = self.file_path_in + "final_dir_barcode/"
        total_all_info = [[] for _ in range(self.start, self.n)]
        count = self.start
        j = self.start - 1
        while j < self.n - 1:
            while count < self.n:
                path_A = path + "barcode_dir_contig_" + str(j + 1) + ".txt"
                path_B = path + "barcode_dir_contig_" + str(count) + ".txt"
                file_A = open(path_A, "r").readlines()
                file_B = open(path_B, "r").readlines()
                sum_barcode_A = 0
                for i in range(len(file_A)):
                    sum_barcode_A += int(file_A[i].split("\t")[1][:-1])
                sum_barcode_B = 0
                for i in range(len(file_B)):
                    sum_barcode_B += int(file_B[i].split("\t")[1][:-1])
                sum_bar = sum_barcode_A + sum_barcode_B
                total_all_info[j - self.start + 1].append(sum_bar)
                count += 1

            count = self.start
            j += 1
        return total_all_info

    def barcode_total_number(self, file_path_in, n, start):
        count = self.start
        j = self.start - 1
        total_barcode_number = [[] for _ in range(self.start, self.n)]
        while j < self.n - 1:
            while count < self.n:
                path_in = self.file_path_in + "compara_file_final_dir/new_info_" + str(j + 1) + "/"
                path_number = path_in + "number_dir_" + str(count) + ".txt"
                file = open(path_number, "r").readlines()

                sum_barcode = 0
                for i in range(len(file)):
                    sum_barcode += int(file[i].split("\t")[1][:-1])
                total_barcode_number[j - self.start + 1].append(sum_barcode)
                count += 1

            count = self.start
            j += 1

        return total_barcode_number

    def get_sorensen_dice(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        total_all_info_list = self.all_count_of_contig_each(file_path_in, n, start)
        total_all_info_np = np.array(total_all_info_list)
        total_all_pd = pd.DataFrame(total_all_info_np, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])
        total_all_pd.to_csv(self.file_path_in + "add_count_barcode_matrix(front_front).csv", index=True, header=True)

        total_barcode_list = self.barcode_total_number(file_path_in, n, start)
        total_num = np.array(total_barcode_list)
        total_num_pd = pd.DataFrame(total_num, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])

        total_pd = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                total_pd.loc["contig" + str(i), "contig" + str(j)] = total_num_pd.loc[
                                                                         "contig" + str(i), "contig" + str(j)] + \
                                                                     total_num_pd.loc[
                                                                         "contig" + str(j), "contig" + str(i)]
        total_pd.to_csv(self.file_path_in + "compare_add_count_matrix(front_front).csv", index=True, header=True)

        Sorensen_Dice_rate = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                          index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                Sorensen_Dice_rate.loc["contig" + str(i), "contig" + str(j)] = total_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(
                                                                                       j)] / total_all_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(j)]

        Sorensen_Dice_rate.to_csv(self.file_path_in + "Sorensen_Dice_rate_matrix_more(front_front).csv", index=True,
                                  header=True)

    def auto_barcode_union(self, file_path_in, n, start):
        import pandas as pd
        path_in = self.file_path_in + "final_int_barcode/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "union_file_final_int/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) | set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def barcode_intersection_len(self, file_path_in, n, start):
        import pandas as pd
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < self.n:
                path_in = self.file_path_in + "compara_file_final_int/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def barcode_union_len(self, file_path_in, n, start):
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "union_file_final_int/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def get_jaccard(self, file_path_in, n, start):
        import numpy as np
        import seaborn as sns
        import pandas as pd
        import matplotlib.pyplot as plt
        info_1 = self.barcode_intersection_len(file_path_in, n, start)
        info_2 = self.barcode_union_len(file_path_in, n, start)
        info_1_array = np.array(info_1)
        info_2_array = np.array(info_2)
        df_1 = pd.DataFrame(info_1_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_2 = pd.DataFrame(info_2_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3 = df_1 / df_2
        df_3_pd = pd.DataFrame(df_3, columns=["contig" + str(i) for i in range(self.start, self.n)],
                               index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3_pd.to_csv(self.file_path_in + "manually_get_jaccard_matrix(f-f).csv", header=True, index=True)


class back_info:
    def __init__(self, file_path, file_path_in, n, start, c, file_compare):
        self.file_path = file_path
        self.file_path_in = file_path_in
        self.n = n
        self.start = start
        self.c = c
        self.file_compare = file_compare

    def create_file(self, file_path_in, n):
        import subprocess
        subprocess.run(['sh', './scripts/create_file2.sh', self.file_path_in,
                        str(self.n - 1)])

    def design_file_intbar(self, file_path, file_path_in, n, start):
        path = self.file_path + "bwa_original_barcode_name_(file_1)/"
        path_out = self.file_path_in + "back_barcode/"
        count = self.start
        while count < self.n:
            full_path = path_out + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'w')
            full_path_read = path + "back_barcode_info_of_contig" + str(count) + '.txt'
            file_read = open(full_path_read, "r").readlines()
            for line in file_read:
                file.writelines(str(line[:-1]) + "\n")

            file.close()
            count += 1

    def barcode_bwa_set(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "back_barcode/"
        path_out = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()

            full_path_write = path_out + "final_barcode_set_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            barcode_set = set(file)

            for line in barcode_set:
                file_write.writelines(line)

            count += 1

    def barcode_bwa_number(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "back_barcode/"
        path_out = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
            full_path_write = path_out + "final_barcode_dir_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            number_dir = Counter(file)
            number_sort = sorted(number_dir.items(), key=lambda x: x[1], reverse=True)
            for i in range(len(number_sort)):
                line = number_sort[i][0][:-1] + "\t" + str(number_sort[i][1]) + "\n"
                # if the number of barcode is more than 2, it will be removed.
                if number_sort[i][1] >= 2:
                    file_write.writelines(line)

            count += 1

    def barcode_bwa_set_few(self, file_path_in, n, start):
        from collections import Counter
        path_out = self.file_path_in + "set_remove_few/"
        path = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_dir_info" + str(count) + '.txt'
            file_read = open(full_path, 'r').readlines()

            file_write = open(path_out + "barcode_set_of_contig_" + str(count) + ".txt", "w")

            for i in range(len(file_read)):
                barcode_name = file_read[i].split("\t")[0]
                file_write.writelines(barcode_name + "\n")

            count += 1

            # get_compare_information_in_order_to_filter_useless_barcode

    def auto_barcode_intersection_sort(self, file_path_in, n, start):
        path_in = self.file_path_in + "set_remove_few/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "barcode_set_of_contig_" + str(count) + "compare_to_contig_" + str(
                    j) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count_sort(self, file_path_in, n, start):
        path_in = self.file_path_in + "bwa_dir_and_set/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before/new_info_" + str(j) + "/"
            while count < self.n:
                full_path = path_in + "final_barcode_dir_info" + str(count) + ".txt"
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "barcode_set_of_contig_" + str(count) + "compare_to_contig_" + str(j) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
                count += 1

            count = self.start
            j += 1

            # filter

    def mv_file(self, file_compare, n):
        import subprocess
        subprocess.run(
            ['sh', './scripts/mv_file2.sh', self.file_compare, str(self.n - 1)])

    def combine_file(self, file_path_in, n, start):
        import os
        import linecache
        i = self.start
        while i < self.n:
            root = self.file_path_in + "compare_before/new_info_" + str(i) + "/compara_to_contig"
            file_names = os.listdir(root)

            file_ob_list = []
            for file_name in file_names:
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

            data = []
            for file_ob in file_ob_list:
                line_num = 1
                length_file = len(open(file_ob, "r").readlines())
                while line_num <= length_file:
                    line = linecache.getline(file_ob, line_num)
                    data.append(line)
                    line_num = line_num + 1
                line_num = 1

            f = open(self.file_path_in + "remove_occur_once/sort_barcode_" + str(i) + ".txt", 'w')
            data_new = list(set(data))
            for k in data_new:
                f.write(k)
            i += 1
            f.close()

    def sort_useful_info(self, file_path_in, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "remove_occur_once/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            fileob = root + '/' + file_name
            file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if v <= self.c}

        f = open(self.file_path_in + "barcode_set_all.txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    def get_int_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "remove_occur_once/"
        path_in = self.file_path_in + "barcode_set_all.txt"
        path_out = self.file_path_in + "final_int_barcode/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "sort_barcode_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "barcode_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode/"
        path_in = self.file_path_in + "bwa_dir_and_set/"
        path_out = self.file_path_in + "final_dir_barcode/"

        count = self.start
        while count < self.n:
            file_1 = open(path_in + "final_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "barcode_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path_out + "barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    # get_final_compare_info    
    def auto_barcode_intersection(self, file_path_in, n, start):
        path_in = self.file_path_in + "final_int_barcode/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compara_file_final_int/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count(self, file_path_in, n, start):
        path_in = self.file_path_in + "final_dir_barcode/"
        count = self.start
        j = self.start
        while j < self.n:
            while count < self.n:
                path_out = self.file_path_in + "compara_file_final_dir/new_info_" + str(j) + "/"
                path = self.file_path_in + "compara_file_final_int/new_info_" + str(j) + "/"

                full_path = path_in + "barcode_dir_contig_" + str(count) + ".txt"
                file = open(full_path, 'r').readlines()

                full_path_1 = path + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])

                count += 1

            count = self.start
            j += 1

    # get_matrix
    def all_count_of_contig_each(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        path = self.file_path_in + "final_dir_barcode/"
        total_all_info = [[] for _ in range(self.start, self.n)]
        count = self.start
        j = self.start - 1
        while j < self.n - 1:
            while count < (self.n):
                path_A = path + "barcode_dir_contig_" + str(j + 1) + ".txt"
                path_B = path + "barcode_dir_contig_" + str(count) + ".txt"
                file_A = open(path_A, "r").readlines()
                file_B = open(path_B, "r").readlines()
                sum_barcode_A = 0
                for i in range(len(file_A)):
                    sum_barcode_A += int(file_A[i].split("\t")[1][:-1])
                sum_barcode_B = 0
                for i in range(len(file_B)):
                    sum_barcode_B += int(file_B[i].split("\t")[1][:-1])
                sum_bar = sum_barcode_A + sum_barcode_B
                total_all_info[j - self.start + 1].append(sum_bar)
                count += 1
            count = self.start
            j += 1
        return total_all_info

    def barcode_total_number(self, file_path_in, n, start):
        count = self.start
        j = self.start - 1
        total_barcode_number = [[] for _ in range(self.start, self.n)]
        while j < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "compara_file_final_dir/new_info_" + str(j + 1) + "/"
                path_number = path_in + "number_dir_" + str(count) + ".txt"
                file = open(path_number, "r").readlines()

                sum_barcode = 0
                for i in range(len(file)):
                    sum_barcode += int(file[i].split("\t")[1][:-1])
                total_barcode_number[j - self.start + 1].append(sum_barcode)
                count += 1

            count = self.start
            j += 1

        return total_barcode_number

    # get_sorensen_dice_matrix
    def get_sorensen_dice(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        total_all_info_list = self.all_count_of_contig_each(file_path_in, n, start)
        total_all_info_np = np.array(total_all_info_list)
        total_all_pd = pd.DataFrame(total_all_info_np, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])
        total_all_pd.to_csv(self.file_path_in + "add_count_barcode_matrix(back_back).csv", index=True, header=True)

        total_barcode_list = self.barcode_total_number(file_path_in, n, start)
        total_num = np.array(total_barcode_list)
        total_num_pd = pd.DataFrame(total_num, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])

        total_pd = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                total_pd.loc["contig" + str(i), "contig" + str(j)] = total_num_pd.loc[
                                                                         "contig" + str(i), "contig" + str(j)] + \
                                                                     total_num_pd.loc[
                                                                         "contig" + str(j), "contig" + str(i)]
        total_pd.to_csv(self.file_path_in + "compare_add_count_matrix(back_back).csv", index=True, header=True)

        Sorensen_Dice_rate = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                          index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                Sorensen_Dice_rate.loc["contig" + str(i), "contig" + str(j)] = total_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(
                                                                                       j)] / total_all_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(j)]

        Sorensen_Dice_rate.to_csv(self.file_path_in + "Sorensen_Dice_rate_matrix_more(back_back).csv", index=True,
                                  header=True)

    def auto_barcode_union(self, file_path_in, n, start):
        import pandas as pd
        path_in = self.file_path_in + "final_int_barcode/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "union_file_final_int/new_info_" + str(j) + "/"
            full_path = path_in + "barcode_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in + "barcode_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) | set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def barcode_intersection_len(self, file_path_in, n, start):
        import pandas as pd
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < self.n:
                path_in = self.file_path_in + "compara_file_final_int/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def barcode_union_len(self, file_path_in, n, start):
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "union_file_final_int/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def get_jaccard(self, file_path_in, n, start):

        info_1 = self.barcode_intersection_len(file_path_in, n, start)
        info_2 = self.barcode_union_len(file_path_in, n, start)
        info_1_array = np.array(info_1)
        info_2_array = np.array(info_2)
        df_1 = pd.DataFrame(info_1_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_2 = pd.DataFrame(info_2_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3 = df_1 / df_2
        df_3_pd = pd.DataFrame(df_3, columns=["contig" + str(i) for i in range(self.start, self.n)],
                               index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3_pd.to_csv(self.file_path_in + "manually_get_jaccard_matrix(b-b).csv", header=True, index=True)


# def main(file_path, file_path_in, n, start, c, file_compare):
#
# parser.add_argument('--file_path', type=str)
# parser.add_argument('--file_path_in', type=str)
# parser.add_argument('--n', type=int)
# parser.add_argument('--start', type=int)
# parser.add_argument('--c', type=int)
# parser.add_argument('--file_compare', type=str)
#
# args = parser.parse_args()
# if __name__ == '__main__':
#     main(args.file_path, args.file_path_in, args.n, args.start, args.c, args.file_compare)
class barcode_info:
    def __init__(self, file_path, file_path_in, n, num, start):
        self.file_path = file_path
        self.file_path_in = file_path_in
        self.n = n
        self.num = num
        self.start = start

    def create_file(self, file_path_in, n):
        import subprocess
        subprocess.run(['sh', './scripts/create_file3.sh', self.file_path_in,
                        str(self.n - 1)])

    def get_front_barcode_info(self, file_path, file_path_in, start, n, num):
        path = self.file_path + "get_bam_info/"
        path_out = self.file_path_in + "original_front_info/"

        length_data = open(self.file_path + "output_with_depth_table.txt", "r").readlines()
        length_list = {}
        for i in range(1, len(length_data)):
            name = length_data[i].split("\t")[0].split("_")[1]
            length = length_data[i].split("\t")[1]
            length_list[name] = int(length)

        for i in range(self.start, self.n):
            if length_list[str(i)] >= 2 * self.num:
                full_path = path + "final_out_" + str(i) + ".info.txt"
                file_read = open(full_path, "r").readlines()
                full_write_path = path_out + "front_barcode_info_of_contig" + str(i) + ".txt"
                file_write = open(full_write_path, "w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) <= self.num:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line + "\n")

            elif length_list[str(i)] < 2 * self.num:
                full_path = path + "final_out_" + str(i) + ".info.txt"
                file_read = open(full_path, "r").readlines()
                full_write_path = path_out + "front_barcode_info_of_contig" + str(i) + ".txt"
                file_write = open(full_write_path, "w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) <= (length_list[str(i)]) // 2:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line + "\n")

    def get_back_barcode_info(self, file_path, file_path_in, start, n, num):
        path = self.file_path + "get_bam_info/"
        path_out = self.file_path_in + "original_back_info/"
        length_data = open(self.file_path + "output_with_depth_table.txt", "r").readlines()
        length_list = {}
        for i in range(1, len(length_data)):
            name = length_data[i].split("\t")[0].split("_")[1]
            length = length_data[i].split("\t")[1]
            length_list[name] = int(length)
        print(length_list)

        for i in range(self.start, self.n):
            if length_list[str(i)] >= 2 * self.num:
                full_path = path + "final_out_" + str(i) + ".info.txt"
                file_read = open(full_path, "r").readlines()
                full_write_path = path_out + "back_barcode_info_of_contig" + str(i) + ".txt"
                file_write = open(full_write_path, "w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) >= int(int(length_list[str(i)]) - self.num):
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line + "\n")
                file_write.close()

            elif length_list[str(i)] < 2 * self.num:
                full_path = path + "final_out_" + str(i) + ".info.txt"
                file_read = open(full_path, "r").readlines()
                full_write_path = path_out + "back_barcode_info_of_contig" + str(i) + ".txt"
                file_write = open(full_write_path, "w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) >= (length_list[str(i)]) // 2:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line + "\n")
                file_write.close()

    def barcode_bwa_set(self, file_path_in, n, start):
        path = self.file_path_in + "original_front_info/"
        path_out = self.file_path_in + "bwa_set_count_front/"
        count = self.start
        while count < self.n:
            full_path = path + "front_barcode_info_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()

            full_path_write = path_out + "front_barcode_int_set_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            barcode_set = set(file)

            for line in barcode_set:
                file_write.writelines(line)

            count += 1

    def barcode_bwa_set_1(self, file_path_in, n, start):
        path = self.file_path_in + "original_back_info/"
        path_out = self.file_path_in + "bwa_set_count_back/"
        count = self.start
        while count < self.n:
            full_path = path + "back_barcode_info_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()

            full_path_write = path_out + "back_barcode_int_set_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            barcode_set = set(file)

            for line in barcode_set:
                file_write.writelines(line)

            count += 1

    # if the barcode only occurs once, it will be remove. so there is already a step to filter useless barcodes.
    def barcode_bwa_number(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "original_front_info/"
        path_out = self.file_path_in + "bwa_dir_of_int_front/"
        count = self.start
        while count < self.n:
            full_path = path + "front_barcode_info_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
            full_path_write = path_out + "front_barcode_dir_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            number_dir = Counter(file)
            number_sort = sorted(number_dir.items(), key=lambda x: x[1], reverse=True)
            for i in range(len(number_sort)):
                line = number_sort[i][0][:-1] + "\t" + str(number_sort[i][1]) + "\n"
                if int(number_sort[i][1]) >= 2:
                    file_write.writelines(line)

            count += 1

    def barcode_bwa_number_1(self, file_path_in, n, start):
        from collections import Counter
        path = self.file_path_in + "original_back_info/"
        path_out = self.file_path_in + "bwa_dir_of_int_back/"
        count = self.start
        while count < self.n:
            full_path = path + "back_barcode_info_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
            full_path_write = path_out + "back_barcode_dir_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            number_dir = Counter(file)
            number_sort = sorted(number_dir.items(), key=lambda x: x[1], reverse=True)
            for i in range(len(number_sort)):
                line = number_sort[i][0][:-1] + "\t" + str(number_sort[i][1]) + "\n"
                if int(number_sort[i][1]) >= 2:
                    file_write.writelines(line)

            count += 1

    def barcode_bwa_set_few(self, file_path_in, n, start):
        from collections import Counter
        path_out = self.file_path_in + "int_set_remove_few_front/"
        path = self.file_path_in + "bwa_dir_of_int_front/"
        count = self.start
        while count < self.n:
            full_path = path + "front_barcode_dir_info" + str(count) + '.txt'
            file_read = open(full_path, 'r').readlines()

            file_write = open(path_out + "front_int_set_of_contig_" + str(count) + ".txt", "w")
            for i in range(len(file_read)):
                barcode_name = file_read[i].split("\t")[0]
                file_write.writelines(barcode_name + "\n")

            count += 1

    def barcode_bwa_set_few_1(self, file_path_in, n, start):
        from collections import Counter
        path_out = self.file_path_in + "int_set_remove_few_back/"
        path = self.file_path_in + "bwa_dir_of_int_back/"
        count = self.start
        while count < self.n:
            full_path = path + "back_barcode_dir_info" + str(count) + '.txt'
            file_read = open(full_path, 'r').readlines()

            file_write = open(path_out + "back_int_set_of_contig_" + str(count) + ".txt", "w")

            for i in range(len(file_read)):
                barcode_name = file_read[i].split("\t")[0]
                file_write.writelines(barcode_name + "\n")

            count += 1

    # front-back
    def auto_barcode_intersection_sort(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "int_set_remove_few_front/"
        path_in_back = self.file_path_in + "int_set_remove_few_back/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before(f-b)/new_info_" + str(j) + "/"
            full_path = path_in_front + "front_int_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in_back + "back_int_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "front_" + str(j) + "compare_to_back_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count_sort(self, file_path_in, n, start):
        path_in_back = self.file_path_in + "bwa_dir_of_int_back/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before(f-b)/new_info_" + str(j) + "/"
            while count < self.n:
                full_path = path_in_back + "back_barcode_dir_info" + str(count) + '.txt'
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "front_" + str(j) + "compare_to_back_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "front_to_back_number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
                count += 1

            count = self.start
            j += 1

    # back-front   
    def auto_barcode_intersection_sort_1(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "int_set_remove_few_front/"
        path_in_back = self.file_path_in + "int_set_remove_few_back/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before(b-f)/new_info_" + str(j) + "/"
            full_path = path_in_back + "back_int_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in_front + "front_int_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "back_" + str(j) + "compare_to_front_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def auto_intersection_count_sort_1(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "bwa_dir_of_int_front/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_before(b-f)/new_info_" + str(j) + "/"
            while count < self.n:
                full_path = path_in_front + "front_barcode_dir_info" + str(count) + '.txt'
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "back_" + str(j) + "compare_to_front_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "back_to_front_number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
                count += 1

            count = self.start
            j += 1


# def main(file_path, file_path_in, n, num, start):
    


# parser = argparse.ArgumentParser(description='Parameters')
# parser.add_argument('--file_path', type=str)
# parser.add_argument('--file_path_in', type=str)
# parser.add_argument('--n', type=int)
# parser.add_argument('--num', type=int)
# parser.add_argument('--start', type=int)
# 
# args = parser.parse_args()
# 
# if __name__ == '__main__':
#     main(args.file_path, args.file_path_in, args.n, args.num, args.start)  
class F_B:
    def __init__(self, file_path_in, n, start, file_compare1, file_compare2, c):
        self.file_path_in = file_path_in
        self.n = n
        self.start = start
        self.file_compare1 = file_compare1
        self.file_compare2 = file_compare2
        self.c = c

    def mv_file(self, file_compare1, n, file_compare2):
        import subprocess
        subprocess.run(
            ['sh', './scripts/mv_file3.sh', self.file_compare1, str(self.n - 1),
             self.file_compare2])

    # filter_useless_info_for_each_front_and_back,when compare each back to front.
    def combine_file(self, file_path_in, n, start):
        import os
        import linecache
        i = self.start
        while i < self.n:
            root = self.file_path_in + "compare_before(f-b)/new_info_" + str(i) + "/compare_to_contig"
            file_names = os.listdir(root)

            file_ob_list = []
            for file_name in file_names:
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

            data = []
            for file_ob in file_ob_list:
                line_num = 1
                length_file = len(open(file_ob, "r").readlines())
                while line_num <= length_file:
                    line = linecache.getline(file_ob, line_num)
                    data.append(line)
                    line_num = line_num + 1
                line_num = 1

            f = open(self.file_path_in + "remove_occur_once(f-b)/sort_barcode_" + str(i) + ".txt", 'w')
            data_new = list(set(data))
            for k in data_new:
                f.write(k)
            i += 1
            f.close()

    def sort_useful_info(self, file_path_in, n, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "remove_occur_once(f-b)/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            fileob = root + '/' + file_name
            file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if v <= self.c}

        f = open(self.file_path_in + "barcode_int_set_all(f-b).txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    # get_final_new_int_and_dir_front_barcode
    def get_int_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "remove_occur_once(f-b)/"
        path_in = self.file_path_in + "barcode_int_set_all(f-b).txt"
        path_out = self.file_path_in + "final_int_barcode(f-b)/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "sort_barcode_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "final_front_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode(f-b)/"
        path_in = self.file_path_in + "bwa_dir_of_int_front/"
        path_out = self.file_path_in + "final_dir_barcode(f-b)/"

        count = self.start
        while count < self.n:
            file_1 = open(path_in + "front_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "final_front_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path_out + "final_front_barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    # get_final_new_int_and_dir_back_barcode
    def get_useful_back_file(self, file_path_in, n, start):
        back_original_path = self.file_path_in + "int_set_remove_few_back/"
        ref_file = open(self.file_path_in + "barcode_int_set_all(f-b).txt", "r").readlines()
        path_out = self.file_path_in + "final_int_barcode(f-b)/"
        count = self.start
        while count < self.n:
            file_back_original = open(back_original_path + "back_int_set_of_contig_" + str(count) + ".txt",
                                      "r").readlines()
            data = list(set(file_back_original) & set(ref_file))
            file_write = open(path_out + "final_back_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def sort_useless_back_info(self, file_path_in, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "final_int_barcode(f-b)/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            if file_name.split("_")[1] == "back":
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if 2 <= v <= self.c}

        f = open(self.file_path_in + "new_back_barcode_all_info.txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    def get_new_final_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode(f-b)/"
        path_in = self.file_path_in + "new_back_barcode_all_info.txt"
        path_out = self.file_path_in + "new_back_info_of_each/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "final_back_set_of_contig_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "final_back_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_new_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "new_back_info_of_each/"
        path_in = self.file_path_in + "bwa_dir_of_int_back/"

        count = self.start
        while count < n:
            file_1 = open(path_in + "back_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "final_back_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path + "back_barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    # get_matrix
    # front-back--compare_after
    def auto_barcode_intersection_sort(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "final_int_barcode(f-b)/"
        path_in_back = self.file_path_in + "new_back_info_of_each/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_after(f-b)/new_info_" + str(j) + "/"
            full_path = path_in_front + "final_front_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in_back + "final_back_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "front_" + str(j) + "compare_to_back_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    # get_compare_after_dir_of_front/back_separately
    def auto_intersection_count_sort(self, file_path_in, n, start):
        path_in_back = self.file_path_in + "new_back_info_of_each/"
        path_in_front = self.file_path_in + "final_dir_barcode(f-b)/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_after(f-b)/new_info_" + str(j) + "/"
            file_f = open(path_in_front + "final_front_barcode_dir_contig_" + str(j) + ".txt", "r").readlines()
            while count < self.n:
                full_path = path_in_back + "back_barcode_dir_contig_" + str(count) + '.txt'
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "front_" + str(j) + "compare_to_back_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "back_number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])

                path_number_1 = path_out + "front_number_dir_" + str(count) + ".txt"
                ans_1 = open(path_number_1, "w")

                dirctory_1 = {}
                for i in range(len(file_f)):
                    dirctory_1[file_f[i].split("\t")[0]] = file_f[i].split("\t")[1]

                for line in file_read:
                    ans_1.writelines(line[:-1] + "\t" + dirctory_1[line[:-1]])

                count += 1

            count = self.start
            j += 1

    # front_and_back
    def auto_barcode_union(self, file_path_in, n, start):
        import pandas as pd
        path_in_front = self.file_path_in + "final_int_barcode(f-b)/"
        path_in_back = self.file_path_in + "new_back_info_of_each/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "union_file_final_int(f-b)/new_info_" + str(j) + "/"
            full_path = path_in_front + "final_front_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in_back + "final_back_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) | set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def barcode_intersection_len(self, file_path_in, n, start):
        import pandas as pd
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "compare_after(f-b)/new_info_" + str(i + 1) + "/"
                full_path = path_in + "front_" + str(i + 1) + "compare_to_back_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def barcode_union_len(self, file_path_in, n, start):
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "union_file_final_int(f-b)/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def get_jaccard(self, file_path_in, n, start):
        import numpy as np
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        info_1 = self.barcode_intersection_len(file_path_in, n, start)
        info_2 = self.barcode_union_len(file_path_in, n, start)
        info_1_array = np.array(info_1)
        info_2_array = np.array(info_2)
        df_1 = pd.DataFrame(info_1_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_2 = pd.DataFrame(info_2_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3 = df_1 / df_2
        df_3_pd = pd.DataFrame(df_3, columns=["contig" + str(i) for i in range(self.start, self.n)],
                               index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3_pd.to_csv(self.file_path_in + "manually_get_jaccard_matrix(f-b).csv", header=True, index=True)

    # get_sorensen_dice
    # front_to_back
    def all_count_of_contig_each(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        path_front = self.file_path_in + "final_dir_barcode(f-b)/"
        path_back = self.file_path_in + "new_back_info_of_each/"
        total_all_info = [[] for _ in range(self.start, self.n)]
        count = self.start
        j = self.start - 1
        while j < self.n - 1:
            while count < (self.n):
                path_A = path_front + "final_front_barcode_dir_contig_" + str(j + 1) + ".txt"
                path_B = path_back + "back_barcode_dir_contig_" + str(count) + ".txt"
                file_A = open(path_A, "r").readlines()
                file_B = open(path_B, "r").readlines()
                sum_barcode_A = 0
                for i in range(len(file_A)):
                    sum_barcode_A += int(file_A[i].split("\t")[1][:-1])
                sum_barcode_B = 0
                for i in range(len(file_B)):
                    sum_barcode_B += int(file_B[i].split("\t")[1][:-1])
                sum_bar = sum_barcode_A + sum_barcode_B
                total_all_info[j - self.start + 1].append(sum_bar)
                count += 1
            count = self.start
            j += 1
        return total_all_info

    def barcode_total_number(self, file_path_in, n, start):
        count = self.start
        j = self.start - 1
        total_barcode_number = [[] for _ in range(self.start, self.n)]
        while j < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "compare_after(f-b)/new_info_" + str(j + 1) + "/"
                path_number = path_in + "back_number_dir_" + str(count) + ".txt"
                file_b = open(path_number, "r").readlines()

                sum_barcode = 0
                for i in range(len(file_b)):
                    sum_barcode += int(file_b[i].split("\t")[1][:-1])

                path_number_f = path_in + "front_number_dir_" + str(count) + ".txt"
                file_f = open(path_number_f, "r").readlines()
                sum = 0
                for m in range(len(file_f)):
                    sum += int(file_f[m].split("\t")[1][:-1])

                total_barcode_number[j - self.start + 1].append(sum + sum_barcode)
                count += 1

            count = self.start
            j += 1

        return total_barcode_number

    def get_sorensen_dice(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        total_all_info_list = self.all_count_of_contig_each(file_path_in, n, start)
        total_all_info_np = np.array(total_all_info_list)
        total_all_pd = pd.DataFrame(total_all_info_np, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])
        total_all_pd.to_csv(self.file_path_in + "add_count_barcode_matrix(f-b).csv", index=True, header=True)

        total_barcode_list = self.barcode_total_number(file_path_in, n, start)
        total_num = np.array(total_barcode_list)
        total_num_pd = pd.DataFrame(total_num, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])

        Sorensen_Dice_rate = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                          index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                Sorensen_Dice_rate.loc["contig" + str(i), "contig" + str(j)] = total_num_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(
                                                                                       j)] / total_all_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(j)]
        Sorensen_Dice_rate.to_csv(self.file_path_in + "Sorensen_Dice_rate_matrix_more(f-b).csv", index=True,
                                  header=True)


#def main(file_path_in, n, start, file_compare1, file_compare2, c):
    


# parser = argparse.ArgumentParser(description='Parameters')
# parser.add_argument('--file_path_in', type=str)
# parser.add_argument('--n', type=int)
# parser.add_argument('--start', type=int)
# parser.add_argument('--file_compare1', type=str)
# parser.add_argument('--file_compare2', type=str)
# parser.add_argument('--c', type=int)
# args = parser.parse_args()

# if __name__ == '__main__':
#     main(args.file_path_in, args.n, args.start, args.file_compare1, args.file_compare2, args.c)
class B_F:
    def __init__(self, file_path_in, n, start, c):
        self.file_path_in = file_path_in
        self.n = n
        self.start = start
        self.c = c

    # filter_useless_info_for_each_front_and_back,when compare each front to back.
    def combine_file(self, file_path_in, n, start):
        import os
        import linecache
        i = self.start
        while i < self.n:
            root = self.file_path_in + "compare_before(b-f)/new_info_" + str(i) + "/compare_to_contig"
            file_names = os.listdir(root)

            file_ob_list = []
            for file_name in file_names:
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

            data = []
            for file_ob in file_ob_list:
                line_num = 1
                length_file = len(open(file_ob, "r").readlines())
                while line_num <= length_file:
                    line = linecache.getline(file_ob, line_num)
                    data.append(line)
                    line_num = line_num + 1
                line_num = 1

            f = open(self.file_path_in + "remove_occur_once(b-f)/sort_barcode_" + str(i) + ".txt", 'w')
            data_new = list(set(data))
            for k in data_new:
                f.write(k)
            i += 1
            f.close()

    def sort_useful_info(self, file_path_in, n, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "remove_occur_once(b-f)/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            fileob = root + '/' + file_name
            file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if v <= self.c}

        f = open(self.file_path_in + "barcode_int_set_all(b-f).txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    # get_final_new_int_and_dir_back_barcode
    def get_int_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "remove_occur_once(b-f)/"
        path_in = self.file_path_in + "barcode_int_set_all(b-f).txt"
        path_out = self.file_path_in + "final_int_barcode(b-f)/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "sort_barcode_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "final_back_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode(b-f)/"
        path_in = self.file_path_in + "bwa_dir_of_int_back/"
        path_out = self.file_path_in + "final_dir_barcode(b-f)/"

        count = self.start
        while count < self.n:
            file_1 = open(path_in + "back_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "final_back_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path_out + "final_back_barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    # get_final_new_int_and_dir_front_barcode
    def get_useful_back_file(self, file_path_in, n, start):
        back_original_path = self.file_path_in + "int_set_remove_few_front/"
        ref_file = open(self.file_path_in + "barcode_int_set_all(b-f).txt", "r").readlines()
        path_out = self.file_path_in + "final_int_barcode(b-f)/"
        count = self.start
        while count < self.n:
            file_back_original = open(back_original_path + "front_int_set_of_contig_" + str(count) + ".txt",
                                      "r").readlines()
            data = list(set(file_back_original) & set(ref_file))
            file_write = open(path_out + "final_front_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def sort_useless_back_info(self, file_path_in, c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path_in + "final_int_barcode(b-f)/"
        file_names = os.listdir(root)

        file_ob_list = []
        for file_name in file_names:
            if file_name.split("_")[1] == "front":
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)

        data = []
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob, "r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1

        result = Counter(data)
        result_new = {k: v for k, v in result.items() if 2 <= v <= self.c}

        f = open(self.file_path_in + "new_front_barcode_all_info.txt", 'w')
        for k, v in result_new.items():
            f.writelines(str(k) + "\n")
        f.close()

    def get_new_final_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "final_int_barcode(b-f)/"
        path_in = self.file_path_in + "new_front_barcode_all_info.txt"
        path_out = self.file_path_in + "new_front_info_of_each/"
        file_ref = open(path_in, "r").readlines()
        count = self.start
        while count < self.n:
            full_path = path + "final_front_set_of_contig_" + str(count) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read) & set(file_ref))

            file_write = open(path_out + "final_front_set_of_contig_" + str(count) + ".txt", "w")
            for i in data:
                file_write.write(i)
            file_write.close()

            count += 1

    def get_new_dir_barcode_set(self, file_path_in, n, start):
        path = self.file_path_in + "new_front_info_of_each/"
        path_in = self.file_path_in + "bwa_dir_of_int_front/"

        count = self.start
        while count < n:
            file_1 = open(path_in + "front_barcode_dir_info" + str(count) + ".txt", "r").readlines()
            file_2 = open(path + "final_front_set_of_contig_" + str(count) + ".txt", "r").readlines()
            f = open(path + "front_barcode_dir_contig_" + str(count) + ".txt", "w")

            dirctory = {}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]] = file_1[i].split("\t")[1]

            for line in file_2:
                f.writelines(line[:-1] + "\t" + dirctory[line[:-1]])
            f.close()

            count += 1

    # get_matrix
    # back--front--compare_after
    def auto_barcode_intersection_sort(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "final_int_barcode(b-f)/"
        path_in_back = self.file_path_in + "new_front_info_of_each/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_after(b-f)/new_info_" + str(j) + "/"
            full_path = path_in_front + "final_back_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()

            while count < self.n:
                full_path_read = path_in_back + "final_front_set_of_contig_" + str(count) + ".txt"
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "back_" + str(j) + "compare_to_front_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) & set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    # get_compare_after_dir_of_front/back_separately
    def auto_intersection_count_sort(self, file_path_in, n, start):
        path_in_front = self.file_path_in + "new_front_info_of_each/"
        path_in_back = self.file_path_in + "final_dir_barcode(b-f)/"
        count = self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path_in + "compare_after(b-f)/new_info_" + str(j) + "/"
            file_b = open(path_in_back + "final_back_barcode_dir_contig_" + str(j) + ".txt", "r").readlines()
            while count < self.n:
                full_path = path_in_front + "front_barcode_dir_contig_" + str(count) + '.txt'
                file = open(full_path, 'r').readlines()

                full_path_1 = path_out + "back_" + str(j) + "compare_to_front_" + str(count) + ".txt"
                file_read = open(full_path_1, "r").readlines()

                path_number = path_out + "front_number_dir_" + str(count) + ".txt"
                ans = open(path_number, "w")

                dirctory = {}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]] = file[i].split("\t")[1]

                for line in file_read:
                    ans.writelines(line[:-1] + "\t" + dirctory[line[:-1]])

                path_number_1 = path_out + "back_number_dir_" + str(count) + ".txt"
                ans_1 = open(path_number_1, "w")

                dirctory_1 = {}
                for i in range(len(file_b)):
                    dirctory_1[file_b[i].split("\t")[0]] = file_b[i].split("\t")[1]

                for line in file_read:
                    ans_1.writelines(line[:-1] + "\t" + dirctory_1[line[:-1]])

                count += 1

            count = self.start
            j += 1

    # back_and_front
    def auto_barcode_union(self, file_path_in, n, start):
        import pandas as pd
        path_in_front = self.file_path_in + "final_int_barcode(b-f)/"
        path_in_back = self.file_path_in + "new_front_info_of_each/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path_in + "union_file_final_int(b-f)/new_info_" + str(j) + "/"
            full_path = path_in_front + "final_back_set_of_contig_" + str(j) + ".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in_back + "final_front_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read, "r").readlines()
                full_path_write = path_out + "compare_to_contige_" + str(count) + ".txt"
                file_write = open(full_path_write, "w")
                barcode_same = list(set(file) | set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count += 1

            count = self.start
            j += 1

    def barcode_intersection_len(self, file_path_in, n, start):
        import pandas as pd
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "compare_after(b-f)/new_info_" + str(i + 1) + "/"
                full_path = path_in + "back_" + str(i + 1) + "compare_to_front_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def barcode_union_len(self, file_path_in, n, start):
        total_barcode_catagory = [[] for _ in range(self.start, self.n)]
        count = self.start
        i = self.start - 1
        while i < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "union_file_final_int(b-f)/new_info_" + str(i + 1) + "/"
                full_path = path_in + "compare_to_contige_" + str(count) + ".txt"
                file_read = open(full_path, "r").readlines()
                total_barcode_catagory[i - self.start + 1].append(len(file_read))
                count += 1
            count = self.start
            i += 1
        return total_barcode_catagory

    def get_jaccard(self, file_path_in, n, start):
        import numpy as np
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        info_1 = self.barcode_intersection_len(file_path_in, n, start)
        info_2 = self.barcode_union_len(file_path_in, n, start)
        info_1_array = np.array(info_1)
        info_2_array = np.array(info_2)
        df_1 = pd.DataFrame(info_1_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_2 = pd.DataFrame(info_2_array, columns=["contig" + str(i) for i in range(self.start, self.n)],
                            index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3 = df_1 / df_2
        df_3_pd = pd.DataFrame(df_3, columns=["contig" + str(i) for i in range(self.start, self.n)],
                               index=["contig" + str(i) for i in range(self.start, self.n)])
        df_3_pd.to_csv(self.file_path_in + "manually_get_jaccard_matrix(b-f).csv", header=True, index=True)

    # get_sorensen_dice
    # front_to_back
    def all_count_of_contig_each(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        path_front = self.file_path_in + "final_dir_barcode(b-f)/"
        path_back = self.file_path_in + "new_front_info_of_each/"
        total_all_info = [[] for _ in range(self.start, self.n)]
        count = self.start
        j = self.start - 1
        while j < self.n - 1:
            while count < (self.n):
                path_A = path_front + "final_back_barcode_dir_contig_" + str(j + 1) + ".txt"
                path_B = path_back + "front_barcode_dir_contig_" + str(count) + ".txt"
                file_A = open(path_A, "r").readlines()
                file_B = open(path_B, "r").readlines()
                sum_barcode_A = 0
                for i in range(len(file_A)):
                    sum_barcode_A += int(file_A[i].split("\t")[1][:-1])
                sum_barcode_B = 0
                for i in range(len(file_B)):
                    sum_barcode_B += int(file_B[i].split("\t")[1][:-1])
                sum_bar = sum_barcode_A + sum_barcode_B
                total_all_info[j - self.start + 1].append(sum_bar)
                count += 1
            count = self.start
            j += 1
        return total_all_info

    def barcode_total_number(self, file_path_in, n, start):
        count = self.start
        j = self.start - 1
        total_barcode_number = [[] for _ in range(self.start, self.n)]
        while j < self.n - 1:
            while count < (self.n):
                path_in = self.file_path_in + "compare_after(b-f)/new_info_" + str(j + 1) + "/"
                path_number = path_in + "front_number_dir_" + str(count) + ".txt"
                file_b = open(path_number, "r").readlines()

                sum_barcode = 0
                for i in range(len(file_b)):
                    sum_barcode += int(file_b[i].split("\t")[1][:-1])

                path_number_f = path_in + "back_number_dir_" + str(count) + ".txt"
                file_f = open(path_number_f, "r").readlines()
                sum = 0
                for m in range(len(file_f)):
                    sum += int(file_f[m].split("\t")[1][:-1])

                total_barcode_number[j - self.start + 1].append(sum + sum_barcode)
                count += 1

            count = self.start
            j += 1

        return total_barcode_number

    def get_sorensen_dice(self, file_path_in, n, start):
        import pandas as pd
        import numpy as np
        total_all_info_list = self.all_count_of_contig_each(file_path_in, n, start)
        total_all_info_np = np.array(total_all_info_list)
        total_all_pd = pd.DataFrame(total_all_info_np, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])
        total_all_pd.to_csv(self.file_path_in + "add_count_barcode_matrix(b-f).csv", index=True, header=True)

        total_barcode_list = self.barcode_total_number(file_path_in, n, start)
        total_num = np.array(total_barcode_list)
        total_num_pd = pd.DataFrame(total_num, columns=["contig" + str(i) for i in range(self.start, self.n)],
                                    index=["contig" + str(i) for i in range(self.start, self.n)])

        Sorensen_Dice_rate = pd.DataFrame(columns=["contig" + str(i) for i in range(self.start, self.n)],
                                          index=["contig" + str(i) for i in range(self.start, self.n)])
        for i in range(self.start, self.n):
            for j in range(self.start, self.n):
                Sorensen_Dice_rate.loc["contig" + str(i), "contig" + str(j)] = total_num_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(
                                                                                       j)] / total_all_pd.loc[
                                                                                   "contig" + str(i), "contig" + str(j)]
        Sorensen_Dice_rate.to_csv(self.file_path_in + "Sorensen_Dice_rate_matrix_more(b-f).csv", index=True,
                                  header=True)


#def main(file_path_in, n, start, c):



# parser = argparse.ArgumentParser(description='Parameters')
# parser.add_argument('--file_path_in', type=str)
# parser.add_argument('--n', type=int)
# parser.add_argument('--start', type=int)
# parser.add_argument('--c', type=int)
# args = parser.parse_args()
# 
# if __name__ == '__main__':
#     main(args.file_path_in, args.n, args.start, args.c)
   