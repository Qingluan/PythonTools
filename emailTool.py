#-*- encoding: gb2312 -*-
#!/usr/bin/python
import email
import string ,sys,os
import time

class emaillib:
	"""
		for email ... constructer
	"""
	def __init__(self):
		self.msg = email.Message.Message()
		self.mail = ""

	
	def create(self,mail_header,mail_data,mail_attach_list=[]):
		"""
		@param main_header : dict
		@param main_data  : list
		@param mail_attach_list  :list [file name]
		"""

		if not mail_header :
			raise ValueError("No header ...")

		for key in mail_header.keys():
				if key == 'subject':
					self.msg[key] = email.Header.Header(mail_header[key], 'gb2312')  
				else:
					self.msg[key] = mail_header[key]
				

		body_plain_text = email.MIMEText.MIMEText(mail_data[0],_subtype='plain',_charset='gb2312')

		body_html = None

		if mail_data[1]:
			body_html  = email.MIMEText.MIMEText(mail_data[1],_subtype="html",_charset='gb2312')

		attach = email.MIMEMultipart.MIMEMultipart()
		attach.attach(body_plain_text)
		
		if body_html:
			attach.attach(body_html)
		#deal with attach
		for fname in mail_attach_list:
				attachment = email.MIMEText.MIMEText(email.Encoders._bencode(open(fname,'rb').read()))
				
				attachment.replace_header('Content-type','Application/octet-stream;name='+os.path.basename(fname)+'""')
				attachment.replace_header('Content-Transfer-Encoding', 'base64')
				attachment.add_header('Content-Disposition','attachment;filename="'+os.path.basename(fname)+'"')
				attach.attach(attachment)
				

		self.mail = self.msg.as_string()[:-1] + attach.as_string()
		return self.mail

if __name__ == "__main__":
	mc = emaillib()
	header = {
			'from':'1026114232@qq.com',
			'to':'wickzt@gmail.com',
			'subject':'test .....',
			}
	data = ['plain text information', '<font color="red">html text information</font>']
	mail = mc.create(header, data)
	f = open('test.eml','wb')
	f.write(mail)
	f.close()
				

