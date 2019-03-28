#!/usr/bin/env python
import os,sys
path = os.getcwd()
files = os.listdir(path)

for name in files:
    full_path = os.path.join(path, name)
    print(full_path)
 	    
    if os.path.isdir(full_path):
    	print('    dir')
    	f = os.listdir(full_path)
    	for n in f:
    		u = os.path.join(full_path, n)
    		print(u)
    		if os.path.isdir(full_path):
    			print('    dir')
    			f = os.listdir(full_path)
    			for n in f:
    				u = os.path.join(full_path, n)
    				print(u)
    		elif os.path.isfile(full_path):
    			print('    file')

        