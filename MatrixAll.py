import argparse

class Barcode_info:
    #the first python demo
    def __init__(self,path_bam,file_path,start,n,num,c,file_compare):
        self.path_bam  = path_bam
        self.file_path = file_path
        self.start = start
        self.n = n
        self.num = num
        self.c = c
        self.file_compare = file_compare
        
    def create_file(self,file_path,n):
        import subprocess
        import os 
        subprocess.run(['sh','./scripts/create_file_all.sh',self.file_path,str(self.n-1)])
    
    def get_front_barcode_info(self,path_bam,file_path,start,n,num):
        path = self.path_bam+"get_bam_info/"
        path_out = self.file_path+"bwa_original_barcode_name_(file_1)/"

        length_data = open(self.file_path+"output_with_depth_table.txt","r").readlines()
        length_list = {}
        for i in range(1,len(length_data)):
            name = length_data[i].split("\t")[0].split("_")[1]
            length = length_data[i].split("\t")[1]
            length_list[name] = int(length)

        for i in range(self.start,self.n):
            if length_list[str(i)] >= 2*self.num:
                full_path = path + "final_out_"+str(i)+".info.txt"
                file_read = open(full_path,"r").readlines()
                full_write_path = path_out + "front_barcode_info_of_contig"+str(i)+".txt"
                file_write = open(full_write_path,"w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) <=self.num:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line+"\n")

            elif length_list[str(i)] < 2*self.num:
                full_path = path + "final_out_"+str(i)+".info.txt"
                file_read = open(full_path,"r").readlines()
                full_write_path = path_out + "front_barcode_info_of_contig"+str(i)+".txt"
                file_write = open(full_write_path,"w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) <= (length_list[str(i)])//2:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line+"\n")
                
    
    def get_back_barcode_info(self,path_bam,file_path,start,num):
        path = self.path_bam+"get_bam_info/"
        path_out = self.file_path+"bwa_original_barcode_name_(file_1)/"
        #import pandas as pd
        length_data = open(self.file_path+"output_with_depth_table.txt","r").readlines()
        length_list = {}
        for i in range(1,len(length_data)):
            name = length_data[i].split("\t")[0].split("_")[1]
            length = length_data[i].split("\t")[1]
            length_list[name] = int(length)
        print(length_list)
        
        for i in range(self.start,self.n):
            if length_list[str(i)] >= 2*self.num:
                full_path = path + "final_out_"+str(i)+".info.txt"
                file_read = open(full_path,"r").readlines()
                full_write_path = path_out + "back_barcode_info_of_contig"+str(i)+".txt"
                file_write = open(full_write_path,"w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) >= int(int(length_list[str(i)])-self.num):
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line+"\n")
                file_write.close()
            
            elif length_list[str(i)] < 2*self.num:
                full_path = path + "final_out_"+str(i)+".info.txt"
                file_read = open(full_path,"r").readlines()
                full_write_path = path_out + "back_barcode_info_of_contig"+str(i)+".txt"
                file_write = open(full_write_path,"w")
                for j in range(len(file_read)):
                    if int(file_read[j].split("\t")[3]) >= (length_list[str(i)])//2:
                        line = file_read[j].split("\t")[0].split(":")[-1]
                        file_write.writelines(line+"\n")
                file_write.close()
                
            
    def design_file_intbar(self,file_path,n,start,num):
        path = self.file_path + "bwa_original_barcode_name_(file_1)/"
        path_out = self.file_path +"front_and_back_barcode_(file_2)/"
        
        length_data = open(self.file_path+"output_with_depth_table.txt","r").readlines()
        length_list = {}
        for i in range(1,len(length_data)):
            name = length_data[i].split("\t")[0].split("_")[1]
            length = length_data[i].split("\t")[1]
            length_list[name] = int(length)
        
        for i in range(self.start,self.n):
            full_path = path_out + "final_barcode_int_name_of_contig" + str(i) + '.txt'
            file = open(full_path, 'w')
            full_path_read = path + "front_barcode_info_of_contig" + str(i) + '.txt'
            file_read_1 = open(full_path_read,"r").readlines()
            full_path_read_1 = path + "back_barcode_info_of_contig" + str(i) + '.txt'
            file_read_2 = open(full_path_read_1,"r").readlines()
            for line in file_read_1:
                file.writelines(str(line[:-1])+"\n")
            for line in file_read_2:
                file.writelines(str(line[:-1])+"\n")
            file.close()


    def barcode_bwa_set(self,file_path,n,start):
        from collections import Counter
        path = self.file_path+"front_and_back_barcode_(file_2)/"
        path_out = self.file_path + "bwa_dir_of_int_(file_3)/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_int_name_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
        
            full_path_write = path_out + "final_barcode_int_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            barcode_set = set(file)
    
            for line in barcode_set:
                file_write.writelines(line)

            count+=1

    def barcode_bwa_number(self,file_path,n,start):
        from collections import Counter
        path = self.file_path+"front_and_back_barcode_(file_2)/"
        path_out = self.file_path+"bwa_dir_of_int_(file_3)/"
        count = self.start
        while count < self.n:
            full_path = path + "final_barcode_int_name_of_contig" + str(count) + '.txt'
            file = open(full_path, 'r').readlines()
            full_path_write = path_out + "final_barcode_dir_info" + str(count) + '.txt'
            file_write = open(full_path_write, 'w')
            number_dir=Counter(file)
            number_sort = sorted(number_dir.items(),key = lambda x:x[1],reverse = True)
            for i in range(len(number_sort)):
                line = number_sort[i][0][:-1] + "\t" + str(number_sort[i][1]) + "\n"
                #if the number of barcode is under 3, it will be removed.
                if number_sort[i][1] >= 3:
                    file_write.writelines(line)

            count+=1

    def barcode_bwa_set_few(self,file_path,n,start):
        from collections import Counter
        path_out = self.file_path + "int_set_remove_few_(file_3)/"
        path = self.file_path + "bwa_dir_of_int_(file_3)/"
        count = self.start
        while count < self.n:    
            full_path = path + "final_barcode_dir_info" + str(count) + '.txt'
            file_read= open(full_path, 'r').readlines()
            file_write= open(path_out+"int_set_of_contig_"+str(count)+".txt","w")
    
            for i in range(len(file_read)):
                barcode_name = file_read[i].split("\t")[0]
                file_write.writelines(barcode_name+"\n")

            count+=1

    #get_compare_info    
    def auto_barcode_intersection_sort(self,file_path,n,start):
        path_in = self.file_path + "int_set_remove_few_(file_3)/"
        j = self.start
        count = self.start
        while j < self.n:
            path_out = self.file_path + "compare_before_(file_4)/new_info_"+str(j)+"/"
            full_path = path_in + "int_set_of_contig_"+str(j)+".txt"
            file = open(full_path, 'r').readlines()
        
            while count < self.n:
                full_path_read = path_in +"int_set_of_contig_"+str(count)+".txt"
                file_read = open(full_path_read,"r").readlines()
                full_path_write = path_out +"int_set_of_contig_"+str(count)+"compare_to_contig_"+str(j)+".txt"
                file_write=open(full_path_write,"w")
                barcode_same=list(set(file)&set(file_read))
                for i in barcode_same:
                    file_write.writelines(i)
                count+=1
            
            count = self.start
            j += 1


    def auto_intersection_count_sort(self,file_path,n,start):
        path_in = self.file_path + "bwa_dir_of_int_(file_3)/"
        count=self.start
        j = self.start
        while j < self.n:
            path_out = self.file_path + "compare_before_(file_4)/new_info_"+str(j)+"/"
            while count < self.n:
                full_path = path_in + "final_barcode_dir_info"+str(count)+".txt"
                file = open(full_path, 'r').readlines()
            
                full_path_1 = path_out + "int_set_of_contig_"+str(count)+"compare_to_contig_"+str(j)+".txt"
                file_read=open(full_path_1,"r").readlines()
            
                path_number = path_out + "number_dir_"+str(count)+".txt"
                ans=open(path_number,"w")
        
                dirctory={}
                for i in range(len(file)):
                    dirctory[file[i].split("\t")[0]]=file[i].split("\t")[1]
                  
                for line in file_read:
                    ans.writelines(line[:-1]+"\t"+dirctory[line[:-1]])            
                count+=1
       
            count = self.start
            j += 1
            
    #remove_barcode        
    def mv_file(self,file_compare,n):
        import subprocess
        subprocess.run(['sh','./scripts/mv_file_all.sh',self.file_compare,str(self.n-1)])
    
    def remove_occur_once(self,file_path,n,start):
        import os
        import linecache
        i = self.start
        while i < self.n:
            root = self.file_path + "compare_before_(file_4)/new_info_"+str(i)+"/compara_to_contig"
            file_names = os.listdir(root)
        
            file_ob_list = []
            for file_name in file_names:
                fileob = root + '/' + file_name
                file_ob_list.append(fileob)
  
            data = []
            for file_ob in file_ob_list:
                line_num = 1
                length_file = len(open(file_ob,"r").readlines())
                while line_num <= length_file:
                    line = linecache.getline(file_ob, line_num)
                    data.append(line)
                    line_num = line_num + 1
                line_num = 1

            f = open(self.file_path + "remove_occur_once_(file_5)/sort_barcode_"+str(i)+".txt", 'w')
            data_new = list(set(data))
            for k in data_new:
                f.write(k)
            i += 1
            f.close()
 
    def remove_more_than_k(self,file_path,n,c):
        import os
        import linecache
        from collections import Counter
        root = self.file_path + "remove_occur_once_(file_5)/"
        file_names = os.listdir(root)
    
        file_ob_list = []
        for file_name in file_names:
            fileob = root + '/' + file_name
            file_ob_list.append(fileob)
    
        data = [] 
        for file_ob in file_ob_list:
            line_num = 1
            length_file = len(open(file_ob,"r").readlines())
            while line_num <= length_file:
                line = linecache.getline(file_ob, line_num)
                data.append(line[:-1])
                line_num = line_num + 1
            line_num = 1
    
        result = Counter(data) 
        result_new = {k:v for k, v in result.items() if v <= int(self.c)}
    
        f=open(self.file_path + "/barcode_int_set_all.txt", 'w')
        for k, v in result_new.items():
            #f.writelines(str(k)+"\t"+str(v)+"\n")
            f.writelines(str(k)+"\n")
        f.close()
        
        
    def get_int_barcode_set(self,file_path,n,start):
        path = self.file_path + "remove_occur_once_(file_5)/"
        path_in = self.file_path + "barcode_int_set_all.txt"
        path_out = self.file_path + "final_int_barcode(file_6)/"
        file_ref = open(path_in,"r").readlines()
        t = self.start
        while t < self.n:
            full_path = path + "sort_barcode_" + str(t) + ".txt"
            file_read = open(full_path, "r").readlines()
            data = list(set(file_read)&set(file_ref))
        
            file_write=open(path_out+"int_set_of_contig_"+str(t)+".txt","w")
            for i in data:
                file_write.write(i)
            file_write.close()
        
            t += 1

    def get_dir_barcode_set(self,file_path,n,start):
        path = self.file_path + "final_int_barcode(file_6)/"
        path_in = self.file_path + "bwa_dir_of_int_(file_3)/"
        path_out = self.file_path + "final_dir_barcode(file_7)/"

        t = self.start
        while t < self.n:
            file_1=open(path_in+"final_barcode_dir_info"+str(t)+".txt","r").readlines()
            file_2=open(path+"int_set_of_contig_"+str(t)+".txt","r").readlines()
            f = open(path_out+"barcode_dir_contig_"+str(t)+".txt","w")
        
            dirctory={}
            for i in range(len(file_1)):
                dirctory[file_1[i].split("\t")[0]]=file_1[i].split("\t")[1]
                  
            for line in file_2:
                f.writelines(line[:-1]+"\t"+dirctory[line[:-1]])
            f.close()  
                      
            t += 1
                        
    def auto_barcode_intersection(self,file_path,n,start):
        path_in = self.file_path + "final_int_barcode(file_6)/"
        j = self.start
        i = self.start
        while j < self.n:
            path_out = self.file_path + "compara_file_final_int_(file_8)/new_info_"+str(j)+"/"
            full_path = path_in + "int_set_of_contig_"+str(j)+".txt"
            file = open(full_path, 'r').readlines()
            while i < self.n:
                full_path_read = path_in +"int_set_of_contig_" + str(i) + '.txt'
                file_read = open(full_path_read,"r").readlines()
                full_path_write = path_out + "compare_to_contige_"+str(i)+".txt"
                file_write=open(full_path_write,"w")
                barcode_same=list(set(file)&set(file_read))
                for m in barcode_same:
                   file_write.writelines(m)
                i += 1
            
            i = self.start
            j += 1

    def auto_intersection_count(self,file_path,n,start):
        path_in = self.file_path + "final_dir_barcode(file_7)/"
        i = self.start
        j = self.start
        while j < self.n:
            while i < self.n:
                path_out = self.file_path + "compara_file_final_dir_(file_9)/new_info_"+str(j)+"/"
                path = self.file_path + "compara_file_final_int_(file_8)/new_info_"+str(j)+"/"
            
                full_path = path_in + "barcode_dir_contig_"+str(i)+".txt"
                file = open(full_path, 'r').readlines()
            
                full_path_1 = path + "compare_to_contige_"+str(i)+".txt"
                file_read=open(full_path_1,"r").readlines()
            
                path_number = path_out + "number_dir_"+str(i)+".txt"
                ans=open(path_number,"w")
        
                dirctory={}
                for m in range(len(file)):
                    dirctory[file[m].split("\t")[0]]=file[m].split("\t")[1]
                  
                for line in file_read:
                    ans.writelines(line[:-1]+"\t"+dirctory[line[:-1]])    
                        
                i += 1
       
            i = self.start
            j += 1

    #get_jaccard
    def auto_barcode_union(self,file_path,n,start):
        import pandas as pd
        path_in = self.file_path + "final_int_barcode(file_6)/"
        j = self.start
        count = self.start 
        while j < self.n:
            path_out = self.file_path + "union_file_final_int_(file_10)/new_info_"+str(j)+"/"
            full_path = path_in + "int_set_of_contig_"+str(j)+".txt"
            file = open(full_path, 'r').readlines()
            while count < self.n:
                full_path_read = path_in +"int_set_of_contig_" + str(count) + '.txt'
                file_read = open(full_path_read,"r").readlines()
                full_path_write = path_out + "compare_to_contige_"+str(count)+".txt"
                file_write=open(full_path_write,"w")
                barcode_same=list(set(file)|set(file_read))
                for i in barcode_same: 
                    file_write.writelines(i)
                count+=1
            
            count = self.start
            j += 1

    def barcode_intersection_len(self,file_path,n,start):
        import pandas as pd
        total_barcode_catagory=[[] for _ in range(self.start,self.n)]
        count=self.start
        i = self.start-1
        while i < self.n-1:
            while count < self.n:
                path_in = self.file_path + "compara_file_final_int_(file_8)/new_info_"+str(i+1)+"/"
                full_path = path_in + "compare_to_contige_"+str(count)+".txt"
                file_read=open(full_path,"r").readlines()
                total_barcode_catagory[i-self.start+1].append(len(file_read))
                count += 1
                
            count = self.start
            i += 1
        return total_barcode_catagory


    def barcode_union_len(self,file_path,n,start):
        import pandas as pd
        total_barcode_catagory=[[] for _ in range(self.start,self.n)]
        count=self.start
        i = self.start-1
        while i < self.n-1:
            while count < self.n:
                path_in = self.file_path + "union_file_final_int_(file_10)/new_info_"+str(i+1)+"/"
                full_path = path_in + "compare_to_contige_"+str(count)+".txt"
                file_read=open(full_path,"r").readlines()
                total_barcode_catagory[i-self.start+1].append(len(file_read))
                count += 1
                
            count = self.start
            i += 1
        return total_barcode_catagory


    def get_jaccard_corr(self,file_path,n,start):
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd
        info_1 = self.barcode_intersection_len(file_path,n,start)
        info_2 = self.barcode_union_len(file_path,n,start)
        info_1_array=np.array(info_1)
        info_2_array=np.array(info_2)
        df_1 = pd.DataFrame(info_1_array, columns=["contig"+str(i) for i in range(self.start,self.n)],index=["contig"+str(i) for i in range(self.start,self.n)])
        df_2 = pd.DataFrame(info_2_array, columns=["contig"+str(i) for i in range(self.start,self.n)],index=["contig"+str(i) for i in range(self.start,self.n)])
        df_3 = df_1 / df_2
        df_3_pd= pd.DataFrame(df_3, columns=["contig"+str(i) for i in range(self.start, self.n)],index=["contig"+str(i) for i in range(self.start,self.n)])
        df_3_pd.to_csv(self.file_path+"manually_get_jaccard_matrix.csv",header = True,index=True)
        
    #get_sorensen_dice
    def all_count_of_contig_each(self,file_path,n,start):
        path = self.file_path + "final_dir_barcode(file_7)/"
        total_all_info = [[] for _ in range(self.start,self.n)]
        count = self.start
        j = self.start-1
        while j < self.n-1:
            while count < self.n:
                path_A = path + "barcode_dir_contig_" + str(j+1) +".txt"
                path_B = path + "barcode_dir_contig_" + str(count) +".txt"
                file_A = open(path_A,"r").readlines()
                file_B = open(path_B,"r").readlines()
                sum_barcode_A = 0
                for i in range(len(file_A)):
                    sum_barcode_A += int(file_A[i].split("\t")[1][:-1])
                sum_barcode_B = 0
                for i in range(len(file_B)):
                    sum_barcode_B += int(file_B[i].split("\t")[1][:-1])
                sum_bar = sum_barcode_A+sum_barcode_B
                total_all_info[j-self.start+1].append(sum_bar)
                count += 1
                
            count = self.start
            j += 1
        return total_all_info
        
    def barcode_total_number(self,file_path,n,start):
        count = self.start
        j = self.start-1
        total_barcode_number=[[] for _ in range(self.start,self.n)]
        while j < self.n-1:
            while count < self.n:
                path_in = self.file_path + "compara_file_final_dir_(file_9)/new_info_"+str(j+1)+"/"
                path_number = path_in + "number_dir_"+str(count)+".txt"
                file = open(path_number,"r").readlines()
            
                sum_barcode=0
                for i in range(len(file)):
                    sum_barcode += int(file[i].split("\t")[1][:-1])
                total_barcode_number[j-self.start+1].append(sum_barcode)                    
                count+=1   

            count = self.start
            j += 1
    
        return total_barcode_number       
 
    def get_sorensen_dice(self,file_path,n,start):
        import pandas as pd
        import numpy as np       
        total_all_info_list = self.all_count_of_contig_each(file_path,n,start)
        total_all_info_np=np.array(total_all_info_list)
        total_all_pd = pd.DataFrame(total_all_info_np,columns=["contig"+str(i) for i in range(self.start,self.n)], index=["contig"+str(i) for i in range(self.start,self.n)])
        total_all_pd.to_csv(self.file_path + "add_count_barcode_matrix.csv",index = True, header = True)    
    
        total_barcode_list = self.barcode_total_number(file_path,n,start)
        total_num=np.array(total_barcode_list)
        total_num_pd = pd.DataFrame(total_num, columns=["contig"+str(i) for i in range(self.start, self.n)], index=["contig"+str(i) for i in range(self.start, self.n)])
        
        total_pd = pd.DataFrame(columns=["contig"+str(i) for i in range(self.start, self.n)], index=["contig"+str(i) for i in range(self.start, self.n)])
        for i in range(self.start,self.n):
            for j in range(self.start,self.n):
                total_pd.loc["contig"+str(i),"contig"+str(j)]=total_num_pd.loc["contig"+str(i),"contig"+str(j)]+total_num_pd.loc["contig"+str(j),"contig"+str(i)]
                #total_pd.loc["contig"+str(i),"contig"+str(j)]=2*min(total_num_pd.loc["contig"+str(i),"contig"+str(j)],total_num_pd.loc["contig"+str(j),"contig"+str(i)])
        total_pd.to_csv(self.file_path + "compare_add_count_matrix.csv",index = True, header = True)
        
        Sorensen_Dice_rate=pd.DataFrame(columns=["contig"+str(i) for i in range(self.start, self.n)], index=["contig"+str(i) for i in range(self.start, self.n)])
        for i in range(self.start,self.n):
            for j in range(self.start,self.n):
                Sorensen_Dice_rate.loc["contig"+str(i),"contig"+str(j)] = total_pd.loc["contig"+str(i),"contig"+str(j)]/total_all_pd.loc["contig"+str(i),"contig"+str(j)]

        Sorensen_Dice_rate.to_csv(self.file_path + "Sorensen_Dice_rate_matrix_more.csv",index = True, header = True)
         

#def main(path_bam,file_path,start,n,num,c,file_compare):

    
# parser = argparse.ArgumentParser(description='Parameters') 
# parser.add_argument('--path_bam',type=str)
# parser.add_argument('--file_path', type=str)
# parser.add_argument('--start', type=int)
# parser.add_argument('--n', type=int)
# parser.add_argument('--num',type=int)
# parser.add_argument('--c', type=int)
# parser.add_argument('--file_compare',type=str)

# args = parser.parse_args() 
#     
# if __name__ == '__main__':
#     main(args.path_bam,args.file_path,args.start,args.n,args.num,args.c,args.file_compare)
    