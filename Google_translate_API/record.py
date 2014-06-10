import time
import os 


setting  = {
	'dir_path' : '/Users/darkh/Documents/English_words/',
}
class utils_check:
	@staticmethod
	def get_today_time():
		#info = {}
		#priary =  time.time()
		#info['year'] = priary[0]
		#info['mon'] = priary[1]
		#info['day'] = priary[2]
		info = time.asctime().split()[:3]
		return ' '.join(info)


	@staticmethod
	def ls_dir():
		files  = list(map((lambda x : x[:-2] ), os.popen("ls "+ setting['dir_path']))) 
		return files

class Write:

	@staticmethod 
	def Log(callback,argu):

		Res ="\n" + callback(argu)
		t_info = utils_check.get_today_time()
		with open(setting['dir_path']+t_info+'.html','a') as FILE:
			FILE.write(Res)



