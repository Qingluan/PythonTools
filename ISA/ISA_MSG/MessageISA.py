import tornado.web
import tornado.ioloop
import tornado.gen
import os,time,json
import bcrypt
import motor
import pymongo

from  SayFactory import Say
from Cookie_client import Authentication

DB_client = motor.MotorClient().open_sync()

temp_users = {
	
}

settings = {
	'db':DB_client,
	'autoreload':True,
	'debug':True,
	'cookie_secret': 'secret make you look better',
}

RESPONSE = {
	"login" : "ok",
	"pass_error" : "your password is wrong ,please check again",
	"account_error" : "no such account",
	"sign_up_T" : "ok",
	"sign_up_nil" : "this name is exist !! try again!!", 
	"unlogin" : "unlogin",
	"alreadyL" : "already login",
	"exit" : "exit successful !!",
}


class BaseHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.db = self.settings['db'] 

class SignUpRequestHandler(BaseHandler):
	def get(self):
		self.write("please sign up !!")

	@tornado.gen.engine
	@tornado.web.asynchronous
	def check(self,name,email,password):
		print ("%s\n%s\n%s\nSign up successful !\n" %(name,email,password))

		name_exist = yield motor.Op(
				self.db.users.contact.find_one, {'name':name }
			)
		if not name_exist :
			contact = {
				'name':name,
				'email' : email
			}

			contact_with_pass = {
				'name' : name,
				'password' : password
			}

			self.db.users.contact_with_pass.insert(contact_with_pass)
			self.db.users.contact.insert(contact)
			resOk  = RESPONSE['sign_up_T']
			Json_response = json.dumps(resOk)
			self.write(Json_response)
			self.finish()
		else :
			resErr = RESPONSE['sign_up_nil']
			Json_response = json.dumps(resErr)
			self.write(Json_response)
			self.finish()
	
	@tornado.web.asynchronous
	def post(self):
		Json_request = json.loads(self.get_argument("JSON_SIGN"))
		name = Json_request['name']
		email = Json_request['email']
		password = Json_request['password']

		self.check(name,email,password)

class LoginRequestHandler(BaseHandler):
	def get(self):
		self.write("please login ")

	@tornado.web.asynchronous
	@tornado.gen.engine
	def check(self,name,password):
		print ("Login :%10s\n%10s" %(name,password))
		#hash_password = bcrypt.hashpw(password,bcrypt.gensalt()) #encripted passs 
		check_dict = {
			'name' : name,
			'password' : password
		}

		document = yield motor.Op(
				self.db.users.contact_with_pass.find_one,
				check_dict
			)
		count = yield motor.Op(self.db.users.message_contact.find().count)
		if document and document['password'] == password:
			Json_response = json.dumps({
				'state' : RESPONSE['login'],
				'count' : count,
				})

			Authentication.record_user(name)
			if not Authentication.check_already_login(name):
				Json_response = json.dumps(RESPONSE['alreadyL'])
				self.write(Json_response)
				self.finish()
			else:
				print "%5s : ===Login ok !!===" %name
				self.write(Json_response)
				self.finish()	

		elif document and document['password'] != password :
			Json_response = json.dumps(RESPONSE[pass_error])
			self.write(Json_response)
			self.finish()
		else :
			Json_response = json.dumps(RESPONSE['account_error'])
			self.write(Json_response)
			self.finish()

	@tornado.web.asynchronous
	def post(self):

		Json_request = self.get_argument("JSON_LOGIN", strip = True)
		
		user_info = json.loads(Json_request)
		name = user_info["name"]
		password = user_info["password"]
		
		self.check(name,password)

class MessageRequestHandler(BaseHandler):
	def get(self):
		if not self.current_user:
			self.write("hello world")
		else :
			self.set_secure_cookie('user','sss')
	
	@tornado.web.asynchronous
	def post(self):
		print "i: %s" %self.get_current_user()
		Got_value = self.get_argument("JSON_MSG")
		print "Server got : %s" %Got_value
		Json_request = json.loads(Got_value)
		name = Json_request['name']

		if not  Authentication.check_time_out(name):#Authentication.check_time_out(name,temp_users):
			print "go to message area"
			Json_response = json.dumps(RESPONSE['unlogin'])
			self.write(Json_response)
			self.finish()
		else:
			msg = Json_request['msg']
			Message = Say.construct(name,msg,time.asctime())
			Authentication.Update_login_info(name)

			self.Save(name,Message)
			Json_response = json.dumps(Message)
			self.write(Json_response)
			self.finish()

	@tornado.gen.engine
	@tornado.web.asynchronous
	def Save(self,name,msg):
		print "Message Area ========"
		print "%s" % msg 
		count = yield  motor.Op( self.db.users.message_contact.find().count)
		count += 1
		message_contact = {
			"i" : count,
			"name" : name,
			"time" : time.asctime(),
			"msg" : msg
		}
		self.db.users.message_contact.insert(message_contact)
		print "all message count : %d" %count
		#db cal



class PushMessageRequestHandler(BaseHandler):
	def get(self):
		self.write("push a message")

	@tornado.web.asynchronous
	def post(self):
		Json_request = json.loads(self.get_argument("JSON_SYNC"))
		name = Json_request['name']

		if not Authentication.check_time_out(name):
			Json_response = json.dumps(RESPONSE['unlogin'])
		else :	
			
			from_item_count =  Json_request['i'] 
			print ("from item : %d"%from_item_count)
			self.do_find(from_item_count)
		
			#db

	@tornado.web.asynchronous
	@tornado.gen.engine
	def do_find(self,i):
		MSG_list = []
		cursor = self.db.users.message_contact.find({'i' : {'$gt' : i }})
		
		while (yield cursor.fetch_next):
			MSG_list.append(cursor.next_object())

		mes_list = map((lambda x: x['msg']),MSG_list)

		Json_response = json.dumps(mes_list)
		self.write(Json_response)
		self.finish()

class ExitRequestHandler(BaseHandler):
	def post(self):
		Json_request =  json.loads(self.get_argument("JSON_EXIT"))
		name = Json_request['name']
		if Authentication.off_online(name):
			self.write(json.dumps(RESPONSE['exit']))
		else :
			self.write(json.dumps(RESPONSE['unlogin']))



appication = tornado.web.Application([
		(r'/regist',SignUpRequestHandler),
		(r'/login',LoginRequestHandler),
		(r'/send_msg',MessageRequestHandler),
		(r'/get_msg',PushMessageRequestHandler),
		(r'/exit',ExitRequestHandler),
	],**settings)

if __name__ == "__main__":
	appication.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
