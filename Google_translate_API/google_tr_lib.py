#!/usr/local/bin/python3

import urllib.request as ur
import re
import sys
import gzip
from functools import reduce
from threading import Event , Thread ,currentThread
from time import asctime ,time
try:
	from sound_tool import Sound 
except ImportError:
	error_string = "your sound moudle is demaged ..check 'sound_tool.py'  "
	print(error_string) #test

try:
	from colorlib import color
except ImportError:
	pass

#Speak_words_list = None  # this argc is for 'sound' thread to use.

event = Event()

class Construc_name :
	"""
		this is for Construct a  keyword which would type into url
	"""
	def __init__(self):
		self.tem_list = None
		self.word = None
		self.url = "http://translate.google.cn/translate_a/t?client=t&sl=auto&tl=zh-CN&hl=en&sc=2&ie=UTF-8&oe=UTF-8&uptl=zh-CN&alttl=en&ssel=0&tsel=0&q="

		self.real_word = ""
		
	def Judge_word(self): 
		################ !!!!!#########################################
		global Speak_words_list # !!!!!!! careful this ,it must !!!  ##
		###############################################################

		if len(sys.argv) >1 :
			self.tem_list = sys.argv[1:]
		else :
			self.word = input("Type : ")						
			self.tem_list = self.word.split()

		Speak_words_list = self.tem_list #caraful this ,it involve global para

		if len(self.tem_list) > 1:
			for word in self.tem_list:
				self.real_word = self.real_word + "%20" +word
		else:
			self.real_word = self.tem_list[0]

		
		if Speak_words_list != None:   #you should care of this ,it involve thread
			#print(currentThread(),Speak_words_list,"1.2")   #test
			event.set()      
	
	def get(self):
		self.Judge_word()
		#print(currentThread(),Speak_words_list,"1.3")  #test
			
		tem = self.url + self.real_word
	#	print(tem) #test
		return tem


class GoogleTranslateLib:
	"""
		create a web request moudle ,this is a import moudle
	"""
	def __init__(self,url):
		self.url = url
		self.request = ur.Request(self.url)
		self.headers = {
			'Host':'translate.google.cn',
			'Refer' : 'http://translate.google.cn/?hl=en',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',								
			'Accept-Encoding':'gzip,deflate,sdch',
			'Accept-Language': 'en-US,en;q=0.8',
					#'gzip, deflate'
			#'Cookie':'PREF=ID=ad8886b7f790ae48:U=3bb00ae363164775:NW=1:TM=1374477391:LM=1375175072:S=uG3Rup9TMB8FXVcC; _ga=GA1.3.2029404992.1385734473; Hm_lvt_3d143f0a07b6487f65609d8411e5464f=1389753542,1390020341,1390192903,1390288106; Hm_lpvt_3d143f0a07b6487f65609d8411e5464f=1390292284'
			'Cookie':'PREF=ID=ad8886b7f790ae48:U=3bb00ae363164775:NW=1:TM=1374477391:LM=1375175072:S=uG3Rup9TMB8FXVcC; Hm_lvt_3d143f0a07b6487f65609d8411e5464f=1389753542,1390020341,1390192903,1390288106; Hm_lpvt_3d143f0a07b6487f65609d8411e5464f=1390292284; _ga=GA1.3.2029404992.1385734473'
			}

		for key in self.headers.keys():
			self.request.add_header(key,self.headers[key])
		#self.opener = ur.build_opener()
		#process by searched 
		self.info = None
		self.first_result = None
		self.second_result = None
		#self.RESULT = None
		self.if_gzip = False
	def search(self):
		fp = ur.urlopen(self.request)
		self.info =  fp.info()
	#	print(self.info)   #test
		b_part1= fp.read(2)
		b_part2 = fp.read()
		
		self.if_gzip =  self.check_gzip(b_part1)
		b = b_part1 + b_part2
		temp_str = str(b)
	#	print (temp_str) #test
		charset = self.find_charset()
		print ("charset : ",charset)
		#print(dir(fp)) #test
		if (fp == None):
			raise "Can't connecting"
		
		b = self.decompress(b)	

		self.first_result = b.decode(charset)
		#print (self.first_result)
	#	with open("/Users/darkh/Desktop/search.html","w") as newhtml:
	#		newhtml.writelines(self.first_result)
		
	def check_gzip(self,char):

		if char ==b'\x1f\x8b' :
			print("this request head contain : gzip")
			return True
		return False 

	def decompress(self,com_bytes):
		if self.if_gzip == True:
			return gzip.decompress(com_bytes)		
		return com_bytes

	def find_charset(self):
		"""
			this is for finding html's charset
		"""
		Response_info = str(self.info)
		pattern1 = re.compile(r'(charset=.+?\n)')
		result = pattern1.findall(Response_info)
		"""
			result = "charset=....\n"
			get charset is result[8:-1]
		"""
									#print (result[0][8:-1]) test
 		#print ("\n\n")
		return result[0][8:-1]

	def format_result(self):
		"""
		this is for finding html's serching-result
		"""
		self.search()
				#print(self.first_result) #test
		if self.first_result != None:
		#	pattern2 = re.compile(r'(<span class=.+?</span>)')
		#	pattern3 = re.compile(r'(<span id=result_box .+?</div>)')
			
			#this is for finding the best result  ex: [[["Linux的","Linux","Linux de",""]]
			#pattern_best_result = re.compile(r'(\[\[\[.+?\])')
			#temp_best_result = pattern_best_result.findall(html_text)[0]
			#pattern_best_result_res = re.compile(r'\".*?\"')
			####best_result_list[result,pre-search,how to read ,None]
			#best_result_list = pattern_best_result_res.findall(temp_best_result)

			#detail = html_text[len(temp_best_result):]
			res_html = self.first_result
			t1 =  self.first_result.replace(",[","\n\t")
			t2 = t1.replace('"\n\t"','"\t===>\t"')
			t3 = t2.replace('[','')
			t4 = t3.replace('],,','\n\t\t')
			t5 = t4.replace('""','\n')
			self.second_result = t5.replace(']','')

			#print (self.second_result)
			return self.second_result
	def get(self):
		
		RESULT = self.format_result()
		#print(RESULT)    #test
		if self.second_result != None:
			return RESULT



		#with open("/Users/darkh/Desktop/search2.html","w") as newhtml:
		#	newhtml.writelines(self.first_result)

