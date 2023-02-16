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
int a=-718091765;
int ret;
ret=ioctl(fd,2147767552,a);
printf("ret=%d\n",ret);
return 0;
}