
#-*-coding:utf-8-*-

import os
import sys
import ConfigParser
import commands
import string

reload(sys)
sys.setdefaultencoding('utf8')

config_file = os.path.split(os.path.realpath(__file__))[0] + "/config.ini"
config = ConfigParser.ConfigParser()
with open(config_file,"r") as cfgfile:
    config.readfp(cfgfile)
global pro_list
pro_list = []#将出现的问题记录在这个数组里
resultPath = '/work/guoshuman/result1'
#得到干净的路径
# def clearPath():
#    if localPath[-1] == '/':
#       localPath.rstrip('/')
#    else:
#       pass


#得到检查路径
def getPath():
    global localPath
    localPath = ''
    global topName  #顶层目录姓名
    num = 1
    if len(sys.argv) == 1:
        print "Usage:python formal_checker <DATA_ID>"

    else:
        localPath = sys.argv[num]
        # clearPath()
        topName = localPath.split('/')[-1]

# 遍历指定目录，得到目录下的所有子文件名和对应的路径
def eachFile(filepath):
    global checkFile
    global checkFilepath
    checkFile = []
    checkFilepath = []
    checkFilepath.append(filepath)
    checkFile.append(topName)
    for i in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath,i)):
            checkFilepath.append(os.path.join(filepath,i))
            checkFile.append(i)

    #checkFilepath.pop(0)
    # for i in xrange(len(checkFilepath)):
    #     checkFile.append(checkFilepath[i].split('/')[-1])

#得到每个想要检查文件的一个keywords
def fileList(filepath,filename):
    global keywords
    types = []
    typeCount = []
    typeList = []

   # num = input(u"希望检验的文件格式数目:")
    if filename in config.sections() :
        num = config.get(filename,'num')
        t_num = 0
        while t_num < int(num):
            types.append(config.get(filename,'type[%s]'%(t_num)))
            t_num += 1
        for type in types:
            typeCount.append(type + u'文件数目')
            typeList.append(type + u'文件目录')
    else:
        num = config.get('top', 'num')
        t_num = 0
        while t_num < int(num):
            types.append(config.get('top', 'type[%s]' % (t_num)))
            t_num += 1
        for type in types:
            typeCount.append(type + u'文件数目')
            typeList.append(type + u'文件目录')

    keywords = {u'所有文件数目':0,u'所有文件列表':[],u'子文件数目':0,u'子文件列表':[]}
    order = [u'所有文件数目',u'所有文件列表',u'子文件数目',u'子文件列表']
    for i in xrange(len(types)):
        keywords[typeCount[i]] = 0
        order.append(typeCount[i])
        keywords[typeList[i]] = []
        order.append(typeList[i])

    #print filepath
    pathDir = os.listdir(filepath)
    keywords[u'所有文件数目'] = len(pathDir)
    for root,dirs,files in os.walk(filepath):
        for dir in dirs:
            keywords[u'子文件列表'].append(dir)
    keywords[u'子文件数目'] = len(keywords[u'子文件列表'])
    for allDir in pathDir:
        keywords[u'所有文件列表'].append(os.path.join('%s'%(allDir)))
        for i in xrange(len(types)):
            if types[i] in allDir:
                keywords[typeCount[i]] += 1
                keywords[typeList[i]].append(os.path.join('%s'%(allDir)))


#对不符合数量要求的文件进行报错，命名格式不正确的文件进行重命名并且提出警告
def chargeNm(filepath,filename):
    types = []
    typeCount = []
    typeList = []
    #fileNum = config.get(filename, 'fileNum')
    if filename in config.sections() :
        fileNum = config.get(filename, 'fileNum')
        #totalNum = config.get(filename, 'totalNum')
        num = config.get(filename,'num')
        t_num = 0
        while t_num < int(num):
             types.append(config.get(filename,'type[%s]'%(t_num)))
             t_num += 1
        for type in types:
             typeCount.append(type + u'文件数目')
             typeList.append(type + u'文件目录')
        #totalNumber(filepath, filename, types, keywords[u'所有文件列表'])

    else:
         fileNum = config.get('top', 'fileNum')
         num = config.get('top', 'num')
         t_num = 0
         while t_num < int(num):
             types.append(config.get('top', 'type[%s]' % (t_num)))
             t_num += 1
         for type in types:
             typeCount.append(type + u'文件数目')
             typeList.append(type + u'文件目录')
    if fileNum :
        for type in typeCount:
            #if '.' in type:
            if keywords[type] == int(fileNum):
                if '.' in type:
                    origin = keywords[type.split('文件数目')[0]+'文件目录'][0].split(type.split('文件数目')[0])[0]
                    if origin == topName:
                        pass
                    else:
                        print u"RENAME: %s -> %s" %(filename,topName)
                        #pro_list.append("Warning:Path:%s ,%s file %s has wrong name,have renamed %s"%(filepath,type.split('文件数目')[0],filename,topName))
                        swapName(filepath,origin,topName,type.split('文件数目')[0])

            elif keywords[type] == 0 :
                print u"File Missing: '%s%s'文件不存在."%(filepath,type.split('文件数目')[0])
                #pro_list.append("Error:Path:%s ,don't have %s file."%(filepath,type.split('文件数目')[0]))
            else:
                print u"File Redundancy: There are more then %s files in '%s'."%(type.split('文件数目')[0], filepath)
                print keywords[type.split('文件数目')[0]+'文件目录']
                #pro_list.append("Error:Path:%s ,have more %s file.  %s"%(filepath,type.split('文件数目')[0],keywords[type.split('文件数目')[0]+'文件目录']))

