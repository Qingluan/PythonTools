#!/usr/local/bin/python3
import urllib.request as ur 
import re
from threading import Thread

class read_hosts:

	def __init__(self):
		with open("hosts_ips.ip",'r') as handler:
			self.hosts_ips = list(map (lambda x:x.strip(), handler.readlines()))
	def callback(self,url):
		test_read_content = read_content(url)
		test_read_content.get_source_ip()
		test_read_content.run_mul()

	def mul_run(self):
		list(map(self.callback,self.hosts_ips))

class read_content:
	all_hosts_ips = []
	threads = []
	def __init__(self,url):
		self.url = url
		self.request = ur.Request(self.url)
		self.fp = ur.urlopen(self.request)	
		self.content_pri = self.fp.read().decode('utf-8')

		self.get_prefix()

	def get_prefix(self):
		h,con = self.url.split(r'//')
		self.base_site = h+"//"+con[:con.find('/')]


	def get_source_ip(self):
		pa = re.compile(r'(?:<a href="(.+?sources.+?)".+?>)')
		res = re.findall(pa,self.content_pri)
		if res:
			read_content.all_hosts_ips = list(map(lambda x: self.base_site + x,res ) )
			for i in read_content.all_hosts_ips:
				print(i)

	def run_mul(self):
		list(map(lambda x : read_content.threads.append(Thread(target=read_content.record_hosts,args=(x,))) ,read_content.all_hosts_ips))
		list(map(lambda x: x.start(),read_content.threads))

	@staticmethod
	def record_hosts(url):
		"""
			mul-thread to from ip get content ..
		"""
		print("downloading ... %s " %url )
		name =  "_".join(url.split("/")[-4:])

		request= ur.Request(url)
		data = ur.urlopen(request).read().decode('utf-8')
		with open(name+".hosts","w") as handler:
			handler.write(data)




if __name__ =="__main__":
	# res = get_content("https://www.projecth.us/sources/9/15/hosts")
	# print(res)
	handler = read_hosts()
	handler.mul_run()

