# -*- coding: gbk -*-   

import smtplib, mimetypes  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart  
import email
import sys,os


def check(arg):
	if len(sys.argv) <3 :
		print ( "argu error \n to [-s|summary] content \r\n")
		sys.exit(0)
	else:
		if (not "@" in sys.argv[1]):
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


	def send(self,to_add,plain_text,summary='subject'):
		plain_text = str(plain_text)
		# print type("stomsd")
		self.msg = MIMEText(plain_text)
		self.msg['From'] = MailServer.setting['user']
		self.msg['To'] = to_add
		self.msg['Subject'] = summary
		# self.msg.set_charset('gb2312')
		# print (text)
		self.smtp.sendmail(MailServer.setting['user'],to_add,self.msg.as_string())
		# self.smtp.sendmail(MailServer.setting['user'],to_add,self.msg.as_string())
		# self.smtp.send("\nfrom Dr.%s"% MailServer.setting['user'])
		# self.smtp.getreply()
		# self.close()
		print "send  email ok"
		# self.smtp.quit()




if __name__ == "__main__":
	check(sys.argv)
	to_addr = sys.argv[1]
	subject =get_summary(sys.argv)

	mineT = sys.argv.pop()

	text = MIMEText(get_plain_text(mineT))

	pass_t = raw_input("pass>")
	mail = MailServer(pass_t)
	mail.send(to_addr,text,summary=subject)

