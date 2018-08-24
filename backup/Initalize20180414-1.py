# Initalize
#-*- coding: utf-8 -*-
#!/usr/bin/python3
# coding=gbk

def OSS2CSV():
	import datetime
	import pymysql.cursors
	namelist=[] 
	#连接配置信息
	config = {
		'host':'da3p-gen-opx-ctd001.syniverse.com',
		'port':3306,
		'user':'dssossreadonly',
		'password':'DsOs_4eaD',
		'db':'dss_oss',
		'charset':'utf8mb4',
		'cursorclass':pymysql.cursors.DictCursor,
		}
	# 创建连接
	connection = pymysql.connect(**config)

# 执行sql语句
	try:
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = """SELECT ss.id AS ssid, ss.customerid, ci.`name`, ci.`country`,
               (SELECT GROUP_CONCAT(`value`) FROM neinfo WHERE item = 'DRACustomerRealmName' AND pkgid = ss.id) AS realm_name,
               (SELECT GROUP_CONCAT(`value`) FROM neinfo WHERE item = 'DRAIMSIPrefix' AND pkgid = ss.id) AS imsi_prefix,
               (SELECT GROUP_CONCAT(`value`) FROM neinfo WHERE item = 'RMT Display' AND pkgid = ss.id) AS status,
               (SELECT dra FROM dssoperatorinfo WHERE ssid = ss.id) AS dra,
               (SELECT connection FROM dssoperatorinfo WHERE ssid = ss.id) AS connection,
               (SELECT coveragestatus FROM dssoperatorinfo where ssid = ss.id) AS coveragestatus,
               (SELECT productcomment FROM dssoperatorinfo where ssid = ss.id) AS productcomment,
               (SELECT commercialstatus FROM dssoperatorinfo where ssid = ss.id) AS commercialstatus,
               (SELECT owner FROM dssoperatorinfo where ssid = ss.id) AS owner,
               (SELECT region FROM dssoperatorinfo where ssid = ss.id) AS region,
               (SELECT tagid FROM dssoperatorinfo where ssid = ss.id) AS tagid,
               (SELECT technicalcomment FROM dssoperatorinfo where ssid = ss.id) AS technicalcomment  
FROM subscribedservice ss 
LEFT JOIN customerinfo ci ON ss.customerid = ci.id 
WHERE ss.service = 'Diameter_Signalling' AND ss.currentstatus IN ('Pre-commercial' , 'Commercial') 
ORDER BY ci.`country` , ci.`name`;"""
			cursor.execute(sql)
			# 获取查询结果
			results = cursor.fetchall()
			namelist_oss=[]
			for row in results:
				namelist_oss.append( row['name'] )
			#没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
 
	finally:
		connection.close();

	import csv

	with open("oss_initial_db.csv", 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		string=[]
		for keys in results[1]:
			string.append(keys)
		spamwriter.writerow(string)
		for row in results:
			string=[]
			string.append(row['ssid'])
			string.append(row['customerid'])
			string.append(row['name'])
			string.append(row['country'])
			string.append(row['realm_name'])
			string.append(row['imsi_prefix'])
			string.append(row['status'])
			string.append(row['dra'])
			string.append(row['connection'])
			string.append(row['coveragestatus'])
			string.append(row['productcomment'])
			string.append(row['commercialstatus'])
			string.append(row['owner'])
			string.append(row['region'])
			string.append(row['tagid'])
			string.append(row['technicalcomment'])
			spamwriter.writerow(string)



def RMTDB2CSV():
	import datetime
	import pymysql.cursors
	namelist=[] 
	#连接配置信息
	config = {
		'host':'hk1p-gen-dsr-mdb001.hk1.syniverse.com',
		'port':4526,
		'user':'rmttool',
		'password':'fxUT3Xku',
		'db':'dss_rmt',
		'charset':'utf8mb4',
		'cursorclass':pymysql.cursors.DictCursor,
		}
	# 创建连接
	connection = pymysql.connect(**config)

# 执行sql语句
	try:
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'select a.name,a.ssid,a.country,a.realm_name,a.imsi_prefix from lte_operator as a order by a.name'
			cursor.execute(sql)
			# 获取查询结果
			results = cursor.fetchall()
			for row in results:
				namelist.append( row['name'] )
			#没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
 
	finally:
		connection.close();

	import csv

	with open("rmtdb.csv", 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		string=[]
		for keys in results[1]:
			string.append(keys)
			#print(string)
		spamwriter.writerow(string)
		for row in results:
			string=[]
			string.append(row['ssid'])
			string.append(row['name'])
			string.append(row['country'])
			string.append(row['realm_name'])
			string.append(row['imsi_prefix'])
			spamwriter.writerow(string)




def SOAP2XML(SURL,SENV,filename):
	import requests
	headers = {'Host': ''}
	headers = {'content-type': 'text/xml'}
	headers = {'soapAction': ''}
	response = requests.post(SURL,data=SENV,headers=headers)
	with open(filename, 'w') as file_object:
		file_object.write(response.text)
	return response


def XML2CSV_LISTCACHE(XML_filename,CSV_filename):
	from xml.etree import ElementTree as ET
	import csv

	tree=ET.parse(XML_filename)
	#root = tree.getroot()
	listCaches= tree.findall('.//listCaches')
	with open(CSV_filename, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		for row in listCaches:
			string=[]
			for item in row:
				if item.tag=="listCacheName":
					string.insert(0,item.text) 
				else:
					string.append(item.text)
			spamwriter.writerow(string)


def Append_LIST_X_Any(LIST_X_Any,CSV_filename):
	import csv
	with open(CSV_filename) as f:
		reader =csv.reader(f)
		for row in reader:
			if (row[0].startswith('LIST_1')) or (row[0].startswith('LIST_2')) or row[0].startswith('LIST_3') or row[0].startswith('LIST_4') or row[0].startswith('LIST_5') or row[0].startswith('LIST_6') or row[0].startswith('LIST_7') or row[0].startswith('LIST_8') or row[0].startswith('LIST_9'):
				for exist_row in LIST_X_Any:
					match_count =0
					if row[0] != exist_row[0]:
						match_count =1
						
				if match_count == 1:
					LIST_X_Any.append(row)
	return(LIST_X_Any)


def csv2dict(in_file):
	import csv
	new_dict = {}
	with open(in_file, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		fieldnames = next(reader)
		reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
		new_dict = [row for row in reader]
	return new_dict
    
    
# Program starts here

#Define Variables for DSS OSS tool
DSC_URL_LIST=[]
DSC_URL_LIST.append(['HKG','AP','1',"http://10.162.28.186:8080/DSC_SOAP/query?"])
DSC_URL_LIST.append(['SNG','AP','2',"http://10.163.28.131:8080/DSC_SOAP/query?"])
DSC_URL_LIST.append(['AMS','EU','1',"http://10.160.28.32:8080/DSC_SOAP/query?"])
DSC_URL_LIST.append(['FRT','EU','2',"http://10.161.28.32:8080/DSC_SOAP/query?"])
DSC_URL_LIST.append(['CHI','NA','1',"http://10.166.28.200:8080/DSC_SOAP/query?"])
DSC_URL_LIST.append(['DAL','NA','2',"http://10.164.28.189:8080/DSC_SOAP/query?"])

#All ListCaches in DSC -> XML file ->CSV file -> Append LIST_XXXX_* to list

#OSS2CSV()
LIST_X_Any =[]
LIST_X_Any.append("0")
for row in DSC_URL_LIST:

	name=row[0]
	region= row[1]
	number= row[2]
	url= row[3]
	XML_filename=name+'_LISTCACHE.xml'
	#print(XML_filename)
	CSV_filename=name+'_LISTCACHE.csv'
	#print(CSV_filename)
	#SOAP2XML(url,SOAP_QueryAllListCaches,XML_filename)
	#XML2CSV_LISTCACHE(XML_filename,CSV_filename)
	Append_LIST_X_Any(LIST_X_Any,CSV_filename)
	for row in LIST_X_Any:
		print(row[0])


OSSDB=csv2dict('oss_initial_db.csv')

for row in OSSDB:
	row['LIST']='DDD'
	print(row)
	input(":")
			


	

