with open('diameter-hkdsc20180809.xml') as file_object:
	contents=file_object.read()
	contents=contents.replace('\n        ','')
	contents=contents.replace('\n          ','')
	lines=contents.split('\n')
	for row in lines:
		if row.startswith('      <Peer display_name=') and 'syniverse' in row:
			print(row)
			input('ddd')