class Speaker:
	"""
		this class will deal a [words...] to string ,then pass string to Sound class 
	"""
	def __init__(self,words_list):
		self.words_list = words_list
	def makeText(self):
		Text = None
		if len(self.words_list) == 1:
			Text = self.words_list[0]
		else:
			Text = reduce((lambda x ,y : x + " " + y),self.words_list)
		if Text != None:
			return Text

	def say(self):
		words = None
		words = self.makeText()
		try :
			speaker = Sound(words)
			#print(asctime(),"2",time())  #test

			speaker.say()
			#print(asctime(),"2.2",time())  #test
		except NameError:
			pass

class load_Sound_thread(Thread):
	"""
		this class is to package a sound to a new thread 
	"""
	def __init__(self):
		Thread.__init__(self)
		self.text_list = None
		global Speak_words_list
	def run(self):
		if Speak_words_list == None: 
			#print ("wait") #test			
			event.wait()  # wait global 'Speak_words_list' get a value 
	
		# global  'Speak_words_list'  have got a value ,this thread start again	
		self.text_list = Speak_words_list
		sound_thread = Speaker(self.text_list)
		sound_thread.say()


if __name__ == "__main__":
	print()
#	word = input(">> Search > ")
#	google = "http://translate.google.cn/translate_a/t?client=t&sl=auto&tl=zh-CN&hl=zh-CN&sc=2&ie=UTF-8&oe=UTF-8&uptl=zh-CN&alttl=en&oc=2&otf=2&ssel=3&tsel=0&q="
	try:
		Speak_words_list = None  # this argc is for 'sound' thread to use.

		speaker_th1 = load_Sound_thread()  #this is another thread
	#print(currentThread(),Speak_words_list,"0") 	#test		
		speaker_th1.start() #thread 1 start !!!!!! 
	except   NameError :
		pass
	except ImportError:
		print("you lose sound moudle")
	#print(currentThread(),Speak_words_list,"1") #test

	google = Construc_name()
	#print(currentThread(),Speak_words_list,"2.1")  #test

	real = google.get()							#print (real)  test 
	#print(currentThread(),Speak_words_list,"2") #test
 
	a = GoogleTranslateLib(real)
	res = a.get()
	try:
		b = color('blue')
		print (b.get_color(res))

	except NameError:
		print("No colorlib")
		#print(asctime(),"1",time())  #test
		print()
		print(res)
		#print(asctime(),"1.1",time())  #test

"""

"""
