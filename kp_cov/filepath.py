base="/home/test/Desktop/kp_cov/"    #Root directory
idapro_dir="/home/test/Desktop/IDA7.2/idat"#ida pro exe directory
basedir=base+"graph/"
total_num="num.txt"
headfile_path="pythonhead.txt"     #C head define
idafile_path="getblockscmd.py"     #Ida pro script
idafile1_path="bbl_preds.py"
basedir=base+"graph/"
predpath=basedir+"pred.txt"
numtxt=basedir+"num.txt"
file_path=base+"example/"          #Target .ko file directory
file_path_c=base+"kprobes/"
file_name="binfmt_misc_x64.ko"      #Target .ko file
file_result="blockresult.txt"      #Block information obtained by script analysis
func_address_path="address.txt"    #Run address in the kernel (by cmd)
sudo_password="123"                #root passwd
file_kprobes=file_name[0:file_name.find('.')]+'_kprobes.ko'
file_coverage_middle="cov_address.txt" #covearage intermediate file
file_coverage="coverage.txt"
basefunc="basefunc.txt"
file_makefile="Makefile"
