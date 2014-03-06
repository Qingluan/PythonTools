import termcolor
import json
import threading
import subprocess
import re

class  Log:
	"""docstring for """
	#@staticmethod
	#def to_people(string):
	#	p = re.compile(r'^<(?P<to_name>.+?)>$')
	#	try : 
	#		to_name = re.match(p,string).group('to_name')
	#		return to_name
	#	except ArithmeticError:
	#		return None



	@staticmethod 
	def type_to_all():
		MSG = input(termcolor.colored("<All> :","red"))
		#if Log.to_people(MSG):
		#	pass #for people to people	
		return MSG


	@staticmethod
	def print_history(List):
		history_list = list(map((lambda x: termcolor.colored("<history>","blue")+x+termcolor.colored('</history>','blue')),List))
		for i in history_list:
			print (i)

	@staticmethod
	def record_in_local(List):
		for line in List:
			subprocess.call(['perl','record.pl',line])
	
	@staticmethod
	def Count_history():
		num = 0
		for line in open("./HISTORY.info","r"):
			num +=1;
		return num

class DealJson:
	def output(self,json_array):
		return json.loads(json_array)

def Msg_get_Timer(callBack):
	t = threading.Timer(0.1,callBack)
	t.start()

