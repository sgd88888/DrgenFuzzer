#include<linux/types.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <linux/ioctl.h>
#include <sys/ioctl.h>
#include<fcntl.h>
#include<unistd.h>
int main(int argc, char *argv[]){
int fd;
fd=open("/dev/snd/controlC0", O_RDWR);
if (fd < 0) {
printf("Couldn't reopen /dev/snd/controlC0");
}
typedef struct {
int a1;
int a2;
int a3;
unsigned char a4[16];
unsigned char a5[16];
unsigned char a6[32];
unsigned char a7[32];
unsigned char a8[16];
unsigned char a9[80];
unsigned char a10[128];
} data;
data s1={-749881202,439634588,950679736,"qx","","iTwGRSBhqmUpKl","jy","SMyFoAV","lqwuTzuMKN","GhReRJbL"};
int ret;
ret=ioctl(fd,2172146945,&s1);
printf("ret=%d\n",ret);
return 0;
}