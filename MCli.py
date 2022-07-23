import requests
import json
import os, fnmatch; os.system("clear")
from multiprocessing import Process, cpu_count, Manager
from collections import defaultdict
from os.path import abspath, dirname
from requests.exceptions import ReadTimeout, Timeout, ConnectionError, ChunkedEncodingError, TooManyRedirects, InvalidURL

columns = defaultdict(list)
txtfiles= []
switch = { "dir": "0" }
playfabapi = "https://20ca2.playfabapi.com/Catalog/GetPublishedItem"
playfab = "20ca2.playfabapi.com"
token = "NHxob1hXTm80ZHVtZXFtNE9OOS9KSmxyTDR3RHZMN0piNTRwMmlKbnVTZlBVPXx7ImkiOiIyMDIyLTA3LTE4VDEyOjIzOjE3LjA3NjI3NDNaIiwiaWRwIjoiQ3VzdG9tIiwiZSI6IjIwMjItMDctMTlUMTI6MjM6MTcuMDc2Mjc0M1oiLCJ0aWQiOiI3OTA0YjIzZGYyN2U0YThhYjU5N2VjN2UxZWYzOTIwMyIsImlkaSI6Ik1DUEY2MTUzMEMzREQyMzg0NzA2Qjk4NTlCODVDREI4NzZCOCIsImgiOiIyNEI5ODFFRjA2RDczMjk5IiwiZWMiOiJtYXN0ZXJfcGxheWVyX2FjY291bnQhQjYzQTA4MDNEMzY1MzY0My82NzhFM0Y1QzZFREZCNDhBLyIsImVpIjoiNjc4RTNGNUM2RURGQjQ4QSIsImV0IjoibWFzdGVyX3BsYXllcl9hY2NvdW50In0="
headers = { "Host": playfab, "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Connection": "Keep-Alive", "Accept-Language": "en-US", "Cache-Control": "public", "Content-Type": "application/json", "User-Agent": "cpprestsdk/2.9.0", "x-entitytoken": token }
expected_response = 200
Resultee=[]
Faily=[]

class colors:
	RED_BG = '\033[41m\033[1m'
	GREEN_BG = '\033[42m'
	ENDC = '\033[m'

def ICustom():
	global UUID
	print("")
	print(colors.RED_BG + " First Use! " + colors.ENDC )
	print("1. Custom Token")
	print("2. Default Token")
	print("")
	ansi=input(" Choose Option : ").lower()
	print("")
	if str(ansi)=="1":
		tokenize=input(" Input your Token : ")
		headers["x-entitytoken"]=f"{tokenize}"
	elif str(ansi)=="2":
		headers["x-entitytoken"]=f"{token}"
	return

def uinput():
	print("")
	print("Scanning Finished!")
	print("1. Go Back to Menu")
	print("2. Scanning Again")
	print("3. Quit Instead")
	print("")
	ans=input("Choose Option: ")
	if ans=="2":
		return
	elif ans=="3":
		exit()
	else:
		Mainlist()

def filet():
	global IDlist, fileselector
	num_file = 1
	print("1. Check Files in Input Folder")
	print("2. Check Files in Current Folder")
	print("q to Quit")
	print("m to Menu")
	print("")
	ans=input(" Choose : ").lower()
	if ans=="1":
		files = os.listdir(hostpath)
		switch["dir"]="0"
	elif ans=="2":
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		switch["dir"]="1"
	elif ans=="q":
		exit()
	elif ans=="m":
		Mainlist()
	else:
		filet()
	print(" [" + colors.RED_BG + " Files Found " + colors.ENDC + "] ")
	for f in files:
		if fnmatch.fnmatch(f, '*.txt'):
			print( str(num_file),str(f))
			num_file=num_file+1
			txtfiles.append(str(f))
	print("")
	print(" M back to Menu ")
	fileselector = input(" Choose Target Files : ")
	if fileselector.isdigit():
		print("")
		print(" Target Chosen : " + colors.RED_BG + " "+txtfiles[int(fileselector)-1]+" "+colors.ENDC)
		direct = str(switch["dir"])
		if direct == "0":
			file_hosts = str(hostpath) +"/"+ str(txtfiles[int(fileselector)-1])
		else:
			file_hosts = str(txtfiles[int(fileselector)-1])
	else:
		Mainlist()

	with open(file_hosts) as f:
		parseddom = f.read().split()
	IDlist = list(set(parseddom))
	IDlist = list(filter(None, parseddom))
	print(" Total of Domains Loaded: " + colors.RED_BG + " " +str(len(IDlist)) + " "+colors.ENDC )
	print("")
	return

