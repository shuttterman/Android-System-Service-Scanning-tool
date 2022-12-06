# Android-System-Service-Scanning-tool

## Description
This tool is for Dectecting NullPointerException(NPE) about Android System service

## Environment & Prerequisite
Linux  
  
adb  
python3.6+

## Usage
```
cnu@ubuntu:~/project$ ./tmp.py -h
usage: tmp.py [-h] -o OUTPUT_PATH [-s SLEEP] [-root]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Set output file path
  -s SLEEP, --sleep_second SLEEP
                        Set sleep second for checking crash
  -root, --root         For rooted deivice

```
First, make sure connection with device
```
cnu@ubuntu:~$ adb devices
List of devices attached
18554286128979	device
```

then, 
