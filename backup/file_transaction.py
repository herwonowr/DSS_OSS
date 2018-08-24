import time,os.path, os,shutil,tkinter.filedialog


def GetFileDate(filename):
	if ".\\" in filename!=True:
		originalname=filename
		filename=filename.strip('.')
		filename=os.getcwd()+filename
	
	if not os.path.exists(filename):		
		print (filename+" dose not exist.")
		return(0)
	
	year=str(time.localtime(os.path.getmtime(filename)).tm_year)

	month=str(time.localtime(os.path.getmtime(filename)).tm_mon)

	day=str(time.localtime(os.path.getmtime(filename)).tm_mday)

	hour=str(time.localtime(os.path.getmtime(filename)).tm_hour)

	minute=str(time.localtime(os.path.getmtime(filename)).tm_min)

	second=str(time.localtime(os.path.getmtime(filename)).tm_sec)

	#print ("File "+ originalname+ " is last modified on "+year+"_"+month+"_"+ day+ "_"+ hour+ "_"+ minute+"_"+ second+ ".")
	
	return(year+"_"+month+"_"+ day+ "_"+ hour+ "_"+ minute)

#print(GetFileDate('.\\DB.csv'))




def BackupFile(filename,homedir,backupdir):
	year=str(time.localtime().tm_year)

	month=str(time.localtime().tm_mon)
	if len(month)==1:
		month="0"+month

	day=str(time.localtime().tm_mday)
	if len(day)==1:
		day="0"+day

	hour=str(time.localtime().tm_hour)
	if len(hour)==1:
		hour="0"+hour

	minute=str(time.localtime().tm_min)
	if len(minute)==1:
		minute="0"+minute

	second=str(time.localtime().tm_sec)
	if len(second)==1:
		second="0"+second
	
	if ".\\" in homedir!=True:
		homedir=homedir.strip('.')
		homedir=os.getcwd()+homedir
	
	sourceFile=os.path.join(homedir,filename)
	
	if not os.path.exists(sourceFile):
		print (sourceFile+" dose not exist.\n")
		return(0)
	
	if ".\\" in backupdir!=True:
		backupdir=backupdir.strip('.')
		backupdir=os.getcwd()+backupdir

	if not os.path.exists(backupdir):
		print (backupdir+" backupdir does not exist. Creating this backup directory...\n")
		os.mkdir(backupdir)
		print ("Backup dirctory created successfully.\n")
	
	name=str(os.path.splitext(filename)[0])

	filetype=str(os.path.splitext(filename)[1])

	newfilename=name+"_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+"_"+second+filetype

	newfilepath=backupdir+'\\'+newfilename
	print("Bacup file location is "+newfilepath)
	shutil.copy(sourceFile,newfilepath)

#Example: BackupFile ('hello_world.py','.\\', '.\\backup')

def RestoreFile(filedir,homedir):
	
	if ".\\" in filedir!=True:
		filedir=filedir.strip('.')
		filedir=os.getcwd()+filedir
	
	if not os.path.exists(filedir):		
		print ("File directory "+ filedir+" dose not exist.")
		return(0)
	
	if ".\\" in homedir!=True:
		homedir=homedir.strip('.')
		homedir=os.getcwd()+homedir
	
	if not os.path.exists(homedir):
		print (homedir+" homedir does not exist. Creating this backup directory...\n")
		os.mkdir(homedir)
		print ("home dirctory created successfully.\n")
	
	fabsname=tkinter.filedialog.askopenfilename(title="Chosse File",initialdir=(os.path.expanduser(filedir)))
	tkinter.Tk().destroy()
	fname=os.path.split(fabsname)[1]
	name=str(os.path.splitext(fname)[0])
	filetype=str(os.path.splitext(fname)[1])
	
	Splitedname=str.split(name,'_')
	for a in range(1,7):
		del Splitedname[-1]
	
	Originalname=''
	for a in Splitedname:
		if a!=Splitedname[-1]:
			Originalname=Originalname+a+'_'
		elif a==Splitedname[-1]:
			Originalname=Originalname+a
	
	newfilename=Originalname+filetype
	newfabsname=homedir+'\\'+newfilename
	print("Backup file is stored at "+newfabsname)
	shutil.copy(fabsname,newfabsname)
	shutil.copy(fabsname,newfabsname)

#RestoreFile(".\\backup",".\\")

