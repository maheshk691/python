import os
output=""
fd=open("ref-list.txt","r")
lines=fd.readlines()
pomFilePath="/home/vsamanth/mahesh/pom.xml"

for line in lines:
	temp=line.split(":")
	if len(temp)>2:
		output=output+"</dependency><dependency><groupId>"+temp[1]+"</groupId><artifactId>"+temp[0]+"</artifactId><version>"+temp[2]+"</version><type>pom</type></dependency>"
os.system("sed -i 's/</dependency>/"+output+"/g' "+pomFilePath)
print (output)
print ("done")

