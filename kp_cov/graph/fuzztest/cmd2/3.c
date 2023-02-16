#include<linux/types.h>
#include <stdlib.h>
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
fd=open("/dev/i2c-0", O_RDWR);
if (fd < 0) {
printf("Couldn't reopen /dev/i2c-0");
}
struct data0{
unsigned short int a0;
unsigned short int a1;
unsigned short int a2;
unsigned char* a3;
};
typedef struct {
struct data0* a0;
unsigned int a1;
} data;
data A;
A.a0=(struct data0 *)malloc(sizeof(A.a0));
(A.a0[0]).a0=36703;
(A.a0[0]).a1=0;
(A.a0[0]).a2=63207;
(A.a0[0]).a3=NULL;
A.a1=29799865;

int ret;
ret=ioctl(fd,1799,&A);
printf("ret=%d\n",ret);
return 0;
}