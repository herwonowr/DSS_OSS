
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
from soap_all_commands_for_dsc import soap_reload_rule_engine,soap_add_decide_route,soap_add_list_cache,soap_reload_listcaches,soap_check_decide_route,soap_add_rule
from file_transaction import *
from SendEmail import *

import os
if not os.path.exists(r'.\\file\DB.csv'):
	INITIALIZE_DB()

PEERINGPOLICY=csv2dict('PeeringPolicy.csv')
DECIDEROUTEPOLICY=csv2dict('DecideRoutePloicy.csv')

	
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

#根据region设置全局共享变量SURL1,SURL2,DSC1,DSC2
def Region2URL_DSC(Region):
		global SURL1,SURL2,DSC1,DSC2,POP
		if Region =="AP":
			SURL1="http://10.162.28.186:8080/DSC_SOAP/query?"
			SURL2="http://10.163.28.131:8080/DSC_SOAP/query?"
			DSC1="HKG"
			DSC2="SNG"
			POP="AP POP"
		if Region =="EU":
			SURL1="http://10.160.28.32:8080/DSC_SOAP/query?"
			SURL2="http://10.161.28.32:8080/DSC_SOAP/query?"
			DSC1="AMS"
			DSC2="FRT"
			POP="EU POP"		
		if Region =="NA":
			SURL1="http://10.166.28.200:8080/DSC_SOAP/query?"
			SURL2="http://10.164.28.189:8080/DSC_SOAP/query?"
			DSC1="CHI"
			DSC2="DAL"
			POP="NA POP"

#DSC OUTPUT 弹窗代码
def MESSAGE_OUTPUT(Title,Output_Text):
	dialog=QDialog()
	dialog.resize(200,100)
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
		


def soap_create_listcache(surl,listcachename):
	return("success")
