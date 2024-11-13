class Feature_extract:
    def __init__(self, file_path, start):
        self.file_path = file_path
        self.start = start

    def get_pair_info(self, file_path, start):
        import pandas as pd
        total_num_read_pd = pd.read_csv(self.file_path + "Sorensen_Dice_rate_matrix_more.csv", index_col=0)
        import numpy as np
        total_num_read_np = np.array(total_num_read_pd)

        max_rate = []
        for i in range(len(total_num_read_np)):
            total_sort = total_num_read_pd.iloc[i].sort_values(na_position='first')
            number_1 = total_sort[-2]
            index_ge = total_sort[total_sort.values == number_1].index
            max_rate.append(("contig" + str(i + self.start) + "\t" + str(index_ge[0]), number_1))
            number_2 = total_sort[-3]
            index_ge_2 = total_sort[total_sort.values == number_2].index
            max_rate.append(("contig" + str(i + self.start) + "\t" + str(index_ge_2[0]), number_2))

        output_max = open(self.file_path + "max_contig_of_Sorensen_Dice.txt", "w")
        for x, y in max_rate:
            data = x + "\t" + str(y) + "\n"
            output_max.writelines(data)
        output_max.close()

        input_max = open(self.file_path + "max_contig_of_Sorensen_Dice.txt", "r").readlines()
        out = open(self.file_path + "max_contig_of_Sorensen_Dice_new.txt", "w")
        for i in range(len(input_max)):
            if float(input_max[i].split("\t")[2][:-1]) != 0.0:
                out.writelines(input_max[i])
        out.close()

    def feature_extract(self, file_path):
        import pandas as pd
        data_in = open(self.file_path + "max_contig_of_Sorensen_Dice_new.txt", "r").readlines()
        pd_5 = pd.read_csv(self.file_path + "fb_and_bf_list/manually_get_jaccard_matrix(b-f).csv", index_col=0)
        pd_6 = pd.read_csv(self.file_path + "bb_list/manually_get_jaccard_matrix(b-b).csv", index_col=0)
        pd_7 = pd.read_csv(self.file_path + "ff_list/manually_get_jaccard_matrix(f-f).csv", index_col=0)
        pd_8 = pd.read_csv(self.file_path + "fb_and_bf_list/manually_get_jaccard_matrix(f-b).csv", index_col=0)

        data_out = open(self.file_path + "label_with_orientation_only_jaccard.txt", "w")

        i = 0
        while i < len(data_in):
            label_1 = data_in[i].split("\t")[0]
            label_2 = data_in[i].split("\t")[1]

            value_1 = str(float(pd_5.loc[label_1, label_2]))
            value_2 = str(float(pd_6.loc[label_1, label_2]))
            value_3 = str(float(pd_7.loc[label_1, label_2]))
            value_4 = str(float(pd_8.loc[label_1, label_2]))
            data_out.writelines(
                data_in[i].split("\n")[0] + "\t" + value_1 + "\t" + value_2 + "\t" + value_3 + "\t" + value_4 + "\n")
            i += 1
        data_out.close()

    def get_label(self, file_path):
        data = open(self.file_path + "label_with_orientation_only_jaccard.txt", "r").readlines()
        data_out = open(self.file_path + "label_list(jaccard).txt", "w")
        import pandas as pd
        for line in data:
            score = line.split()[2]
            list_i = line.split()[3:]
            label = list_i.index(max(list_i))
            data_out.writelines(
                line.split("\t")[0] + "_" + line.split("\t")[1] + "\t" + score + "\t" + str(label) + "\n")
        data_out.close()


#def main(file_path, start):



# parser = argparse.ArgumentParser(description='Parameters')
# parser.add_argument('--file_path', type=str)
# parser.add_argument("--start", type=int)
# 
# args = parser.parse_args()
# 
# if __name__ == '__main__':
#     main(args.file_path, args.start)