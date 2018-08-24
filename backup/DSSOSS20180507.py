
# coding=gbk
import csv
import os, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QComboBox,QPushButton
from PyQt5 import QtCore
from Initalize20180424 import *
from soap_all_commands_for_dsc import *
from file_transaction import *
from SendEmail import *

import os
if not os.path.exists(r'.\\file\DB.csv'):
	INITIALIZE_DB()

PEERINGPOLICY=csv2dict('.\\file\PeeringPolicy.csv')
DECIDEROUTEPOLICY=csv2dict('.\\file\DecideRoutePloicy.csv')
#the following 2 variant is used in sync OPA OPB from Open Route to OP ONLINE
global OPAAA
OPAAA=''
global OPBBB
OPBBB=''
global List_Add_Route_Local
List_Add_Route_Local=[]

def refresh_all():
	INITIALIZE_DB()
	PEERINGPOLICY=csv2dict('.\\file\PeeringPolicy.csv')
	DECIDEROUTEPOLICY=csv2dict('.\\file\DecideRoutePloicy.csv')
	DB_sheet = csv2dict(".\\file\DB.csv")

def NEW_EMAIL2PEER(SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
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

def PROVISIONED_EMAIL2PEER(SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
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
	
def ONLINE_EMAIL(OP,BODY):
	Tolist='DSS_Route_Provision@syniverse.com'
	Subject='New OP online on DSC completed : '+OP
	email_body=BODY
	sende_plain_mail(Tolist,'',Subject,email_body)
	
def BACKUP_DB():
	file_list=['DB.csv','AMS_LISTCACHE.csv','FRT_LISTCACHE.csv','CHI_LISTCACHE.csv','DAL_LISTCACHE.csv','HKG_LISTCACHE.csv','SNG_LISTCACHE.csv']
	for file in file_list:
		#BackupFile ('hello_world.py','.\\', '.\\backup')
		BackupFile(file,'.\\file\\', '.\\backup')
	
#Read DB from CSV file and initialize variable
def csv2dict(filename):
	new_dict = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		fieldnames = next(reader)
		reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
		new_dict = [row for row in reader]
	return new_dict

DB_sheet = csv2dict(".\\file\DB.csv")

DRAlist=['HKG','AMS','CHI','SNG','FRT','DAL']
RegionList=['AP','EU','NA']
Local_DSC_List=[]
global SURL1,SURL2,DSC1,DSC2
#This function split strings seperates by ; or , to a LIST and strip spaces in each string
def SPLIT2LIST(items):
	LIST=[]
	items = items.lower()
	items = items.replace(",",";")
	temp =  items.split(";")
	for item in temp:
		LIST.append(item.strip())
	return(LIST)
	
def JOIN_STR(current,new,symble):
	if current=='' and new=='':
		return('')
	if current=='' and new!='':
		return(new)
	if current!='' and new=='':
		return(current)

	string=current+symble+new
	return(string)
	


	


#根据region设置全局共享变量SURL1,SURL2,DSC1,DSC2
def Region2URL_DSC(Region):
		global SURL1,SURL2,DSC1,DSC2,POP
		if Region =="AP":
			SURL1="http://10.162.28.186:8080/DSC_SOAP/query?"
			SURL2="http://10.163.28.131:8080/DSC_SOAP/query?"
			DSC1="HKG"
			DSC2="SNG"
			POP="AP PoP"
		if Region =="EU":
			SURL1="http://10.160.28.32:8080/DSC_SOAP/query?"
			SURL2="http://10.161.28.32:8080/DSC_SOAP/query?"
			DSC1="AMS"
			DSC2="FRT"
			POP="EU PoP"		
		if Region =="NA":
			SURL1="http://10.166.28.200:8080/DSC_SOAP/query?"
			SURL2="http://10.164.28.189:8080/DSC_SOAP/query?"
			DSC1="CHI"
			DSC2="DAL"
			POP="NA PoP"

#DSC OUTPUT 弹窗代码
def MESSAGE_OUTPUT(Title,Output_Text):
	dialog=QDialog()
	dialog.resize(400,100)
	MSG = QLabel(Output_Text,dialog)
	MSG.move(50,20)

	dialog.setWindowTitle(Title)
	dialog.setWindowModality(Qt.ApplicationModal)
	dialog.exec_()
	
def BIOUTPUT(Title,Outputlist_1,Outputlist_2):
		dialog=QDialog()
		dialog.resize(1250,600)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,20)
		DSC_2 = QLabel(DSC2,dialog)
		DSC_2.move(650,20)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,50)
		OUTPUT_1.resize(550,500)
		
		OUTPUT_2 = QTextEdit(dialog)
		for row in Outputlist_2:
			OUTPUT_2.append(row)
		OUTPUT_2.move(650,50)
		OUTPUT_2.resize(550,500)

		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
def BIOUTPUT_UPDOWN(Title,Outputlist_1,Outputlist_2):
		dialog=QDialog()
		dialog.resize(1366,740)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,15)
		DSC_2 = QLabel(DSC2,dialog)
		DSC_2.move(50,350)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,30)
		OUTPUT_1.resize(1300,300)
		
		OUTPUT_2 = QTextEdit(dialog)
		for row in Outputlist_2:
			OUTPUT_2.append(row)
		OUTPUT_2.move(50,370)
		OUTPUT_2.resize(1300,300)

		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
def SINGLE_OUTPUT(Title,Outputlist_1):
		dialog=QDialog()
		dialog.resize(1366,768)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,20)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,50)
		OUTPUT_1.resize(1360,750)
		
		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
#DSC 组合命令功能执行代码
def Reload_Region_LIST(region):
	Region2URL_DSC(region)
	Outputlist_1=[]
	Outputlist_2=[]	
	Output1=soap_reload_listcaches(SURL1)
	Output2=soap_reload_listcaches(SURL2)
	Outputlist_1.append(Output1)
	Outputlist_2.append(Output2)
	BIOUTPUT("Reload ListCaches",Outputlist_1,Outputlist_2)

def Reload_Region_RULE(region):
	Region2URL_DSC(region)
	Outputlist_1=[]
	Outputlist_2=[]
	Output1=soap_reload_rule_engine(SURL1)
	Output2=soap_reload_rule_engine(SURL2)
	Outputlist_1.append(Output1)
	Outputlist_2.append(Output2)
	BIOUTPUT("Reload Rule Engine",Outputlist_1,Outputlist_2)
	
def CHECK_DECIDE_ROUTE2OP(region,source_realms,dest_realms):
	Region2URL_DSC(region)
	source_realm_list = []
	dest_realm_list = []
	source_realm_list.insert(0,'*')
	Outputlist_1=[]
	Outputlist_2=[]
	source_realm_list = SPLIT2LIST(source_realms)
	source_realm_list.insert(0,'*')
	dest_realm_list = SPLIT2LIST(dest_realms)
	
	for source_realm in source_realm_list:
		for dest_realm in dest_realm_list:
			
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			for Output in Output1:
				Outputlist_1.append(source_realm+"->"+dest_realm)
				if Output==None:
					Output="None"
				Outputlist_1.append(Output)
				
			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			for Output in Output2:
				Outputlist_2.append(source_realm+"->"+dest_realm)
				if Output==None:
					Output="None"
				Outputlist_2.append(Output)
			#@将来写成HTML代码带颜色
	BIOUTPUT_UPDOWN("Check Decide Route:*->OP and Source->OP",Outputlist_1,Outputlist_2)
	
#add realms to list on regional DSCs and sent output to popup window
def ADD_REALMS2LIST(Region,Realms,LIST_Name):
	if Region=='':
		MESSAGE_OUTPUT("Error","Empty Region")
	elif Realms=='':
		MESSAGE_OUTPUT("Error","Empty Realm")
	elif LIST_Name=='':
		MESSAGE_OUTPUT("Error","Empty LIST")
	else:	
		Region2URL_DSC(Region)
		Outputlist_1=[]
		Outputlist_2=[]
		Realm_LIST=[]
		Realms = Realms.lower()
		Realms = Realms.replace(",",";")
		temp =  Realms.split(";")
		for realm in temp:
			Realm_LIST.append(realm.strip())
		
		for realm in Realm_LIST:
			response=soap_add_list_cache(LIST_Name,realm,SURL1)
			response="#"+realm+"->"+LIST_Name+'\n#'+response
			Outputlist_1.append(response)
			
			response=soap_add_list_cache(LIST_Name,realm,SURL2)
			response="#"+realm+"->"+LIST_Name+'\n#'+response
			Outputlist_2.append(response)
			
		BIOUTPUT('Add ListCache',Outputlist_1,Outputlist_2)
		
def K2R(Region,Realms2,List1,Realms1,Name1,Name2):
	REALMLIST1=SPLIT2LIST(Realms1)
	REALMLIST2=SPLIT2LIST(Realms2)
	suffix='.key2roam.comfone.com'
	if Region=='':
		MESSAGE_OUTPUT("Error","Empty Region")
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Realms2")
	if List1=='':
		MESSAGE_OUTPUT("Error","Empty List1")
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Name1")
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Name2")
	Region2URL_DSC(Region)
	Outputlist_1=[]
	Outputlist_2=[]
	
	if Region =='NA':
		print("na selected")
		#Verison K2R route on NA DSC
		if Name1 =='Verizon Wireless' or Name2 =='Verizon Wireless':
			if Name1 =='Verizon Wireless':
				Realms = SPLIT2LIST(Realms2)
			if Name2 =='Verizon Wireless':
				Realms = SPLIT2LIST(Realms1)
			for realm in Realms:
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL1)
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_1.append(response)
				
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL2)
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_2.append(response)
				
			BIOUTPUT('Add ListCache LIST_VERIZON_WIRELESS_K2R_RP_REALM',Outputlist_1,Outputlist_2)
		else:
			#NA none Vzw K2R create RF for all realms
			for realm1 in REALMLIST1:
				for realm2 in REALMLIST2:
					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2+suffix)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
					Outputlist_1.append(response)

			for realm2 in REALMLIST2:
				for realm1 in REALMLIST1:
					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1+suffix)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
					Outputlist_1.append(response)					

			for realm1 in REALMLIST1:
				for realm2 in REALMLIST2:
					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
					Outputlist_2.append(response)

					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2+suffix)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
					Outputlist_2.append(response)

			for realm2 in REALMLIST2:
				for realm1 in REALMLIST1:
					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
					Outputlist_2.append(response)

					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1+suffix)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
					Outputlist_2.append(response)
					
			BIOUTPUT('Add K2R Filter on NA DSC',Outputlist_1,Outputlist_2)

	elif Region == 'AP' or Region == 'EU':
		KKK=''
		for realm in REALMLIST2:
			KKK=KKK+realm+','+realm+suffix+','
		KKK=KKK[:-1]
		ADD_REALMS2LIST(Region,KKK,List1)		
				

