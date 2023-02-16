#include "net/if.h"
#include "arpa/inet.h"
#include "linux/sockios.h"
#include <linux/module.h>
#include <linux/fs.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <linux/ioctl.h>
#include <sys/ioctl.h>
#define MAX_SIZE 1024
 typedef struct my_command{
	char *buf;
	int len;
} my_command; 
int main(int argc, char *argv[])
{
    char* inf = "ens33";//通过这个接口名称来建立通信线路，可通过ifconfig查看
	int sock;
	struct ifreq ifr;
	int ret = 0;
	char buf[MAX_SIZE];		   // MAX_SIZE是自定义的传送指令buffer最大的大小
	struct my_command command; //自定义的结构体
	//创建socket柄
	sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (sock < 0)
	{
		printf("wrong sock!\n");
		return -1;
	}
	memset(&ifr, 0, sizeof(ifr)); //初始化req，准备发送
	strcpy(ifr.ifr_name, inf);	  //将网络接口名称填入req里

	//通信前先检查下接口的状态
	if (ioctl(sock, SIOCGIFFLAGS, &ifr) != 0)
	{
		printf("%s Could not read interface %s flags: %s", __func__, inf, strerror(errno));
		return -1;
	}

	if (!(ifr.ifr_flags & IFF_UP))
	{
		printf("%s is not up!\n", inf);
		return -1;
	}

	memset(&command, 0, sizeof(command)); //初始化
	memset(buf, 0, sizeof(buf));

	command.buf = buf;
	command.len = sizeof(buf);
	printf("buf:%s\n\n",buf);
	ifr.ifr_data = (void *)&command; //将待发送数据存入ifr中

	if ((ret = ioctl(sock, 35144, &ifr)) < 0)//SIOCGMIIREG
	{ //发给下层内核空间
		printf("%s: error ioctl[SIOCGMIIREG] ret= %d\n", __func__, ret);
		return ret;
	}

	memcpy(&command, ifr.ifr_data, sizeof(struct my_command));
	//通信返回的结果可以通过command.buf中传递回来。由驱动赋好值后，传到用户层来读取。
	printf("i'm back: a= 0x%x   b=%d\n", *(unsigned int *)command.buf, *(unsigned int *)&command.buf[4]);
	//例如，这里这句输出意味着，buf中[0]-[3]这四个byte（也就是一个int的大小），存着第一个数值，用八进制输出。
	// buf中[4]-[7]这四个byte，存第二个数，用十进制输出。
	
	

	return 0;
}

