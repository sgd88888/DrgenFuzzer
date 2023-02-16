基于适应度和输入约束模型的内核驱动漏洞挖掘
# DrgenFuzzer

#
将待测ko（XXX.ko）放入example文件夹，并重命名为XXX_x64.ko
filepath.py处修改file_name
kprobes/Makefile处修改obj-m


python kprobescombination.py 插装
python coverage.py 统计覆盖率


ida pro ->blockresult.txt    num.txt
kernel memory func address-> address.txt
dmesg ->  num.txt

python kprobescombination.py
报错：有可能是没安装测试目标驱动target。也有可能是检测模块Makefile文件生成有问题。再之后就是路径问题。
测试程序还没写
