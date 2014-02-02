#!/usr/local/bin/python3

from sys import argv
from os import system ,popen
target_path = "/Users/darkh/temp/" #default ,if '.path.set' exist ,this will not be used.
path_set_Path = "/Users/darkh/" #there store a '.path.set' file ,this file decide uncompress target path.
type_dict = {
	"tar.gz" : "tar -zxvf ",
	"tar.bz2" : "tar -jxvf ",
	"tar.bz" : "tar -jxvf ",
	"tar" : "tar xvf ",
	"zip" : "unzip ",
	"rar" : "rar x ",
	"tgz" : "tar -zxvf "
}


def path_check(path):
	res = system("cd " + path)
	if res== 0:
		return path
	else :return False

if __name__ == "__main__":
	if len(argv) == 2:
		newPath = path_check(argv[1])
		if newPath != False:
			command = 'echo "' +newPath + '" > ' + path_set_Path + '.path.set'
			re = system(command)
			print(command)
			if re == 0:
				print("ok ,seting successful !")
			else :
				print("command error")
		else :
			raise ValueError("This path is not right ,check it !")
	else :
		print ("this is set uncompress path ,by type into 'setting_path.py someNewPath'")