#对speech文件进行单独判断和处理
def speechCheck(filepath,filename):
    if filename == 'speech':
        if keywords[u'.pcm文件数目'] == 0:
            pass
        else :
            print u"Speech Format: There are %s 'pcm' files in directory %s/%s." %(keywords[u'.pcm文件数目'],filepath,filename)
           #pro_list.append('Warning:Pah:%s. Name:%s have %s .pcm file. have convert pcm to wav with:sox -r 16000 -s -b 16 -c 2'%(filepath,filename,keywords[u'.pcm文件数目']))
            #os.popen("bash trancePcm.sh %s"%(filepath))
            



#得到txt路径，得到info路径，得到对应的wav路径
def txtinfoCheck(filepath,filename):
    global txtpath
    global infopath
    global wavpath
    if filename == 'annotation':
        if keywords[u'.txt文件数目'] == 1:
            txtpath = os.path.join(filepath,'%s.txt' % (topName))
        # txtpath = filepath + "/" + '*.txt'
        else:
            txtpath = ''
    if filename == topName :
        if keywords[u'.info文件数目'] == 1:
            infopath = os.path.join(filepath,'%s.info'%(topName))
        else:
            infopath = ''
    if filename == 'speech':
            wavpath = filepath


#判断目录下是否有多的不需要的文件
def totalNumber(filepath,filename,types,typelist):
    wrongfile = typelist
    if len(types) == 0:
        pass
    else:
        #print typelist
        for type in types:
             for list in typelist:
                 #print list
                 if '.' in list:
                     print list.split('.')[-1]#为什么这句话对有的文件适用有的就不适用
                     if  list.split('.')[-1] == type.split('.')[-1]:
                         print list
                         #print type.split('.')[-1]
                         wrongfile.remove(list)
                 else :
                     if list == type:
                         wrongfile.remove(list)
                         #count += 1

        #print wrongfile
        for wrong in wrongfile:
             print "Error:path %s has other files %s"%(filepath,wrong)
        # if count == int(0):
        #     for wrong in wrongfile:
        #         print "Error:path %s name %s has other files %s"%(filepath,filename,wrong)
        # else:
        #     pass




#换名字，filepath+filename换名为changename
def swapName(filepath,wrongname,changeName,type):
    #orifile = os.path.join(filepath,wrongname,'%s'%(type))
    #chafile = os.path.join(filepath,changeName,'%s'%(type))
    orifile = filepath + '/' + wrongname + '%s'%(type)
    chafile = filepath + '/' + changeName + '%s'%(type)
    os.rename(orifile,chafile)


def differ(filepath,wavpath,type):
    wav = []
    fil = []
    #os.system("sed -i 's/.pcm/.wav/'  %s"%(filepath))
    os.system("awk '{if (!seen[$1]++) {print $1}}' %s>/tmp/middle.txt"%(filepath))
    if os.path.isdir(wavpath):
        wav = os.listdir(wavpath)
    if os.path.isfile('/tmp/middle.txt'):
        text = open('/tmp/middle.txt', 'r')
        for fr in text.readlines():
            if not '.wav' in fr:
                pass
            else:
                fil.append(fr.strip())
    os.remove('/tmp/middle.txt')
    dif = set(wav).difference(set(fil))
    #dif1 = set(fil).difference(set(wav))
    if len(dif) != 0:
        print "wav:%s files. %s:%s files"%(len(wav),type,len(fil))
    if len(dif) > 0:
        #print len(dif)
        #print "Error:missing %s file in %s compire with speech:"%(len(dif),type)
        pro_list.append("Error:missing file in %s compire with speech:"%(type))
        for dir in dif:
            pro_list.append(dir)
    dif1 = set(fil).difference(set(wav))
    if len(dif1) > 0:
        #print "Error:missing %s file in speech compire with %s:"%(len(dif),type)
        #print "Error:missing file in speech compire with %s:" % (type)
        pro_list.append("Error:missing file in speech compire with %s:" % (type))
        for dir in dif1:
            pro_list.append(dir)

