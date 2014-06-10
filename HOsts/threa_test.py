import threading
from threading import Thread


from time import sleep

def run(time_t):
	print ("sleep ...%ds"%time_t)
	sleep(time_t)



if __name__ =="__main__":
	thea = []
	for i in range(5):
		tt = Thread(target=run,args=(i,))
		thea.append(tt)

	for i in thea:
		i.start()


