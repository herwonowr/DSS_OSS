import time,os.path, os,shutil,tkinter.filedialog
initial_dir=r"\file\soap_output"
initial_path=os.getcwd()+initial_dir
root1=tkinter.Tk()
root1.withdraw()
full_name=tkinter.filedialog.askopenfilename(title="Chosse File",initialdir=(os.path.expanduser(initial_path)))
dir_name=os.path.split(full_name)[0]
print(dir_name)

file_name=os.path.split(full_name)[1]
root1.destroy()


with open(full_name) as file_object:
	contents=file_object.read()
output=""
s=r""" `1234567890-=~!@#$%^&*()_+qwertyuiop[]\asdfghjkl;'zxcvbnm,./!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""

for i in contents:
	for m in s:
		if i==m:
			i=""
	output=output+i
output=output.replace("\n","")
print("invalid letters are as follow:")
print(output)
output_filename="invalid_letter_in_file.txt"
output_path_file_name=dir_name+r"\invalid_letter_in_file.txt"
with open(output_path_file_name,'w') as file_object:
	file_object.write(output)
os.system("explorer.exe %s" % dir_name)


#location_file=os.getcwd()+r'\file\xml\{0}'.format(peer_info_csv_name)
	#print(location_file)
#with open(location_file, 'w',newline='') as csvfile:

