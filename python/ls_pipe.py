import os

# detect the current working directory
path = os.getcwd()

for root, dirs, files in os.walk(path):
	for directory in dirs:
		print(directory)
		#dir = os.getcwd()+"\\"+directory
		#print(dir)
		for filename in files:
			if filename.find('.java') != -1:
				print(filename)
				final = {}
				# Open file 
				fileHandler = open (dir+filename, "r")
				if file not in final:
					final[file]=[]
					while True:
					# Get next line from file
						line = fileHandler.readline()
						# If line is empty then end of file reached
						if not line :
							break;
							# How to use find()
						if (line.find('import') != -1):
							final[file].append(line)
							# Close Close
				fileHandler.close()
				print(final)   