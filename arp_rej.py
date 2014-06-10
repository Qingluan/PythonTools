#!/usr/bin/python
import re
import sys
import os

class Arp:
	def __init__(self):
		print "get arp ...."
		self.all_arp_list = os.popen("arp -a ").read().strip()
		self.arps_ips = re.findall(r"(?P<ip>(?:\d+?\.){3}\d+?).+?(?P<arp>(?:\w{1,2}:){5}\w{1,2})",self.all_arp_list)
		self.arps_ips = map(lambda x: "arp -s " + " ".join(x),self.arps_ips)

	def run(self):
		print self.arps_ips
		map(lambda x: os.system(x),self.arps_ips)



if __name__ == "__main__":
	arp = Arp()
	arp.run()
