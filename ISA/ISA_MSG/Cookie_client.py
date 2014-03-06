import time
from re import compile
from os import system
import subprocess

settings = {
	'online_users' : './users.info',
}

scripts = {
	'remove_user' : "./remove_user.pl",
	'update_user' : './update_user.pl'
}

class Authentication:

	@staticmethod
	def record_user(name):
		if   Authentication.do_find(name):
			Authentication.Update_login_info(name)
		else:	
			info = name +"    " + str(time.time())
			command = "echo %s  >> ./users.info" %info
			system(command)
		
	@staticmethod
	def do_find(name):
		finded_line = None
		try:
			for line in open("./users.info","r"):
				if name in line:
					finded_line = line
		except IOError:
			pass
		return finded_line

	@staticmethod
	def check_already_login(name):
		if not Authentication.do_find(name):
			return True
		else :
			if not Authentication.check_time_out(name):
				return False
			else :
				return True

	@staticmethod
	def off_online(name):
		if Authentication.do_find(name):
			subprocess.call(['perl',scripts['remove_user'],name,settings['online_users']])
			return True
		else :
			return False

	@staticmethod
	def check_time_out(name):
		finded_line = None
		finded_line = Authentication.do_find(name)

		if not finded_line:

			return False


		now_time = time.time()
		last_time = float (finded_line.split()[1] )
		
		if now_time - last_time > 180:
			subprocess.call(['perl',scripts['remove_user'],name,settings['online_users']])
			return False
		else :
			return True
		
	@staticmethod
	def Update_login_info(name):
		new_time =str( time.time() )
		subprocess.call(['perl',scripts['update_user'],name,new_time,settings['online_users']])

