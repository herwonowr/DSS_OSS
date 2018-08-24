#coding:utf-8



# -*- coding: utf-8 -*-
import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
import getpass

user_name = input("Please input your GID: ")
password = getpass.getpass("Please input your password: ")
user_name = "g707446"
password = "Ysyhl9t#!@"

ip_add = input("Please input the IP address: ")
ip_add = ip_add.strip()

#firewall_ip_addresses = {
#	'HK Firewall':'173.209.220.113',
#	'SG Firewall':'173.209.221.113',
#	'AMS Firewall':'173.209.215.97',
#	'FRT Firewall':'173.209.215.161',
#	'CHI Firewall':'131.166.129.113',
#	'DAL Firewall':'131.166.129.145',
#	}


firewall_ip_addresses = [
	'173.209.220.113',
	'173.209.221.113',
	'173.209.215.97',
	'173.209.215.161',
	'131.166.129.113',
	'131.166.129.145',
	]


def get_router_hostname(ip_add):
	for ip in firewall_ip_addresses:
		if ip_add == ip:
			alert = "this is IP address of firewall: " + ip_add
			print(alert)
			break
		else:
			try:
				auth=HTTPBasicAuth(user_name,password)
				url_query ="http://10.12.7.109:8581/odata/api/routers?$filter=((interfaces/IPAddresses eq"+" "+"'"+ip_add+"'))"
				r=requests.get(url= url_query,auth=auth)
				#print(r.text)
				t = r.text
				list = t.split(',')
				#print(t)
				#print(list[19])
				print("The route below owns the IP address "+ ip_add + ":\n"+list[19])
				break
			except IndexError:
				msg = "this IP could not be found on Netqos: " + ip_add
				print(msg)
				break


get_router_hostname(ip_add)

