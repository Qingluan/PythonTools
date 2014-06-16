#!/usr/local/bin/python3
import urllib.request as ur 
import urllib
import re
from threading import Thread

###### load setting file ######
from hosts_ips import ips
from hosts_ips import setting	

class read_hosts:

	def __init__(self,ips):
		self.hosts_ips = ips

		
	def callback(self,url_key):
		test_read_content = read_content(url_key,self.hosts_ips[url_key]['ip'],if_prefix=self.hosts_ips[url_key]['pre'])
		test_read_content.get_source_ip()
		test_read_content.run_mul()

	def mul_run(self):
		list(map(self.callback,self.hosts_ips))

class read_content:
	all_hosts_ips = []
	threads = []
	def __init__(self,url,pattern,if_prefix=True):
		self.url = url
		self.pattern = pattern
		self.if_prefix = if_prefix

		self.request = ur.Request(self.url)
		self.fp = ur.urlopen(self.request)	
		self.content_pri = self.fp.read().decode('utf-8')

		self.get_prefix()

	def get_prefix(self):
		h,con = self.url.split(r'//')
		self.base_site = h+"//"+con[:con.find('/')]

	def filter(self,li):
		"""
			filter some site
		"""
		for item in li:
			if ".bat" in li:
				li.remove(item)

			if re.findall(r'[<>]',item):
				li.remove(item)
			
		return li

	def get_source_ip(self):
		pattern_content = '(?:<a href="%s".+?>)' %(self.pattern)
		pa = re.compile(pattern_content)
		res = re.findall(pa,self.content_pri)

		res = self.filter(res)
		if self.if_prefix:
			list(map(lambda x:read_content.all_hosts_ips.append(self.base_site + x),res ))
			for i in read_content.all_hosts_ips:
				print(i)
		else :
			list(map(lambda x:read_content.all_hosts_ips.append(x),res))

	def run_mul(self):
		list(map(lambda x : read_content.threads.append(Thread(target=read_content.record_hosts,args=(x,))) ,read_content.all_hosts_ips))
		# list(map(self.start_thread ,read_content.threads))

	

	@staticmethod
	def record_hosts(url):
		"""
			mul-thread to from ip get content ..
		"""
		### this is for fliter url whitch site include ".../hosts.bat(py/perl)"
		if not '.' in url.split("/")[-1]:  
			

			print("downloading ... %s " %url )
			dir_index = setting['dir']
			name = dir_index +  "_".join(url.split("/")[-4:])

			request= ur.Request(url)
			try:
				data = ur.urlopen(request).read()
				try:
					data = data.decode('utf-8')
					with open(name+".hosts","w") as handler:
						handler.write(data)
				except UnicodeDecodeError :
					print (url,"decode error ...try again")
					data_res = ""
					for i in range(int(len(data)/2)):
						try:
							data_res += data[i:i+1].decode("utf-8")
						except UnicodeDecodeError:
							pass
					with open(name+".hosts","w") as handler:
						handler.write(data_res)
			except urllib.error.HTTPError :
				print ("%s not 404 error "%url)
			

class run_all:

	def run_all_threads(self):
		list(map(self.start_thread ,read_content.threads))

	def start_thread(self,item):
		if item.is_alive():
			pass
		else :
			item.start()

if __name__ =="__main__":
	# res = get_content("https://www.projecth.us/sources/9/15/hosts")
	# print(res)


	handler = read_hosts(ips)
	handler.mul_run()
	run_all().run_all_threads()


