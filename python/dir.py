import os
import shutil
def main():
	jar_files = []                                                                                                           
	rootDir = os.getcwd()
	jar_loc = rootDir+"\\Sources"
	print(jar_loc)
	for dirName, subdirList, fileList in os.walk(jar_loc, topdown=False):
		for fname in fileList:
			if fname.find('.jar') != -1:
				jar_files.append(dirName+"\\"+fname)
	for jarDir in jar_files:
		#print (jarDir)
		rootDir = os.getcwd()
		dir = rootDir+"\\jar"
		shutil.move(jarDir, dir)

if __name__ == '__main__':
	main()
