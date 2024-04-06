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
    parser.add_argument('--coincidenceThreshold', type=float, default=97, help='序列有效重合比例阈值')
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
        a.readDirection()
        a.readGenome()
        a.extendSeries(args.coincidenceThreshold)
        b = GraphicalProcess.GraphicalProcessUtil(a)
        b.showCommandLineGraphics(a.contigs)
        b.showCommandLineGraphics_Extend(a.contigs, args.outputSpace)
        b.generateSvg(a.contigs, args.outputSpace)
        print('段数:' + str(a.writeFastA(args.outputSpace)))
        print('延伸后断裂位点总数量:', str(a.encodeFastA(args.outputSpace)))
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
                a.readDirection()
                a.readGenome()
                a.extendSeries(args.coincidenceThreshold)
                b = GraphicalProcess.GraphicalProcessUtil(a)
                b.showCommandLineGraphics(a.contigs)
                b.showCommandLineGraphics_Extend(a.contigs, space)
                b.generateSvg(a.contigs, space)
                print('段数:' + str(a.writeFastA(space)))
                print('延伸后断裂位点总数量:', str(a.encodeFastA(space)))
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
