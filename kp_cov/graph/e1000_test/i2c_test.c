/*
//作者:王磊
//日期:2013.11.17
//文件功能:实现ioctl函数调用，并操作i2c设备/dev/i2c/0进行读写数据
//可以用i2c -r来检验数据是否已写入
*/
#include<stdio.h>
#include<linux/types.h>
#include<fcntl.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/ioctl.h>
#include<errno.h>
#include<assert.h>
#include<string.h>
#include<linux/i2c.h>
#include<linux/i2c-dev.h>
 
int main(int argc, char** argv)
{
	struct i2c_rdwr_ioctl_data work_queue;
 
	unsigned int slave_address,reg_address,dat;
	unsigned int fd;
	int ret;
	char select;
 
	fd=open("/dev/i2c/0",O_RDWR);
	if(!fd)
	{
		printf("error on opening the device file\n");
		exit(1);
	}
	ioctl(fd,I2C_TIMEOUT,2);//超时时间
	ioctl(fd,I2C_RETRIES,1);//重复次数
	
	//nmsgs决定了有多少start信号,一个msgs对应一个start信号,但这个start信号又不能适用于repeat start
	//在nmsg个信号结束后总线会产生一个stop
	work_queue.nmsgs = 1;
	work_queue.msgs = (struct i2c_msg *)malloc(work_queue.nmsgs * sizeof(work_queue.msgs));
	if(!work_queue.msgs)
	{
		printf("memory alloc failed");
		close(fd);
		exit(1);
	}
 
	slave_address = 0x50;//24c08的访问地址是101000b
	printf("please select:w or r?\n");
	scanf("%c", &select);
	if('w' == select)
	{
		printf("please input:address,dat?(example:0x00,0x00)\n");
		scanf("%x,%x", &reg_address, &dat);
		//往i2c里面写数据
		printf("began to write\n");
		work_queue.nmsgs  = 1;	
		(work_queue.msgs[0]).len = 2;//buf的长度
		(work_queue.msgs[0]).flags = 0;//write
		(work_queue.msgs[0]).addr = slave_address;//设备地址
		(work_queue.msgs[0]).buf = (unsigned char *)malloc(2);
		(work_queue.msgs[0]).buf[0] = reg_address;//写的地址
		(work_queue.msgs[0]).buf[1] = dat;//你要写的数据
 
		ret = ioctl(fd, I2C_RDWR, (unsigned long)&work_queue);
		if(ret < 0)
			printf("error during I2C_RDWR ioctl with error code %d\n", ret);
	}
	else if('r' == select)
	{
		printf("please input:address?(example:0x00)\n");
		scanf("%x", &reg_address);
		//从i2c里面读出数据
		printf("began to read:");
		work_queue.nmsgs  = 1;
		//先设定一下地址	
		(work_queue.msgs[0]).flags = 0;//write
		(work_queue.msgs[0]).addr = slave_address;
		(work_queue.msgs[0]).len = 1;
		(work_queue.msgs[0]).buf = (unsigned char *)malloc(1);
		(work_queue.msgs[0]).buf[0] = reg_address;//因为上面buf已经分配过了
		ret = ioctl(fd, I2C_RDWR, (unsigned long)&work_queue);
		if(ret < 0)
			printf("error during I2C_RDWR ioctl with error code %d\n", ret);
 
	//因为i2c-dev不支持repeat start，所以只能将读数据操作中的写地址和读数据分为两次消息。	
		//然后从刚才设定的地址处读
		work_queue.nmsgs  = 1;
		(work_queue.msgs[0]).flags = I2C_M_RD;
		(work_queue.msgs[0]).addr = slave_address;
		(work_queue.msgs[0]).len = 1;
		(work_queue.msgs[0]).buf[0] = 0;//初始化读缓冲
		ret = ioctl(fd, I2C_RDWR, (unsigned long)&work_queue);
		if(ret < 0)
			printf("error during I2C_RDWR ioctl with error code %d\n", ret);
		printf("reg_address=0x%2x,dat=0x%2x\n", reg_address, work_queue.msgs[0].buf[0]);
	}
	close(fd);
	free((work_queue.msgs[0]).buf);
	free(work_queue.msgs);
	return 0; 
	
}