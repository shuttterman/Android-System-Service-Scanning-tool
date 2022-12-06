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
./pseudo_fuzz.py [-h] -o OUTPUT_PATH [-s SLEEP] [-root]
```

