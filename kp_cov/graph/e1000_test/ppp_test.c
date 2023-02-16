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
#include"ppp_ioctl.h"
#define MAX_SIZE 1024

int main()
{
     
 int fd;
    int ret;
   fd = open("/dev/ppp", O_RDWR);
   printf("fd=%d\n",fd);
    if (fd < 0) {
        printf("Couldn't reopen /dev/ppp");        
    }
    
   struct {
      unsigned int a1;
      int a2;
      } A;
     A.a1 = 2;
     A.a2 = 3;
 
    ret=ioctl(fd,PPPIOCSCOMPRESS,&A);
    printf("ret=%d\n",ret);
    printf("PPPIOCGFLAGS=%ld\n",PPPIOCSCOMPRESS);


     return 0;
}

