# Android-System-Service-Scanning-tool

## Description
This tool is for Dectecting NullPointerException(NPE) about Android System service

## Environment & Prerequisite
Linux  
  
adb  
python3.6+

## Usage
First, make sure connection with device
```
cnu@ubuntu:~$ adb devices
List of devices attached
18554286128979	device
```

then, excute script like the following command
```
./pseudo_fuzz.py -o OUTPUT_PATH
```

after a series of processes, crash dump is stored in the specified output directory


### Options
```
usage: pseudo_fuzz.py [-h] -o OUTPUT_PATH [-s SLEEP] [-root] [-null]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        set output file path
  -s SLEEP, --sleep_second SLEEP
                        set sleep second for checking crash
  -root, --root         for rooted deivice
  -null, --null         service call with null
```

