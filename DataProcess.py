import os
import sys
import subprocess
class DataProcessUtil:
    def __init__(self,path):
        self.path=path
        self.headContigs = {}
        self.endFiles = {}
        self.contigs = {}
        self.tinyContigs = {}
        # plasmids=[35,36,37,39,41,42,45,46,47,48,52,53,54]
        self.plasmids = []
        self.filter=set()
        self.lv = []
        #
        self.maxContigLength = 0
        self.minContigLength = sys.maxsize
        self.contigPreBps = {}
        self.contigNextBps = {}
        self.seriesLength={}
        self.repeatLongContigs=[]
        self.ignoreContigs=[]

        #self.plasmids_plasmids=[]
    def readPlasmids(self):
        if os.path.exists(self.path+'/spades_result_unique_new/prediction_plasmid_plasflow.txt'):
            with open(self.path+'/spades_result_unique_new/prediction_plasmid_plasflow.txt', 'r') as file:
                # 按行读取文件内容
                lines = file.readlines()
                for line in lines:
                    index = line.find('_')
                    if index != -1:
                        nums=line.split('_')
                        self.plasmids.append(int(nums[1]))
                        print(nums[1])
                    else:
                        self.plasmids.append(int(line.split(' ')[0].replace('>','')))

    # def readPlasmids_plasmids(self):
    #     if os.path.exists(self.path+'/prediction_plasmid_plasflow.txt'):
    #         with open(self.path+'/prediction_plasmid_plasflow.txt', 'r') as file:
    #             # 按行读取文件内容
    #             lines = file.readlines()
    #             for line in lines:
    #                 index = line.find('_')
    #                 if index != -1:
    #                     nums=line.split('_')
    #                     self.plasmids_plasmids.append(int(nums[1]))
    #                     print(nums[1])
    #                 else:
    #                     self.plasmids_plasmids.append(int(line.split(' ')[0].replace('>','')))



    def printSeries(self,id1,id2):
        print(self.tinyContigs[id1].series[166-1:242])
        #print(self.reverseSeries(self.tinyContigs[id1].series[166-1:242]))
        print('------')
        #print(self.tinyContigs[id2].series[2873-1:2949])
        print(self.reverseSeries(self.tinyContigs[id2].series[0:2949]))
    def  reverseSeries(self,series):
        temp = ''

        for char in series:
            if char == 'A':
                temp = temp + 'T'
            elif char == 'T':
                temp = temp + 'A'
            elif char == 'C':
                temp = temp + 'G'
            elif char == 'G':
                temp = temp + 'C'
        temp = ''.join(reversed(temp))
        return temp
    def readDepthTable_Plasmid(self,length_threshold):
        self.generateFilter()
        if os.path.exists(self.path + '/spades_result_unique_new/output_with_depth_table.txt'):
            with open(self.path + '/spades_result_unique_new/output_with_depth_table.txt', 'r') as file:
                # 按行读取文件内容
                lines = file.readlines()
                lines.pop(0)
                # 打印每一行的内容
                for line in lines:
                    nums = line.split('\t')
                    length = int(nums[1])
                    idStr = nums[0].split('_')[1]
                    if (int(idStr) not in self.lv):
                        self.contigPreBps[idStr] = {}
                        self.contigNextBps[idStr] = {}
                        if length >= length_threshold and int(idStr) in self.plasmids:
                            # print(idStr)
                            if (idStr.replace(" ", "") in self.filter):
                                self.contigs[idStr] = Contig(idStr, length)
                            # print(self.contigs)

                        else:
                            # if (int(idStr) in self.plasmids):
                            #     continue
                            self.tinyContigs[idStr] = Contig(idStr, length)
                        if (length > self.maxContigLength):
                            self.maxContigLength = length
                        if (length < self.minContigLength):
                            self.minContigLength = length
    def readRepeat(self,space):
        print("读取可重复长序列信息")
        print(space + '/duplicated_long_contigs_name.txt')
        if os.path.exists(space + '/duplicated_long_contigs_name.txt'):
            with open(space + '/duplicated_long_contigs_name.txt', 'r') as file:
                lines=file.readlines()
                for line in lines:
                    self.repeatLongContigs.append(int(line))
        print("读取可重复长序列信息over")
    def readDepthTable(self,length_threshold):
        self.generateFilter()
        if os.path.exists(self.path+'/spades_result_unique_new/output_with_depth_table.txt'):
            with open(self.path+'/spades_result_unique_new/output_with_depth_table.txt', 'r') as file:
                # 按行读取文件内容
                lines = file.readlines()
                lines.pop(0)
                # 打印每一行的内容
                for line in lines:
                    nums=line.split('\t')
                    length=int(nums[1])
                    idStr=nums[0].split('_')[1]
                    if(int(idStr) not in self.lv  ):
                        self.contigPreBps[idStr]={}
                        self.contigNextBps[idStr]={}
                        if length>=length_threshold:
                            #print(idStr)
                            if(idStr.replace(" ","") in self.filter):
                                self.contigs[idStr]=Contig(idStr,length)
                            if(int(idStr) in self.repeatLongContigs):
                                print("添加重复序列:"+idStr)
                                if length < 10000:
                                    self.ignoreContigs.append(int(idStr))
                                else:
                                    self.tinyContigs[idStr] = Contig(idStr, length)
                            #print(self.contigs)

                        else:
                            # if (int(idStr) in self.plasmids):
                            #     continue
                            self.tinyContigs[idStr] = Contig(idStr, length)
                        if (length > self.maxContigLength):
                            self.maxContigLength = length
                        if (length < self.minContigLength):
                            self.minContigLength = length
                #print(self.contigs)
    def isContigDirectionConflict(self,pairs,directionPair,direction):
        directionPairNums=directionPair.split('_')
        pair=directionPairNums[1]+'_'+directionPairNums[0]
        if(pair in pairs):
            if(pairs[pair]=='0'):
                if(direction!='3'):
                    return True
            if (pairs[pair] == '1'or pairs[pair] == '2'):
                if (direction != pairs[pair]):
                    return True
            if (pairs[pair] == '3'):
                if (direction != '0'):
                    return True
        return False

    def isContigDirectionCompeteConflict(self, pairs, directionPair, contigNextPairs,contigPrePairs,direction):
        directionPairNums = directionPair.split('_')
        a=None
        b=None
        if (direction == '0'):
            if directionPairNums[0] in contigNextPairs:
                a=contigNextPairs[directionPairNums[0]]
            if directionPairNums[1] in contigPrePairs:
                b=contigPrePairs[directionPairNums[1]]
        elif (direction == '1'):
            if directionPairNums[0] in contigNextPairs:
                a=contigNextPairs[directionPairNums[0]]
            if directionPairNums[1] in contigNextPairs:
                b=contigNextPairs[directionPairNums[1]]
        elif (direction == '2'):
            if directionPairNums[0] in contigPrePairs:
                a=contigPrePairs[directionPairNums[0]]
            if directionPairNums[1] in contigPrePairs:
                b=contigPrePairs[directionPairNums[1]]
        elif (direction == '3'):
            if directionPairNums[0] in contigPrePairs:
                a=contigPrePairs[directionPairNums[0]]
            if directionPairNums[1] in contigNextPairs:
                b=contigNextPairs[directionPairNums[1]]
        return a,b

    def generateContigNextOrPrePairs(self,directionPair,contigNextPairs,contigPrePairs,direction):
        directionPairNums = directionPair.split('_')
        if(direction=='0'):
            contigNextPairs[directionPairNums[0]]=directionPair
            contigPrePairs[directionPairNums[1]]=directionPair
        elif(direction=='1'):
            contigNextPairs[directionPairNums[0]] = directionPair
            contigNextPairs[directionPairNums[1]] = directionPair
        elif (direction == '2'):
            contigPrePairs[directionPairNums[0]] = directionPair
            contigPrePairs[directionPairNums[1]] = directionPair
        elif (direction == '3'):
            contigPrePairs[directionPairNums[0]] = directionPair
            contigNextPairs[directionPairNums[1]] = directionPair
    def deletePairInformation(self,pairs,pairsScore,directionPair,contigNextPairs,contigPrePairs):
        direction=pairs[directionPair]
        directionPairNums = directionPair.split('_')
        del pairsScore[directionPair]
        del pairs[directionPair]
        if (direction == '0'):
            del contigNextPairs[directionPairNums[0]]
            del contigPrePairs[directionPairNums[1]]
        elif (direction =='1'):
            del contigNextPairs[directionPairNums[0]]
            del contigNextPairs[directionPairNums[1]]
        elif (direction == '2'):
            del contigPrePairs[directionPairNums[0]]
            del contigPrePairs[directionPairNums[1]]
        elif (direction == '3'):
            del contigPrePairs[directionPairNums[0]]
            del contigNextPairs[directionPairNums[1]]
    def generateFilter(self):
        with open(self.path+'/spades_result_unique_new/label_list(jaccard).txt', 'r') as file:
            # 按行读取文件内容
            lines = file.readlines()
            for line in lines:
                nums = line.split('\t')
                directionPair = nums[0].replace('contig', '')
                directionPairNums = directionPair.split('_')
                self.filter.add(directionPairNums[0])
                self.filter.add(directionPairNums[1])
    #10 3 10 5
    def isTwoContigPairConflict(self,directionPairNums,directionPairNums1,direction,direction1):
        if(direction=='0' or direction=='1'):
            if(direction1=='1' or direction1=='0'):
                return True
        if (direction == '2' or direction == '3'):
            if (direction1 == '2' or direction1 == '3'):
                return True
        return False


    def readDirection(self,isPlasmids):
        pairs={}
        pairsScore={}
        contigNextPairs={}
        contigPrePairs = {}

        # 打开文件
        with open(self.path+'/spades_result_unique_new/label_list(jaccard).txt', 'r') as file:
            # 按行读取文件内容
            lines = file.readlines()
            # 打印每一行的内容
            index=0
            while index <len(lines):
                line = lines[index]
                #print(contigNextPairs)
                nums=line.split('\t')
                directionPair=nums[0].replace('contig','')
                directionPairNums = directionPair.split('_')
                if(int(directionPairNums[0]) in self.ignoreContigs or
                int(directionPairNums[1]) in self.ignoreContigs):
                    continue
                direction=nums[2].replace('\n','')
                score=float(nums[1])
                if(directionPairNums[0] in self.contigs and directionPairNums[1] in self.contigs):
                    if(self.isContigDirectionConflict(pairs,directionPair,direction)):
                        print('匹配对本身conflict')
                        if(directionPairNums[0] in contigNextPairs and directionPairNums[0] in contigPrePairs
                        and directionPairNums[1] in contigNextPairs and directionPairNums[1] in contigPrePairs):
                            print("优化匹配")
                            if(int(directionPairNums[0])>int(directionPairNums[1])):
                                if(index+1<len(lines)):
                                    line1=lines[index+1]
                                    nums1 = line1.split('\t')
                                    directionPair1 = nums1[0].replace('contig', '')
                                    directionPairNums1 = directionPair1.split('_')
                                    direction1 = nums1[2].replace('\n', '')
                                    score1 = float(nums1[1])
                                    if(directionPairNums1[0] ==directionPairNums[0]):
                                        if(self.isTwoContigPairConflict(directionPairNums,directionPairNums1,direction,direction1)==False):
                                            pair = directionPairNums[1] + '_' + directionPairNums[0]
                                            self.deletePairInformation(pairs, pairsScore, pair, contigNextPairs,
                                                                       contigPrePairs)
                                            pairs[directionPair] = direction
                                            pairsScore[directionPair] = score
                                            self.generateContigNextOrPrePairs(directionPair, contigNextPairs,
                                                                              contigPrePairs, direction)

                                            pair1 = directionPairNums1[1] + '_' + directionPairNums1[0]
                                            self.deletePairInformation(pairs, pairsScore, pair1, contigNextPairs,
                                                                       contigPrePairs)
                                            pairs[directionPair1] = direction1
                                            pairsScore[directionPair1] = score1
                                            self.generateContigNextOrPrePairs(directionPair1, contigNextPairs,
                                                                              contigPrePairs, direction1)
                                            index=index+1
                                            print("优化匹配top")
                        elif(int(directionPairNums[0])>int(directionPairNums[1])):
                            pair=directionPairNums[1]+'_'+directionPairNums[0]
                            self.deletePairInformation(pairs, pairsScore, pair, contigNextPairs,
                                                       contigPrePairs)
                            pairs[directionPair] = direction
                            pairsScore[directionPair] = score
                            self.generateContigNextOrPrePairs(directionPair,contigNextPairs,contigPrePairs,direction)
                    else:
                        CompetePaira,CompetePairb=self.isContigDirectionCompeteConflict(pairs, directionPair, contigNextPairs,contigPrePairs,direction)
                        if(CompetePaira!=None or CompetePairb!=None):
                            isAdd=True
                            if(CompetePaira!=None and score<=pairsScore[CompetePaira]) :
                                print('匹配竞争conflict' + '___' + directionPair + 'vs' + CompetePaira)
                                isAdd=False
                            if (CompetePairb != None and score <= pairsScore[CompetePairb]):
                                print('匹配竞争conflict' + '___' + directionPair + 'vs' + CompetePairb)
                                isAdd = False
                            if (CompetePaira != None and score > pairsScore[CompetePaira] and isAdd==True):
                                self.deletePairInformation(pairs, pairsScore, CompetePaira, contigNextPairs,
                                                           contigPrePairs)
                            if (CompetePairb != None and score > pairsScore[CompetePairb] and isAdd==True):
                                self.deletePairInformation(pairs, pairsScore, CompetePairb, contigNextPairs,
                                                           contigPrePairs)
                            if(isAdd==True):
                                pairs[directionPair] = direction
                                pairsScore[directionPair] = score
                                self.generateContigNextOrPrePairs(directionPair, contigNextPairs, contigPrePairs, direction)
                        else:
                            pairs[directionPair] = direction
                            pairsScore[directionPair] = score
                            self.generateContigNextOrPrePairs(directionPair, contigNextPairs, contigPrePairs, direction)
                index=index+1
        for key1, value in pairs.items():
            key=key1.split('_')
            print(key)
            if key[0] in self.contigs and key[1] in self.contigs:
                if value == '0':
                    self.contigs[key[0]].next = self.contigs[key[1]]
                    self.contigs[key[1]].pre = self.contigs[key[0]]
                elif value == '1':
                    # self.contigs[directionPair[0]].direction = 0
                    # self.contigs[directionPair[1]].direction = 1
                    self.contigs[key[0]].next = self.contigs[key[1]]
                    self.contigs[key[1]].next = self.contigs[key[0]]
                elif value == '2':
                    # self.contigs[directionPair[0]].direction = 1
                    # self.contigs[directionPair[1]].direction = 0
                    self.contigs[key[0]].pre = self.contigs[key[1]]
                    self.contigs[key[1]].pre = self.contigs[key[0]]
                elif value == '3':
                    # self.contigs[directionPair[0]].direction = 1
                    # self.contigs[directionPair[1]].direction = 1
                    self.contigs[key[0]].pre = self.contigs[key[1]]
                    self.contigs[key[1]].next = self.contigs[key[0]]
        if(isPlasmids==True):
            self.plasmids.clear()
        self.deletePlasmidsContigs()
    def isContigConnected(self,contig,contig1):
        if(contig1==None):
            return False
        elif((contig1.next!=None and contig1.next==contig )or ( contig1.pre!=None and contig1.pre==contig)):
            return True
        else:
            return False
    def deletePlasmidsContigs(self):
        for c in self.contigs:
            if self.contigs[c].using == False and (
                    (self.isContigConnected(self.contigs[c],self.contigs[c].pre) and self.isContigConnected(self.contigs[c],self.contigs[c].next)==False
                                                   )
            or(self.isContigConnected(self.contigs[c],self.contigs[c].pre)==False and self.isContigConnected(self.contigs[c],self.contigs[c].next))
            ):
                contigHead = self.contigs[c]
                contigX=None
                lastDirection = 0
                if self.isContigConnected(self.contigs[c],self.contigs[c].next):
                    self.headContigs[c]=0
                    #print('--' + contigHead.i + '-->', end='|')
                    contigX = contigHead.next
                    lastDirection = 0
                if self.isContigConnected(self.contigs[c],self.contigs[c].pre):
                    self.headContigs[c] = 1
                    #print('<--' + contigHead.i + '--', end='|')
                    contigX = contigHead.pre
                    lastDirection = 1
                contigHead.using = True
                contigPre = contigHead

                while contigX != None and contigX != contigHead:
                    print("de"+contigX.i)
                    if contigX.pre != None and contigX.pre == contigPre:
                        contigX.using = True
                        if (int(contigX.i) in self.plasmids):
                            self.deleteContig(contigX, lastDirection, contigPre, 0)
                            if (lastDirection == 0):
                                contigX = contigPre.next
                            else:
                                contigX = contigPre.pre
                        else:
                            contigPre = contigX
                            contigX = contigX.next
                            lastDirection = 0
                    elif contigX.next != None and contigX.next == contigPre:
                        contigX.using = True
                        if (int(contigX.i) in self.plasmids):

                            self.deleteContig(contigX, lastDirection, contigPre, 1)
                            if (lastDirection == 0):
                                contigX = contigPre.next
                            else:
                                contigX = contigPre.pre
                        else:
                            contigPre = contigX
                            contigX = contigX.pre
                            lastDirection = 1
                    elif contigX.pre==None and contigX.next==contigPre:
                        contigX.using = True
                        break
                    else:
                        if (lastDirection == 0):
                            contigPre.next=None
                        else:
                            contigPre.pre=None
                        break
        for c in self.contigs:
            if self.contigs[c].using==False:
                contigHead = self.contigs[c]
                if (contigHead.next == None):
                    self.headContigs[c]=0
                    continue
                self.headContigs[c] = 0
                lastDirection = 0
                #print('--' + contigHead.i + '-->', end='|')
                contigX = contigHead.next
                contigHead.using = True
                contigPre = contigHead
                while contigX != None and contigX != contigHead:
                    print("de1" + contigX.i)
                    if contigX.pre != None and contigX.pre == contigPre:
                        contigX.using = True
                        if (int(contigX.i) in self.plasmids):
                            self.deleteContig(contigX, lastDirection, contigPre, 0)
                            if (lastDirection == 0):
                                contigX = contigPre.next
                            else:
                                contigX = contigPre.pre
                        else:
                            contigPre = contigX
                            contigX = contigX.next
                            lastDirection = 0
                    elif contigX.pre != None and contigX.next == contigPre:
                        contigX.using = True
                        if (int(contigX.i) in self.plasmids):

                            self.deleteContig(contigX, lastDirection, contigPre, 1)
                            if (lastDirection == 0):
                                contigX = contigPre.next
                            else:
                                contigX = contigPre.pre
                        else:
                            contigPre = contigX
                            contigX = contigX.pre
                            lastDirection = 1
                    else:
                        break
        for c in self.contigs:
            self.contigs[c].using=False
        for i in self.plasmids:
            if(str(i) in self.headContigs):
                print(str(i))
                contigP=None
                if(self.headContigs[str(i)]==0):
                    contigP=self.contigs[str(i)].next
                else:
                    contigP =self.contigs[str(i)].pre
                if(contigP!=None):
                    if(contigP.pre!=None and contigP.pre==self.contigs[str(i)]):
                        self.headContigs[contigP.i]=0
                        contigP.pre=None
                    else:
                        self.headContigs[contigP.i] = 1
                        contigP.next = None
                del self.headContigs[str(i)]
            if (str(i) in self.contigs):
                del self.contigs[str(i)]
        for i in self.repeatLongContigs:
            if(str(i)) in self.headContigs:
                if self.contigs[str(i)].next==None and self.contigs[str(i)].pre==None:
                    del self.headContigs[str(i)]
        # toRemove = {}
        # for i in self.headContigs:
        #     if (self.contigs[i].length < 8000 and self.contigs[i].next == None and self.contigs[i].pre == None):
        #         toRemove[i] = 0
        # for i in toRemove:
        #     del self.headContigs[i]


        # contigHead = self.contigs['1']
        # contigX = contigHead.next
        # contigPre = contigHead
        # lastDirection=0

    def deleteContig(self,contigX,lastDirection,contigPre,currentDirection):
        if(currentDirection==0):
            contigLater=contigX.next
        else:
            contigLater=contigX.pre
        if(lastDirection==0):
            contigPre.next=contigLater
        else:
            contigPre.pre=contigLater
        if contigLater!=None:
            if contigLater.pre != None and contigLater.pre == contigX:
                contigLater.pre=contigPre
            elif contigLater.next != None and contigLater.next == contigX:
                contigLater.next=contigPre
        #del self.contigs[contigX.i]






                # if int(nums[1])>=length_threshold:
                #     self.contigs[nums[0].split('_')[1]]=Contig(0,nums[1])

    def readGenome(self):
        # 打开文件
        with open(self.path+'/spades_result_unique_new/outfile_genome.txt', 'r') as file:
            # 按行读取文件内容
            lines = file.readlines()
            preLine=''
            for line in lines:
                if line.__contains__('>'):
                    preLine=line.replace('>','').replace('\n','')
                if preLine in self.contigs:
                    self.contigs[preLine].series=line.replace('\n','')
                if preLine in self.tinyContigs:
                    self.tinyContigs[preLine].series=line.replace('\n','')
    def writeN(self,file,cnt,c,indexx,id):
        temp=''
        #temp+=str(id)
        for i in range(cnt):
            temp+=c
        if len(temp)<60-indexx:
            file.write(temp[0:])
            return len(temp)+indexx
        index=0
        file.write(temp[0:60-indexx]+'\n')
        index=index+60-indexx
        indexy=0
        while index <= len(temp) - 60:
            file.write(temp[index:index + 60] + '\n')
            index = index + 60
        if index < len(temp):
            file.write(temp[index:] )
            indexy=len(temp)-index
        file.flush()
        return indexy
    def encodeFastA(self,outputSpace):
        i=-1
        fileId=-1
        if os.path.exists(outputSpace+'/fastA.txt'):
            with open(outputSpace+'/fastA.txt', 'r') as file:
                lines = file.readlines()
                x=EndContig(i)
                isNewN=True
                cnt=0
                self.endFiles[-1]={}
                for line in lines:
                    if(line.__contains__('>')):
                        if (isNewN == True):
                            self.endFiles[fileId][i] = x
                        i=0
                        x = EndContig(i)
                        isNewN = True
                        cnt = 0
                        fileId+=1
                        self.endFiles[fileId]={}
                    else:
                        index=line.find('N')
                        if index != -1:
                            endIndex=line.rfind('N')
                            if isNewN==True:
                                x.series+=line.replace('N','').replace('\n','')
                                cnt=endIndex-index+1
                                isNewN=False
                            else:
                                cnt+=endIndex-index+1
                                if(cnt==100):
                                    isNewN=True
                                    self.endFiles[fileId][i]=x
                                    i=i+1
                                    x=EndContig(i)
                                    x.series+=line.replace('N','').replace('\n','')
                        else:
                            x.series+=line.replace('\n','')
                if (isNewN==True):
                    self.endFiles[fileId][i] = x
        #print(len(self.endFiles[0]))
        rs=0
        fileId = 0
        for headId in self.headContigs:
            with open(outputSpace + '/MultiSeries_'+headId+'.txt', "w") as file1:
                for id in range(0,len(self.endFiles[fileId])):
                    rs+=1
                    file1.write('>'+str(id)+'\n')
                    file1.write(self.endFiles[fileId][id].series+'\n')
                    file1.flush()
                rs-=1
            fileId+=1
        return rs


    def writeFastA(self,outputSpace,isInit):
        tinyBreakCnt = 0
        with open(outputSpace + "/fastA.txt", "w") as file:
            duanId=1
            for headId in self.headContigs:
                if(isInit==False):
                    file.write('>'+str(duanId)+'_sequence_length_'+str(self.seriesLength[duanId])+'bp'+'\n')
                else:
                    self.seriesLength[duanId]=0
                file.flush()

                index = 0
                contigHead = self.contigs[headId]
                contigX = None
                if self.headContigs[headId] == 0:
                    #print('--' + contigHead.i + '-->', end='|')
                    contigPre = contigHead.tinyPre
                    index = self.writeSeries(file, contigPre, contigHead, 0, index,duanId)
                    contigX = contigHead.next
                    index, isConnected = self.showTinySeries(contigHead, contigX, index, file, 0,duanId)
                if self.headContigs[headId] == 1:
                    #print('<--' + contigHead.i + '--', end='|')
                    contigPre = contigHead.tinyNext
                    index = self.writeSeries(file, contigPre, contigHead, 1, index,duanId)
                    contigX = contigHead.pre
                    index, isConnected = self.showTinySeries(contigHead, contigX, index, file, 1,duanId)
                contigPre = contigHead
                isBreak = False  # bigContig break
                while contigX != contigHead and contigX!=None:
                    if contigX.pre != None and contigX.pre == contigPre:
                        if (isConnected == False):
                            index = self.writeN(file, 100, 'N', index, tinyBreakCnt)
                            tinyBreakCnt += 1
                            index = self.showleftTinySeries(contigX, index, file, 0,duanId)
                        index = self.writeSeries(file, contigX.tinyPre, contigX, 0, index,duanId)
                        contigPre = contigX
                        if contigX.next == None:
                            index, isConnected = self.showTinySeries(contigPre, None, index, file, 0,duanId)
                            isBreak = True
                            break
                        contigX = contigX.next
                        index, isConnected = self.showTinySeries(contigPre, contigX, index, file, 0,duanId)
                    elif contigX.pre != None and contigX.next == contigPre:
                        if (isConnected == False):
                            index = self.writeN(file, 100, 'N', index, tinyBreakCnt)
                            tinyBreakCnt += 1
                            index = self.showleftTinySeries(contigX, index, file, 1,duanId)

                        index = self.writeSeries(file, contigX.tinyNext, contigX, 1, index,duanId)
                        contigPre = contigX
                        contigX = contigX.pre
                        index, isConnected = self.showTinySeries(contigPre, contigX, index, file, 1,duanId)
                    elif contigX.pre == None and contigX.next == contigPre:
                        if (isConnected == False):
                            index = self.writeN(file, 100, 'N', index, tinyBreakCnt)
                            tinyBreakCnt += 1
                            index = self.showleftTinySeries(contigX, index, file, 1,duanId)
                        index = self.writeSeries(file, contigX.tinyNext, contigX, 1, index,duanId)
                        index, isConnected = self.showTinySeries(contigX, None, index, file, 1,duanId)
                        isBreak = True
                        break
                    else:
                        #contigX.pre == None and contigX.next != contigPre:
                        isBreak = True
                        break
                if (isBreak == False and isConnected == False):
                    index = self.writeN(file, 100, 'N', index, tinyBreakCnt)
                    tinyBreakCnt += 1
                    if(contigX!=None):
                        index = self.showleftTinySeries(contigX, index, file, 0,duanId)
                file.write('\n')
                duanId += 1

            file.close()
        print('已生成序列文件：' + outputSpace + '/fastA.txt')
        return duanId-1
            # contigHead = self.contigs['1']
            # contigPre=contigHead.tinyPre
            # index=self.writeSeries(file, contigPre,contigHead, 0,index)
            # contigX = contigHead.next
            # index,isConnected=self.showTinySeries(contigHead, contigX,index,file,0)
        #     contigPre = contigHead
        #     isBreak=False #bigContig break
        #     while contigX != contigHead:
        #         if contigX.pre != None and contigX.pre == contigPre:
        #             if(isConnected==False):
        #                 index=self.writeN(file,100,'N',index,tinyBreakCnt)
        #                 tinyBreakCnt+=1
        #                 index=self.showleftTinySeries(contigX,index,file,0)
        #             index=self.writeSeries(file, contigX.tinyPre,contigX, 0,index)
        #             contigPre = contigX
        #             if contigX.next == None:
        #                 index,isConnected = self.showTinySeries(contigPre, None, index, file, 0)
        #                 isBreak=True
        #                 break
        #             contigX = contigX.next
        #             index,isConnected = self.showTinySeries(contigPre, contigX, index, file,0)
        #         elif contigX.pre != None and contigX.next == contigPre:
        #             if (isConnected == False):
        #                 index = self.writeN(file, 100, 'N', index,tinyBreakCnt)
        #                 tinyBreakCnt += 1
        #                 index = self.showleftTinySeries(contigX, index, file, 1)
        #
        #             index=self.writeSeries(file,contigX.tinyNext, contigX, 1,index)
        #             contigPre = contigX
        #             contigX = contigX.pre
        #             index,isConnected = self.showTinySeries(contigPre, contigX, index, file,1)
        #         elif contigX.pre == None and contigX.next == contigPre:
        #             if (isConnected == False):
        #                 index = self.writeN(file, 100, 'N', index,tinyBreakCnt)
        #                 tinyBreakCnt += 1
        #                 index = self.showleftTinySeries(contigX, index, file, 1)
        #             index=self.writeSeries(file,contigX.tinyNext, contigX, 1,index)
        #             index,isConnected = self.showTinySeries(contigX, None, index, file,1)
        #             isBreak = True
        #             break
        #         elif contigX.pre == None and contigX.next != contigPre:
        #             isBreak = True
        #             break
        #     if (isBreak==False and isConnected == False):
        #         index = self.writeN(file, 100, 'N', index,tinyBreakCnt)
        #         tinyBreakCnt += 1
        #         index = self.showleftTinySeries(contigX, index, file, 0)
        # file.close()
        # print('已生成序列文件：' + outputSpace + '/fastA.txt')
        # return tinyBreakCnt
    def showTinySeries(self,contigHead,contigNext,index,file,direction,duanId):
        indexX=index
        if direction == 0:
            contigX = contigHead.tinyNext
        else:
            contigX = contigHead.tinyPre
        contigPre = contigHead
        #hasTiny=False
        while contigX!=None :
            #hasTiny=True
            if contigPre in contigX.tiny_bigPre or contigX.tinyPre == contigPre:
                indexX=self.writeSeries(file, contigPre,contigX, 0,indexX,duanId)
                contigPre = contigX
                contigX = contigX.tinyNext
            elif contigPre in contigX.tiny_bigNext or contigX.tinyNext == contigPre:
                indexX=self.writeSeries(file, contigPre,contigX, 1,indexX,duanId)
                contigPre = contigX
                contigX = contigX.tinyPre
        isConnected=False
        if(contigNext in contigPre.tiny_bigNext or contigNext in contigPre.tiny_bigPre):
            isConnected=True
        return indexX,isConnected
    def showleftTinySeries(self,contigRight,index1,file,rightContigDirection,duanId):
        temp = ''
        indexx=index1
        if rightContigDirection == 0:
            contigX = contigRight.tinyPre
        else:
            contigX = contigRight.tinyNext
        contigPre = contigRight
        #hasTiny=False
        while contigX!=None :
            #hasTiny=True
            if contigPre in contigX.tiny_bigPre or contigX.tinyPre == contigPre:
                temp=self.generateLeftSeries(file,contigPre.i,contigX,1,temp)
                contigPre = contigX
                contigX = contigX.tinyNext
            elif contigPre in contigX.tiny_bigNext or contigX.tinyNext == contigPre:
                temp = self.generateLeftSeries(file, contigPre.i,contigX, 0, temp)
                contigPre = contigX
                contigX = contigX.tinyPre
        self.seriesLength[duanId] = self.seriesLength[duanId] + len(temp)
        if len(temp)<60-indexx:
            file.write(temp[0:])
            file.flush()
            return len(temp)+indexx
        index=0

        file.write(temp[0:60-indexx]+'\n')
        index=index+60-indexx
        indexy=0
        while index <= len(temp) - 60:
            file.write(temp[index:index + 60] + '\n')
            index = index + 60
        if index < len(temp):
            file.write(temp[index:] )
            indexy=len(temp)-index
        file.flush()
        return indexy

    def writeFastA_Old(self,outputSpace):
        # 使用with语句打开文件并自动关闭
        with open(outputSpace+"/fastA.txt", "w") as file:
            contigHead = self.contigs['1']
            # print('--' + contigHead.i + '-->', end='|')
            #file.print('>'+contigHead.i+'_length_'+self.contigs['1'].length+'\n')
            self.writeSeries(file,contigHead,0)
            contigX = contigHead.next
            contigPre = contigHead
            while contigX != contigHead:
                if contigX.pre != None and contigX.pre == contigPre:
                    self.writeSeries(file, contigX, 0)
                    contigPre = contigX
                    if contigX.next == None:
                        break
                    contigX = contigX.next
                elif contigX.pre != None and contigX.next == contigPre:
                    self.writeSeries(file, contigX, 1)
                    contigPre = contigX
                    contigX = contigX.pre
                elif contigX.pre == None and contigX.next == contigPre:
                    self.writeSeries(file, contigX, 1)
                    break
                elif contigX.pre == None and contigX.next != contigPre:
                    break


        print('已生成序列文件：' + outputSpace + '/fastA.txt')

    def generateLeftSeries(self, file,lastId, contig, direction,str):
        temp = ''
        if direction == 1:
            for char in contig.series:
                if   char == 'A':
                    temp = temp + 'T'
                elif char == 'T':
                    temp = temp + 'A'
                elif char == 'C':
                    temp = temp + 'G'
                elif char == 'G':
                    temp = temp + 'C'
            temp = ''.join(reversed(temp))
        else:
            temp = contig.series
        #if contig.i in self.tinyContigs:
        if direction == 1:
            temp = temp[:-1*self.contigPreBps[contig.i][lastId]]
        else:
            temp = temp[:-1*self.contigNextBps[contig.i][lastId]]
        return temp+str
    def writeSeries(self,file,lastContigId,contig,direction,indexx,duanId):
        temp = ''
        if direction == 1:
            for char in contig.series:
                if char == 'A':
                    temp = temp + 'T'
                elif char == 'T':
                    temp = temp + 'A'
                elif char == 'C':
                    temp = temp + 'G'
                elif char == 'G':
                    temp = temp + 'C'
            temp = ''.join(reversed(temp))

        else:
            temp = contig.series

        #if contig.i in self.tinyContigs:
        if direction == 1:
            #print(contig.i+'...'+lastContigId)
            #print(self.contigNextBps[contig.i])
            if(lastContigId!=None):
                if lastContigId.i in self.contigNextBps[contig.i]:
                    temp=temp[self.contigNextBps[contig.i][lastContigId.i]:]

        else :
            if (lastContigId != None):
                if lastContigId.i in self.contigPreBps[contig.i]:
                    temp=temp[self.contigPreBps[contig.i][lastContigId.i]:]
        self.seriesLength[duanId] = self.seriesLength[duanId] + len(temp)
        if len(temp)<60-indexx:
            file.write(temp[0:])
            file.flush()

            return len(temp)+indexx
        index=0
        file.write(temp[0:60-indexx]+'\n')

        index=index+60-indexx
        indexy=0
        while index <= len(temp) - 60:
            file.write(temp[index:index + 60] + '\n')

            index = index + 60
        if index < len(temp):
            file.write(temp[index:] )
            indexy=len(temp)-index
        file.flush()
        return indexy

    def writeSeries_old(self,file,contig,direction):
        temp=''
        if direction==1:
            for char in contig.series:
                if char =='A':
                    temp=temp+'T'
                elif char =='T':
                    temp=temp+'A'
                elif char =='C':
                    temp=temp+'G'
                elif char=='G':
                    temp=temp+'C'
            temp= ''.join(reversed(temp))

        else:
            temp = contig.series

        file.write('>' + contig.i + '_length_' + str(contig.length) + '\n')
        index=0
        while index<=contig.length-60:
            file.write(temp[index:index+60]+'\n')
            index=index+60
        if index<contig.length:
            file.write(temp[index:]+'\n')

    def realExtendSeries(self,contig,path,direction,bigContig,isN):
        i=0
        preContig=self.tinyContigs[path.list[i]].deepCopy()
        if(direction==0):#next later
            contig.tinyNext=preContig
        else:#pre
            contig.tinyPre = preContig
        if (path.directions[i] == 0):  # next last
            preContig.tiny_bigNext.append(contig)
        else:
            preContig.tiny_bigPre.append(contig)
        #preContig=self.tinyContigs[path.list[i]]
        preDirection=path.directions[i]
        i+=1
        while(i<len(path.list)):
            x=self.tinyContigs[path.list[i]].deepCopy()
            if(preDirection==0):
                preContig.tinyPre=x
            else:
                preContig.tinyNext = x
            if(path.directions[i]==0):
                x.tinyNext=preContig
            else:
                x.tinyPre=preContig
            preContig=x
            preDirection=path.directions[i]
            i+=1
        if(isN==False):
            if(preDirection==0):#next last
                preContig.tiny_bigPre.append(bigContig)
            else:
                preContig.tiny_bigNext.append(bigContig)
            if(bigContig.pre==contig):
                bigContig.tinyPre=preContig
            else:
                bigContig.tinyNext = preContig









    #深度优先遍历寻找最长序列
    def extendSeries(self,coincidenceThreshold,coincidenceThreshold_1):
        for contigId in self.contigs:
            contig=self.contigs[contigId]
            nextContig=contig.next
            preContig=contig.pre
            if contig.tinyNext==None:
                tinyList = []
                nList=[]
                path=Path()
                self.extendTail(contigId,coincidenceThreshold,nextContig,tinyList,nList,path,coincidenceThreshold_1,True)
                path=Path.getLongestPath(tinyList)
                if path==None:
                    path = Path.getLongestPathMultiplePriorities(nList)
                    if path!=None:
                        self.realExtendSeries(contig, path, 0, nextContig, True)
                else:
                    self.realExtendSeries(contig, path, 0, nextContig, False)
            if contig.tinyPre==None:
                tinyList = []
                nList = []
                path = Path()
                self.extendHead(contigId,coincidenceThreshold,preContig,tinyList,nList,path,coincidenceThreshold_1,True)
                path = Path.getLongestPath(tinyList)
                if path == None:
                    path = Path.getLongestPathMultiplePriorities(nList)
                    if path != None:
                        self.realExtendSeries(contig, path, 1, preContig, True)
                else:
                    self.realExtendSeries(contig, path, 1, preContig, False)
                print(contigId + 'head')
                if (contig.tinyPre != None):
                    print('is' + contig.tinyPre.i)
    def extendTail(self,id,coincidenceThreshold,bigContig,lists,nLists,path,coincidenceThreshold_1,isLongContig):
        contig=None
        isTiny = False
        if (isLongContig):
            contig = self.contigs[id]
        else:
            isTiny = True
            contig = self.tinyContigs[id]
        length = contig.length
        if os.path.exists(self.path+'/blast_connection/blast_all_info/all_'+id+'.txt'):
            with open(self.path+'/blast_connection/blast_all_info/all_'+id+'.txt', 'r') as file:
                lines = file.readlines()
                if(bigContig!=None):
                    for line in lines:
                        nums=line.split('\t')
                        bps = int(nums[3])
                        coincidenceEquality=float(nums[2])
                        if nums[0] == bigContig.i \
                        and bps>=32\
                        and float(nums[2])>coincidenceThreshold_1 and nums[0]!=id:
                            tinyLength = self.contigs[nums[0]].length
                            if (nums[6] in ['1','2','3','4','5'] and nums[9] in [str(length),str(length-1),str(length-2) \
                                    ,str(length-3),str(length-4)]):
                                #self.tinyContigs[nums[0]].preCoincidence[id] = bps
                                self.contigPreBps[nums[0]][id] = bps
                                self.contigNextBps[id][nums[0]] = bps
                                appendPath = path.deepCopy()
                                lists.append(appendPath)
                                return
                            elif (nums[7] in [str(tinyLength),str(tinyLength-1),str(tinyLength-2) \
                                    ,str(tinyLength-3),str(tinyLength-4)] and
                                  nums[8] in [str(length),str(length-1),str(length-2) \
                                    ,str(length-3),str(length-4)] ):
                                #self.tinyContigs[nums[0]].nextCoincidence[id] = bps
                                self.contigNextBps[nums[0]][id] = bps
                                self.contigNextBps[id][nums[0]] = bps
                                appendPath = path.deepCopy()
                                lists.append(appendPath)

                                return
                isN=True
                for line in lines:#->->
                    nums=line.split('\t')
                    bps = int(nums[3])
                    coincidenceEquality=float(nums[2])
                    if nums[0] in self.tinyContigs \
                    and bps>=32\
                    and float(nums[2])>coincidenceThreshold and nums[0]!=id:
                        tinyLength=self.tinyContigs[nums[0]].length
                        if nums[6] in ['1','2','3','4','5'] and nums[9]in [str(length),str(length-1),str(length-2) \
                                ,str(length-3),str(length-4)] and path.isThreeRepeat(nums[0])==False:
                            isN=False
                            self.contigPreBps[nums[0]][id] = bps
                            self.contigNextBps[id][nums[0]]=bps
                            path.list.append(nums[0])
                            path.directions.append(1)
                            path.length+=tinyLength
                            path.score+=float(nums[2])
                            self.extendTail(nums[0], coincidenceThreshold,bigContig,lists,nLists,path,coincidenceThreshold_1,False)
                            path.list.pop()
                            path.directions.pop()
                            path.length -= tinyLength
                            path.score -= float(nums[2])
                        # -><-
                        if nums[7] in [str(tinyLength),str(tinyLength-1),str(tinyLength-2) \
                                ,str(tinyLength-3),str(tinyLength-4)] and \
                              nums[8] in [str(length),str(length-1),str(length-2) \
                                ,str(length-3),str(length-4)] and path.isThreeRepeat(nums[0])==False:
                            isN=False
                            self.contigNextBps[nums[0]][id] = bps
                            self.contigNextBps[id][nums[0]] = bps
                            #self.tinyContigs[nums[0]].nextCoincidence[id] = bps
                            path.list.append(nums[0])
                            path.directions.append(0)
                            path.length += tinyLength
                            path.score += float(nums[2])
                            self.extendHead(nums[0], coincidenceThreshold, bigContig, lists,nLists, path,coincidenceThreshold_1,False)

                            path.list.pop()
                            path.directions.pop()
                            path.length-=tinyLength
                            path.score -= float(nums[2])
                if isN==True:
                    appendPath = path.deepCopy()
                    nLists.append(appendPath)
    def extendHead(self,id,coincidenceThreshold,bigContig,lists,nLists,path,coincidenceThreshold_1,isLongContig):
        #print(path.list)
        contig=None
        isTiny=False
        if(isLongContig):
            contig = self.contigs[id]
        else:
            isTiny=True
            contig=self.tinyContigs[id]
        length = contig.length
        #maxId = '-1'
        #maxBps = 0
        #maxerCoincidence = 0
        #direction = 0  # 同向
        if os.path.exists(self.path + '/blast_connection/blast_all_info/all_' + id + '.txt'):
            with open(self.path+'/blast_connection/blast_all_info/all_'+id+'.txt', 'r') as file:
                lines = file.readlines()
                if(bigContig!=None):
                    if (bigContig.i == '52'):
                        for key in self.contigs.keys():
                            print(key)
                    for line in lines:
                        nums=line.split('\t')
                        bps = int(nums[3])
                        coincidenceEquality=float(nums[2])
                        if nums[0] == bigContig.i \
                        and bps>=32\
                        and coincidenceEquality>coincidenceThreshold_1 and nums[0]!=id:
                            tinyLength = self.contigs[nums[0]].length
                            if (nums[7] in [str(tinyLength),str(tinyLength-1),str(tinyLength-2) \
                                    ,str(tinyLength-3),str(tinyLength-4)] and nums[8] in ['1','2','3','4','5']) :
                                #self.tinyContigs[nums[0]].nextCoincidence[id] = bps
                                self.contigNextBps[nums[0]][id] = bps
                                self.contigPreBps[id][nums[0]] = bps
                                appendPath=path.deepCopy()
                                lists.append(appendPath)
                                return
                            elif (nums[6] in ['1','2','3','4','5'] and nums[9] in ['1','2','3','4','5']):
                                #self.tinyContigs[nums[0]].preCoincidence[id] = bps
                                self.contigPreBps[nums[0]][id] = bps
                                self.contigPreBps[id][nums[0]] = bps
                                appendPath = path.deepCopy()
                                lists.append(appendPath)
                                return
                isN=True
                for line in lines:
                    nums=line.split('\t')
                    bps = int(nums[3])
                    coincidenceEquality = float(nums[2])
                    if nums[0] in self.tinyContigs \
                    and bps >= 32 \
                    and float(nums[2])>coincidenceThreshold and nums[0]!=id:
                        tinyLength = self.tinyContigs[nums[0]].length
                        if nums[7] in [str(tinyLength),str(tinyLength-1),str(tinyLength-2) \
                                ,str(tinyLength-3),str(tinyLength-4)] and nums[8] in ['1','2','3','4','5'] and path.isThreeRepeat(nums[0])==False:
                            # if coincidenceEquality > maxerCoincidence or (
                            #         coincidenceEquality == maxerCoincidence and bps > maxBps):
                            # #if bps>maxBps or (bps==maxBps and float(nums[2])>maxerCoincidence):
                            #     maxBps=bps
                            #     maxId=nums[0]
                            #     maxerCoincidence=float(nums[2])
                            #     direction=0
                            isN = False
                            self.contigNextBps[nums[0]][id] = bps
                            self.contigPreBps[id][nums[0]] = bps
                            #self.tinyContigs[nums[0]].nextCoincidence[id] = bps
                            path.list.append(nums[0])
                            path.directions.append(0)
                            path.length += tinyLength
                            path.score += coincidenceEquality
                            self.extendHead(nums[0], coincidenceThreshold, bigContig, lists, nLists, path,coincidenceThreshold_1,False)
                            path.list.pop()
                            path.directions.pop()
                            path.length -= tinyLength
                            path.score -= coincidenceEquality
                        if nums[6] in ['1','2','3','4','5'] and nums[9] in ['1','2','3','4','5'] and path.isThreeRepeat(nums[0])==False:
                            # if coincidenceEquality > maxerCoincidence or (
                            #         coincidenceEquality == maxerCoincidence and bps > maxBps):
                            #
                            # #if bps>maxBps or (bps==maxBps and float(nums[2])>maxerCoincidence):
                            #     maxBps=bps
                            #     maxId=nums[0]
                            #     maxerCoincidence=float(nums[2])
                            #     direction=1
                            isN=False
                            self.contigPreBps[nums[0]][id] = bps
                            self.contigPreBps[id][nums[0]] = bps
                            #self.tinyContigs[nums[0]].preCoincidence[id] = bps
                            path.list.append(nums[0])
                            path.directions.append(1)
                            path.length += tinyLength
                            path.score += coincidenceEquality
                            self.extendTail(nums[0], coincidenceThreshold, bigContig, lists, nLists, path,coincidenceThreshold_1,False)
                            path.list.pop()
                            path.directions.pop()
                            path.length -= tinyLength
                            path.score -= coincidenceEquality
                if isN==True:
                    appendPath = path.deepCopy()
                    nLists.append(appendPath)
        # if maxId!='-1':
        #     if direction==0:
        #         if isTiny and self.tinyContigs[maxId].tinyNext==None:
        #             contig.tinyPre = self.tinyContigs[maxId]
        #             self.tinyContigs[maxId].tinyNext = contig
        #             self.tinyContigs[maxId].nextCoincidence[id]=maxBps
        #             if self.tinyContigs[maxId].tinyPre==None:
        #                 self.extendHead(maxId,coincidenceThreshold)
        #         elif isTiny==False:
        #             contig.tinyPre = self.tinyContigs[maxId]
        #             self.tinyContigs[maxId].tiny_bigNext.append(contig)
        #             self.tinyContigs[maxId].nextCoincidence[id] = maxBps
        #             if self.tinyContigs[maxId].tinyPre == None:
        #                 self.extendHead(maxId, coincidenceThreshold)
        #     elif direction==1:
        #         if isTiny and self.tinyContigs[maxId].tinyPre==None:
        #             contig.tinyPre = self.tinyContigs[maxId]
        #             self.tinyContigs[maxId].tinyPre = contig
        #             self.tinyContigs[maxId].preCoincidence[id] = maxBps
        #             if self.tinyContigs[maxId].tinyNext==None:
        #                 self.extendTail(maxId, coincidenceThreshold)
        #         elif isTiny == False:
        #             contig.tinyPre = self.tinyContigs[maxId]
        #             self.tinyContigs[maxId].tiny_bigPre.append(contig)
        #             self.tinyContigs[maxId].preCoincidence[id] = maxBps
        #             if self.tinyContigs[maxId].tinyNext == None:
        #                 self.extendTail(maxId, coincidenceThreshold)