#soap_check_decide_route(dsc_url,source_host,source_realm,dest_host,dest_realm,adjacent_source_peer,adjacent_source_realm)
		


#open route window layout


		
class OPEN_ROUTE(QWidget):
	signal_opa_change = QtCore.pyqtSignal(str)
	
	
	def __init__(self,parent=None):
		super(OPEN_ROUTE,self).__init__(parent)
			
		self.Full_list=['']
		for row in DB_sheet:
			self.Full_list.append(row["name"])
			
		self.resize(1000,800)
		QE_length = 400
		QE_hight = 20
		Y_start = 40
		Y_step = 30
		X10 =1080
		X11 = 1160
		X12 = 1240
		X13 = 1240


#COMMAND BUTTONS ON RIGHT		
#DB BUTTON
		Y_start=70	
		self.Lable_DB_DATE = QLabel("DB_Date",self)
		self.Lable_DB_DATE .move (X10,Y_start-Y_step*1)		
		self.DB_DATE = QLineEdit(self)
		self.DB_DATE.setText(GetFileDate('.\\file\DB.csv'))
		self.DB_DATE.setGeometry(QtCore.QRect(X11, Y_start-Y_step*1, QE_length/3.9, QE_hight))
		
		self.UPD_DB = QPushButton('UPD_DB',self)
		self.UPD_DB.move(X10,Y_start+Y_step*0)
		self.UPD_DB.clicked.connect(lambda:refresh_all())
		#需要研究如何在INITIALIZE DB完成后刷新DB_DATE
		
		self.UPD_DB = QPushButton('BACKUP_DB',self)
		self.UPD_DB.move(X11,Y_start+Y_step*0)
		self.UPD_DB.clicked.connect(lambda:BACKUP_DB())
		
		self.UPD_DB = QPushButton('Restore_DB',self)
		self.UPD_DB.move(X12,Y_start+Y_step*0)
		self.UPD_DB.clicked.connect(lambda:RestoreFile(".\\backup",".\\file"))
#RULE ENGINE BUTTON		
		#self.Lable_DB_DATE = QLabel("RULE_Date",self)
		#self.Lable_DB_DATE .move (X10,Y_start+Y_step*1)		
		#self.DB_DATE = QLineEdit(self)
		#self.DB_DATE.setGeometry(QtCore.QRect(X11, Y_start+Y_step*1, QE_length/3.9, QE_hight))
		
		#self.UPD_DB = QPushButton('UPD_RULE',self)
		#self.UPD_DB.move(X10,Y_start+Y_step*2)
		#self.UPD_DB.clicked.connect(self.UPDATE_RULE)
		
		#self.UPD_DB = QPushButton('BACKUP_RULE',self)
		#self.UPD_DB.move(X11,Y_start+Y_step*2)
		#self.UPD_DB.clicked.connect(self.UPDATE_DB)
		
		#self.UPD_DB = QPushButton('Restore_RULE',self)
		#self.UPD_DB.move(X12,Y_start+Y_step*2)
		#self.UPD_DB.clicked.connect(lambda:RestoreFile(".\\backup",".\\"))
#RELOAD BUTTON

		self.Lable_DB_DATE = QLabel("Reload ListCaches",self)
		self.Lable_DB_DATE .move (X10,Y_start+Y_step*4)	
		self.Lable_DB_DATE = QLabel("Reload Rule",self)
		self.Lable_DB_DATE .move (X13,Y_start+Y_step*4)	
					
		self.Re_AP_LIST = QPushButton('Re_AP_LIST',self)
		self.Re_AP_LIST.move(X10,Y_start+Y_step*5)
		self.Re_AP_LIST.clicked.connect(lambda: Reload_Region_LIST("AP"))
		
		self.Re_EU_LIST = QPushButton('Re_EU_LIST',self)
		self.Re_EU_LIST.move(X10,Y_start+Y_step*6)
		self.Re_EU_LIST.clicked.connect(lambda: Reload_Region_LIST("EU"))
		
		self.Re_NA_LIST = QPushButton('Re_NA_LIST',self)
		self.Re_NA_LIST.move(X10,Y_start+Y_step*7)
		self.Re_NA_LIST.clicked.connect(lambda: Reload_Region_LIST("NA"))
		
		self.Re_AP_RULE = QPushButton('Re_AP_RULE',self)
		self.Re_AP_RULE.move(X13,Y_start+Y_step*5)
		self.Re_AP_RULE.clicked.connect(lambda: Reload_Region_RULE("AP"))
		
		self.Re_EU_RULE = QPushButton('Re_EU_RULE',self)
		self.Re_EU_RULE.move(X13,Y_start+Y_step*6)
		self.Re_EU_RULE.clicked.connect(lambda: Reload_Region_RULE("EU"))
		
		self.Re_NA_RULE = QPushButton('Re_NA_RULE',self)
		self.Re_NA_RULE.move(X13,Y_start+Y_step*7)
		self.Re_NA_RULE.clicked.connect(lambda: Reload_Region_RULE("NA"))

#send email
		
		self.Lable_DB_DATE = QLabel("Send Email to Peer",self)
		self.Lable_DB_DATE .move (X10,Y_start+Y_step*9+10)	

		self.New_Election = QPushButton('New_Election',self)
		self.New_Election.move(X10,Y_start+Y_step*10)
		self.New_Election.clicked.connect(lambda: NEW_EMAIL2PEER(self.Combo_SCENARIO.currentText(),self.OP_A.text(),self.realm_A.text(),self.IMSI_A.text(),self.OP_B.text(),self.realm_B.text(),self.IMSI_B.text()))
		
		self.Provisoned = QPushButton('Provisoned',self)
		self.Provisoned.move(X10,Y_start+Y_step*11)
		self.Provisoned.clicked.connect(lambda: PROVISIONED_EMAIL2PEER(self.Combo_SCENARIO.currentText(),self.OP_A.text(),self.realm_A.text(),self.IMSI_A.text(),self.OP_B.text(),self.realm_B.text(),self.IMSI_B.text()))

		SCENARIO=[]
		for row in PEERINGPOLICY:
			SCENARIO.append(row['SCENARIO'])
			
		self.Combo_SCENARIO = QComboBox(self)
		for i in SCENARIO:
			self.Combo_SCENARIO.addItem(i)
		self.Combo_SCENARIO.move(X11,Y_start+Y_step*10)
		self.Combo_SCENARIO.setMaxVisibleItems (10)
		self.Combo_SCENARIO.currentIndexChanged.connect(self.update_POLICY)
		
		self.POLICY = QLineEdit('POLICY',self)
		self.POLICY.setGeometry(QtCore.QRect(X11, Y_start+Y_step*11, 175, QE_hight))


## OPA and OPB
		Y_start=40	
## code for OPA only start
		X1 = 10 #label1 start
		X2 = 100#text1 start
		X3 = 200#labe2 start
		X4 = 250#text2 start
		X5 = 320#button3 start

		self.Lable_TADIG_A = QLabel("TADIG_A",self)
		self.Lable_TADIG_A.move (X4,Y_start-Y_step*1)		
		self.TADIG_A = QLineEdit(self)
		self.TADIG_A.setText("")
		self.TADIG_A.setGeometry(QtCore.QRect(X5, Y_start-Y_step*1, QE_length/2.2, QE_hight))
		
		self.Lable_SSID_A = QLabel("SSID_A",self)
		self.Lable_SSID_A.move (X1,Y_start-Y_step)		
		self.SSID_A = QLineEdit(self)
		self.SSID_A.setText("")
		self.SSID_A.setGeometry(QtCore.QRect(X2, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_A = QLabel("OP_A",self)
		self.Lable_OP_A.move (X1,Y_start)		
		self.OP_A = QLineEdit(self)
		self.OP_A.setText("")
		self.OP_A.setGeometry(QtCore.QRect(X2, Y_start, QE_length, QE_hight))
		
		self.Lable_Country_A = QLabel("Country_A",self)
		self.Lable_Country_A.move (X1,Y_start+Y_step*2)		
		self.Country_A = QLineEdit(self)
		self.Country_A.setText("")
		self.Country_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_Realm_A = QLabel("Realm_A",self)
		self.Lable_Realm_A.move (X1,Y_start+Y_step*3)				
		self.realm_A = QLineEdit(self)
		self.realm_A.setText("")
		self.realm_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*3, QE_length, QE_hight))

		self.Lable_IMSI_A = QLabel("IMSI_A",self)
		self.Lable_IMSI_A.move (X1,Y_start+Y_step*4)				
		self.IMSI_A = QLineEdit(self)
		self.IMSI_A.setText("")
		self.IMSI_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*4, QE_length, QE_hight))
		
		self.Lable_LIST_A = QLabel("LIST_A",self)
		self.Lable_LIST_A.move(X1,Y_start+Y_step*5)		
		self.LIST_A = QLineEdit(self)
		self.LIST_A.setText("")
		self.LIST_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*5, QE_length, QE_hight))
		
		self.Label_Owner_A = QLabel("Owner_A",self)
		self.Label_Owner_A.move(X1,Y_start+Y_step*6)		
		self.Owner_A = QLineEdit(self)
		self.Owner_A.setText("")
		self.Owner_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*6, QE_length/3, QE_hight))
		
		self.Label_RMT_A = QLabel("RMT_A",self)
		self.Label_RMT_A.move(X4,Y_start+Y_step*6)		
		self.RMT_A = QLineEdit(self)
		self.RMT_A.setText("")
		self.RMT_A.setGeometry(QtCore.QRect(X5,Y_start+Y_step*6, QE_length/2.2, QE_hight))
		
		self.Lable_DRA_A = QLabel("DRA_A",self)
		self.Lable_DRA_A.move(X1,Y_start+Y_step*7)		
		self.DRA_A = QLineEdit(self)
		self.DRA_A.setText("")
		self.DRA_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*7, QE_length, QE_hight))		
		
		self.Lable_HUB_PLOICY_A = QLabel("HUB_POLICY_A",self)
		self.Lable_HUB_PLOICY_A.move(X1,Y_start+Y_step*8)		
		self.HUB_PLOICY_A = QTextEdit(self)
		self.HUB_PLOICY_A.setText("")
		self.HUB_PLOICY_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*8, QE_length, QE_hight*4))
		
		self.Lable_TECH_COMMENT_A = QLabel("TECH_COMMENT_A",self)
		self.Lable_TECH_COMMENT_A.move(X1,Y_start+Y_step*11)		
		self.TECH_COMMENT_A = QTextEdit(self)
		self.TECH_COMMENT_A.LineWrapMode
		self.TECH_COMMENT_A.setText("")
		self.TECH_COMMENT_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*11, QE_length, QE_hight*11))				

