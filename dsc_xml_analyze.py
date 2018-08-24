"""*******************************************************************************************************

This script convert DSC config xml file into desired format

1. dscxmlpeer2csv(dsc_config_xml_name,peer_info_csv_name)
2. dscxml_ip_host(dsc_config_xml_name,ip_host_csv_name)


Author: Wind Wang
Version: v1.0 2018.08.15

*******************************************************************************************************"""
import xml.etree.ElementTree as ET
import copy
import os


def dscxmlpeer2csv(dsc_config_xml_name,peer_info_csv_name):
	tree = ET.parse(dsc_config_xml_name)
	root = tree.getroot()
	#print(root.tag)
	record={}
	result_list=[]
	keys=['display_name','name','realm','remote_ip','remote_pip','attempt_connect','maxActive',\
	'disabled','peer_test_mode','peer_mtu','local_port_range_1','local_port_range_2',\
	'local_port_range_3','local_port_range_4','local_port_range_5','local_port_range_6','local_port_range_7',\
	'local_port_range_8','MaxInboundStreams','MaxOutboundStreams']
	
	for layer1 in root:
	
		if layer1.tag=='{http://www.syniverse.com/diameter-server}Network':
			for layer2 in layer1:
				if layer2.tag=='{http://www.syniverse.com/diameter-server}Peers':
					for layer3 in layer2:
						if layer3.tag=='{http://www.syniverse.com/diameter-server}Peer':
							#add empty value to each key so they can be correctly printed in CSV even if the parameter not exist in config
							for key in keys:
								record[key]=''
							#parameters which must exist
							record['display_name']=layer3.attrib['display_name']
							record['name']=layer3.attrib['name']
							record['realm']=layer3.attrib['realm']
							record['remote_ip']=layer3.attrib['remote_ip']
							record['remote_pip']=layer3.attrib['remote_pip']
							record['attempt_connect']=layer3.attrib['attempt_connect']
							record['maxActive']=layer3.attrib['maxActive']
							#optional parameters
							try:
								record['disabled']=layer3.attrib['disabled']
							except KeyError:
								record['disabled']='Null'
							try:
								record['peer_test_mode']=layer3.attrib['peer_test_mode']
							except KeyError:
								record['peer_test_mode']='Null'
							try:
								record['peer_mtu']=layer3.attrib['peer_mtu']
							except KeyError:
								record['peer_mtu']='Null'
	
							for layer4 in layer3:#Peerconnections or PeerParameters
								if layer4.tag=='{http://www.syniverse.com/diameter-server}PeerParameters':
									for layer5 in layer4:#Inbound or Outbound
										if layer5.tag=='{http://www.syniverse.com/diameter-server}MaxInboundStreams':
											record['MaxInboundStreams']=layer5.attrib['value']
										if layer5.tag=='{http://www.syniverse.com/diameter-server}MaxOutboundStreams':
											record['MaxOutboundStreams']=layer5.attrib['value']
							
								if layer4.tag=='{http://www.syniverse.com/diameter-server}PeerConnections':
									local_port_range_index=0
									for layer5 in layer4:#Peerconnection
										local_port_range_index=local_port_range_index+1
										id='local_port_range_'+str(local_port_range_index)
										#print(layer5.tag)
										#print(layer5.attrib)
										try:
											record[id]=layer5.attrib['local_port_range']
										except KeyError:
											break
							result_list.append(copy.deepcopy(record))
	
	#there are easier way to obtain item instead of warp layer by layer
	#for item in root.iter('{http://www.syniverse.com/diameter-server}Peer'):
	#	print(item.attrib)
	
	import csv
	location_file=os.getcwd()+r'\file\xml\{0}'.format(peer_info_csv_name)
	#print(location_file)
	with open(location_file, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		string=[]
		for key in keys:
			string.append(key)
		spamwriter.writerow(string)
		for row in result_list:
			string=[]
			for key in keys:
				string.append(row[key])
			spamwriter.writerow(string)
		
def dscxml_ip_host(dsc_config_xml_name,ip_host_csv_name):
	record={}
	tree = ET.parse(dsc_config_xml_name)
	root = tree.getroot()
	content=''
	for item in root.iter('{http://www.syniverse.com/diameter-server}Peer'):
		ips=item.attrib['remote_ip']
		display_name=item.attrib['display_name']
		ip_list=ips.split(",")
		for i in ip_list:
			content=content+i+","+display_name+'\n'
	with open(ip_host_csv_name,'w') as file_object:
		file_object.write(content)
		
#test script
#filename='HKG201808130946.xml'
#dsc_config_xml_name=os.getcwd()+r'\file\xml\{0}'.format(filename)
#dscxml_ip_host(dsc_config_xml_name,'HKG_ip_host.csv'')