def NEW_EMAIL2PEER(PEERINGPOLICY,SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
	for row in PEERINGPOLICY:
		if row['SCENARIO']==SCENARIO:
			SVR_PEER=row['SVR_PEER']
			HUB_PEER=row['HUB_PEER']
			SVR_NODE=row['SVR_NODE']
			HUB_NODE=row['HUB_NODE']
			Tolist=row['EMAIL']
	Subject='New Election Request: '+OP_A+' - '+OP_B
	email_body='''<html><body>
	
		<p style='font-family:Arial;font-size:13;color:black'>
		Dear Colleagues,<br/><br/>
		Greeting from Syniverse!<br/>
		We received a request to establish LTE roaming relationship between OP_A and OP_B.<br/><br/>
		Please let us know if you are interested in open this route via Syniverse.<br/><br/>
		<strong><font color="#0066CC">OP_A<br/></font></strong>
		<Strong>Realm         :</Strong>REALM_A<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_A<br><br/>
		<strong><font color="#0066CC">OP_B<br/></font></strong>
		<strong>Realm         :</Strong>REALM_B<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_B<br/><br/> 
		<strong>Peering Point :</Strong><Strong><font color="green">SVR_PEER<==>HUB_PEER</font></Strong><br/><br/>
		<strong>Syniverse Node:</Strong>SVR_NODE<br/><br/>
		<strong>Peering   Node:</Strong>HUB_NODE<br/><br/>
		B.R.<br/><br/>
		<Strong>Syniverse DSS Team<br/></Strong>
		</p>
		</body></html>'''
	email_body=email_body.replace('OP_A',OP_A)
	email_body=email_body.replace('OP_B',OP_B)
	email_body=email_body.replace('REALM_A',REALM_A)
	email_body=email_body.replace('REALM_B',REALM_B)
	email_body=email_body.replace('IMSI_A',IMSI_A)
	email_body=email_body.replace('IMSI_B',IMSI_B)
	email_body=email_body.replace('SVR_PEER',SVR_PEER)
	email_body=email_body.replace('HUB_PEER',HUB_PEER)
	email_body=email_body.replace('SVR_NODE',SVR_NODE)
	email_body=email_body.replace('HUB_NODE',HUB_NODE)
	sendemail(Tolist,'DSS_Route_Provision@syniverse.com',Subject,email_body)

def PROVISIONED_EMAIL2PEER(PEERINGPOLICY,SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
	for row in PEERINGPOLICY:
		if row['SCENARIO']==SCENARIO:
			SVR_PEER=row['SVR_PEER']
			HUB_PEER=row['HUB_PEER']
			SVR_NODE=row['SVR_NODE']
			HUB_NODE=row['HUB_NODE']
			Tolist=row['EMAIL']
	Subject='Provision complete announcement: '+OP_A+' - '+OP_B
	email_body='''<html><body>
	
		<p style='font-family:Arial;font-size:13;color:black'>
		Dear Colleagues,<br/><br/>
		Greeting from Syniverse!<br/><br/>
		Kindly be informed that we have provisioned the LTE route between OP_A and OP_B<br/><br/>
		<strong><font color="#0066CC">OP_A<br/></font></strong>
		<Strong>Realm         :</Strong>REALM_A<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_A<br><br/>
		<strong><font color="#0066CC">OP_B<br/></font></strong>
		<strong>Realm         :</Strong>REALM_B<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_B<br/><br/> 
		<strong>Peering Point :</Strong><Strong><font color="green">SVR_PEER<==>HUB_PEER</font></Strong><br/><br/>
		<strong>Syniverse Node:</Strong>SVR_NODE<br/><br/>
		<strong>Peering   Node:</Strong>HUB_NODE<br/><br/>
		B.R.<br/><br/>
		<Strong>Syniverse DSS Team<br/></Strong>
		</p>
		</body></html>'''
	email_body=email_body.replace('OP_A',OP_A)
	email_body=email_body.replace('OP_B',OP_B)
	email_body=email_body.replace('REALM_A',REALM_A)
	email_body=email_body.replace('REALM_B',REALM_B)
	email_body=email_body.replace('IMSI_A',IMSI_A)
	email_body=email_body.replace('IMSI_B',IMSI_B)
	email_body=email_body.replace('SVR_PEER',SVR_PEER)
	email_body=email_body.replace('HUB_PEER',HUB_PEER)
	email_body=email_body.replace('SVR_NODE',SVR_NODE)
	email_body=email_body.replace('HUB_NODE',HUB_NODE)
	sendemail(Tolist,'DSS_Route_Provision@syniverse.com',Subject,email_body)
