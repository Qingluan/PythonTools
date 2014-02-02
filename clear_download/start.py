#!/usr/local/bin/python3
from os import getcwd ,system ,popen
import re
import time
import threading

Path = "/usr/local/bin/clear_download/"
command_0 ="ls " + Path + "Cl"

scrip_list = popen(command_0)
scrip_list = map((lambda x : x[:-1]),scrip_list)

thread_pool = []

"""
def load_thread(scrip_list):
	
	for item in scrip_list:
		new_thread(item)

class thread_pool(threading):
	def __init__(self,name):
		threading.__init__(self)		
		self.name = name
	def run(self):
		new_thread(self.name)

"""

def run_thread(scrip_list):
	for item in scrip_list:
		new_thread(item)

def new_thread(name):
	if name_check(name) == True:
		command = Path+"/Cl/"+item
			#print(command)  #test
			system(command)
	else :
			pass

def name_check(file_name):
	pattern = re.compile(r"\.py$")

	try :
		re.search(pattern,file_name).group()
		return True
	except AttributeError :
		return False

if __name__ == "__main__":
	run_thread(scrip_list)
	print(time.asctime())