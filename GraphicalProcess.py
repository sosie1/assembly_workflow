import svgwrite
from DataProcess import DataProcessUtil
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM
class GraphicalProcessUtil:
    dataProcessUtil=None
    def __init__(self,dataProcessUtil):
        self.dataProcessUtil=dataProcessUtil
    def doubleWrite(self,file,s,end):
        print(s,end=end)
        file.write(s+end)
    def isContigConnected(self,contig,contig1):
        if(contig1==None):
            return False
        elif((contig1.next!=None and contig1.next==contig )or ( contig1.pre!=None and contig1.pre==contig)):
            return True
        else:
            return False
    def showCommandLineGraphics(self,contigs):
        print('初始序列')
        #print("next"+contigs['31'].next.i)
        #print("pre" + contigs['31'].pre.i)

        # while (hasNonUsing == True):
        #     hasNonUsing=False
        #     for c in contigs:
        #         if contigs[c].using == False:
        #             hasNonUsing=True
        #             break
        #     if hasNonUsing==True:
        for c in contigs:
            #if contigs[c].using == False and ((contigs[c].pre==None and contigs[c].next!=None) or(contigs[c].pre!=None and contigs[c].next==None)):
            if contigs[c].using == False and (
                    (self.isContigConnected(contigs[c], contigs[
                c].pre) and self.isContigConnected(contigs[c], contigs[c].next) == False)
                                                   or (self.isContigConnected(contigs[c], contigs[
                        c].pre) == False and self.isContigConnected(contigs[c], contigs[c].next))
            ):
                contigHead = contigs[c]
                contigX=None
                if self.isContigConnected(contigs[c], contigs[c].next):

                    print('--' + contigHead.i + '-->', end='|')
                    contigX = contigHead.next
                if self.isContigConnected(contigs[c], contigs[
                c].pre):
                    print('<--' + contigHead.i + '--', end='|')
                    contigX = contigHead.pre


