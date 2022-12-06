#!/usr/bin/env python3
import os, re, sys
import argparse
from time import sleep

OUTPUT_PATH = ''
SU = ''
NULL = ''

class Current:
	def __init__(self):
		self.status = 0
		self.total = 0
		self.service = ''
		self.code = 0
		self.number = 0
		self.service_list = []

	def set_total(self, total):
		self.total = total

	def set_status(self, status):
		self.status = status

	def set_current(self, service, code):
		self.service = service
		self.code = code

	def inc_number(self):
		self.number += 1

	def append_service(self, service):
		self.service_list.append(service)

	def print_current(self):
		os.system("clear")
		if self.status == 0:
			print(f"[*] Check Transaction ID max value for {self.service}")
		elif self.status == 1:
			print("[*] Check vulnerable service")
			print(f"[i]crash in {self.service_list}")
		else:
			print("[*] Check NullPointerException")
			print(f"[i] Progress: {self.number}/{self.total}")

def service_call(service, code):
	is_rebooted = False
	os.system("clear")
	current.print_current()
	print(f"[+] service call {service} {code}{NULL}")
	res = os.popen(f'adb shell "{SU}service call {service} {code}{NULL}" 2>&1').read()
	if ("does not exist" in res) or ("no devices/emulators found" in res):
		is_rebooted = True
		wait_reboot(service, code)
	print("------------------------------------------------------------------\n")
	print(res)
	print("------------------------------------------------------------------\n")
	
	return (res, is_rebooted)

def wait_reboot(service, code):
	while True:
		sleep(2)
		print("waiting...")
		res = os.popen(f'adb shell "{SU}service call {service} {code+1}{NULL}" 2>&1').read()
		if ("does not exist" not in res) and ("no devices/emulators found" not in res):
			break
			
def get_service_list():
	global current
	service_list = []
	code_list = [x for x in range(10, 10000, 20)]
	p = re.compile(r"(\d+\t)(.+)\[(.+)\]")

	os.system(f'adb shell "{SU}service list" > service_list')

	with open("service_list", 'r') as f:
		f.readline()
		lines = f.readlines()
		for line in lines:
			line = line.replace(": ", "")
			m = p.match(line) 
			if m:
				service_list.append(m.group(2))

	tmp_list = []
	for service in service_list:
		for code in code_list:
			current.set_current(service, code)
			res = service_call(service, code)[0]
			if "Not a data message" in res:
				max_code = code
				break
		
		for code in range(max_code, 0, -1):
			current.set_current(service, code)
			res = service_call(service, code)[0]
			if "Not a data message" not in res:
				tmp_list.append((service, code))
				break

	service_list = []
	current.set_status(1)
	for service in tmp_list:
		logcat_flush()
		for code in range(1, service[1]+1):
			current.set_current(service[0], code)
			if service_call(service[0], code)[1]:
				break
		if check_crash():
			current.append_service(service[0])
			service_list.append(service)

	total = 0
	for service in service_list:
		total += service[1]
	current.set_total(total)
	
	return service_list

def logcat_flush():
	os.system(f'adb logcat -c')
			
def check_crash():
	sleep(args.sleep)
	res = os.popen('adb logcat -b crash -d -v brief | grep "E/AndroidRuntime"').read()
	return res != ''

def restore_crash_dump(service, code):
	res = os.popen('adb logcat -b crash -d -v brief | grep "E/AndroidRuntime"').read()
	with open(f'{OUTPUT_PATH}/{service}_{code}', 'w') as f:
		f.write(res)

def print_intro():
	os.system("clear")
	print('\n\n\n')
	print('\t----------------------------------------------------------------------------')
	print("\t|		      _           _     _                                  |")
	print("\t|     /\             | |         (_)   | |                                 |")
	print("\t|    /  \   _ __   __| |_ __ ___  _  __| |                                 |")
	print("\t|   / /\ \ | '_ \ / _` | '__/ _ \| |/ _` |                                 |")
	print("\t|  / ____ \| | | | (_| | | | (_) | | (_| |                                 |")
	print("\t| /_/____\_\_| |_|\__,_|_|  \___/|_|\__,_|____                 _           |")
	print("\t|  / ____|         | |                  / ____|               (_)          |")
	print("\t| | (___  _   _ ___| |_ ___ _ __ ___   | (___   ___ _ ____   ___  ___ ___  |")
	print("\t|  \___ \| | | / __| __/ _ \ '_ ` _ \   \___ \ / _ \ '__\ \ / / |/ __/ _ \ |")
	print("\t|  ____) | |_| \__ \ ||  __/ | | | | |  ____) |  __/ |   \ V /| | (_|  __/ |")
	print("\t| |_____/ \__, |___/\__\___|_| |_| |_| |_____/ \___|_|    \_/ |_|\___\___| |")
	print("\t|          __/ |                                                           |")
	print("\t|         |___/                                                            |")
	print("\t|	   								   |")
	print("\t|									   |")
	print("\t|						 - settopbobs -		   |")
	print("\t|									   |")
	print("\t|									   |")
	print('\t----------------------------------------------------------------------------\n')
	sleep(1.5)

def fuzz():
	global current
	service_list = get_service_list()
	current.set_status(2)
	for service in service_list:
		for code in range(1, service[1]+1):
			current.set_current(service[0], code)
			current.inc_number()
			current.print_current()
			logcat_flush()
			service_call(service[0], code)
			if check_crash():
				restore_crash_dump(service[0], code)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output_path', type=str, dest='output_path',required=True, help='set output file path')
	parser.add_argument('-s', '--sleep_second', type=float, dest='sleep', default=1.5, help='set sleep second for checking crash')
	parser.add_argument('-root', '--root', action='store_true', help='for rooted deivice')
	parser.add_argument('-null', '--null', action='store_true', help='service call with null')

	args = parser.parse_args()

	OUTPUT_PATH = args.output_path
	if args.root:
		SU = "su -c "
	if args.null:
		NULL = " null"

	current = Current()
	print_intro()
	fuzz()
