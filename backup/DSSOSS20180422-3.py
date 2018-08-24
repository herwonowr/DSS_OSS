
# coding=gbk
import csv
import os, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QComboBox,QPushButton
from PyQt5 import QtCore
from Initalize20180421 import *
from soap_all_commands_for_dsc import soap_reload_rule_engine,soap_add_decide_route,soap_add_list_cache,soap_reload_listcaches,soap_check_decide_route
from file_transaction import *
import os
if not os.path.exists(r'.\\file\DB.csv'):
	INITIALIZE_DB()

def NEW_EMAIL2PEER(POLICY,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
	print(POLICY+OP_A+REALM_A+IMSI_A+OP_B+REALM_B+IMSI_B)
	
def BACKUP_DB():
	file_list=['DB.csv','HKG_LISTCACHE.csv']
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
PEERINGPOLICY=csv2dict('PeeringPolicy.csv')
DRAlist=['HKG','AMS','CHI','SNG','FRT','DAL']
RegionList=['AP','EU','NA']

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
		global SURL1,SURL2,DSC1,DSC2
		if Region =="AP":
			SURL1="http://10.162.28.186:8080/DSC_SOAP/query?"
			SURL2="http://10.163.28.131:8080/DSC_SOAP/query?"
			DSC1="HKG"
			DSC2="SNG"
		if Region =="EU":
			SURL1="http://10.160.28.32:8080/DSC_SOAP/query?"
			SURL2="http://10.161.28.32:8080/DSC_SOAP/query?"
			DSC1="AMS"
			DSC2="FRT"		
		if Region =="NA":
			SURL1="http://10.166.28.200:8080/DSC_SOAP/query?"
			SURL2="http://10.164.28.189:8080/DSC_SOAP/query?"
			DSC1="CHI"
			DSC2="DAL"

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
			Outputlist_1.append(source_realm+"->"+dest_realm)
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			if Output1==None:
				Output1="None"
			Outputlist_1.append(Output1)
			
			Outputlist_2.append(source_realm+"->"+dest_realm)
			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			if Output2==None:
				Output2="None"
			Outputlist_2.append(Output2)
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
			#response="Success!!"
			response=realm+" "+response
			Outputlist_1.append(response)
			
			response=soap_add_list_cache(LIST_Name,realm,SURL2)
			#response="Success!!"
			response=realm+" "+response
			Outputlist_2.append(response)
			
		BIOUTPUT('Add ListCache',Outputlist_1,Outputlist_2)
		
def K2R(Region,Realms2,List1,Realms1,Name1,Name2):
	
	if Region=='':
		MESSAGE_OUTPUT("Error","Empty Region")
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Realms2")
	Region2URL_DSC(Region)
	Outputlist_1=[]
	Outputlist_2=[]
	
	if Region =='NA':
		#Verison K2R route on NA DSC
		if Name1 =='Verizon Wireless' or Name2 =='Verizon Wireless':
			if Name1 =='Verizon Wireless':
				Realms = SPLITLIST(Reams2)
			if Name2 =='Verizon Wireless':
				Realms = SPLITLIST(Reams1)
			print(Realms)
			for realm in Realms:
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL1)
				#response="Success!!"
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_1.append(response)
				
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL2)
				#response="Success!!"
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_2.append(response)
				
			BIOUTPUT('Add ListCache LIST_VERIZON_WIRELESS_K2R_RP_REALM',Outputlist_1,Outputlist_2)
		else:
			#NA K2R create RF for all realms
			for realm1 in Realms1:
				for realm2 in Realms2:
					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response=Name1+':'+realm1+'>'+Name2+':'+realm2+'RF '+response
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response=Name1+':'+realm1+'>'+Name2+':'+realm2+'RF '+response
					Outputlist_2.append(response)

			for realm2 in Realms2:
				for realm1 in Realms1:
					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response=Name1+':'+realm1+'>'+Name2+':'+realm2+'RF '+response
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response=Name1+':'+realm1+'>'+Name2+':'+realm2+'RF '+response
					Outputlist_2.append(response)					
			
			BIOUTPUT('Add K2R Filter on NA DSC',Outputlist_1,Outputlist_2)

	elif Region == 'AP' or Region == 'EU':
		ADD_REALMS2LIST(Region,Realms2,LIST1)		
				
			
	
#soap_check_decide_route(dsc_url,source_host,source_realm,dest_host,dest_realm,adjacent_source_peer,adjacent_source_realm)

