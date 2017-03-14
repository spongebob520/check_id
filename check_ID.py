#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re

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
			line=line.strip()
			#找到数据编号对应的行
			pattern=re.compile(u'[\u6570][\u636E][\u7F16][\u53F7]:|：\s+(.+)')
			ID_num=pattern.findall(line.strip().decode('utf8'))
			print ID_num[0].encode('utf8')
			if(speech_id==ID_num):
				print 'Correct!'
			else:
				print 'aaa'
				line.replace(ID_num,speech_id)
				print 'ERROR!'+ID_num+'-->'+speech_id
