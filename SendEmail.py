#First, install pywin32 by using "python -m pip install pypiwin32" on Windows Command console

import win32com.client as win32 




def sendemail (Tolist, Cclist, Subject, Sentence1):
	outlook = win32.Dispatch('outlook.application') 
	mail = outlook.CreateItem(0)
	mail.To = Tolist
	mail.CC = Cclist
	mail.Subject = Subject
	mail.HTMLBody=Sentence1
	#mail.Attachments.Add(r'C:\Users\g801781\Desktop\python_work\SendEmail.py')
	mail.Display()
	return(0)
	
def sende_plain_mail (Tolist, Cclist, Subject, Sentence1):
	outlook = win32.Dispatch('outlook.application') 
	mail = outlook.CreateItem(0)
	mail.To = Tolist
	mail.CC = Cclist
	mail.Subject = Subject
	mail.Body=Sentence1
	#mail.Attachments.Add(r'C:\Users\g801781\Desktop\python_work\SendEmail.py')
	mail.Display() 


#sendemail ('greg.zhai@syniverse.com;jason.qin@syniverse.com;joe.feng@syniverse.com','wind.wang@syniverse.com;ts-dss@syniverse.com', 'Test Email','This Email is sent using Python script','Now it is a just simple version as attachment, please check')
