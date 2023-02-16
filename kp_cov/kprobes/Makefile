ifneq ($(KERNELRELEASE),)
obj-m :=e1000_x64_kprobes.o
else
KDIR :=/lib/modules/$(shell uname -r)/build
all:
	make -C $(KDIR) M=$(PWD) modules
clean:
	rm -f *.ko *.o *.mod.o *.mod *.mod.c *.symvers *.order *.cmd *.mk
endif
