import os
import shutil
import csv
def main():
	jar_files = []                                                                                                           
	rootDir = os.getcwd()
	jar_loc = rootDir+"\\jar"
	#print(jar_loc)
	for dirName, subdirList, fileList in os.walk(jar_loc, topdown=False):
		for fname in fileList:
			if fname.find('.jar') != -1:
				jar_files.append(dirName+"\\"+fname)
	#print(jar_files)
	java_files = []    
	count=0        
	fileLine=""                                                                 
	for jarDir in jar_files:
		#print (jarDir)
		rootDir = os.getcwd()
		tempFileName=jarDir.split("\\")[-1][:-4]

		dir = rootDir+"\\jar\\"+tempFileName
		count=count+1	
		#print(dir)
		os.mkdir(dir)
		os.chdir(dir)
		#rootDir = os.getcwd()
		#print(rootDir)
		os.system("\"C:\\Program Files\\Java\\jdk-11.0.2\\bin\\jar.exe\" xf "+jarDir)
		os.remove(jarDir)
		for dirName, subdirList, fileList in os.walk(rootDir+"\\jar", topdown=False):
			for fname in fileList:
				if fname.find('.java') != -1:
					java_files.append(dirName+"\\"+fname)
		#print(java_files)

		final = {}
		talkoOutput={}
		count=0
		for file in java_files:
			count=0
			fileHandler = open (file, "r")
			while True:
				line = fileHandler.readline()
				if not line :
					break;
				if count>100:
					break
				if file not in final:
					final[file] = []
				if (line.find('import') != -1):
					talkoOutput[file]=[]
					final[file].append(line)
				count=count+1
			fileHandler.close()
		#print(final)

		taco_lists = []
		compare = []
		os.chdir(rootDir)
		f = open('Java_package.txt', 'r')
		f = f.readlines()
		for x in f:
			taco_lists.append(x)
		#print(taco_lists)
		
		for file in final:
			for line in final[file]:
				for stmt in taco_lists:
					temp=stmt.split(" ")[1][:-1]
					#print (temp)
					if temp in line:
						talkoOutput[file].append(line[:-2].split()[1])
		#print(jarDir)

		for i in talkoOutput:
			if (len(talkoOutput[i]))>1:
				print(i,talkoOutput[i])
				fileLine=fileLine+i+","
				for line in talkoOutput[i]:
					fileLine=fileLine+line+","
				fileLine=fileLine[:-1]+"\n"
		 
			
				#print("Yes")
		#os.remove(rootDir+"\\jar\\temp\\*")
		#shutil.rmtree(dir)
	fd= open(rootDir+'\\end.csv', 'w+')
	fd.write(fileLine)

if __name__ == '__main__':
	main()