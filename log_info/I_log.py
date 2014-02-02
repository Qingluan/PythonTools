#!/usr/bin/python

import sys
from os import popen,system
import time
from functools import reduce
import sqlite3

def get_argv(path):
	com1 = "ls " + path_check(path)
	lis = list(popen(com1))
	lis = list(map((lambda x:x[:-1]),lis))
	return lis 

def test_con(script,lis):
	argv = reduce((lambda x,y:  x + " " + y),lis)
	com2 = script + " " + argv
	print(com2)
	res = list(popen(com2))
	return res

def path_check(path):
	res = system("cd " + path)
	if res== 0:
		return path
	else :
	 	raise ValueError("check you path !")
 

def log(res):
	for i in res :
		print(i)
def search_in_db(name_list,row_name=None,value=None):
	if len(name_list) != 0:
		if row_name == None:
			line_names = reduce((lambda x,y : x + ","+y),name_list)
			command = """select """ + line_names +"from log"
			return command
		elif row_name != None and value != None:
			line_names = reduce((lambda x,y : x+","+y),name_list)
			command = "select " + line_names + "from log where "+row_name+"="+value
			return command
	else :
		if row_name == None:
			command = "select " + " * " + " from log "
			return command
		elif row_name != None and value != None:
			command = "select * from log where " + row_name + "=" + '"'+ value + '"'
			return command
def insert_in_db(values):
	print(values)
	Id  = values["id"]
	Name = values["name"]
	Type = values["type"]
	Path = values["path"]
	Time = time.asctime()
	command_part = Id +',' + '"' + Name+'"'+','+'"'+Type+'"'+','+'"' + Path+'"'+',' +'"'+Time + '"'
	command = "insert into log values(" +command_part + ")"
	return command

if __name__ =="__main__":
	ar = sys.argv
	if len(ar) >= 2:
		if ar[1] == "test":
			sc = input(">>script name (ex:python3 ./some.py) :\t")
			pa = input(">>target path :\t")
			ars = get_argv(pa)
			res = test_con(sc,ars)
			log(res)
		
		elif ar[1] == "log":
			with sqlite3.connect("/Users/darkh/Desktop/.my_process.db") as cx:
				cu = cx.cursor()
				cu.execute("select name,time from log ")
				res = cu.fetchall()
				for item in res :
					print(item)
		elif ar[1] == "find":
			row = ar[2]
			val = ar[3]	
			with sqlite3.connect("/Users/darkh/Desktop/.my_process.db") as cx:
				cu = cx.cursor()
				com = search_in_db([],row_name=row,value=val)
				print(com)
				cu.execute(com)
				res = cu.fetchall()
				for item in res :
					print(item)
		elif ar[1] == "record":
			tem= dict()
			tem["id"] = ar[2]
			tem["name"] = ar[3]
			tem["type"] = ar[4]
			tem["path"] = ar[5]
			with sqlite3.connect("/Users/darkh/Desktop/.my_process.db") as cx:
				cu = cx.cursor()
				com = insert_in_db(tem)
				cu.execute(com)
				cx.commit()
		elif ar[1] == "-h":
			print("\nthis could be uesed to test some process ....\n   by\n\t ' test [arg1=somescript] [arg2=path] '\nthis could be log some log info by:\n\t 'log'  ")
			print("\n  db info :lines id\tname\ttype\tpath\ttime\n\t'find [arg1=row_nama_in_db] [arg2=value_where_row_name_equal]'")
			print("it also could insert new info by\n\t'record  [arg1=id] [arg2=name] [arg3=type] [arg4=path] '")
	else  :
		print("\nthis could be uesed to test some process ....\n   by\n\t ' test [arg1=somescript] [arg2=path] '\nthis could be log some log info by:\n\t 'log'  ")
		print("\n  db info :lines id\tname\ttype\tpath\ttime\n\t'find [arg1=row_nama_in_db] [arg2=value_where_row_name_equal]'")
		print("it also could insert new info by\n\t'record  [arg1=id] [arg2=name] [arg3=type] [arg4=path] '")
