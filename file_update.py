import tkinter
import tkinter.messagebox
import os
import os.path
import requests
import sys
from requests_ntlm import HttpNtlmAuth
import datetime,time
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

global user
global pwd
user=''
pwd=''

def show_login():

	def login():
		global user
		global pwd
		user=entryName.get()
		pwd=entryPwd.get()
		root.destroy()

	def cancel():
		root.destroy()
		sys.exit()
	root = tkinter.Tk()
	root.title("Enter your gid/pass to update file")
	root.geometry('330x170+500+200')

	labelName = tkinter.Label(root,text='Your Gid:',justify=tkinter.RIGHT,width=100)
	labelName.place(x=40, y=20, width=110, height=20)

	varName = tkinter.StringVar(root, value='')
	entryName = tkinter.Entry(root,width=80,textvariable=varName)
	entryName.place(x=170, y=20, width=100, height=20)

	labelPwd = tkinter.Label(root,text='Your Lan Password:',justify=tkinter.RIGHT,width=100)
	labelPwd.place(x=40, y=55, width=110, height=20)

	varPwd = tkinter.StringVar(root, value='')
	entryPwd = tkinter.Entry(root,show='*',width=80,textvariable=varPwd)
	entryPwd.place(x=170, y=55, width=100, height=20)

	buttonOk = tkinter.Button(root,text='Update File',command=login)
	buttonOk.place(x=80, y=100, width=80, height=20)

	buttonCancel = tkinter.Button(root,text='Cancel',command=cancel)
	buttonCancel.place(x=180, y=100, width=80, height=20)
	
	root.mainloop()
	userinfodirectory=os.getcwd()+r'\file\userinfo.txt'
	output = open(userinfodirectory, 'w')
	output.write(user+' '+pwd)
	output.close()



def fileUpdate(url1,filename1,dirname):

# url replacement
	if url1=='DSSOSS.rar':
		url1='http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/DSSOSS.rar'
	if url1=='PeeringPolicy.csv':
		url1='http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv'
	if url1=='DecideRoutePloicy.csv':
		url1='http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/DecideRoutePloicy.csv'
	
	userinfodirectory=os.getcwd()+r'\file\userinfo.txt'

# if the userinfo.txt exists, if not, write one via show_login()
	if not os.path.exists(userinfodirectory):
		show_login()

# read user and pwd
	input=open(userinfodirectory)
	info=input.read().split(' ')
	input.close()
# decide if the userinfo.txt is empty, if so, write one via show_login()
	if len(info)==1:
		show_login()
		input=open(userinfodirectory)
		info=input.read().split(' ')
	user= info[0]
	pwd=info[1]
	input.close()

# return NTLM authentication result
	try:
		r1=requests.get(url1,auth=HttpNtlmAuth(user,pwd))
	except requests.exceptions.ConnectionError:
		print ('Connection error, URL address not found, please check URL.\n')
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', 'Connection error, URL address not found, please check URL.')
		sys.exit()
	except requests.exceptions.MissingSchema:
		print ('Invalid URL '+url1+' : No schema supplied. Perhaps you meant http://'+ url1+'?\n')
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', 'Invalid URL '+url1+' : No schema supplied. Perhaps you meant http://'+ url1+'?\n')
		sys.exit()
	else:
		res1= r1.status_code


# process different HTTP reponse codes 
	while res1==401:
		
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning','User name or password incorrect.')
		print('User name or password incorrect.')
		root1.destroy()

		show_login()
		input=open(userinfodirectory)
		info=input.read().split(' ')
		user= info[0]
		pwd=info[1]
		input.close()
		#print (user, pwd)
		r1=requests.get(url1,auth=HttpNtlmAuth(user,pwd))
		res1= r1.status_code
	if res1==404:
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning','No file in the URL, please double check URL.')
		print ('No file in the URL, please double check URL.\n\n')
		sys.exit()

		

# process ".\\" directory
	if ".\\" in dirname!=True:
		dirname=dirname.strip('.')
		dirname=os.getcwd()+dirname
		filename1=os.path.join(dirname,filename1)
	#print (filename1)
	file1=os.path.split(filename1)[1]
	file1directory=os.path.split(filename1)[0]

	if not os.path.exists(file1directory):
		print ("The directory of "+file1directory+" dose not exist. Please double check the file directory name.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning',"The directory of " +file1directory+" dose not exist. Please double check the file directory name.")
		sys.exit()

# get url file modification time
	c1=r1.headers
	time1=datetime.datetime.strptime(c1 ['Last-Modified'], GMT_FORMAT)
	timeArray1 = time.strptime(str(time1), "%Y-%m-%d %H:%M:%S")
	url1timestamp = int(time.mktime(timeArray1))
	
	#print ('urltime:')
	#print (url1timestamp)
	


# if the file in target directory does not exit, download file dircetly from url
	if not os.path.exists(filename1):		
		print (file1+" dose not exist. Start downloading "+ file1 +" from provided URL1\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', file1+" dose not exist. Start downloading "+ file1 +" from provided URL.")
		with open(filename1, "wb") as code:
			code.write(r1.content)
		print (file1+" is downloaded successful\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', file1+" is downloaded successful.")
		return (0)


# if file exits, get the local file's modification time
	file1timestamp=int(os.path.getmtime(filename1))

	#print ('file time')
	#print (file1timestamp)


# if local file is older than url file, start updating file
	if file1timestamp > url1timestamp:
		print ("The "+file1 +" in your local directory is the lastest version.\n")

	else:
		print ("A new version of " +file1+" is found. Start downloading the new version of "+ file1 +" from provided URL.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', "A new version of " +file1+" is found. Start downloading the new version of "+ file1 +" from provided URL.")
		with open(filename1, "wb") as code:
			code.write(r1.content)
		print (file1+" is updated successful.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', file1+" is updated successful.")




#fileUpdate ('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','PeeringPolicy.csv','.\\file')
#fileUpdate ('DecideRoutePloicy.csv','DecideRoutePloicy.csv','.\\file')
#fileUpdate ('DSSOSS.rar','DSSOSS.rar','.\\file')