#BUILD COMBO LIST_A WITH DROP DOWN SELECTION
		Combo_LIST_A=self.Full_list
		self.Combo_Select_A = QComboBox(self)
		for i in Combo_LIST_A:
			self.Combo_Select_A.addItem(i)
		self.Combo_Select_A.move(X2,Y_start+Y_step*1)
		self.Combo_Select_A.setMaxVisibleItems (10)
		self.Combo_Select_A.currentIndexChanged.connect(self.update_A)
		#self.connect(self.btn,SIGNAL('clicked()'),self,SLOT('myfunc()'))
		#self.Combo_Select_A.currentIndexChanged.connect(self.sync_op)
		#self.connect(self.Combo_Select,SIGNAL('currentIndexChanged()'),self,SLOT,('sync_op'))
		self.OP_A.returnPressed.connect(self.rebuild_A_list)

#Add LISTCACHE FUNCTION_A
		self.Combo_Region_A = QComboBox(self)
		for i in RegionList:
			self.Combo_Region_A.addItem(i)
		
		self.Combo_Region_A.move(X2,Y_start+Y_step*19)
		self.Combo_Region_A.setMaxVisibleItems (4)
		self.Lable_Region_A = QLabel("Normal Route",self)
		self.Lable_Region_A.move(X1,Y_start+Y_step*19)		

		self.B_Reams2A_LIST = QPushButton('B_Realms2A_List',self)
		self.B_Reams2A_LIST.move(X3,Y_start+Y_step*19)
		self.B_Reams2A_LIST.clicked.connect(lambda: ADD_REALMS2LIST(self.Combo_Region_A.currentText(),self.realm_B.displayText(),self.LIST_A.displayText()))

#Check DECIDE ROUTE	FUNCTION_A
		self.Check_TO_A_Route = QPushButton('Check to A route',self)
		self.Check_TO_A_Route.move(X5,Y_start+Y_step*19)
		self.Check_TO_A_Route.clicked.connect(lambda: CHECK_DECIDE_ROUTE2OP(self.Combo_Region_A.currentText(),self.realm_B.displayText(),self.realm_A.displayText()))
		
		
#Add K2R FUNCTION_A
		self.Lable_Region_K2R_A = QLabel("K2R Route",self)
		self.Lable_Region_K2R_A.move(X1,Y_start+Y_step*20)		

		self.K2R_B_Reams2A_LIST = QPushButton('K2R_B_Realms2A_List/ADD RequestFilter/UPD vzw LIST',self)
		self.K2R_B_Reams2A_LIST.move(X3,Y_start+Y_step*20)
		#PARA:REGION A, REALMs B, LIST A, REALMs A, Name A, Name B
		self.K2R_B_Reams2A_LIST.clicked.connect(lambda: K2R(self.Combo_Region_A.currentText(),self.realm_B.displayText(),self.LIST_A.displayText(),self.realm_A.displayText(),self.OP_A.displayText(),self.OP_B.displayText()))

		

## code for OPB only start
		distance=550
		X1 = distance+X1 #label1 start
		X2 = distance+X2#text1 start
		X3 = distance+X3#labe2 start
		X4 = distance+X4#text2 start
		X5 = distance+X5#button3 start

		self.Lable_TADIG_B = QLabel("TADIG_B",self)
		self.Lable_TADIG_B.move (X4,Y_start-Y_step*1)		
		self.TADIG_B = QLineEdit(self)
		self.TADIG_B.setText("")
		self.TADIG_B.setGeometry(QtCore.QRect(X5, Y_start-Y_step*1, QE_length/2.2, QE_hight))
		
		self.Lable_SSID_B = QLabel("SSID_B",self)
		self.Lable_SSID_B.move (X1,Y_start-Y_step)		
		self.SSID_B = QLineEdit(self)
		self.SSID_B.setText("")
		self.SSID_B.setGeometry(QtCore.QRect(X2, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_B = QLabel("OP_B",self)
		self.Lable_OP_B.move (X1,Y_start)		
		self.OP_B = QLineEdit(self)
		self.OP_B.setText("")
		self.OP_B.setGeometry(QtCore.QRect(X2, Y_start, QE_length, QE_hight))
		
		self.Lable_Country_B = QLabel("Country_B",self)
		self.Lable_Country_B.move (X1,Y_start+Y_step*2)		
		self.Country_B = QLineEdit(self)
		self.Country_B.setText("")
		self.Country_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_Realm_B = QLabel("Realm_B",self)
		self.Lable_Realm_B.move (X1,Y_start+Y_step*3)				
		self.realm_B = QLineEdit(self)
		self.realm_B.setText("")
		self.realm_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*3, QE_length, QE_hight))

		self.Lable_IMSI_B = QLabel("IMSI_B",self)
		self.Lable_IMSI_B.move (X1,Y_start+Y_step*4)				
		self.IMSI_B = QLineEdit(self)
		self.IMSI_B.setText("")
		self.IMSI_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*4, QE_length, QE_hight))
		
		self.Lable_LIST_B = QLabel("LIST_B",self)
		self.Lable_LIST_B.move(X1,Y_start+Y_step*5)		
		self.LIST_B = QLineEdit(self)
		self.LIST_B.setText("")
		self.LIST_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*5, QE_length, QE_hight))
		
		self.Owner_B = QLabel("Owner_B",self)
		self.Owner_B.move(X1,Y_start+Y_step*6)		
		self.Owner_B = QLineEdit(self)
		self.Owner_B.setText("owner B")
		self.Owner_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*6, QE_length/3, QE_hight))
		
		self.Label_RMT_B = QLabel("RMT_B",self)
		self.Label_RMT_B.move(X4,Y_start+Y_step*6)		
		self.RMT_B = QLineEdit(self)
		self.RMT_B.setText("RMT B")
		self.RMT_B.setGeometry(QtCore.QRect(X5,Y_start+Y_step*6, QE_length/2.2, QE_hight))
		
		self.Lable_DRA_B = QLabel("DRA_B",self)
		self.Lable_DRA_B.move(X1,Y_start+Y_step*7)		
		self.DRA_B = QLineEdit(self)
		self.DRA_B.setText("")
		self.DRA_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*7, QE_length, QE_hight))		
		
		#self.Lable_HUB_B = QLabel("HUB_B",self)
		#self.Lable_HUB_B.move(X1,Y_start+Y_step*8)		
		#self.HUB_B = QLineEdit(self)
		#self.HUB_B.setText("")
		#self.HUB_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*8, QE_length, QE_hight))
		
		self.Lable_HUB_PLOICY_B = QLabel("HUB_POLICY_B",self)
		self.Lable_HUB_PLOICY_B.move(X1,Y_start+Y_step*8)		
		self.HUB_PLOICY_B = QTextEdit(self)
		self.HUB_PLOICY_B.setText("")
		self.HUB_PLOICY_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*8, QE_length, QE_hight*4))
		
		self.Lable_TECH_COMMENT_B = QLabel("TECH_COMMENT_B",self)
		self.Lable_TECH_COMMENT_B.move(X1,Y_start+Y_step*11)		
		self.TECH_COMMENT_B = QTextEdit(self)
		self.TECH_COMMENT_B.LineWrapMode
		self.TECH_COMMENT_B.setText("")
		self.TECH_COMMENT_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*11, QE_length, QE_hight*11))				

#COMBO LIST_B WITH DROP DOWN SELECTION
		Combo_LIST_B=self.Full_list
		self.Combo_Select_B = QComboBox(self)
		for i in Combo_LIST_B:
			self.Combo_Select_B.addItem(i)
		self.Combo_Select_B.move(X2,Y_start+Y_step*1)
		self.Combo_Select_B.setMaxVisibleItems (10)
		self.Combo_Select_B.currentIndexChanged.connect(self.update_B)
		self.OP_B.returnPressed.connect(self.rebuild_B_list)

#Add LISTCACHE FUNCTION_B
		self.Combo_Region_B = QComboBox(self)
		for i in RegionList:
			self.Combo_Region_B.addItem(i)
		
		self.Combo_Region_B.move(X2,Y_start+Y_step*19)
		self.Combo_Region_B.setMaxVisibleItems (4)
		self.Lable_Region_B = QLabel("Normal Route",self)
		self.Lable_Region_B.move(X1,Y_start+Y_step*19)		

		self.A_Reams2B_LIST = QPushButton('A_Realms2B_List',self)
		self.A_Reams2B_LIST.move(X3,Y_start+Y_step*19)
		self.A_Reams2B_LIST.clicked.connect(lambda: ADD_REALMS2LIST(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.LIST_B.displayText()))
		
#Check DECIDE ROUTE	FUNCTION_B
		self.Check_TO_B_Route = QPushButton('Check to B route',self)
		self.Check_TO_B_Route.move(X5,Y_start+Y_step*19)
		self.Check_TO_B_Route.clicked.connect(lambda: CHECK_DECIDE_ROUTE2OP(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.realm_B.displayText()))
		
