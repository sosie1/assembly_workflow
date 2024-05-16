### 依赖
svg-> pdf : pip3 install svglib  
writeSvg : pip3 install svgwrite

pip3 install --user --upgrade cutadapt
todo： bin移动到目的bin路径

fastp(调用位置修改)
fastqc jdk
bwa 
samtools

plasfow安装
blast安装

### tips
图像长短
线粗细up 窄一些 
重合长度：32 比质量ok
100n补齐 fastA ok 
输出几个地方断开了 ok 大contig本身就有100n
fastA 要延伸后的 重叠要体现  没输出左边延伸的ok
39 10
10 39 冲突 选 39 10 ok 
10 5 0
10 3 0 冲突 选重合度大的 ok 二次扫描  加回来没有的
plasmids 过滤小？contig ok
判断小的接的是否为大contig 
组一个plasmids的 
小重复contig序列延伸循环最多2次//ban
小contig可以重复使用//不同的对象ok
多条序列（到下一个大contig）都要遍历 选一个最长的 ok

判断较长contig收否可以重复出现（覆盖度信息）（未给）
重叠两边都要记录吧

首尾延伸 xbp(5)误差 序列如何生成？ 不要断开的 2-9  去掉1 

248 276 多处 97比例才可以 
93 34  中间匹配给连上了
延伸时 41 42（2）53属于plasmids不用 但例子用了
plasmids
初始序列 用 不展示  ok 
延伸序列 不用 不展示
plasmids自动化读取问题


bugfix:
1.第一次延伸重复问题
2.孤立序列去除
3.部分样本不适配

Sample_JZ23090075-23HH460DEC-lib 大样本允许重复使用的话 就是两个环


plasmids 小样本延伸要用 ok
大样本 重复序列 延伸时候用 实现：归为小样本 ok

短长 短长 不冲突 优先级top 45样本eg ok

粗略图 单独一个长contig < 8000 ok
重复序列 < 10000 直接不考虑32这个样本









