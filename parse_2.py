# coding=UTF-8

import sys
import re
import math

#class declaration
class info:
	def get_second(self):
		second=int(self.time[0:2])*60*60*1000+int(self.time[3:5])*60*1000+int(self.time[6:8])*1000+int(self.time[9:12])
		return second
	def get_ec_no(self):
		return (int(self.ec_no,0)/4-int('0xffff',0)/4)
	def get_rscp(self):
		return (int(self.rscp,0)/4-int('0xffff',0)/4)		
#	pass

# test_pattern setting
test_pattern1=r'MSG_ID_CPHY_MEASUREMENT_CELL_IND'
# test time
test_pattern2=r'\d+:\d+:\d+:\d+'
test_pattern3=r'ec_no ='
test_pattern4=r'rscp ='
test_pattern5=r'\w*0x\w+'
#cell id
test_pattern6=r'psc ='
# in/out file declare
infile=open(sys.argv[1],'r')
outfile=open(sys.argv[2],'wb')
outfile2=open(sys.argv[3],'wb')

# dictionary, list, class declaration
result={}
string={}
time={}
ec_no={}
rscp={}
temp_list=[]


#index declare
i=0
time_index=0;
ec_no_index=0;
rscp_index=0;
total_lines=0
cell_nums=0;
times=""
ec_nos=""
rscps=""


# lock flag declare
flag1=False
flag2=False


#file input
while True :
	string[i]=infile.readline()
	if not string[i]:
		break
	i=i+1
total_lines=i


#parsing
for i in range(0,total_lines):	
	# set lock1
	if cell_nums == 32:
		flag1=False
		cell_nums=0
    # test pattern1	
	match1=re.search(test_pattern1,string[i],re.M|re.I)
	if match1:
		flag1=True
		match2=re.search(test_pattern2,string[i])
		times=match2.group()
		time[time_index]=match2.group()
		time_index=time_index+1
		
	#test lock1

	if flag1:
		# test ec_no pattern
		match1=re.search(test_pattern3,string[i],re.M|re.I)
		if match1:
			#extract value
			match2=re.search(test_pattern5,string[i],re.M|re.I)
			if match2:
				flag2=True
				ec_nos=match2.group()
				ec_no[ec_no_index]=match2.group()
				ec_no_index=ec_no_index+1
		# test lock2
		if flag2:
			# test RSCP pattern
			match1=re.search(test_pattern4,string[i],re.M|re.I)
			if match1:
				#extract value
				match2=re.search(test_pattern5,string[i],re.M)
				if match2:
					rscps=match2.group()
					rscp[rscp_index]=match2.group()
					rscp_index=rscp_index+1
		if flag2:
			# test PSC pattern
			match1=re.search(test_pattern6,string[i],re.M|re.I)					
			if match1:
				#extract value
				match2=re.search(test_pattern5,string[i],re.M)
				if match2:
					cell_nums=cell_nums+1
					flag2=False
					psc=match2.group()
					if psc != '0x0000':
						check=result.get(psc)
						if check:
							temp_list=result[psc]
						temp=info()
						temp.time=times
						temp.ec_no=ec_nos
						temp.rscp=rscps
						temp_list=temp_list+[temp]
						result[psc]=temp_list
						temp_list=[]
					
infile.close()


for key, value in result.iteritems():
	#outfile.write(str(int(key,0))+'\n')
	temp_list=[]
	temp_list=result[key]
	for value in temp_list:
		#print str(value.time)+" "+str(value.ec_no)+" "+str(value.rscp)
		outfile.write(str(int(key,0))+" "+str(value.get_second())+" "+str(value.get_ec_no())+" "+str(value.get_rscp())+'\n')

# can sort over there 2014/10/28
s=time[0]
initial_time=int(s[0:2])*60*60*1000+int(s[3:5])*60*1000+int(s[6:8])*1000+int(s[9:12])
temp_time=0
print	initial_time
# output to file
for i in range(0,time_index):
	s=time[i]
	for j in range(0,1) :
			# convert from 2's complement
		if ec_no[j+i*32] != '0x0000':
			temp1=(int(ec_no[j+i*32],0)-int('0xffff',0))/4
			temp2=(int(rscp[j+i*32],0)-int('0xffff',0))/4
			outfile2.write(str(temp1)+' '+str(temp2)+' ')
		else:
			temp1=0
			temp2=0
			outfile2.write(str(temp1)+' '+str(temp2)+' ')
	outfile2.write(str(s)+' ')
	outfile2.write('\n')			

outfile.close()





print "successfully terminated"