# contigHead = contigs['28']
# print('--' + contigHead.i + '-->', end='|')
# contigX = contigHead.next
                contigHead.using=True
                contigPre = contigHead
                while contigX != contigHead:
                    if contigX.pre!=None and contigX.pre == contigPre:

                        print('--' + contigX.i + '-->', end='|')
                        contigX.using = True
                        contigPre = contigX
                        if contigX.next==None:
                            print('|')
                            break
                        contigX = contigX.next
                    elif contigX.next!=None and contigX.next==contigPre:

                        print('<--' + contigX.i + '--', end='|')
                        contigX.using = True
                        contigPre = contigX
                        if contigX.pre==None:
                            print('|')
                            break
                        contigX = contigX.pre
                    # elif contigX.pre==None and contigX.next==contigPre:
                    #     print('<--' + contigX.i + '--', end='||')
                    #     contigX.using = True
                    #     break
                    # elif contigX.pre==None and contigX.next!=contigPre:
                    #     print("|")
                    #     break
                    else:
                        print('|')
                        break
                if(contigX == contigHead):
                    print('*')
                print('\n')
        for c in contigs:
            if contigs[c].using == False:#存在环
                contigHead = contigs[c]
                if(contigHead.next==None):
                    print('--' + contigHead.i + '-->', end='||')
                    print('\n')
                    contigHead.using = True
                    continue
                print('--' + contigHead.i + '-->', end='|')
                contigX = contigHead.next
                contigHead.using = True
                contigPre = contigHead
                while contigX != contigHead:
                    if contigX.pre != None and contigX.pre == contigPre:
                        print('--' + contigX.i + '-->', end='|')
                        contigX.using = True
                        contigPre = contigX
                        if contigX.next == None:
                            print('|')
                            break
                        contigX = contigX.next
                    elif contigX.next != None and contigX.next == contigPre:
                        print('<--' + contigX.i + '--', end='|')
                        contigX.using = True
                        contigPre = contigX
                        if contigX.pre == None:
                            print('|')
                            break
                        contigX = contigX.pre
                    # elif contigX.pre == None and contigX.next == contigPre:
                    #     print('<--' + contigX.i + '--', end='||')
                    #     contigX.using = True
                    #     break
                    # elif contigX.pre == None and contigX.next != contigPre:
                    #     print("|")
                    #     break
                    else:
                        print('|')
                        break
                if (contigX == contigHead):
                    print('*')
                print('\n')

    def showCommandLineGraphics_Extend(self,contigs,outputSpace):

        nCnt=0
        #print(contigs['1'].tinyNext.i)
        print('延伸后序列')
        isConnected=True
        with open(outputSpace + "/seriesExtended.txt", "w") as file:
            for headId in self.dataProcessUtil.headContigs:

                contigHead = contigs[headId]
                contigX = None
                if self.dataProcessUtil.headContigs[headId] == 0:
                    file.write('--' + contigHead.i + '-->'+'|')
                    print('--' + contigHead.i + '-->', end='|')
                    contigX = contigHead.next
                    isConnected = self.showTinySeriesCommand(contigHead, contigX, 0,file)

                if self.dataProcessUtil.headContigs[headId] == 1:
                    file.write('<--' + contigHead.i + '--'+'|')
                    print('<--' + contigHead.i + '--', end='|')
                    contigX = contigHead.pre
                    isConnected = self.showTinySeriesCommand(contigHead, contigX, 1,file)

                contigPre = contigHead
                while contigX != contigHead and contigX!=None:
                    #print(contigX.i)
                    if contigX.pre != None and contigX.pre == contigPre:
                        if (isConnected == False):
                            file.write('N')
                            print('N', end='')
                            nCnt += 1
                            self.showleftTinySeriesCommand(contigX, 0,file)
                        file.write('--' + contigX.i + '-->'+'|')
                        print('--' + contigX.i + '-->', end='|')
                        contigPre = contigX
                        if contigX.next == None:
                            isConnected = self.showTinySeriesCommand(contigPre, None, 0,file)
                            file.write('|')
                            print('|',end='')
                            break
                        contigX = contigX.next
                        isConnected = self.showTinySeriesCommand(contigPre, contigX, 0,file)
                    elif contigX.pre != None and contigX.next == contigPre:
                        if (isConnected == False):
                            file.write('N')
                            print('N', end='')
                            nCnt += 1
                            self.showleftTinySeriesCommand(contigX, 1,file)
                        file.write('<--' + contigX.i + '--'+'|')
                        print('<--' + contigX.i + '--', end='|')
                        contigPre = contigX
                        contigX = contigX.pre
                        isConnected = self.showTinySeriesCommand(contigPre, contigX, 1,file)
                    elif contigX.pre == None and contigX.next == contigPre:
                        if (isConnected == False):
                            file.write('N')
                            print('N', end='')
                            nCnt += 1
                            self.showleftTinySeriesCommand(contigX, 1,file)
                        file.write('<--' + contigX.i + '--'+'|')
                        print('<--' + contigX.i + '--', end='|')
                        isConnected = self.showTinySeriesCommand(contigX, None, 1,file)
                        file.write('|')
                        print('|',end='')
                        break
                    #elif contigX.pre == None and contigX.next != contigPre:

                    else:
                        file.write('|')
                        print("|", end='')
                        break

                if (isConnected == False):
                    file.write('N')
                    print('N', end='')
                    nCnt += 1
                    if(contigX!=None):
                        self.showleftTinySeriesCommand(contigX, 0,file)
                file.write('\n')
                self.doubleWrite(file,'\n','')

            # contigHead = contigs['28']
            # print('--' + contigHead.i + '-->', end='|')
            # contigX = contigHead.next
            # isConnected=self.showTinySeriesCommand(contigHead,contigX,0)
            # contigPre = contigHead
            # while contigX != contigHead:
            #     if contigX.pre != None and contigX.pre == contigPre:
            #         if (isConnected == False):
            #             print('N',end='')
            #             nCnt+=1
            #             self.showleftTinySeriesCommand(contigX, 0)
            #         print('--' + contigX.i + '-->', end='|')
            #         contigPre = contigX
            #         if contigX.next == None:
            #             isConnected=self.showTinySeriesCommand(contigPre, None,0)
            #             print('|')
            #             break
            #         contigX = contigX.next
            #         isConnected=self.showTinySeriesCommand(contigPre, contigX,0)
            #     elif contigX.pre != None and contigX.next == contigPre:
            #         if (isConnected == False):
            #             print('N',end='')
            #             nCnt += 1
            #             self.showleftTinySeriesCommand(contigX, 1)
            #         print('<--' + contigX.i + '--', end='|')
            #         contigPre = contigX
            #         contigX = contigX.pre
            #         isConnected=self.showTinySeriesCommand(contigPre, contigX, 1)
            #     elif contigX.pre == None and contigX.next == contigPre:
            #         if (isConnected == False):
            #             print('N',end='')
            #             nCnt += 1
            #             self.showleftTinySeriesCommand(contigX, 1)
            #         print('<--' + contigX.i + '--', end='|')
            #         isConnected=self.showTinySeriesCommand(contigX, None,1)
            #         print('|')
            #         break
            #     elif contigX.pre == None and contigX.next != contigPre:
            #         print("|")
            #         break
            # if (isConnected == False):
            #         print('N', end='')
            #         nCnt += 1
            #         self.showleftTinySeriesCommand(contigX, 0)
            #
            # print('\n')
            #print('n个数' + str(nCnt))

    def showleftTinySeriesCommand(self,contigRight,rightContigDirection,file):
        temp=''
        if rightContigDirection == 0:
            contigX = contigRight.tinyPre
        else:
            contigX = contigRight.tinyNext
        contigPre = contigRight
        hasTiny=False
        while contigX != None:
            hasTiny=True
            if contigPre in contigX.tiny_bigPre or contigX.tinyPre == contigPre:
                temp='<-' + contigX.i + '-'+temp
                contigPre = contigX
                contigX = contigX.tinyNext
            elif contigPre in contigX.tiny_bigNext or contigX.tinyNext == contigPre:
                temp = '-' + contigX.i + '->'+temp
                contigPre = contigX
                contigX = contigX.tinyPre
        print(temp,end='')
        self.doubleWrite(file,temp,'')
        if hasTiny:
            print('|',end='')
            self.doubleWrite(file,'|','')


    def showTinySeriesCommand(self,contigHead,contigNext,direction,file):
        if direction==0:
            contigX = contigHead.tinyNext
        else :
            contigX=contigHead.tinyPre
        contigPre = contigHead
        hasTiny=False
        while contigX!=None :
            hasTiny=True
            if contigPre in contigX.tiny_bigPre or  contigX.tinyPre == contigPre:
                self.doubleWrite(file,'-' + contigX.i + '->', end='')

                contigPre = contigX
                contigX = contigX.tinyNext
            elif contigPre in contigX.tiny_bigNext or contigX.tinyNext == contigPre:
                self.doubleWrite(file,'<-' + contigX.i + '-', end='')
                contigPre = contigX
                contigX = contigX.tinyPre
        if hasTiny:
            self.doubleWrite(file,'|',end='')
        isConnected = False
        if (contigNext in contigPre.tiny_bigNext or contigNext in contigPre.tiny_bigPre ):
            isConnected = True
        return isConnected
    def generateArrowLength(self,length):
        wholeRate=self.dataProcessUtil.maxContigLength-self.dataProcessUtil.minContigLength
        leftRate=length-self.dataProcessUtil.minContigLength
        return 50+leftRate/wholeRate*90
    def generateSvg(self,contigs,outputSpace):
        dwg = svgwrite.Drawing(outputSpace+'/test1.svg', profile='tiny')
        currentY = 50
        for headId in self.dataProcessUtil.headContigs:
            currentX = 10
            contigHead = contigs[headId]
            contigX = None
            arrowLength = self.generateArrowLength(contigHead.length)
            if self.dataProcessUtil.headContigs[headId] == 0:


                self.drawRightArrow(dwg, currentX, currentY, int(headId), arrowLength)
                contigX = contigHead.next
            if self.dataProcessUtil.headContigs[headId] == 1:

                self.drawleftArrow(dwg, currentX, currentY, int(headId), arrowLength)

                contigX = contigHead.pre
            currentX = currentX + arrowLength + 10
            self.drawTriangle(dwg, currentX, currentY)
            currentX = currentX + 30
            contigPre = contigHead
            cnt = 1
            while contigX != contigHead and contigX!=None:
                if cnt % 9 == 0:
                    currentY = currentY + 50
                    currentX = 10
                if contigX.pre != None and contigX.pre == contigPre:
                    arrowLength = self.generateArrowLength(contigX.length)
                    self.drawRightArrow(dwg, currentX, currentY, int(contigX.i), arrowLength)
                    currentX = currentX + arrowLength + 10
                    self.drawTriangle(dwg, currentX, currentY)
                    currentX = currentX + 30
                    contigPre = contigX
                    if contigX.next == None:
                        break
                    contigX = contigX.next
                elif contigX.pre != None and contigX.next == contigPre:
                    arrowLength = self.generateArrowLength(contigX.length)
                    self.drawleftArrow(dwg, currentX, currentY, int(contigX.i), arrowLength)
                    currentX = currentX + arrowLength + 10
                    self.drawTriangle(dwg, currentX, currentY)
                    currentX = currentX + 30
                    contigPre = contigX
                    contigX = contigX.pre
                elif contigX.pre == None and contigX.next == contigPre:
                    arrowLength = self.generateArrowLength(contigX.length)
                    self.drawleftArrow(dwg, currentX, currentY, int(contigX.i), arrowLength)
                    currentX = currentX + arrowLength + 10
                    self.drawTriangle(dwg, currentX, currentY)
                    break
                #elif contigX.pre == None and contigX.next != contigPre:
                else:
                    break
                cnt = cnt + 1
            currentY+=100
        #dwg = svgwrite.Drawing('ca_green.svg', profile='tiny')
        #dwg.add(dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=None, ry=None, fill='green')))

        #currentX=10
        #contigHead = contigs['1']
        #arrowLength=self.generateArrowLength(contigHead.length)
        #print('--' + contigHead.i + '-->', end='|')
        #self.drawRightArrow(dwg, currentX, currentY, 1,arrowLength)
        # currentX=currentX+arrowLength+10
        # self.drawTriangle(dwg, currentX ,currentY)
        # currentX=currentX+30
        # contigX = contigHead.next
        # contigPre = contigHead
        # cnt=1
        # while contigX != contigHead:
        #     if cnt%9==0:
        #         currentY=currentY+50
        #         currentX=10
        #     if contigX.pre!=None and contigX.pre == contigPre:
        #         arrowLength = self.generateArrowLength(contigX.length)
        #         self.drawRightArrow(dwg, currentX, currentY, int(contigX.i),arrowLength)
        #         currentX = currentX +arrowLength+10
        #         self.drawTriangle(dwg, currentX, currentY)
        #         currentX = currentX + 30
        #         contigPre = contigX
        #         if contigX.next==None:
        #             break
        #         contigX = contigX.next
        #     elif contigX.pre!=None and contigX.next==contigPre:
        #         arrowLength = self.generateArrowLength(contigX.length)
        #         self.drawleftArrow(dwg, currentX, currentY, int(contigX.i),arrowLength)
        #         currentX = currentX +arrowLength+10
        #         self.drawTriangle(dwg, currentX, currentY)
        #         currentX = currentX + 30
        #         contigPre = contigX
        #         contigX = contigX.pre
        #     elif contigX.pre==None and contigX.next==contigPre:
        #         arrowLength = self.generateArrowLength(contigX.length)
        #         self.drawleftArrow(dwg, currentX, currentY, int(contigX.i),arrowLength)
        #         currentX = currentX +arrowLength+10
        #         self.drawTriangle(dwg, currentX, currentY)
        #         break
        #     elif contigX.pre==None and contigX.next!=contigPre:
        #         break
        #     cnt=cnt+1

        dwg.save()
        print('已生成图像：'+outputSpace+'/test1.svg')
        #self.convertSvgToPng('/Users/yangweiyi/Desktop/ca_green.svg')
    # def convertSvgToPng(self,svg_file):
    #     svg=svg2rlg(svg_file)
    #     renderPDF.drawToFile(svg, "file.pdf")
    #     #renderPM.drawToFile(svg, "file.png", fmt="PNG")

    def drawRightArrow(self,dwg,startX,startY,id,arrowLength):
        dwg.add(dwg.line((startX, startY), (startX+arrowLength, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.line((startX+arrowLength-10, startY-10), (startX+arrowLength, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.line((startX+arrowLength-10, startY+10), (startX+arrowLength, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.text(id, insert=(startX+arrowLength/3, startY-10)))
    def drawTriangle(self,dwg,startX,startY):
        dwg.add(dwg.line((startX, startY), (startX+10, startY-10), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=2))
        dwg.add(dwg.line((startX, startY), (startX+20, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=2))
        dwg.add(dwg.line((startX+10, startY-10), (startX+20, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=2))
    def drawleftArrow(self,dwg,startX,startY,id,arrowLength):
        dwg.add(dwg.line((startX, startY), (startX+10, startY-10), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.line((startX, startY), (startX+10, startY+10), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.line((startX, startY), (startX+arrowLength, startY), stroke=svgwrite.rgb(10, 10, 16, '%'),stroke_width=3))
        dwg.add(dwg.text(id, insert=(startX+arrowLength/3, startY-10)))