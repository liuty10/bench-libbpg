# bench-libbpg

This repo is for benchmarking bpg

# How to install
- download, configure, make and make install PNG 1.6
```
wget -O libpng-1.6.37.tar.gz
tar xf libpng-1.6.37.tar.gz
./configure --help
./configure
make -j
sudo make install
```
- uninstall libnuma-dev.
- conda has problem with bpg compile. Please "conda uninstall libtiff".
- then, compile the libbpg-0.9.8
```
wget http://bellard.org/bpg/libbpg-0.9.8.tar.gz
tar xzf libbpg-0.9.5.tar.gz
cd libbpg-0.9.5/
```
Modify Makefile:
```
"CFLAGS+=-I/usr/local/include"      after the line "CFLAGS+=-I"
"LDFLAGS+=-L /usr/local/lib"        before the line "CFLAGS+=-g"
```
Then, compile
```
make -j 6 sudo make install sudo checkinstall sudo ldconfig /usr/local/lib
```
see: https://github.com/liuty10/Things-IamLearning/issues/68

# How to use
```
./libbpg-0.9.8/bpgenc -f 444 -q ${qp_value} ${inpng}
./libbpg-0.9.8/bpgdec out.bpg
```
For more help:
```
./libbpg-0.9.8/bpgenc -h 
```
