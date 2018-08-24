# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys  
import time  

global driver

def rmt_route_edit(url,flag,username,password):
	global driver
	#Login RMT
	if flag==0:
		driver = webdriver.Firefox()
	try:
		driver.get(url)  
	#except selenium.common.exceptions.WebDriverException, ConnectionAbortedError:
	except:
		driver = webdriver.Firefox()
		driver.get(url)
		elem_user = driver.find_element_by_name("username")  
		elem_user.send_keys(username)  
		elem_pwd = driver.find_element_by_name("password")  
		elem_pwd.send_keys(password)  
		#time.sleep(3) 
		while True:
			try:
				elem_pwd.send_keys(Keys.RETURN)
			except:
				pass
			else:
				break 

	if flag==0:
		#input username/password
		elem_user = driver.find_element_by_name("username")  
		elem_user.send_keys(username)  
		elem_pwd = driver.find_element_by_name("password")  
		elem_pwd.send_keys(password)  
		#time.sleep(1) 
		while True:
			try:
				elem_pwd.send_keys(Keys.RETURN)
			except:
				pass
			else:
				break  
	
	#time.sleep(3) 
		#driver.find_element_by_xpath('//a[text()="testsaveas.zip"]').click()  
		#driver.find_element_by_partial_link_text('"Rogers Wireless","Viaero').click()
	while True:
		try:
			driver.find_element_by_partial_link_text('Edit').click()
		except selenium.common.exceptions.NoSuchElementException:
			pass
		else:
			break


#rmt_route_edit("https://dssrmt.syniverse.com/rmt/route?oSsid=6731&oCountry=&oRealHub=&rSsid=12614&rCountry=&rRealHub=&priority=&status=",0,'Jason','JasonRMT')
"""
time.sleep(3)
rmt_route_edit("https://dssrmt.syniverse.com/rmt/route?oSsid=6731&oCountry=&oRealHub=&rSsid=12663&rCountry=&rRealHub=&priority=&status=",1,'Jason','JasonRMT')
time.sleep(3)


rmt_route_edit("https://dssrmt.syniverse.com/rmt/route?oSsid=6731&oCountry=&oRealHub=&rSsid=12663&rCountry=&rRealHub=&priority=&status=",2,'Jason','JasonRMT')
time.sleep(3)
rmt_route_edit("https://dssrmt.syniverse.com/rmt/route?oSsid=6731&oCountry=&oRealHub=&rSsid=12663&rCountry=&rRealHub=&priority=&status=",3,'Jason','JasonRMT')
time.sleep(3)
rmt_route_edit("https://dssrmt.syniverse.com/rmt/route?oSsid=6731&oCountry=&oRealHub=&rSsid=12663&rCountry=&rRealHub=&priority=&status=",4,'Jason','JasonRMT')"""


def rmt_route_comment_directOP_when_update_peer(url,username,password,comment):
	global driver
	#Login RMT
	try:
		driver.get(url)  
	#except selenium.common.exceptions.WebDriverException, ConnectionAbortedError:
	except:
		driver = webdriver.Firefox()
		#print(dir(driver))
		home_handle = driver.current_window_handle
		
		driver.get(url)
		
	elem_user = driver.find_element_by_name("username")  
	elem_user.send_keys(username)  
	elem_pwd = driver.find_element_by_name("password")  
	elem_pwd.send_keys(password)  
 
	while True:
		try:
			elem_pwd.send_keys(Keys.RETURN)
		except:
			pass
		else:
			break 


		
	while True:
		try:
			driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td[16]/a[1]').click()  
		except selenium.common.exceptions.NoSuchElementException:
			pass
		else:
			break

	all_handles = driver.window_handles
	#print('home window+loction window')
	#print(all_handles)

	for handle in all_handles:
		if handle != home_handle:
			driver.switch_to_window(handle)
		#print('Window now is: '+handle)
		
		
	while True:
		try:
			driver.find_element_by_id("comment1").click()
			driver.maximize_window()
		except:
			pass
		else:
			break

	while True:
		try:
			driver.find_element_by_id("comment1").clear()
		except :
			pass
		else:
			break
	while True:
		try:
			driver.find_element_by_id("comment1").send_keys(comment)
		except :
			pass
		else:
			break


#rmt_route_comment_directOP_when_update_peer("https://dssrmt.syniverse.com/rmt/route?oSsid=6869&oCountry=&oRealHub=&rSsid=6855&rCountry=&rRealHub=&priority=&status=","Wind","abc123","test")