#Add K2R FUNCTION_B
		self.Lable_Region_K2R_B = QLabel("K2R Route",self)
		self.Lable_Region_K2R_B.move(X1,Y_start+Y_step*20)		

		self.K2R_A_Reams2B_LIST = QPushButton('K2R_A_Realms2B_List/ADD RequestFilter/UPD vzw LIST',self)
		self.K2R_A_Reams2B_LIST.move(X3,Y_start+Y_step*20)
		self.K2R_A_Reams2B_LIST.clicked.connect(lambda: K2R(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.LIST_B.displayText(),self.realm_B.displayText(),self.OP_B.displayText(),self.OP_A.displayText()))

		
	def update_POLICY(self):
		#PEERINGPOLICY=csv2dict('PeeringPolicy.csv')
		for row in PEERINGPOLICY:
			if row['SCENARIO']==self.Combo_SCENARIO.currentText():
				self.POLICY.setText(row['SVR_PEER']+'-'+row['HUB_PEER'])
			

	def update_A(self,ii):
		OPA_Name = self.Combo_Select_A.currentText()
		self.OP_A.setText(OPA_Name)
		global OPAAA
		OPAAA=OPA_Name
		for row in DB_sheet:
			if row["name"] == OPA_Name:
				self.SSID_A.setText(row["ssid"])
				self.IMSI_A.setText(row["imsi_prefix"])
				self.Country_A.setText(row["country"])
				self.realm_A.setText(row["realm_name"])
				self.LIST_A.setText(row["LIST"])
				self.Owner_A.setText(row["owner"])
				self.RMT_A.setText(row["status"])
				self.DRA_A.setText(row["dra"])
				self.HUB_PLOICY_A.setText(row["hub_policy"])
				self.TECH_COMMENT_A.setText(row["technicalcomment"])
				self.TADIG_A.setText(row["tagid"])
				self.Combo_Region_A.currentIndex=1
				
	def update_B(self,ii):
		OPB_Name = self.Combo_Select_B.currentText()
		global OPBBB
		OPBBB=OPB_Name
		self.OP_B.setText(OPB_Name)

		for row in DB_sheet:
			if row["name"] == OPB_Name:
				self.SSID_B.setText(row["ssid"])
				self.IMSI_B.setText(row["imsi_prefix"])
				self.Country_B.setText(row["country"])
				self.realm_B.setText(row["realm_name"])
				self.LIST_B.setText(row["LIST"])
				self.Owner_B.setText(row["owner"])
				self.RMT_B.setText(row["status"])
				self.DRA_B.setText(row["dra"])
				self.HUB_PLOICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.TADIG_B.setText(row["tagid"])
				self.Combo_Region_B.currentIndex=1

## code for OPB only end

	def rebuild_A_list(self):
		list=[]
		key= self.OP_A.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_A.clear()
		for i in list:
			self.Combo_Select_A.addItem(i)

	def rebuild_B_list(self):
		list=[]
		key= self.OP_B.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_B.clear()
		for i in list:
			self.Combo_Select_B.addItem(i)


	
