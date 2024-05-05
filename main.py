# This is a sample Python script.
from DataProcess import DataProcessUtil
import GraphicalProcess
import argparse
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

    # def __init__(self):
    #     #super().__init__(6)  # 显式调用父类的构造函数
    #     print("Child class constructor called")
    #     print(super().a)
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
def processArgs():
    parser = argparse.ArgumentParser(description='SeriesAnalysis_1.0')
    parser.add_argument('--coincidenceThreshold', type=float, default=99, help='序列有效重合比例阈值')
    parser.add_argument('--lengthThreshold', type=int,  default=5000,help='序列长度阈值')
    parser.add_argument('--workingSpace',type=str,default='/Users/yangweiyi/Desktop/输入文件',help='工作路径')
    parser.add_argument('--outputSpace',type=str,default='.',help='输出路径')
    parser.add_argument('--batch',type=bool,default=False)
    # parser.add_argument('--output', type=str, default='output.txt', help='输出文件路径（默认：output.txt）')
    # parser.add_argument('--flag', action='store_true', help='一个布尔标志')

    args = parser.parse_args()
    if(args.batch==False):
        a = DataProcessUtil(args.workingSpace)
        a.readPlasmids()
        a.readDepthTable(args.lengthThreshold)
        a.readDirection(False)
        a.readGenome()
        a.extendSeries(args.coincidenceThreshold)
        b = GraphicalProcess.GraphicalProcessUtil(a)
        b.showCommandLineGraphics(a.contigs)
        b.showCommandLineGraphics_Extend(a.contigs, args.outputSpace)
        b.generateSvg(a.contigs, args.outputSpace)
        a.writeFastA(args.outputSpace,True)
        print('段数:' + str(a.writeFastA(args.outputSpace,False)))
        print('延伸后断裂位点总数量:', str(a.encodeFastA(args.outputSpace)))

        folder = os.path.exists(args.outputSpace + '/plasmid')
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(args.outputSpace + '/plasmid')  # makedirs 创建文件时如果路径不存在会创建这个路径

        a1 = DataProcessUtil(args.workingSpace)
        a1.readPlasmids()
        a1.readDepthTable_Plasmid(args.lengthThreshold)
        a1.readDirection(True)
        a1.readGenome()
        a1.extendSeries(args.coincidenceThreshold)
        b1 = GraphicalProcess.GraphicalProcessUtil(a1)
        b1.showCommandLineGraphics(a1.contigs)
        b1.showCommandLineGraphics_Extend(a1.contigs, args.outputSpace  + '/plasmid')
        b1.generateSvg(a1.contigs, args.outputSpace  + '/plasmid')
        a1.writeFastA(args.outputSpace  + '/plasmid', True)
        print('plasmid:段数:' + str(a1.writeFastA(args.outputSpace  + '/plasmid', False)))
        print('plasmid:延伸后断裂位点总数量:', str(a1.encodeFastA(args.outputSpace  + '/plasmid')))


    else:
        for root, dirs, files in os.walk(args.workingSpace):
            # for name in files:
            #     print(os.path.join(root, name))
            for name in dirs:
                space=os.path.join(root, name)
                print(space)
                a = DataProcessUtil(space)
                a.readPlasmids()
                a.readDepthTable(args.lengthThreshold)
                a.readDirection(False)
                a.readGenome()
                a.extendSeries(args.coincidenceThreshold)
                b = GraphicalProcess.GraphicalProcessUtil(a)
                b.showCommandLineGraphics(a.contigs)
                b.showCommandLineGraphics_Extend(a.contigs, space)
                b.generateSvg(a.contigs, space)
                a.writeFastA(space, True)
                print('段数:' + str(a.writeFastA(space, False)))
                print('延伸后断裂位点总数量:', str(a.encodeFastA(space)))

                folder = os.path.exists(space + '/plasmid')

                if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(space + '/plasmid')  # makedirs 创建文件时如果路径不存在会创建这个路径

                a1 = DataProcessUtil(space)
                a1.readPlasmids()
                a1.readDepthTable_Plasmid(args.lengthThreshold)
                a1.readDirection(True)
                a1.readGenome()
                a1.extendSeries(args.coincidenceThreshold)
                b1 = GraphicalProcess.GraphicalProcessUtil(a1)
                b1.showCommandLineGraphics(a1.contigs)
                b1.showCommandLineGraphics_Extend(a1.contigs, space + '/plasmid')
                b1.generateSvg(a1.contigs, space + '/plasmid')
                a1.writeFastA(space + '/plasmid', True)
                print('plasmid:段数:' + str(a1.writeFastA(space + '/plasmid', False)))
                print('plasmid:延伸后断裂位点总数量:', str(a1.encodeFastA(space + '/plasmid')))
            break




                # if args.flag:
    #     print('Flag 已设置')
    # else:
    #     print('Flag 未设置')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    processArgs()





    # 创建ChildClass的实例





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