#检查info文件是否有表头，第一列是否为.wav，如果不是的话提醒
def checkinfo(info):
    count = 0
    with open(info) as content:
        for line in content:
            line = line.decode("utf-8")
            count += 1
            fields = line.split('\t')
            if (count != 1 and not '.wav' in fields[0]):
                print u"ERROR: 属性文件第%s行不含'.wav'" %(count)
            elif (count == 1 and '.wav' in fields[0]):
                print u"ERROR: 属性文件不含表头."

#检查txt文件是不是4列，不是4列给出提醒，检查txt文件每列是否有内容，并且比较四列时时间的大小
def checktxt(txt):
    count = 0
    num_field = 0
    with open(txt) as content:
        for line in content:
            line = line.decode("utf-8")
            count += 1
            fields = line.split('\t')
            if (count != 1 and not '.wav' in fields[0]):
                print u"标注文件第%s行不含'.wav'" %(count)
            if (int(count) == int(1)):
                num_field = len(fields)
            if(int(num_field) == int(4)):
                if ( len(fields) == num_field ):
                    if(float(fields[1]) < float(fields[2])):
                        pass
                    else:
                        print "Error:%s row %s wrong time.%s > %s"%(txt,count,fields[1],fields[2])
                       
                else:
                    print "Error:%s row %s absent content."%(txt,count)
            elif(int(num_field) == int(2)):
                if (int(count) == int(1)):
                    print "Error:%s only has 2 column."%(txt)
                if( len(fields) != num_field ):
                    print "Error:%s row %s absent content."%(txt, count)
            else:
                if(int(count) == int(1)):
                    print "Error:%s has %s column."%(txt,len(fields))




#打印列表内容到txt文件中
def printList(result,filename,prolist):
    with open(os.path.join(result,'%s.txt'%(filename)), 'wb') as out:
        for str in prolist:
            out.write(str)
            out.write('\r\n')


#检验.desc文件中的目录编号是否与所在目录名称一致
def check_data_id(localPath,topName):
	desc_file = os.path.join(localPath,topName + '.desc')
	print desc_file
	with open(desc_file) as f:
		for line in f:
			line = line.strip().decode('utf-8')
			#找到数据编号对应的行
			if (string.find(line,u'数据编号') !=-1):
				print line
				origin_id = line.split('\t')[1]
				print topName + '\n' + origin_id
				if (topName == origin_id):
					print u'数据编号'+'is correct!'
				else:
					line.replace(origin_id,topName)
					print 'EROOR!' + u'数据编号修改：' + origin_id + '-->' + topName


if __name__ == '__main__':
    getPath()
    if os.path.isdir(localPath):
        eachFile(localPath)
        count_a = 0
        print u"数据ID：" + localPath
        for i in xrange(len(checkFile)):
            if checkFile[i] == topName:
                fileList(checkFilepath[i],checkFile[i])
                chargeNm(checkFilepath[i], checkFile[i])
                txtinfoCheck(checkFilepath[i], checkFile[i])
                speechCheck(checkFilepath[i], checkFile[i])
            elif checkFile[i] == 'annotation':
                fileList(checkFilepath[i], checkFile[i])
                chargeNm(checkFilepath[i], checkFile[i])
                txtinfoCheck(checkFilepath[i], checkFile[i])
                speechCheck(checkFilepath[i], checkFile[i])
                count_a += 1
            elif checkFile[i] == 'speech':
                fileList(checkFilepath[i], checkFile[i])
                chargeNm(checkFilepath[i], checkFile[i])
                txtinfoCheck(checkFilepath[i], checkFile[i])
                speechCheck(checkFilepath[i], checkFile[i])
            elif checkFile[i] == 'doc':
                fileList(checkFilepath[i], checkFile[i])
                chargeNm(checkFilepath[i], checkFile[i])
                txtinfoCheck(checkFilepath[i], checkFile[i])
                speechCheck(checkFilepath[i], checkFile[i])
            else:
                print u"Error:多出以下文件夹%s."%(checkFile[i])
        if count_a == 0:
            txtpath = ''
        if len(txtpath) == 0 :
            pass
        else:
            checktxt(txtpath)
            differ(txtpath,wavpath,'txt')
            #print "missing file in txt compire with speech:"
            #os.system("bash txt_check.sh %s %s %s" % (txtpath,wavpath,resultPath + '/' +'%s.txt'%(topName)))
        if len(infopath) == 0:
            pass
        else:
            checkinfo(infopath)
            differ(infopath,wavpath,'info')
            #os.system("bash info_check.sh %s %s %s" % (infopath,wavpath,resultPath + '/' +'%s.txt'%(topName)))
        #printList(resultPath, topName, pro_list)
	check_data_id(localPath,topName)
    else:
        print u"数据ID：'" + localPath + u"'不存在"