class OthersWidget(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget, self).__init__(parent)
		self.setStyleSheet("background:lightgrey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OthersWidget2(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget2, self).__init__(parent)
		self.setStyleSheet("background:lightgrey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OP_Online(QWidget):
	def __init__(self,parent=None):
		super(OP_Online,self).__init__(parent)
		#self.setStyleSheet("background:lightgrey")
		QE_length = 800
		QE_hight = 20
		Y_start = 80
		Y_step = 25
		
		X11 = 180
		X12 = 290
		X13 = 630
## OPA and OPB	
## code for OPA only start
		TEXTDOWN=7
		X1 = 70 #label1 start
		X2 = 430#text1 start
		X3 = 720#RIGHT HALF START
		X4 = 900
		X5 = 1100

		self.Lable_0 = QLabel("<font color=%s>%s</font>" %("blue","0.*Provision CCB common attributes. *Click UPD DB in Open route *Select OP_A in Open Route."),self)
		self.Lable_0.move (X1,Y_start-Y_step*3+20)

		self.Lable_DRACustomerRealmNameBeforeTranslation = QLabel("<font color=%s>%s</font>" %("blue","1.*Click Sync.   *Select In/Direct *check all Paremeters *Check Local DSC"),self)
		self.Lable_DRACustomerRealmNameBeforeTranslation.move (X1,Y_start-Y_step*2+12)

		self.sync = QPushButton('Sync',self)
		self.sync.move(X1,Y_start-Y_step*1+5)
		self.sync.clicked.connect(lambda:self.OPERATOR.setText(OPAAA))
		self.sync.clicked.connect(lambda:self.update_online_info(self.OPERATOR.text()))
		self.sync.clicked.connect(lambda:self.check_list_name())
		
		self.btn_direct = QRadioButton("Direct OP",self)
		self.btn_direct.move (X11,Y_start-Y_step*1+TEXTDOWN)		
		self.btn_direct.setChecked(False)
		self.btn_direct.toggled.connect(lambda:self.tuggle())
		
		self.btn_indirect = QRadioButton("InDirect OP",self)
		self.btn_indirect.move (X12,Y_start-Y_step*1+TEXTDOWN)	
		
		self.btn_indirect.setChecked(True)
		
		self.SSID = QLineEdit(self)
		self.SSID.setText('SSID')
		self.SSID.setGeometry(QtCore.QRect(X2, Y_start-Y_step*1+10, QE_length/4, QE_hight))

		self.Lable_OPERATOR = QLabel("Operator Name: ",self)
		self.Lable_OPERATOR.move (X1,Y_start+Y_step*0+TEXTDOWN)		
		self.OPERATOR = QLineEdit(self)
		self.OPERATOR.setText('')
		self.OPERATOR.setGeometry(QtCore.QRect(X1, Y_start+Y_step*1, QE_length/2.5, QE_hight))

		
		self.Lable_VIRTUAL_REALM = QLabel("VIRTUAL_REALM Name on direct DSC",self)
		self.Lable_VIRTUAL_REALM.move (X2,Y_start+Y_step*0+TEXTDOWN)
		self.Lable_VIRTUAL_REALM.hide()	
		self.VIRTUAL_REALM = QLineEdit(self)
		self.VIRTUAL_REALM.setText("Change Me!")
		self.VIRTUAL_REALM.setStyleSheet("color: rgb(255, 0, 255);")
		self.VIRTUAL_REALM.setGeometry(QtCore.QRect(X2, Y_start+Y_step*1, QE_length/4, QE_hight))
		#self.VIRTUAL_REALM.returnPressed.connect(lambda:self.update_vr(self.VIRTUAL_REALM.text())) to be developed by joe feng
		self.VIRTUAL_REALM.hide()
		
		
		self.Lable_LISTNAME = QLabel("Proposed/Existing LIST Name:",self)
		self.Lable_LISTNAME.move (X1,Y_start+Y_step*2+TEXTDOWN)		
		self.LISTNAME = QLineEdit(self)
		self.LISTNAME.setText("")
		self.LISTNAME.setGeometry(QtCore.QRect(X1, Y_start+Y_step*3, QE_length/2.5, QE_hight))
		self.Exisisting_LISTNAME = QLineEdit(self)
		self.Exisisting_LISTNAME.setText("")
		self.Exisisting_LISTNAME.setGeometry(QtCore.QRect(X1, Y_start+Y_step*4, QE_length/2.5, QE_hight))
		
		self.Lable_R2OP_NAME = QLabel("Proposed Realm2OP:",self)
		self.Lable_R2OP_NAME.move (X2,Y_start+Y_step*2+TEXTDOWN)		
		self.R2OP_NAME = QLineEdit(self)
		self.R2OP_NAME.setText("")
		self.R2OP_NAME.setGeometry(QtCore.QRect(X2, Y_start+Y_step*3, QE_length/4, QE_hight))
		
		self.Lable_Local_DSC=QLabel("Local DSC",self)
		self.Lable_Local_DSC.move (X1,Y_start+Y_step*5+7)
		
		
		self.Local_DSC_AP=QCheckBox("AP_DSC",self)
		self.Local_DSC_AP.move (X11,Y_start+Y_step*5+7)
		self.Local_DSC_AP.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_AP.checkState(),"AP"))


		self.Local_DSC_EU=QCheckBox("EU_DSC",self)
		self.Local_DSC_EU.move (X12,Y_start+Y_step*5+7)
		self.Local_DSC_EU.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_EU.checkState(),"EU"))

		
		self.Local_DSC_NA=QCheckBox("NA_DSC",self)
		self.Local_DSC_NA.move (X2,Y_start+Y_step*5+7)
		self.Local_DSC_NA.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_AP.checkState(),"NA"))

		
		self.Lable_DRACustomerRealmName = QLabel("DRACustomerRealmName:Public Realms used by customer's RP to route s6a messages to the customer",self)
		self.Lable_DRACustomerRealmName.move (X1,Y_start+Y_step*6+13)
		#self.Lable_DRACustomerRealmName2 = QLabel("#To setup Request Filter, DecideRoute,Realm2OP, the first realm will setup MAP_IMSIWREALM,MAP_IMSI2K2RREALM",self)
		#self.Lable_DRACustomerRealmName2.move (X1,Y_start+Y_step*5+13)
				
		self.DRACustomerRealmName = QLineEdit(self)
		self.DRACustomerRealmName.setText("")
		self.DRACustomerRealmName.setGeometry(QtCore.QRect(X1, Y_start+Y_step*7+4, QE_length/1.425, QE_hight))

		self.Lable_DRACustomerNodeName = QLabel("DRACustomerNodeRealm:Customer peer realm name in Peer display_name which is different with DRACustomerRealmName",self)
		self.Lable_DRACustomerNodeName.move (X1,Y_start+Y_step*8+5)
		#self.Lable_DRACustomerNodeName2 = QLabel("#To setup Realm2OP",self)
		#self.Lable_DRACustomerNodeName2.move (X1,Y_start+Y_step*7+20)		
		self.DRACustomerNodeName = QLineEdit(self)
		self.DRACustomerNodeName.setText("")
		self.DRACustomerNodeName.setGeometry(QtCore.QRect(X1, Y_start+Y_step*9, QE_length/1.425, QE_hight))

		self.Lable_DRACustomerRealmNameBeforeTranslation = QLabel("DRACustomerRealmNameBeforeTranslation:Private Realms used by customer's node route s6a messages to the customer",self)
		self.Lable_DRACustomerRealmNameBeforeTranslation.move (X1,Y_start+Y_step*9+26)
		#self.Lable_DRACustomerRealmNameBeforeTranslation2 = QLabel("#To setup Request Filter, DecideRoute, Realm2OP",self)
		#self.Lable_DRACustomerRealmNameBeforeTranslation2.move (X1,Y_start+Y_step*9+26)		
		self.DRACustomerRealmNameBeforeTranslation = QLineEdit(self)
		self.DRACustomerRealmNameBeforeTranslation.setText("")
		self.DRACustomerRealmNameBeforeTranslation.setGeometry(QtCore.QRect(X1, Y_start+Y_step*10+17, QE_length/1.425, QE_hight))
		
		self.Lable_IMSI = QLabel("IMSI prefix #used in MAP_IMSI2REALM & MAP_IMSI2K2RREALM ",self)
		self.Lable_IMSI.move (X1,Y_start+Y_step*11+17)
		
		self.IMSI = QLineEdit(self)
		self.IMSI.setText("")
		self.IMSI.setGeometry(QtCore.QRect(X1, Y_start+Y_step*12+8, QE_length/1.425, QE_hight))

		#Add test entry in listcache

		self.Lable_DRACustomerRealmNameBeforeTranslation = QLabel("<font color=%s>%s</font>" %("blue","2.On local DSCs,manually create Cacheable=True,PLAIN_LIST Listcache with the name finalized in Proposed/Existing LIST Name"),self)
		self.Lable_DRACustomerRealmNameBeforeTranslation.move (X1,Y_start+Y_step*13+7)
		
		self.Lable_DRACustomerRealmNameBeforeTranslation = QLabel("<font color=%s>%s</font>" %("blue","3.On local DSCs, add test entry to verify and aviod alarm then reload listcache"),self)
		self.Lable_DRACustomerRealmNameBeforeTranslation.move (X1,Y_start+Y_step*14+3)
		
		self.Combo_LIST_REGION= QComboBox(self)
		self.Combo_LIST_REGION.addItem('Select Region')
		for row in Local_DSC_List:
			self.Combo_LIST_REGION.addItem(row)
		self.Combo_LIST_REGION.move(X1,Y_start+Y_step*15)
		self.Combo_LIST_REGION.setMaxVisibleItems (4)
		
		self.ADD_TEST_ENTRY = QPushButton('Add test entry in List (Local DSC)',self)
		self.ADD_TEST_ENTRY.move(X11,Y_start+Y_step*15)
		self.ADD_TEST_ENTRY.clicked.connect(lambda:self.add_test_entry_listcache(self.Combo_LIST_REGION.currentText(),self.LISTNAME.text()))
		
		self.RELOADLIST = QPushButton('Reload LISTCACHE on the region ',self)
		self.RELOADLIST.move(X2,Y_start+Y_step*15)
		self.RELOADLIST.clicked.connect(lambda:self.RELOAD_LISTCACHES_ALLDSC(self.Combo_LIST_REGION.currentText()))	
		
		#Add request filter
		
		self.Lable_REQUESTFILTER = QLabel("<font color=%s>%s</font>" %("blue","4.On local DSCs, create Request Filter, linking DRACustomerRealmName & RealmNameBeforeTranslation to LIST"),self)
		self.Lable_REQUESTFILTER.move (X1,Y_start+Y_step*16+7)
		
		self.Combo_RF_REGION= QComboBox(self)
		self.Combo_RF_REGION.addItem('Select Region')
		for row in RegionList:
			self.Combo_RF_REGION.addItem(row)
		self.Combo_RF_REGION.move(X1,Y_start+Y_step*17)
		self.Combo_RF_REGION.setMaxVisibleItems (4)
		
		self.C_RequestFilter = QPushButton('Create Request Filter(Local DSC)',self)
		self.C_RequestFilter.move(X11,Y_start+Y_step*17)
		self.C_RequestFilter.clicked.connect(lambda:self.create_request_filter(self.Combo_RF_REGION.currentText(),self.DRACustomerRealmName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.LISTNAME.text(),self.SSID.text()))
		
		self.C_RequestFilter_reload = QPushButton('Reload Rule Engine on the region',self)
		self.C_RequestFilter_reload.move(X2,Y_start+Y_step*17)
		self.C_RequestFilter_reload.clicked.connect(lambda:self.reload_rule_engine_op_online(self.Combo_RF_REGION.currentText()))
		

		#Add Decide Route
		self.Lable_DECIDEROUTE = QLabel("<font color=%s>%s</font>" %("blue","5.Create DecideRoute to CustomerRealmName on all region and to CustomerRealmNameBeforeTranslation on local DSC"),self)
		self.Lable_DECIDEROUTE.move (X1,Y_start+Y_step*18+7)
		
		self.Combo_DR_REGION= QComboBox(self)
		self.Combo_DR_REGION.addItem('Select Region')
		for row in RegionList:
			self.Combo_DR_REGION.addItem(row)
		self.Combo_DR_REGION.move(X1,Y_start+Y_step*19)
		self.Combo_DR_REGION.setMaxVisibleItems (4)
		self.Combo_DR_REGION.currentIndexChanged.connect(self.update_DR_Region)		
		
		self.Combo_DR_TYPE = QComboBox(self)
		self.Combo_DR_TYPE.addItem('Select Rule Type')
		self.Combo_DR_TYPE.move(X11,Y_start+Y_step*19)
		self.Combo_DR_TYPE.setMaxVisibleItems (10)
		self.Combo_DR_TYPE.currentIndexChanged.connect(self.update_Online_CondCons)
		
		self.C_Route = QPushButton('Add Decide Route',self)
		self.C_Route.move(X2-100,Y_start+Y_step*19)
		self.C_Route.clicked.connect(lambda:self.add_decide_route2op(self.Combo_DR_REGION.currentText(),self.DRACustomerRealmName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.CONDITION.toPlainText(),self.CONSEQUENCE.toPlainText()))

		self.RELOAD_DECIDE_ROUTE_ON_REGION = QPushButton('Reload Rule Engine on the region',self)
		self.RELOAD_DECIDE_ROUTE_ON_REGION.move(X2,Y_start+Y_step*19)
		self.RELOAD_DECIDE_ROUTE_ON_REGION.clicked.connect(lambda:self.reload_rule_engine_op_online(self.Combo_DR_REGION.currentText()))
		
		self.Lable_CONDITION = QLabel("COND:",self)
		self.Lable_CONDITION.move (X1,Y_start+Y_step*20+TEXTDOWN)		
		self.CONDITION = QTextEdit(self)
		self.CONDITION.setText("")
		self.CONDITION.setGeometry(QtCore.QRect(X1+65,Y_start+Y_step*20, QE_length/1.6, QE_hight*2))
		
		self.Lable_CONSEQUENCE = QLabel("CONS:",self)
		self.Lable_CONSEQUENCE.move (X1,Y_start+Y_step*22-2+TEXTDOWN)		
		self.CONSEQUENCE = QTextEdit(self)
		self.CONSEQUENCE.setText("")
		self.CONSEQUENCE.setGeometry(QtCore.QRect(X1+65,Y_start+Y_step*22-3, QE_length/1.6, QE_hight*2))
		



		
# RITHT HALF
		#MAPCACHE
		self.Lable_MAP = QLabel("<font color=%s>%s</font>" %("blue","6.ADD MAP_IMSI2REALM, ADD MAP_IMSI2K2RREALM on all regions and Reload MAPCACHE for the 2 translation"),self)
		self.Lable_MAP.move (X3,Y_start-Y_step*3+20)		
		self.Lable_MAP = QLabel("<font color=%s>%s</font>" %("blue"," #All IMSI will be mapped according to the first realm of DRACustomerRealmName "),self)
		self.Lable_MAP.move (X3,Y_start-Y_step*2+12)
		self.IMSI2REALM = QPushButton('Add MAP_IMSI2REALM',self)
		self.IMSI2REALM.move(X3,Y_start-Y_step*1)
		self.IMSI2REALM.clicked.connect(lambda:self.MAP_IMSI2REALM(self.DRACustomerRealmName.text(),self.IMSI.text()))
		
		self.IMSI_TO_K2RREALM = QPushButton('Add MAP_IMSI_TO_K2RREALM',self)
		self.IMSI_TO_K2RREALM.move(X4,Y_start-Y_step*1)
		self.IMSI_TO_K2RREALM.clicked.connect(lambda:self.MAP_IMSI_TO_K2RREALM(self.DRACustomerRealmName.text(),self.IMSI.text()))	
		
		self.RELOADMAP = QPushButton('Reload MAP on All',self)
		self.RELOADMAP.move(X5,Y_start-Y_step*1)
		self.RELOADMAP.clicked.connect(lambda:self.RELOAD_MAPCACHES())
		#REALM2OP
		self.Lable_MAP = QLabel("<font color=%s>%s</font>" %("blue","7.ADD REALM2OP on all regional DSC and Reload REALM2OP for billing"),self)
		self.Lable_MAP.move (X3,Y_start+12)
		
		self.ADDREAL2OP = QPushButton('Add Realm2OP on All',self)
		self.ADDREAL2OP.move(X3,Y_start+Y_step*1)
		self.ADDREAL2OP.clicked.connect(lambda:self.ADD_REALM2OP(self.DRACustomerRealmName.text(),self.DRACustomerNodeName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.R2OP_NAME.text()))
		
		self.RELOADREALM2OP = QPushButton('Reload Realm2OP on All',self)
		self.RELOADREALM2OP.move(X4,Y_start+Y_step*1)
		self.RELOADREALM2OP.clicked.connect(lambda:self.RELOAD_REALM2OP_ALLDSC())
		#SEND EMAIL
		self.Lable_EMAIL = QLabel("<font color=%s>%s</font>" %("blue","8.Send Email for review"),self)
		self.Lable_EMAIL.move (X3,Y_start+Y_step*2+12)
		self.EMAIL = QPushButton('Send Email',self)
		self.EMAIL.move(X3,Y_start+Y_step*3)
		self.EMAIL.clicked.connect(lambda:ONLINE_EMAIL(self.OPERATOR.text(),self.LOG.toPlainText()))
		
		self.Lable_LOG = QLabel("LOG",self)
		self.Lable_LOG.move (X3,Y_start+Y_step*4+TEXTDOWN)		
		self.LOG = QTextEdit(self)
		self.LOG.setGeometry(QtCore.QRect(X3, Y_start+Y_step*5, QE_length/1.4, QE_hight*25))


	def toggle_local_dsc(self,state,region):
		global List_Add_Route_Local
		Local_DSC_List=[]
		if self.Local_DSC_AP.checkState()==2:
			Local_DSC_List.append("AP")
		if self.Local_DSC_EU.checkState()==2:
			Local_DSC_List.append("EU")
		if self.Local_DSC_NA.checkState()==2:
			Local_DSC_List.append("NA")
		List_Add_Route_Local=[]
		self.Combo_LIST_REGION.clear()
		self.Combo_RF_REGION.clear()

		self.Combo_LIST_REGION.addItem('Select Region')
		self.Combo_RF_REGION.addItem('Select Region')
		self.Combo_DR_REGION.addItem('Select Region')
		for row in Local_DSC_List:
			self.Combo_LIST_REGION.addItem(row)
			self.Combo_RF_REGION.addItem(row)
			List_Add_Route_Local.append(row)

			

			
	def check_list_name(self):
		for row in DB_sheet:
			if row['name']==OPAAA:
				self.Exisisting_LISTNAME.setText(row['LIST'])
		if self.Exisisting_LISTNAME.text()=='':
			self.Exisisting_LISTNAME.setText('Not Exist')

	def update_DR_Region(self):
		if self.Local_DSC_AP.checkState()==0 and self.Local_DSC_EU.checkState()==0 and self.Local_DSC_NA.checkState()==0:
			MESSAGE_OUTPUT("WRONG","No Local DSC Checked!")
			return()
		self.CONSEQUENCE.setText("")
		self.CONDITION.setText("")
		self.Combo_DR_TYPE.clear()
		self.Combo_DR_TYPE.addItem('Select Rule Type')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_DR_REGION.currentText():
				self.Combo_DR_TYPE.addItem(row['TYPE'])
		
		
	def update_Online_CondCons(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_DR_REGION.currentText():
				if row['TYPE']==self.Combo_DR_TYPE.currentText():
					self.CONSEQUENCE.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VIRTUAL_REALM.text()))
					self.CONDITION.setText(row['CONDITION'])
					

