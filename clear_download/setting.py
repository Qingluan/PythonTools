from os import system
from os import popen
from start import name_check
from time import sleep
Path = "/usr/local/bin/clear_download/"
command_1 = "ls "+Path + "Cl"

scrip_list = popen(command_1)
scrip_list = map((lambda x: x[:-1]),scrip_list)

def chomod_add_exe():
	for itme in scrip_list :
		if name_check(itme) == True:
			command_2 = "chmod +x " + Path+"Cl/" + itme
			system(command_2)
			print(command_2) #test
		else :
			pass

	command_3 = "chmod +x "+Path +"start.py"
	system(command_3)
	
if __name__=="__main__":
	chomod_add_exe()
	sleep(1)
	system("clear")