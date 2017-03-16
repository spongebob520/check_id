#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import string

speech_id=sys.argv[1]
print speech_id
current_dir=os.getcwd()
print current_dir
#speech_id对应的文件夹的路径
folder_dir=os.path.join(current_dir,speech_id)
print folder_dir

#判断speech—_id对应的目录是否存在
if not os.path.exists(folder_dir):
	print'ERROER:file does not exit！'
else:
	desc_file=os.path.join(folder_dir,speech_id+'.desc')
	print desc_file
	with open(desc_file) as f:
		for line in f:
			line=line.strip().decode('utf-8')
			#找到数据编号对应的行
			if(string.find(line,u'数据编号') != -1):
				print line
				origin_id=line.solit('\t')[1]
				if(speech_id==origin_id):
					print 'Correct!'
				else:
					line.replace(origin_id,speech_id)
					print 'ERROR!'+origin_id+'-->'+speech_id