#def soap_add_list_cache(list_cache_name,realm_to_add,dsc_url):
	def add_test_entry_listcache(self,region,listcachename):
		if region== 'AP' or region== 'EU' or region== 'NA':
			if listcachename!='':
				Region2URL_DSC(region)
				Outputlist_1=[]
				Outputlist_2=[]
				Output1=DSC1+':'+'add test entry to '+listcachename+':'+soap_add_list_cache(listcachename,'test',SURL1)
				Output2=DSC2+':'+'add test entry to '+listcachename+':'+soap_add_list_cache(listcachename,'test',SURL2)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				BIOUTPUT("Add Test Entry in Listcache",Outputlist_1,Outputlist_2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			else:
				MESSAGE_OUTPUT('Prompt','empty listcache name')
		else:
			MESSAGE_OUTPUT('Prompt','Wrong region when add listcache')

#. soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0")
	def create_request_filter(self,region,realm_names,private_realm_names,listname,SSID):
		all_realms=JOIN_STR(realm_names,private_realm_names,',')
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		if all_realms== '':
			MESSAGE_OUTPUT('Wrong','Empty realmName')
			return
		if listname== '':
			MESSAGE_OUTPUT('Wrong','Empty listname')
			return
		if SSID== '':
			MESSAGE_OUTPUT('Wrong','Empty SSID')
			return
		Outputlist_1=[]
		Outputlist_2=[]	
		Region2URL_DSC(region)
		desc_from_op=self.OPERATOR.text()+' SSID '+SSID+' %request filter% if dest realm in LISTCACHE,let pass'
		desc_to_op  =self.OPERATOR.text()+' SSID '+SSID+' %request filter% if origin realm in LISTCACHE,let pass'
		realms=SPLIT2LIST(all_realms)
		#283-destination realm 296-oringinal realm
		condition_from_op='''(IsExist(#AVP283)&amp;&amp;InList(ToLower(AVP283),"'''+listname+'''"))'''
		condition_to_op='''(IsExist(#AVP296)&amp;&amp;InList(ToLower(AVP296),"'''+listname+'''"))'''
		for realm in realms:
			Output1=DSC1+' RF from OP:orig realm='+realm+' con:'+condition_from_op+':'
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_from_op,pop_name=POP,origrealm=realm,condition=condition_from_op)
			Output1=Output1+'\n'
			Output1=Output1+DSC1+' RF to OP:dest realm='+realm+' con:'+condition_to_op+':'
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_to_op,pop_name=POP,destrealm=realm,condition=condition_to_op)
			
			Output2=DSC2+' RF from OP:orig realm='+realm+' con:'+condition_from_op+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=desc_from_op,pop_name=POP,origrealm=realm,condition=condition_from_op)
			Output2=Output2+'\n'
			Output2=Output2+DSC2+' RF to OP:dest realm='+realm+' con:'+condition_to_op+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=desc_to_op,pop_name=POP,destrealm=realm,condition=condition_to_op)

			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)			
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
		BIOUTPUT("Add request filter",Outputlist_1,Outputlist_2)


	def add_decide_route2op(self,region,realm_names,private_realm_names,condi,cons):
		global List_Add_Route_Local
		SSID=self.SSID.text()
		Local=0
		print(List_Add_Route_Local)
		for row in List_Add_Route_Local:
			print("list"+row)
			print("region"+region)
			print(region in row)
			if region in row:
				Local=1
		if Local ==1:
			all_realms=JOIN_STR(realm_names,private_realm_names,',')
		else:
			all_realms=realm_names
		Outputlist_1=[]
		Outputlist_2=[]
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		if all_realms== '':
			MESSAGE_OUTPUT('Wrong','Empty Region Name')
			return
		if condi== '':
			MESSAGE_OUTPUT('Wrong','Empty condition')
			return
		if cons== '':
			MESSAGE_OUTPUT('Wrong','Empty consequence')
			return
		Region2URL_DSC(region)
		desc=self.OPERATOR.text()+' SSID '+SSID+' %decide route% * to OP'
		realms=SPLIT2LIST(all_realms)
		for realm in realms:
			Output1= DSC1+' DecideRoute to OP:* to '+realm+' condi:'+condi+' cons:'+cons+':'
			Output1= Output1+soap_add_rule(dsc_url=SURL1,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons)
			Output2= DSC2+' DecideRoute to OP:* to '+realm+' condi:'+condi+' cons:'+cons+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
		BIOUTPUT("Add Decide route to OP",Outputlist_1,Outputlist_2)
		
	def MAP_IMSI2REALM(self,realms,IMSIs):
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty DRACustomerRealmName')
			return
		if IMSIs=='':
			MESSAGE_OUTPUT('Wrong','Empty IMSI Prefix')
			return
		MESSAGE_OUTPUT('Warning','All IMSI will be mapped to \nthe 1st realm in DRACustomerRealmName ')
		realm_list=SPLIT2LIST(realms)
		first_realm=realm_list[0].strip()
		imsi_list=SPLIT2LIST(IMSIs)
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for imsi in imsi_list:
				imsi=imsi.strip()
				Output1=DSC1+' '+imsi+'->'+first_realm+'->MAP_IMSITOREALM '
				Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSITOREALM',imsi,first_realm)
				Output2=DSC2+' '+imsi+'->'+first_realm+'->MAP_IMSITOREALM '
				Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSITOREALM',imsi,first_realm)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  MAP_IMSITOREALM",Outputlist_1,Outputlist_2)

	def MAP_IMSI_TO_K2RREALM(self,realms,IMSIs):
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty DRACustomerRealmName')
			return
		if IMSIs=='':
			MESSAGE_OUTPUT('Wrong','Empty IMSI Prefix')
			return
		MESSAGE_OUTPUT('Warning','All IMSI will be mapped to \nthe 1st realm in DRACustomerRealmName ')
		realm_list=SPLIT2LIST(realms)
		first_realm=realm_list[0].strip()
		first_realm=first_realm+'.key2roam.comfone.com'
		imsi_list=SPLIT2LIST(IMSIs)
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for imsi in imsi_list:
				imsi=imsi.strip()
				Output1=DSC1+' '+imsi+'->'+first_realm+'->MAP_IMSI_TO_K2RREALM '
				Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSI_TO_K2RREALM',imsi,first_realm)
				Output2=DSC2+' '+imsi+'->'+first_realm+'->MAP_IMSI_TO_K2RREALM '
				Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSI_TO_K2RREALM',imsi,first_realm)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  MAP_IMSI2K2R REALM",Outputlist_1,Outputlist_2)

	def RELOAD_MAPCACHES(self,reg=''):
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		if reg=='AP' or reg=='EU' or reg=='NA':
			region_list=[reg]
		for re in region_list:
			Region2URL_DSC(re)
			Output1=DSC1+':reload all MAPCACHE:'
			Output1=Output1+soap_reload_mapcache(SURL1)
			Output2=DSC2+':reload all MAPCACHE:'
			Output2=Output2+soap_reload_mapcache(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
		BIOUTPUT("Reload LISTCACHES",Outputlist_1,Outputlist_2)
			
	def RELOAD_LISTCACHES_ALLDSC(self,reg=''):
		region_list=['AP','EU','NA']
		if reg=='AP' or reg=='EU' or reg=='NA':
			region_list=[reg]
		for re in region_list:
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(re)
			Output1=DSC1+':reload all LISTCACHE:'
			Output1=Output1+soap_reload_listcaches(SURL1)
			Output2=DSC2+':reload all LISTCACHE:'
			Output2=Output2+soap_reload_listcaches(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload LISTCACHES",Outputlist_1,Outputlist_2)
			
	def RELOAD_REALM2OP_ALLDSC(self):
		region_list=['AP','EU','NA']
		for re in region_list:
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(re)
			Output1=DSC1+':reload REALM2OP:'
			Output1=Output1+soap_reload_realm2op(SURL1)
			Output2=DSC2+':reload REALM2OP:'
			Output2=Output2+soap_reload_realm2op(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload REALM2OP",Outputlist_1,Outputlist_2)

	def ADD_REALM2OP(self,realms,node_realms,private_realms,R2OP_NAME):
		realms=JOIN_STR(realms,node_realms,',')
		realms=JOIN_STR(realms,private_realms,',')
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty Realm')
			return
		if R2OP_NAME=='':
			MESSAGE_OUTPUT('Wrong','Empty Realm2OP name')
			return

		realm_list=SPLIT2LIST(realms)
		
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for realm in realm_list:
				Output1=DSC1+' Realm2OP '+realm+'->'+R2OP_NAME
				Output1=Output1+soap_add_realm2op(SURL1,realm,R2OP_NAME)
				Output2=DSC2+' Realm2OP '+realm+'->'+R2OP_NAME
				Output2=Output2+soap_add_realm2op(SURL2,realm,R2OP_NAME)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  Realm2OP",Outputlist_1,Outputlist_2)

	def reload_rule_engine_op_online(self,region):
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		Region2URL_DSC(region)
		Outputlist_1=[]
		Outputlist_2=[]
		Output1= DSC1+' reload rule engine '
		Output1= Output1+soap_reload_rule_engine(dsc_url=SURL1)
		Output2= DSC2+' reload rule engine '
		Output2= Output2+soap_reload_rule_engine(dsc_url=SURL1)
		Outputlist_1.append(Output1)
		Outputlist_2.append(Output2)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
		self.LOG.setPlainText(LOGTEXT)
		BIOUTPUT("Add Decide route to OP",Outputlist_1,Outputlist_2)



	def update_online_info(self,OP):
		RealmName1=''
		NodeRealm1=''
		RealmNameBeforeTranslation1=''
		DRAIMSIPrefix1=''
		result=CCB_ONLINE2CSV()
		ssid="n/a"
		#print(OP)
		for row in result:
			if row['name']==OP:
				ssid=row['id']
				if row['item']=='DRACustomerRealmName':
					RealmName1=JOIN_STR(RealmName1,row['value'],',')
				if row['item']=='CustomerNodeRealm':
					NodeRealm1=JOIN_STR(NodeRealm1,row['value'],',')
				if row['item']=='DRACustomerRealmNameBeforeTranslation':
					RealmNameBeforeTranslation1=JOIN_STR(RealmNameBeforeTranslation1,row['value'],',')
				if row['item']=='DRAIMSIPrefix':
					DRAIMSIPrefix1=JOIN_STR(DRAIMSIPrefix1,row['value'],',')
					
					

		self.SSID.setText(str(ssid))	
		self.DRACustomerRealmName.setText(RealmName1)
		self.DRACustomerNodeName.setText(NodeRealm1)		
		self.DRACustomerRealmNameBeforeTranslation.setText(RealmNameBeforeTranslation1)
		self.IMSI.setText(DRAIMSIPrefix1)
		temp=OP.replace(' ','_').upper()
		LISTNAME='LIST_'+str(ssid)+'_'+temp
		self.LISTNAME.setText(LISTNAME)
		temp=OP.replace(' ','-')
		R2OP_NAME=str(ssid)+'#'+temp
		self.R2OP_NAME.setText(R2OP_NAME)
	def tuggle(self):
		if self.btn_direct.isChecked()==True:
			self.VIRTUAL_REALM.show()
			self.Lable_VIRTUAL_REALM.show()
			MESSAGE_OUTPUT('Prompt','Please input Virtual_Realm name!')
		else:
			self.VIRTUAL_REALM.hide()
			self.VIRTUAL_REALM.setText("")	
					

class DECIDE_ROUTE(QWidget):
	def __init__(self,parent=None):
		super(DECIDE_ROUTE,self).__init__(parent)
		
		self.Full_list=[]
		for row in DB_sheet:
			self.Full_list.append(row["name"])
			
		QE_length = 400
		QE_hight = 20
		Y_start = 40
		Y_step = 30
		X10 =1080
		X11 = 1160
		X12 = 1240
		X13 = 1240
		distance=550

		
## OPA and OPB
		Y_start=40	
## code for OPA only start
		X1 = 10 #OPA lable start
		X2 = 100#OPA text start
		X3 = 200#labe2 start
		X4 = 250#text2 start

		
		X11 = distance+X1 #OPB start
		X12 = distance+X2

		


		self.Lable_SSID_A = QLabel("SSID_A",self)
		self.Lable_SSID_A.move (X1,Y_start-Y_step)		
		self.SSID_A = QLineEdit(self)
		self.SSID_A.setText("NULL")
		self.SSID_A.setGeometry(QtCore.QRect(X2, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_A = QLabel("OP_A",self)
		self.Lable_OP_A.move (X1,Y_start)		
		self.OP_A = QLineEdit(self)
		self.OP_A.setText("*")
		self.OP_A.setGeometry(QtCore.QRect(X2, Y_start, QE_length, QE_hight))
		
		Combo_LIST_A=self.Full_list[:]
		Combo_LIST_A.insert(0,'*')
		self.Combo_Select_A = QComboBox(self)
		for i in Combo_LIST_A:
			self.Combo_Select_A.addItem(i)
		self.Combo_Select_A.move(X2,Y_start+Y_step*1)
		self.Combo_Select_A.setMaxVisibleItems (10)
		self.Combo_Select_A.currentIndexChanged.connect(self.update_A)
		self.OP_A.returnPressed.connect(self.rebuild_A_list)
			
		self.Lable_Realm_A = QLabel("SourceRealm(A)",self)
		self.Lable_Realm_A.move (X1,Y_start+Y_step*2)				
		self.realm_A = QLineEdit(self)
		self.realm_A.setText("*")
		self.realm_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_SSID_B = QLabel("SSID_B",self)
		self.Lable_SSID_B.move (X11,Y_start-Y_step)		
		self.SSID_B = QLineEdit(self)
		self.SSID_B.setText("")
		self.SSID_B.setGeometry(QtCore.QRect(X12, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_B = QLabel("OP_B",self)
		self.Lable_OP_B.move (X11,Y_start)		
		self.OP_B = QLineEdit(self)
		self.OP_B.setText("")
		self.OP_B.setGeometry(QtCore.QRect(X12, Y_start, QE_length, QE_hight))
		
		Combo_LIST_B=self.Full_list[:]
		self.Combo_Select_B = QComboBox(self)
		for i in Combo_LIST_B:
			self.Combo_Select_B.addItem(i)
		self.Combo_Select_B.move(X12,Y_start+Y_step*1)
		self.Combo_Select_B.setMaxVisibleItems (10)
		self.Combo_Select_B.currentIndexChanged.connect(self.update_B)
		self.OP_B.returnPressed.connect(self.rebuild_B_list)
			
		self.Lable_Realm_B = QLabel("DestRealm(B)",self)
		self.Lable_Realm_B.move (X11,Y_start+Y_step*2)				
		self.realm_B = QLineEdit(self)
		self.realm_B.setText("")
		self.realm_B.setGeometry(QtCore.QRect(X12,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_Region = QLabel("Region",self)
		self.Lable_Region.move (X1,Y_start+Y_step*3)
		
		self.Combo_Region = QComboBox(self)
		self.Combo_Region.addItem('')
		for i in RegionList:
			self.Combo_Region.addItem(i)
		self.Combo_Region.setCurrentIndex(0)
		self.Combo_Region.move(X2,Y_start+Y_step*3)
		self.Combo_Region.setMaxVisibleItems (4)
		self.Combo_Region.currentIndexChanged.connect(self.update_Scenario)
		self.Combo_Region.currentIndexChanged.connect(self.update_CondCons)


		self.Lable_Scenario = QLabel("Scenario",self)
		self.Lable_Scenario.move (X3,Y_start+Y_step*3)
		
		self.Combo_Scenario = QComboBox(self)
		self.Combo_Scenario.setMaxVisibleItems (4)
		self.Combo_Scenario.addItem('Please Select Scenario')		
		#for row in DECIDEROUTEPOLICY:
		#	if row['REGION']==self.Combo_Region.currentText():
		#		self.Combo_Scenario.addItem(row['TYPE'])
		self.Combo_Scenario.move(X4,Y_start+Y_step*3)
		self.Combo_Scenario.setMaxVisibleItems (10)
		self.Combo_Scenario.currentIndexChanged.connect(self.update_CondCons)	
		
		self.Lable_VRB = QLabel("Virtual Realm B",self)
		self.Lable_VRB.move (X11,Y_start+Y_step*3)
		self.VRB = QLineEdit(self)
		self.VRB.setText("")
		self.VRB.setGeometry(QtCore.QRect(X12, Y_start+Y_step*3, QE_length, QE_hight))
		self.VRB.returnPressed.connect(self.update_VRB)

		self.Lable_Condition = QLabel("Condition",self)
		self.Lable_Condition.move(X1,Y_start+Y_step*4)		
		self.Condition = QTextEdit(self)
		self.Condition.setText("")
		self.Condition.setGeometry(QtCore.QRect(X2,Y_start+Y_step*4, QE_length, QE_hight*4))
		
		self.Lable_Consequence = QLabel("Consequence",self)
		self.Lable_Consequence.move(X1,Y_start+Y_step*7)		
		self.Consequence = QTextEdit(self)
		self.Consequence.setText("")
		self.Consequence.setGeometry(QtCore.QRect(X2,Y_start+Y_step*7, QE_length, QE_hight*4))
		
		self.Lable_Origin_Host = QLabel("Origin_Host",self)
		self.Lable_Origin_Host.move (X1,Y_start+Y_step*10)				
		self.Origin_Host = QLineEdit(self)
		self.Origin_Host.setText("*")
		self.Origin_Host.setGeometry(QtCore.QRect(X2,Y_start+Y_step*10, QE_length, QE_hight))
		
		self.Lable_Dest_Host = QLabel("Dest_Host",self)
		self.Lable_Dest_Host.move (X1,Y_start+Y_step*11)				
		self.Dest_Host = QLineEdit(self)
		self.Dest_Host.setText("*")
		self.Dest_Host.setGeometry(QtCore.QRect(X2,Y_start+Y_step*11, QE_length, QE_hight))
		
		self.Lable_SRC_Peer = QLabel("SRC_Peer",self)
		self.Lable_SRC_Peer.move (X1,Y_start+Y_step*12)				
		self.SRC_Peer = QLineEdit(self)
		self.SRC_Peer.setText("*")
		self.SRC_Peer.setGeometry(QtCore.QRect(X2,Y_start+Y_step*12, QE_length, QE_hight))
		
		self.Lable_SRC_Realm = QLabel("SRC_Realm",self)
		self.Lable_SRC_Realm.move (X1,Y_start+Y_step*13)				
		self.SRC_Realm = QLineEdit(self)
		self.SRC_Realm.setText("*")
		self.SRC_Realm.setGeometry(QtCore.QRect(X2,Y_start+Y_step*13, QE_length, QE_hight))

		self.Lable_Type = QLabel("Type",self)
		self.Lable_Type.move (X1,Y_start+Y_step*14)				
		self.Type = QLineEdit(self)
		self.Type.setText("DECIDE_ROUTE")
		self.Type.setGeometry(QtCore.QRect(X2,Y_start+Y_step*14, QE_length, QE_hight))
		
		self.Lable_Appid = QLabel("Appid",self)
		self.Lable_Appid.move (X1,Y_start+Y_step*15)				
		self.Appid = QLineEdit(self)
		self.Appid.setText("16777251")
		self.Appid.setGeometry(QtCore.QRect(X2,Y_start+Y_step*15, QE_length, QE_hight))
		
		self.Lable_Priority = QLabel("Priority",self)
		self.Lable_Priority.move (X1,Y_start+Y_step*16)				
		self.Priority = QLineEdit(self)
		self.Priority.setText("10")
		self.Priority.setGeometry(QtCore.QRect(X2,Y_start+Y_step*16, QE_length, QE_hight))
		
	
		self.Description = QTextEdit(self)
		self.Description.setText("")
		self.Description.setGeometry(QtCore.QRect(X2,Y_start+Y_step*17, QE_length, QE_hight*4))
		
		self.Build_Description = QPushButton('Build_Description',self)
		self.Build_Description.move(X1,Y_start+Y_step*17)
		self.Build_Description.clicked.connect(self.BD_Description)
		
		self.Provision = QPushButton('Provision',self)
		self.Provision.move(X1,Y_start+Y_step*20)
		self.Provision.clicked.connect(lambda:self.provsion())
		
		self.Reload = QPushButton('Reload Rule Engine',self)
		self.Reload.move(X2,Y_start+Y_step*20)
		self.Reload.clicked.connect(lambda:self.reload_rule_engine())
		
		self.Lable_LOG = QLabel("LOG",self)
		self.Lable_LOG.move (X11,Y_start+Y_step*4)		
		self.LOG = QTextEdit(self)
		self.LOG.setGeometry(QtCore.QRect(X12, Y_start+Y_step*4, QE_length*1.5, QE_hight*25))
		
		self.rule_email = QPushButton('Email',self)
		self.rule_email.move(X11,Y_start+Y_step*5)
		self.rule_email.clicked.connect(lambda:self.email())
		
	def email(self):
		Tolist='DSS_Route_Provision@syniverse.com'
		Subject='New rule provsioned : '+self.OP_A.text()+'-'+self.OP_B.text()
		email_body=self.LOG.toPlainText()
		sende_plain_mail(Tolist,'',Subject,email_body)

		
	def provsion(self):
		
		if self.Combo_Region.currentText()!='AP' and self.Combo_Region.currentText()!='EU' and self.Combo_Region.currentText()!='NA':
			MESSAGE_OUTPUT("ERROR","NO REGION Selected!")
			return
		if self.realm_A.text()=='':
			MESSAGE_OUTPUT("ERROR","SOURCE REALM(A) EMPTY!")
			return
		if self.realm_B.text()=='':
			MESSAGE_OUTPUT("ERROR","SOURCE REALM(B) EMPTY!")
			return
		if self.Description.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","description EMPTY!")
			return
		if self.Condition.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","Condition EMPTY!")
		if self.Consequence.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","Consequence EMPTY!")
			return
			
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(self.Combo_Region.currentText())
		realm_a_list=SPLIT2LIST(self.realm_A.text())
		realm_b_list=SPLIT2LIST(self.realm_B.text())
		for realm_a in realm_a_list:
			for realm_b in realm_b_list:
#V=def soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0"):
				
				Output1=DSC1+' '+self.Type.text()+' from '+self.OP_A.text()+' '+realm_a+' to '+self.OP_B.text()+' '+realm_b+' cond: '+self.Condition.toPlainText()+' cons '+ self.Consequence.toPlainText()
				Output1=Output1+' : '+soap_add_rule(dsc_url=SURL1,ruletype=self.Type.text(),description=self.Description.toPlainText()\
,pop_name=POP,orighost=self.Origin_Host.text(),origrealm=realm_a,desthost=self.Dest_Host.text(),destrealm=realm_b,\
srchost=self.Origin_Host.text(),srcrealm=self.SRC_Realm.text(),priority=self.Priority.text(),condition=self.Condition.toPlainText(),\
consequence=self.Consequence.toPlainText())
				Output2=DSC2+' '+self.Type.text()+' from '+self.OP_A.text()+' '+realm_a+' to '+self.OP_B.text()+' '+realm_b+' cond: '+self.Condition.toPlainText()+' cons '+ self.Consequence.toPlainText()
				Output2=Output2+' : '+soap_add_rule(dsc_url=SURL2,ruletype=self.Type.text(),description=self.Description.toPlainText()\
,pop_name=POP,orighost=self.Origin_Host.text(),origrealm=realm_a,desthost=self.Dest_Host.text(),destrealm=realm_b,\
srchost=self.Origin_Host.text(),srcrealm=self.SRC_Realm.text(),priority=self.Priority.text(),condition=self.Condition.toPlainText(),\
consequence=self.Consequence.toPlainText())

				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)		
				
		BIOUTPUT("Add Rule",Outputlist_1,Outputlist_2)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
		self.LOG.setPlainText(LOGTEXT)
		
	def reload_rule_engine(self):
		
		if self.Combo_Region.currentText()!='AP' and self.Combo_Region.currentText()!='EU' and self.Combo_Region.currentText()!='NA':
			MESSAGE_OUTPUT("ERROR","NO REGION Selected!")
			return

		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(self.Combo_Region.currentText())
		Output1=DSC1+' reload rule engine '
		Output1=Output1+soap_reload_rule_engine(SURL1)
		Output2=DSC2+' reload rule engine '
		Output2=Output2+soap_reload_rule_engine(SURL2)

		Outputlist_1.append(Output1)
		Outputlist_2.append(Output2)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
		self.LOG.setPlainText(LOGTEXT)		
				
		BIOUTPUT("Reload Rule engine",Outputlist_1,Outputlist_2)

		
	def BD_Description(self):
		DESC_A = self.OP_A.text()+' SSID '+self.SSID_A.text()
		if self.SSID_A.text()== 'NULL':
			DESC_A=' any '
		DESC_B = self.OP_B.text()+' SSID '+self.SSID_B.text()
		DESC='%'+self.Type.text()+'% from '+DESC_A+' to '+DESC_B
		self.Description.setPlainText(DESC)


	def update_CondCons(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_Region.currentText():
				if row['TYPE']==self.Combo_Scenario.currentText():
					self.Consequence.setText(row['CONSEQUENCE'])
					if self.VRB.text()=='' and '#REPLACEME#' in self.Consequence.toPlainText():
						MESSAGE_OUTPUT('Wrong Parameter','Virtual RealmB is empty!')
					else:
						self.Consequence.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VRB.text()))
					self.Condition.setText(row['CONDITION'])

	
	def update_VRB(self):
		if '#REPLACEME#' in self.Consequence.toPlainText() and self.VRB.text()!='':
			self.Consequence.setText(self.Consequence.toPlainText().replace('#REPLACEME#',self.VRB.text()))
			
	def update_Scenario(self):
		self.Combo_Scenario.clear()
		self.Combo_Scenario.addItem('Please Select Scenario')

		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_Region.currentText():
				self.Combo_Scenario.addItem(row['TYPE'])
				
	def update_A(self,ii):
		OPA_Name = self.Combo_Select_A.currentText()
		self.OP_A.setText(OPA_Name)
		for row in DB_sheet:
			if row["name"] == OPA_Name:
				self.SSID_A.setText(row["ssid"])
				self.realm_A.setText(row["realm_name"])
			if OPA_Name == '*':
				self.SSID_A.setText('NULL')
				self.realm_A.setText('*')				
	def update_B(self,ii):
		OPB_Name = self.Combo_Select_B.currentText()
		self.OP_B.setText(OPB_Name)

		for row in DB_sheet:
			if row["name"] == OPB_Name:
				self.SSID_B.setText(row["ssid"])
				self.realm_B.setText(row["realm_name"])


	def rebuild_A_list(self):
		list=[]
		key= self.OP_A.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_A.clear()
		list.insert(0,'*')
		for i in list:
			self.Combo_Select_A.addItem(i)

	def rebuild_B_list(self):
		list=[]
		key= self.OP_B.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_B.clear()
		for i in list:
			self.Combo_Select_B.addItem(i)



class Main_TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(Main_TabWidget, self).__init__(parent)
        self.resize(1366, 768)
        self.mContent = OPEN_ROUTE()
        self.mContent2 = OP_Online()
        self.mContent3 = DECIDE_ROUTE()
        self.mIndex = OthersWidget()
        self.mIndex2 = OthersWidget2()
        self.addTab(self.mContent, u"Open Route")
        self.addTab(self.mContent2, u"OP_Online")
        self.addTab(self.mContent3, u"DECIDE_ROUTE")
        self.addTab(self.mIndex, u"Others")
        self.addTab(self.mIndex2, u"Others2")


if __name__ == '__main__':
     import sys
     app = QApplication(sys.argv)
     t = Main_TabWidget()
     t.show()
     app.exec_()



