# -*- coding: utf-8 -*-
"""
Ping tool with timestamp before response
work for windows only
Coded By Martin Verret
verret.martin@gmail.com
Python 3.0
"""
import argparse
import re
import sys
import subprocess
import datetime
import os
import socket
"""
TODO:
"""

class timePing():
	"""
	main program class
	"""
	version = 0.1
	def __init__(self):
		self.args = self.getArgs()
		self.runPing()
		
	def getArgs(self):
		"""
		function to get argument from command line
		"""
		ipRegEx = "^((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9]).(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9]))$"
		#regex to validate ip adresses
		
		parser = argparse.ArgumentParser(description="Ping tool with time")
		parser.add_argument('ip', help="IP address of host to ping")
		parser.add_argument('-o', '--output-file', help='Output file to write Result')
		parser.add_argument('-v', '--version', action='version', version='Time Ping Version {0}'.format(self.version), help='Show Version')
		args = parser.parse_args()
		
		if not re.match(ipRegEx, args.ip):# or not re.match(ipRegEx, socket.gethostbyname(args.ip)):#look if ip or domain name is valid
			try:
				if not re.match(ipRegEx, socket.gethostbyname(args.ip)):
					print("Error, ipv4 address format or hostname is invalid\r\n")
					parser.print_help()
					sys.exit(1)					
			except:				
				print("Error, ipv4 address format is invalid\r\n")
				parser.print_help()
				sys.exit(1)
					
		return args
		
	def runPing(self):
		"""
		function to run the ping command
		"""
		
		global openFile
		#create a global variable to store the open file, so we could close it when ctrl+c
		ip = self.args.ip
		file = self.args.output_file
		windowsCommand="ping -t {0} ".format(ip)#windows command, special identification in case we need other OS, -t for infinite ping
		writeToFile = False
		i = 0
		#bool to activate or desactivate the output to file
		
		if not file == None:#if output to file is selected
			if not os.path.isdir(timePing.getDir(file)) and os.path.isdir(timePing.getDir(os.path.join(os.getcwd(), file))):#test for relative path and turn it to absolute
				file = os.path.join(os.getcwd(), file)
			
			if timePing.testPath(file):#test if path exist
				testResult = timePing.testFile(file)
				
				while testResult == 2:#if file exist and we don'T overwrite add (1) to filename until file not exist
					splitedName = file.split("\\")
					fileName = splitedName[len(splitedName) - 1]
					fileName = "{0}(1).{1}".format(fileName.split(".")[0], fileName.split(".")[1])
					splitedName[len(splitedName) - 1] = fileName
					file = "\\".join(splitedName)
					testResult = timePing.testFile(file)
					
				if testResult == 1:
					#if overwrite
					openFile = open(file, 'w')
									
				if testResult == 0:
					#if create new file
					openFile = open(file, 'x')
									
				writeToFile = True#enable write to file
			
		process = subprocess.Popen(['ping', '-t {0}',format(ip)],stdout = subprocess.PIPE)#start ping command
		while True:#infinite loop to run ping until ctrl+c
			
			data = process.stdout.readline().decode('437', "replace").replace("\r\n", "")#get data and encode it for french accent			
			time = datetime.datetime.now().strftime('%H:%M:%S')#get time
			if i > 1:#skip the first line which is empty
				result = "{0} {1}".format(time, data)
				if writeToFile:#write data to file if enabled
					openFile.write(result)
					openFile.write("\r")#add carriage return
			else:
				result = data
			print(result)#print data on screen
			
			i += 1
		openFile.close()#close file
								
	def testPath(file):
		"""
		function to test if path is valid
		"""
		if not os.path.isdir(timePing.getDir(file)):
			print("Invalid path, all folder must exist")
			sys.exit(1)
		else:
			return True
	
	def getDir(file):
		"""
		function to get directory from file path
		"""
		dir = file.split("\\")
		dirLen = len(dir)
		j = 0
		dirPath = ""
		while j < dirLen - 1 :
			dirPath += "{0}{1}".format(dir[j], "\\")
			j += 1
		return dirPath
	
	def testFile(file):
		"""
		function to test if file exist
		return 0 if file exist
		return 1 if file exist but we overwrite it
		return 2 if file exist but we append a number to the file name
		"""
		if os.path.exists(file):
			overwrite = None
			while not overwrite == "y" or not overwrite == "n":
				overwrite = input("File {0} exist, do you want to overwrite it(Y/N):".format(file))
				if overwrite.lower() == "y":
					return 1
				if overwrite.lower() == "n":
					return 2
		else:
			return 0
			
if __name__ ==  "__main__":
	try:
		timePing()
	except (KeyboardInterrupt):
		try:
			openFile.close()
		except:
			pass
		sys.exit(0)