def executor():
	with Manager() as manager:
		global Resultee, Faily
		num_cpus = cpu_count()
		processes = []
		Resultee = manager.list()
		Faily = manager.list()
		for process_num in range(num_cpus):
			section = IDlist[process_num::num_cpus]
			p = Process(target=MCli, args=(section,))
			p.start()
			processes.append(p)
		for p in processes:
			p.join()
		Resultee = list(Resultee)
		Faily = list(Faily)
		print("")
		print(" Failed Result : "  + colors.RED_BG + " "+str(len(Faily)) +" "+ colors.ENDC )
		print(" Successfull Result : " + colors.GREEN_BG + " "+str(len(Resultee))+ " "+colors.ENDC)

def MCli(IDlist):
	for UUID in IDlist:
		try:
			r = requests.post(playfabapi, headers=headers, json={"ItemId":UUID}, allow_redirects=False)
			if r.status_code == expected_response:
				print(" ["+colors.GREEN_BG+" HIT "+colors.ENDC+"] " + UUID)
				print(UUID, file=open(f"output/success.txt", "a"))
				with open(f'output/{UUID}.json', 'w') as f:
					json.dump(r.json(), f, indent = 4)
				r = response.json()["data"]["Item"]["Contents"]
				for i in r:
					print(i["Url"], file=open(f"output/success-url.txt", "a"))
				Resultee.append(str(UUID))
			elif r.status_code != expected_response:
				print(" ["+colors.RED_BG+" FAIL "+colors.ENDC+"] " + UUID + " [" +colors.RED_BG+" " + str(r.status_code) + " "+colors.ENDC+"]")
				print(UUID, file=open(f"output/failed.txt", "a"))
				Faily.append(str(UUID))
		except (Timeout, ReadTimeout, ConnectionError):
			print(" ["+colors.RED_BG+" FAIL "+colors.ENDC+"] " + UUID + " [" + colors.RED_BG +" TIMEOUT "+colors.ENDC+"]")
			print(UUID, file=open(f"output/failed.txt", "a"))
			Faily.append(str(UUID))
			pass
		except(ChunkedEncodingError):
			print(" ["+colors.RED_BG+" FAIL "+colors.ENDC+"] " + UUID + " [" + colors.RED_BG+" Invalid Length "+colors.ENDC + "]")
			print(UUID, file=open(f"output/failed.txt", "a"))
			Faily.append(str(UUID))
			pass
		except(TooManyRedirects):
			print(" ["+colors.RED_BG+" FAIL "+colors.ENDC+"] " + UUID + " [" +colors.RED_BG+" Redirects Loop "+colors.ENDC+"]")
			print(UUID, file=open(f"output/failed.txt", "a"))
			Faily.append(str(UUID))
			pass
		except(InvalidURL):
			print(" ["+colors.RED_BG+" FAIL "+colors.ENDC+"] " + UUID + " [" +colors.RED_BG+" Invalid URL "+colors.ENDC+"]")
			print(UUID, file=open(f"output/failed.txt", "a"))
			Faily.append(str(UUID))
			pass

def Mainlist():
	print('''
      ___     
     /  /\    
    /  /:/    
   /  /:/     
  /  /:/  ___ 
 /__/:/  /  /\
 \  \:\ /  /:/
  \  \:\  /:/ 
   \  \:\/:/  
    \  \::/   
     \__\/

	''')
	print("    [" + colors.RED_BG + " MarketPlace : Extractor " + colors.ENDC + "]")
	print("     ["+colors.RED_BG+" Author " + colors.ENDC + ":" + colors.GREEN_BG + " Kiynox " + colors.ENDC + "]")
	print("")

	print("1. Marketplace Metadata")
	print("2. Marketplace Downloader")
	print("3. Marketplace Decryptor")
	print("Q to Quit")
	print("")
	ans=input(" Choose Option: ").lower()
	print("")
	if str(ans)=="1":
		ICustom()
		filet()
		executor()
		uinput()
	elif str(ans)=="2":
		downloader()
	elif str(ans)=="3":
		decryptod()
	else:
		exit()

if __name__ == '__main__':
	os.chdir(dirname(abspath(__file__)))
	if not os.path.exists("input"):
		os.makedirs("input")
	if not os.path.exists("output"):
		os.makedirs("output")
	if not os.path.exists("output/metadata"):
		os.makedirs("output/metadata")
	Mainlist()
    