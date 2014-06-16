setting = {
	'dir' : './sources/',
}

ips = {
	#### '(?:<a href="%s".+?>)' %(self.pattern) ' ###
	'https://www.projecth.us/sources' :{
		'ip':r'(.+?sources.+?)' ,
		'pre':True,
	},
	'https://code.google.com/p/smarthosts/' :{
		'ip':r'(.+?trunk/host.+?)', #(?:<a href="(.+?trunk/host.+?)".+?>)
		'pre':False,
	}
}
