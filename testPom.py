import os
output=""
fd=open("talko.txt","r")
lines=fd.readlines()


for line in lines:
	temp=line.split(":")
	if len(temp)>2:
		output=output+"<\/dependency><dependency><groupId>"+temp[1]+"<\/groupId><artifactId>"+temp[0]+"<\/artifactId><version>"+temp[2]+"<\/version><type>pom<\/type><\/dependency>"

print (output)
print ("done")