#open route window layout


		
class OPEN_ROUTE(QWidget):
	signal_opa_change = QtCore.pyqtSignal(str)
	
	
	def __init__(self,parent=None):
		super(OPEN_ROUTE,self).__init__(parent)
			
		self.Full_list=['']
		#DB_sheet = csv2dict(".\\file\DB.csv")
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
		self.UPD_DB.clicked.connect(lambda:INITIALIZE_DB())
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
		
		self.Lable_HUB_PLOICY_A = QLabel("HUB_PLOICY_A",self)
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
		
		self.Lable_HUB_PLOICY_B = QLabel("HUB_PLOICY_B",self)
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
		OP_Online.test(OP_Online.self)
		self.OP_A.setText(OPA_Name)
		self.signal_opa_change.emit(OPA_Name)
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
		self.setStyleSheet("background: blue grey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OthersWidget2(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget2, self).__init__(parent)
		self.setStyleSheet("background: blue grey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OP_Online(QWidget):
	def __init__(self,parent=None):
		super(OP_Online,self).__init__(parent)
		QE_length = 800
		QE_hight = 20
		Y_start = 40
		Y_step = 25
		
		X11 = 180
		X12 = 290
		X13 = 630
## OPA and OPB
		Y_start=40	
## code for OPA only start
		TEXTDOWN=10
		X1 = 70 #label1 start
		X2 = 430#text1 start
		X3 = 720#log start

			
		self.btn_direct = QRadioButton("Direct OP",self)
		self.btn_direct.move (X1,Y_start-Y_step*1+TEXTDOWN)		
		self.btn_direct.setChecked(False)
		self.btn_direct.toggled.connect(lambda:self.tuggle())
		
		self.btn_indirect = QRadioButton("InDirect OP",self)
		self.btn_indirect.move (X11,Y_start-Y_step*1+TEXTDOWN)	
		
		self.btn_indirect.setChecked(True)
		
		self.SSID = QLineEdit(self)
		self.SSID.setText('SSID')
		self.SSID.setGeometry(QtCore.QRect(X2, Y_start-Y_step*1+10, QE_length/4, QE_hight))


		self.Lable_LOG = QLabel("LOG",self)
		self.Lable_LOG.move (X3,Y_start+Y_step*0+TEXTDOWN)		
		self.LOG = QTextEdit(self)
		self.LOG.setText("Bharti Airtel India")
		self.LOG.setGeometry(QtCore.QRect(X3, Y_start+Y_step*1, QE_length/1.4, QE_hight*32))
		

		self.Lable_OPERATOR = QLabel("Operator Name: Paste Operator name here",self)
		self.Lable_OPERATOR.move (X1,Y_start+Y_step*0+TEXTDOWN)		
		self.OPERATOR = QLineEdit(self)
		self.OPERATOR.setText('DDD')
		self.OPERATOR.setGeometry(QtCore.QRect(X1, Y_start+Y_step*1, QE_length/4, QE_hight))
		self.OPERATOR.returnPressed.connect(lambda:self.update_online_info(self.OPERATOR.text()))
		
		self.Lable_VIRTUAL_REALM = QLabel("VIRTUAL_REALM Name on direct DSC(Direct OP Only)",self)
		self.Lable_VIRTUAL_REALM.move (X2,Y_start+Y_step*0+TEXTDOWN)		
		self.VIRTUAL_REALM = QLineEdit(self)
		self.VIRTUAL_REALM.setText("")
		self.VIRTUAL_REALM.setGeometry(QtCore.QRect(X2, Y_start+Y_step*1, QE_length/4, QE_hight))
		self.VIRTUAL_REALM.returnPressed.connect(lambda:self.update_online_info(self.VIRTUAL_REALM.text()))
		self.VIRTUAL_REALM.hide()
		
		
		self.Lable_LISTNAME = QLabel("Proposed LIST Name:",self)
		self.Lable_LISTNAME.move (X1,Y_start+Y_step*2+TEXTDOWN)		
		self.LISTNAME = QLineEdit(self)
		self.LISTNAME.setText("")
		self.LISTNAME.setGeometry(QtCore.QRect(X1, Y_start+Y_step*3, QE_length/4, QE_hight))
		
		self.Lable_existing_LISTNAME = QLabel("Existing LIST Name:",self)
		self.Lable_existing_LISTNAME.move (X2,Y_start+Y_step*2+TEXTDOWN)		
		self.existing_LISTNAME = QLineEdit(self)
		self.existing_LISTNAME.setText("Not support,check LISTNAME with LIST_SSID")
		self.existing_LISTNAME.setGeometry(QtCore.QRect(X2, Y_start+Y_step*3, QE_length/4, QE_hight))
		
		
		self.Lable_R2OP_NAME = QLabel("Proposed Realm2OP:",self)
		self.Lable_R2OP_NAME.move (X1,Y_start+Y_step*4+TEXTDOWN)		
		self.R2OP_NAME = QLineEdit(self)
		self.R2OP_NAME.setText("")
		self.R2OP_NAME.setGeometry(QtCore.QRect(X1, Y_start+Y_step*5, QE_length/4, QE_hight))
		
		self.existing_Lable_R2OP_NAME = QLabel("Existing Realm2OP:",self)
		self.existing_Lable_R2OP_NAME.move (X2,Y_start+Y_step*4+TEXTDOWN)		
		self.existing_R2OP_NAME = QLineEdit(self)
		self.existing_R2OP_NAME.setText("Not supported yet!")
		self.existing_R2OP_NAME.setGeometry(QtCore.QRect(X2, Y_start+Y_step*5, QE_length/4, QE_hight))
		
		
		self.Lable_DRACustomerRealmName = QLabel("DRACustomerRealmName:Public Realms used by customer's RP to route s6a messages to the customer",self)
		self.Lable_DRACustomerRealmName.move (X1,Y_start+Y_step*6+TEXTDOWN)		
		self.DRACustomerRealmName = QLineEdit(self)
		self.DRACustomerRealmName.setText("")
		self.DRACustomerRealmName.setGeometry(QtCore.QRect(X1, Y_start+Y_step*7, QE_length/1.425, QE_hight))

		self.Lable_DRACustomerNodeName = QLabel("DRACustomerNodeName:Customer peer realm name in Peer display_name which is different with DRACustomerRealmName",self)
		self.Lable_DRACustomerNodeName.move (X1,Y_start+Y_step*8+TEXTDOWN)		
		self.DRACustomerNodeName = QLineEdit(self)
		self.DRACustomerNodeName.setText("")
		self.DRACustomerNodeName.setGeometry(QtCore.QRect(X1, Y_start+Y_step*9, QE_length/1.425, QE_hight))

		self.Lable_DRACustomerRealmNameBeforeTranslation = QLabel("DRACustomerRealmNameBeforeTranslation:Private Realms used by customer's node route s6a messages to the customer",self)
		self.Lable_DRACustomerRealmNameBeforeTranslation.move (X1,Y_start+Y_step*10+TEXTDOWN)		
		self.DRACustomerRealmNameBeforeTranslation = QLineEdit(self)
		self.DRACustomerRealmNameBeforeTranslation.setText("")
		self.DRACustomerRealmNameBeforeTranslation.setGeometry(QtCore.QRect(X1, Y_start+Y_step*11, QE_length/1.425, QE_hight))
		
		#Command Buttom List

		
		self.C_LIST_AP = QPushButton('Create LIST on AP',self)
		self.C_LIST_AP.move(X1,Y_start+Y_step*13)
		self.C_LIST_AP.clicked.connect(lambda:self.create_listcache('AP',self.LISTNAME.text()))
		
		self.C_LIST_EU = QPushButton('Create LIST on EU',self)
		self.C_LIST_EU.move(X11,Y_start+Y_step*13)
		self.C_LIST_EU.clicked.connect(lambda:self.create_listcache('EU',self.LISTNAME.text()))
		
		self.C_LIST_NA = QPushButton('Create LIST on NA',self)
		self.C_LIST_NA.move(X12,Y_start+Y_step*13)
		self.C_LIST_NA.clicked.connect(lambda:self.create_listcache('NA',self.LISTNAME.text()))
		
		self.C_RequestFilter_AP = QPushButton('Create RF on AP  ',self)
		self.C_RequestFilter_AP.move(X1,Y_start+Y_step*14)
		self.C_RequestFilter_AP.clicked.connect(lambda:self.create_request_filter('AP',self.DRACustomerRealmName.text(),self.LISTNAME.text(),self.SSID.text()))
		
		self.C_RequestFilter_EU = QPushButton('Create RF on EU  ',self)
		self.C_RequestFilter_EU.move(X11,Y_start+Y_step*14)
		self.C_RequestFilter_EU.clicked.connect(lambda:self.create_request_filter('EU',self.DRACustomerRealmName.text(),self.LISTNAME.text(),self.SSID.text()))
		
		self.C_RequestFilter_NA = QPushButton('Create RF on NA  ',self)
		self.C_RequestFilter_NA.move(X12,Y_start+Y_step*14)
		self.C_RequestFilter_NA.clicked.connect(lambda:self.create_request_filter('NA',self.DRACustomerRealmName.text(),self.LISTNAME.text(),self.SSID.text()))
		
		#AP add route
		self.C_Route_AP = QPushButton('Create DR on AP  ',self)
		self.C_Route_AP.move(X1,Y_start+Y_step*15)
		self.C_Route_AP.clicked.connect(lambda:add_decide_route2op('AP',self.DRACustomerRealmName.text(),self.CONDITION_AP.text(),self.NextContent_AP.text()))

				
		self.Combo_Next_AP = QComboBox(self)
		self.Combo_Next_AP.addItem('')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='AP DSC':
				self.Combo_Next_AP.addItem(row['TYPE'])
		self.Combo_Next_AP.move(X11,Y_start+Y_step*15)
		self.Combo_Next_AP.setMaxVisibleItems (10)
		self.Combo_Next_AP.currentIndexChanged.connect(self.update_AP_Next)
		
		self.CONDITION_AP = QLineEdit(self)
		self.CONDITION_AP.setText("CONDITION_AP")
		self.CONDITION_AP.setGeometry(QtCore.QRect(X12, Y_start+Y_step*15, QE_length/2.35, QE_hight))
		
		self.NextContent_AP = QLineEdit(self)
		self.NextContent_AP.setText("CONSEQUENCE_AP")
		self.NextContent_AP.setGeometry(QtCore.QRect(X11, Y_start+Y_step*16, QE_length/1.775, QE_hight))
		
		#EU add route
		self.C_Route_EU = QPushButton('Create DR on EU  ',self)
		self.C_Route_EU.move(X1,Y_start+Y_step*17)
		self.C_Route_EU.clicked.connect(lambda:add_decide_route2op('EU',self.DRACustomerRealmName.text(),self.CONDITION_EU.text(),self.NextContent_EU.text()))

		self.Combo_Next_EU = QComboBox(self)
		self.Combo_Next_EU.addItem('')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='EU DSC':
				self.Combo_Next_EU.addItem(row['TYPE'])
		self.Combo_Next_EU.move(X11,Y_start+Y_step*17)
		self.Combo_Next_EU.setMaxVisibleItems (10)
		self.Combo_Next_EU.currentIndexChanged.connect(self.update_EU_Next)
		
		self.CONDITION_EU = QLineEdit(self)
		self.CONDITION_EU.setText("CONDITION_EU")
		self.CONDITION_EU.setGeometry(QtCore.QRect(X12, Y_start+Y_step*17, QE_length/2.35, QE_hight))
		
		self.NextContent_EU = QLineEdit(self)
		self.NextContent_EU.setText("CONSEQUENCE_EU")
		self.NextContent_EU.setGeometry(QtCore.QRect(X11, Y_start+Y_step*18, QE_length/1.775, QE_hight))
		#NA add route
		self.C_Route_NA = QPushButton('Create DR on NA  ',self)
		self.C_Route_NA.move(X1,Y_start+Y_step*19)
		self.C_Route_NA.clicked.connect(lambda:add_decide_route2op('NA',self.DRACustomerRealmName.text(),self.CONDITION_NA.text(),self.NextContent_NA.text()))

		self.Combo_Next_NA = QComboBox(self)
		self.Combo_Next_NA.addItem('')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='NA DSC':
				self.Combo_Next_NA.addItem(row['TYPE'])
		self.Combo_Next_NA.move(X11,Y_start+Y_step*19)
		self.Combo_Next_NA.setMaxVisibleItems (10)
		self.Combo_Next_NA.currentIndexChanged.connect(self.update_NA_Next)
		
		self.CONDITION_NA = QLineEdit(self)
		self.CONDITION_NA.setText("CONDITION_NA")
		self.CONDITION_NA.setGeometry(QtCore.QRect(X12, Y_start+Y_step*19, QE_length/2.35, QE_hight))
		
		self.NextContent_NA = QLineEdit(self)
		self.NextContent_NA.setText("CONSEQUENCE_NA")
		self.NextContent_NA.setGeometry(QtCore.QRect(X11, Y_start+Y_step*20, QE_length/1.775, QE_hight))

		self.IMSI2REALM = QPushButton('Add MAP_IMSI2REALM',self)
		self.IMSI2REALM.move(X1,Y_start+Y_step*21)
		self.IMSI2REALM.clicked.connect(lambda:MAP_IMSI2REALM())
		
		self.IMSI_TO_K2RREALM = QPushButton('Add MAP_IMSI_TO_K2RREALM',self)
		self.IMSI_TO_K2RREALM.move(X1,Y_start+Y_step*22)
		self.IMSI_TO_K2RREALM.clicked.connect(lambda:MAP_IMSI_TO_K2RREALM())	
		
		self.RELOADMAP = QPushButton('Reload MAP on All',self)
		self.RELOADMAP.move(X1,Y_start+Y_step*23)
		self.RELOADMAP.clicked.connect(lambda:self.RELOAD_MAPCACHES_ALLDSC())
		
		self.RELOADLIST = QPushButton('Reload LIST on All',self)
		self.RELOADLIST.move(X1,Y_start+Y_step*24)
		self.RELOADLIST.clicked.connect(lambda:self.RELOAD_LISTCACHES_ALLDSC())			

		self.ADDREAL2OP = QPushButton('Add Realm2OP on All',self)
		self.ADDREAL2OP.move(X1,Y_start+Y_step*25)
		self.ADDREAL2OP.clicked.connect(lambda:ADD_REALM2OP())
		
		self.RELOADREALM2OP = QPushButton('Reload Realm2OP on All',self)
		self.RELOADREALM2OP.move(X1,Y_start+Y_step*26)
		self.RELOADREALM2OP.clicked.connect(lambda:self.RELOAD_REALM2OP_ALLDSC())
		
		self.ONLINE_EMAIL = QPushButton('Send Email',self)
		self.ONLINE_EMAIL.move(X3,Y_start-Y_step*1+10)
		self.ONLINE_EMAIL.clicked.connect(lambda:ONLINE_EMAIL())

	def test(self):
		self.OPERATOR.setText('DDDDDDDD')
		
	def update_AP_Next(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='AP DSC':
				if row['TYPE']==self.Combo_Next_AP.currentText():
					self.NextContent_AP.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VIRTUAL_REALM.text()))
					self.CONDITION_AP.setText(row['CONDITION'])
					
	def update_EU_Next(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='EU DSC':
				if row['TYPE']==self.Combo_Next_EU.currentText():
					self.NextContent_EU.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VIRTUAL_REALM.text()))
					self.CONDITION_EU.setText(row['CONDITION'])
					
	def update_NA_Next(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']=='NA DSC':
				if row['TYPE']==self.Combo_Next_NA.currentText():
					self.NextContent_NA.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VIRTUAL_REALM.text()))
					self.CONDITION_NA.setText(row['CONDITION'])

	def create_listcache(self,region,listcachename):
		if region!= 'AP' or region!= 'EU' or region!= 'NA':
			if listcachename!='':
				Region2URL_DSC(region)
				Outputlist_1=[]
				Outputlist_2=[]
				Output1=DSC1+'+'+listcachename+':'+soap_create_listcache(SURL1,listcachename)
				Output2=DSC2+'+'+listcachename+':'+soap_create_listcache(SURL2,listcachename)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				BIOUTPUT("Create ListCache",Outputlist_1,Outputlist_2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			else:
				print('empty listcachename')
				return('empty listcachename')
		else:
			print('Wrong Region Name')
			return('Wrong Region Name')	
			
	def create_request_filter(self,region,realm_names,listname,SSID):
		Region2URL_DSC(region)
		desc_from_op=self.OPERATOR.text()+' '+SSID+': %request filter% if dest realm in LISTCACHE,let pass'
		desc_to_op=self.OPERATOR.text()+' '+SSID+': %request filter% if origin realm in LISTCACHE,let pass'
		realms=SPLIT2LIST(realm_names)
		#283-destination realm 296-oringinal realm
		condition_from_op='''(IsExist(#AVP283)&amp;&amp;InList(ToLower(AVP283),"'''+listname+'''"))'''
		condition_to_op='''(IsExist(#AVP296)&amp;&amp;InList(ToLower(AVP296),"'''+listname+'''"))'''
		for realm in realms:
		#. soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0")
			Output1='RF from OP:origin realm='+realm+'con:'+condition_from_op+':'
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_from_op,pop_name=POP,origrealm=realm,condition=condition_from_op)
			Output2='RF to OP:origin realm='+realm+'con:'+condition_from_op+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_to_op,pop_name=POP,destrealm=realm,condition=condition_from_op)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Add request filter",Outputlist_1,Outputlist_2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)

	def add_decide_route2op(self,region,realm_names,condi,cons):
		Region2URL_DSC(region)
		desc=self.OPERATOR.text()+' '+SSID+':%decide route% * to OP'
		realms=SPLIT2LIST(realm_names)
		for realm in realms:
			Output1='DR to OP:* to '+realm+' condi:'+condi+' cons:'+cons
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons)
			Output2='DR to OP:* to '+realm+' condi:'+condi+' cons:'+cons
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Add Decide route to OP",Outputlist_1,Outputlist_2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			
	def MAP_IMSI2REALM():
		realm_names=DRACustomerRealmName.text()
		if realm_names=='':
			print('empty realm')
		else:
			realmlist=SPLIT2LIST(realm_names)
			Outputlist_1=[]
			Outputlist_2=[]
			region_list=['AP','EU','NA']
			for re in region_list:
				Region2URL_DSC(re)
				for realm in realmlist:
					Output1=DSC1+':'+realm+'->MAP_IMSITOREALM'
					Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSITOREALM:',realm)
					Output2=DSC2+':'+realm+'->MAP_IMSITOREALM'
					Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSITOREALM:',realm)
					Outputlist_1.append(Output1)
					Outputlist_2.append(Output2)
					LOGTEXT=self.LOG.toPlainText()
					LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
					self.LOG.setPlainText(LOGTEXT)
				BIOUTPUT("Add Reaml to MAP_IMSITOREALM",Outputlist_1,Outputlist_2)

	def MAP_IMSI_TO_K2RREALM():
		realm_names=DRACustomerRealmName.text()
		if realm_names=='':
			print('empty realm')
		else:
			realmlist=SPLIT2LIST(realm_names)
			Outputlist_1=[]
			Outputlist_2=[]
			region_list=['AP','EU','NA']
			for re in region_list:
				Region2URL_DSC(re)
				for realm in realmlist:
					Output1=DSC1+':'+realm+'->MAP_IMSI_TO_K2RREALM'
					Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSI_TO_K2RREALM:',realm)
					Output2=DSC2+':'+realm+'->MAP_IMSITOREALM'
					Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSI_TO_K2RREALM:',realm)
					Outputlist_1.append(Output1)
					Outputlist_2.append(Output2)
					LOGTEXT=self.LOG.toPlainText()
					LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
					self.LOG.setPlainText(LOGTEXT)
				BIOUTPUT("Add Reaml to MAP_IMSI_TO_K2RREALM",Outputlist_1,Outputlist_2)

	def RELOAD_MAPCACHES_ALLDSC(self):
		region_list=['AP','EU','NA']
		for re in region_list:
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(re)
			Output1=DSC1+':reload all MAPCACHE:'
			Output1=Output1+soap_reload_mapcaches(SURL1)
			Output2=DSC2+':reload all MAPCACHE:'
			Output2=Output2+soap_reload_mapcaches(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload LISTCACHES",Outputlist_1,Outputlist_2)
			
	def RELOAD_LISTCACHES_ALLDSC(self):
		region_list=['AP','EU','NA']
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
			Output1=Output1+soap_reload_realm2OP(SURL1)
			Output2=DSC2+':reload REALM2OP:'
			Output2=Output2+soap_reload_realm2OP(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload REALM2OP",Outputlist_1,Outputlist_2)


		
	def MAP_IMSI_TO_K2RREALM():
		print('MAP_IMSI2REALM()')
		
	def ADD_REALM2OP():
		print('ADD_REALM2OP')
		
	def RELOAD_REALM2OP():
		print('RELOAD_REALM2OP()')
		
	def ONLINE_EMAIL():
		print(ONLINE_EMAIL)

	def update_online_info(self,OP):
		RealmName1=''
		NodeRealm1=''
		RealmNameBeforeTranslation1=''
		result=CCB_ONLINE2CSV()
		#print(OP)
		for row in result:
			if row['name']==OP:
				ssid=row['id']
				if row['item']=='DRACustomerRealmName':
					RealmName1=RealmName1+row['value']+','
				if row['item']=='CustomerNodeRealm':
					NodeRealm1=NodeRealm1+row['value']+','
				if row['item']=='DRACustomerRealmNameBeforeTranslation':
					RealmNameBeforeTranslation1=RealmNameBeforeTranslation1+row['value']+','
		if len(RealmName1)>1:
			if RealmName1[-1]==',':
				RealmName1=RealmName1[:-1]
		if len(NodeRealm1)>1:		
			if NodeRealm1[-1]==',':
				NodeRealm1=NodeRealm1[:-1]
		if len(RealmNameBeforeTranslation1)>1:
			if RealmNameBeforeTranslation1[-1]==',':
				RealmNameBeforeTranslation1=RealmNameBeforeTranslation1[:-1]
		self.SSID.setText(str(ssid))	
		self.DRACustomerRealmName.setText(RealmName1)
		self.DRACustomerNodeName.setText(NodeRealm1)		
		self.DRACustomerRealmNameBeforeTranslation.setText(RealmNameBeforeTranslation1)
		temp=OP.replace(' ','_').upper()
		LISTNAME='LIST_'+str(ssid)+'_'+temp
		self.LISTNAME.setText(LISTNAME)
		temp=OP.replace(' ','-')
		R2OP_NAME=str(ssid)+'#'+temp
		self.R2OP_NAME.setText(R2OP_NAME)
	def tuggle(self):
		if self.btn_direct.isChecked()==True:
			self.VIRTUAL_REALM.show()
		else:
			self.VIRTUAL_REALM.hide()
			self.VIRTUAL_REALM.setText("")	
					


		
				
class Main_TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(Main_TabWidget, self).__init__(parent)
        self.resize(1366, 768)
        self.mContent = OPEN_ROUTE()
        self.mContent2 = OP_Online()
        self.mIndex = OthersWidget()
        self.mIndex2 = OthersWidget2()
        self.addTab(self.mContent, u"Open Route")
        self.addTab(self.mContent2, u"OP_Online")
        self.addTab(self.mIndex, u"Others")
        self.addTab(self.mIndex2, u"Others2")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    t = Main_TabWidget()
    t.show()
    app.exec_()



