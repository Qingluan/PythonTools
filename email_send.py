#!/usr/bin/python
# -*- coding: gbk -*-   

import smtplib, mimetypes  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart  
import email
import sys,os


class Contact:
	
	Contact = {
	#<contact>
		'mao' : 'maoxinhorizon@gmail.com',
		'tong': 'wickzt@gmail.com',
		'meng': 'mengwei607@gmail.com',
	#<contact>
	}	
	@staticmethod
	def get(key):
		return Contact.Contact[key]

def check(arg):
	if len(sys.argv) <3 :
		print ( "argu error \n to [-s|summary] content \r\n")
		sys.exit(0)
	else:

		if sys.argv[1] != '-q':
 			if (not "@" in sys.argv[1]) and '-q' != sys.argv[1]:
				print ("first argu must be a email address")
				sys.exit(0)


def get_summary(arg):
	if arg[2] == "-s":
		return arg[3]
	else :
		return 'subject'


def get_plain_text(arg):
	if os.path.isfile(arg):
		email_t = open(arg,'r')
		Text = email_t.read()
		email_t.close()
		return Text 
	else :
		return arg

def get_attach():
	last_arg = sys.argv.pop()
	if (os.path.isfile(last_arg)):
		return last_arg
	else :
		return None

def get_to_addr():
	if sys.argv[1] == "-q" and sys.argv[2] in Contact.Contact.keys(): 
		con = Contact.get(sys.argv[2])
		sys.argv.remove(sys.argv[1])
		return con 
	else :
		return sys.argv[1]

class MailServer:
	setting = {
		'server': 'smtp.qq.com',
		'user'	: "1026114232@qq.com",
		# 'pass'	: 'ohiqjqcxbmyxfiuu',
		'port'	: 465,
	}

	def __init__(self,pass_t):
		print ("Connecting ...")

		self.smtp = smtplib.SMTP()
		# self.smtp.set_debuglevel(1)

		try:
			self.smtp.connect(MailServer.setting['server'])
		except :
			print ("\rConnecting error **********")
		# self.smtp.ehlo()
		# self.smtp.starttls()
		
		try:
			print ("logging....")
			print ("user : ",MailServer.setting['user'])
			self.smtp.login(MailServer.setting['user'],pass_t)
			print ("login ok!!!******************")
			# self.smtp.ehlo()
		except :
			print ("login ...error  *************")
		# print self.smtp.getreply()


	def send(self,to_add,plain_text,summary='subject',attach=""):
		plain_text = str(plain_text)
		# print type("stomsd")
		self.msg = MIMEMultipart()
		self.msg['From'] = MailServer.setting['user']
		self.msg['To'] = to_add
		self.msg['Subject'] = summary
		T = MIMEText(plain_text)
		self.msg.attach(T)
		# self.msg.set_charset('gb2312')
		# print (text)
		if attach:
			ctype,encoding = mimetypes.guess_type(attach)
			if ctype is None or encoding is not None:
				ctype='application/octet-stream'
			maintype,subtype = ctype.split('/',1)
			print maintype ,subtype

			att=MIMEImage(open(attach, 'rb').read(),subtype)
			print ctype,encoding
			Content_dis = 'attachmemt;filename="%s"' %attach
			print Content_dis
			att["Content-Disposition"] = Content_dis 
			self.msg.attach(att)
		# self.smtp.sendmail(MailServer.setting['user'],to_add,self.msg.as_string())
		try:
			self.smtp.sendmail(MailServer.setting['user'],to_add,self.msg.as_string())
			print "send  email ok"
		except smtplib.SMTPSenderRefused :
			print "Error Pass check again\n"
			exit(0)
		# self.smtp.send("\nfrom Dr.%s"% MailServer.setting['user'])
		# self.smtp.getreply()
		# self.close()
		
		# self.smtp.quit()




if __name__ == "__main__":
	############## test ####################
	check(sys.argv)
	to_addr = get_to_addr()
	print "to :",to_addr
	subject =get_summary(sys.argv)
	attach = get_attach()
	mineT = sys.argv.pop()

	text = MIMEText(get_plain_text(mineT))
	pass_t = raw_input("pass>")
	########################################
	
	mail = MailServer(pass_t)
	mail.send(to_addr,text,summary=subject,attach=attach)