#open route window layout
class OPEN_ROUTE(QWidget):
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
		
		self.UPD_DB = QPushButton('BACKUP_DB',self)
		self.UPD_DB.move(X11,Y_start+Y_step*0)
		self.UPD_DB.clicked.connect(lambda:BACKUP_DB())
		
		self.UPD_DB = QPushButton('Restore_DB',self)
		self.UPD_DB.move(X12,Y_start+Y_step*0)
		self.UPD_DB.clicked.connect(lambda:RestoreFile(".\\backup",".\\"))
#RULE ENGINE BUTTON		
		self.Lable_DB_DATE = QLabel("RULE_Date",self)
		self.Lable_DB_DATE .move (X10,Y_start+Y_step*1)		
		self.DB_DATE = QLineEdit(self)
		#GetFileDate(filename)
		#self.DB_DATE.setText(GetFileDate("DB.csv"))
		self.DB_DATE.setGeometry(QtCore.QRect(X11, Y_start+Y_step*1, QE_length/3.9, QE_hight))
		
		self.UPD_DB = QPushButton('UPD_RULE',self)
		self.UPD_DB.move(X10,Y_start+Y_step*2)
		self.UPD_DB.clicked.connect(self.UPDATE_DB)
		
		self.UPD_DB = QPushButton('BACKUP_RULE',self)
		self.UPD_DB.move(X11,Y_start+Y_step*2)
		self.UPD_DB.clicked.connect(self.UPDATE_DB)
		
		self.UPD_DB = QPushButton('Restore_RULE',self)
		self.UPD_DB.move(X12,Y_start+Y_step*2)
		self.UPD_DB.clicked.connect(lambda:RestoreFile(".\\backup",".\\"))
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
		self.Provisoned.clicked.connect(lambda: PROVISONED_EMAIL2PEER(self.Combo_SCENARIO.currentText()))

		#PEERINGPOLICY=csv2dict('PeeringPolicy.csv')
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
		
		#self.Lable_HUB_A = QLabel("HUB_A",self)
		#self.Lable_HUB_A.move(X1,Y_start+Y_step*8)		
		#self.HUB_A = QLineEdit(self)
		#self.HUB_A.setText("")
		#self.HUB_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*8, QE_length, QE_hight))
		
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
		self.Owner_B.setGeometry(QtCore.QRect(X2,Y_start+Y_step*6, QE_length/4, QE_hight))
		
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

		self.K2R_B_Reams2B_LIST = QPushButton('K2R_A_Realms2B_List/ADD RequestFilter/UPD vzw LIST',self)
		self.K2R_B_Reams2B_LIST.move(X3,Y_start+Y_step*20)
		self.K2R_B_Reams2A_LIST.clicked.connect(lambda: K2R(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.LIST_B.displayText(),self.realm_B.displayText(),self.OP_B.displayText(),self.OP_A.displayText()))

	def update_POLICY(self):
		#PEERINGPOLICY=csv2dict('PeeringPolicy.csv')
		for row in PEERINGPOLICY:
			if row['SCENARIO']==self.Combo_SCENARIO.currentText():
				self.POLICY.setText(row['SVR_PEER']+'-'+row['HUB_PEER'])
			

	def update_A(self,ii):
		OPA_Name = self.Combo_Select_A.currentText()
		self.OP_A.setText(OPA_Name)

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
				#self.HUB_A.setText(row["hub"])
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
				#self.HUB_B.setText(row["hub"])
				self.HUB_PLOICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.TADIG_B.setText(row["tagid"])
				self.Combo_Region_B.currentIndex=1

## code for OPB only end



		
	def rebuild_A_list(self):
		list=[]
		key= self.OP_A.text()
		print(key)
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_A.clear()
		for i in list:
			self.Combo_Select_A.addItem(i)
			
				
		print(self.OP_A.text)
		print(list)

	def rebuild_B_list(self):
		list=[]
		key= self.OP_B.text()
		print(key)
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_B.clear()
		for i in list:
			self.Combo_Select_B.addItem(i)




	def Reload_RULE(self,region):
		print("RELOAD RULE "+region)	

	def UPDATE_DB(self):
		print("DB updated")

	
class OthersWidget(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget, self).__init__(parent)
		self.setStyleSheet("background: blue grey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)


class Main_TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(Main_TabWidget, self).__init__(parent)
        self.resize(1366, 768)
        self.mContent = OPEN_ROUTE()
        self.mIndex = OthersWidget()
        self.addTab(self.mContent, u"Open Route")
        self.addTab(self.mIndex, u"Others")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    t = Main_TabWidget()
    t.show()
    app.exec_()
    input("ddd")


