#!/usr/bin/python
import os

from functools import reduce
from os import system,popen
from sys import argv
from time import asctime
import threading
from threading import Thread

from set_unpack import target_path ,path_set_Path
path_set_Path = path_set_Path
with open(path_set_Path+".path.set","r") as pa:
	global target_path
	sign =  pa.readline()
	if sign[0] != "#":
		target_path = sign
		print("load ..path..ok")
from set_unpack import type_dict

file_list = argv[1:]
files = []


class Uncompress:
	def __init__(self,file_name,type_dict):
		dir_name = os.path.dirname(file_name)
		self.name = file_name[len(dir_name):]
		self.file_name = file_name 
		self.type_dict = type_dict
	#	print(1,self.type_dict)
	#	print(2,self.name)
	def re_order_key(self):
		tem_keys = list(self.type_dict.keys())
		for num in range(len(tem_keys)) :
			for num2 in range(len(tem_keys)):
				tem = None
				if len(tem_keys[num2]) > len(tem_keys[num]):
					tem = tem_keys[num]
					tem_keys[num] = tem_keys[num2]
					tem_keys[num2] = tem
		tem_keys.reverse()
#		print(tem_keys)
		return tem_keys
	def check_file_type(self):
		name_poor = self.name.split(".")
		if len(name_poor) == 3:
			tem_dict_keys = self.re_order_key()
			for ty in tem_dict_keys :
				if ty in self.name :
			#		print("ty",ty)
					return ty
		elif len(name_poor) == 2:
			tem = name_poor[1]
#			print(3.2,os.path.basename(tem))
			return os.path.basename(tem)
		else :
			tem_dict_keys = self.re_order_key()
			for ty in tem_dict_keys:
				if ty in self.name :
			#		print(ty)
					return ty

	def uncompress(self):
		key = self.check_file_type()
	#	print(4,key)
		command_part1 = self.type_dict[key] + self.file_name
		command_part2 = "mv " + "./"+ self.name[:len(self.name)-len(key)-1] + " " + target_path
		print(1,command_part1)
		print(2,command_part2)

		system(command_part2)
		system(command_part1)
		
class load_thread(Thread):
	def __init__(self,file_name):
		Thread.__init__(self)
		self.name = file_name	
		self.Un_th = Uncompress(self.name,type_dict)
	def run(self):
		self.Un_th.uncompress()

class thread_tree:
	def __init__(self,Obj,argv_list):
		self.Obj  = Obj
		self.argv_list = argv_list
	#	print(7,self.argv_list)
	def Tree (self,argc):
		return self.Obj(argc)

	def create(self):
		return list(map(self.Tree,self.argv_list))

def check():
	if len(argv) < 1:
		raise ValueError("you should at least input one file")

def main():
	files = map((lambda x: path.basename(x).split(".")[0]),file_list)
	tree = thread_tree(load_thread,file_list)
	th_tree = tree.create()
	for i in th_tree:
		i.start()

if __name__ == "__main__":
	check()
	main()