class Path:
    def __init__(self):
        self.list=[] #tiny序列
        self.directions=[]# 0 next连接上一个 1 pre连接上一个
        self.length=0
        self.score=0



    def deepCopy(self):
        appendPath = Path()
        appendPath.list = [item for item in self.list]
        appendPath.directions = [item for item in self.directions]
        appendPath.length = self.length
        return appendPath
    def isThreeRepeat(self,str):#两段序列重复
        cnt=0
        if(len(self.list)>1):
            last=self.list[-1]
            for a in self.list:
                if a==last:
                    cnt+=1
            if cnt>=2:
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def getLongestPath(lists):
        maxLength=0
        res=None
        for path in lists:
            number=len(path.list)
            s=(path.score/number*path.length)/number
            if s>maxLength:
                maxLength=s
                res=path
        return res

    @staticmethod
    def getLongestPathMultiplePriorities(lists):
        maxLength = 0
        maxnumber = sys.maxsize
        maxscore=0
        res = None
        for path in lists:
            number = len(path.list)
            score=path.score/number
            isBetter=False
            if path.length > maxLength:
                isBetter=True
            elif path.length == maxLength:
                if(number<maxnumber):
                    isBetter=True
                elif number==maxnumber:
                    if(score>maxscore):
                        isBetter=True
            if isBetter==True:
                maxLength = path.length
                maxnumber = number
                maxscore = score
                res = path
        return res

class EndContig:
    def __init__(self, i):
        self.i = i
        self.series = ''
class Contig:



    def __init__(self, i, length):
        self.i=i
        self.length = length
        self.pre = None
        self.next = None
        self.direction = 0  # ->0 <-1
        self.series = ''
        self.tinyNext = None
        self.tinyPre = None
        self.tiny_bigNext = []
        self.tiny_bigPre = []
        self.nextCoincidence = {}
        self.preCoincidence = {}
        self.using=False
    def deepCopy(self):
        tinyContig=Contig(self.i,self.length)
        tinyContig.series=self.series
        tinyContig.tiny_bigPre=self.tiny_bigPre
        tinyContig.tiny_bigNext=self.tiny_bigNext
        tinyContig.nextCoincidence=self.nextCoincidence
        tinyContig.preCoincidence=self.preCoincidence
        return tinyContig
