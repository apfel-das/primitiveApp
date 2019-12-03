#!/usr/bin/env python3

import operator


#returns -1 if dictionary with given_afm does not exist
def existent_afm_check(records,given_afm):
	
	ret = records.get(given_afm,-1) 
	
	
	
	return ret


#controller of saving to nested dictionary procedure

def save_context(initIndex,endIndex,Arr,s,el):

	afm = Arr[initIndex].split()[1]
	k= existent_afm_check(s,afm) 

	if k == -1:

		


	#construct  a dictionary (the nested one)
		info = {}
		

		for line in range(initIndex + 1, endIndex):

			prod = Arr[line].split()[0].upper().replace(':', '')  #product name properly formated
			#extend product name for products consisting of 2 words
			if ':' in Arr[line].split()[1].upper():
				prod = prod +" "+Arr[line].split()[1].upper().replace(':','')

			

			price = Arr[line].split()[3].upper()

			#get the lists with products and sales in the dictionary, update records
			
		

			#re insert with proper values
			try:
				#treat and exclude duplicates in same input,just recalculate amount charged
				
				info[prod] = round(float(price)+info[prod],4)
			except:
				
				info[prod] = float(price)
			
			

				
				

		s[afm] = info
		prod = "---"
	else:
		#if afm is already stored, just update catalogues	


		
		for line in range(initIndex + 1, endIndex):

			prod = Arr[line].split()[0].upper().replace(':', '')  #product name properly formated
				#extend product name for products consisting of 2 words
			if ':' in Arr[line].split()[1].upper():
				prod = prod +" "+Arr[line].split()[1].upper().replace(':','')

			price = Arr[line].split()[3].upper()
			#given product is already enlisted, modify total sales 
			try:									
				d = s[afm].get(prod)
				

				s[afm][prod] =float(round(s[afm][prod] + float(price),4))
				

				 
			except:
				s[afm][prod] = float(price)
			

		


	

		

#chech if AFM is  valid based on Greek paterns

def afm_validity_check(num):

	ret = 1
	if len(num) != 10: #afm has not the appropriate length
		
		ret = 0 
	if num.isdigit() != 1:  #afm contains characters
		
		ret = 0
	return ret

def is_valid_total_line(line):

	ret = 1
	words = line.split()

	try:
		if len(words) != 2:
			ret = 0
			#if special keyword does not exist, or total is not expressed as float
		elif words[0].upper() != "ΣΥΝΟΛΟ:" or not "." in words[1]:  
			ret = 0
			#total contains digits,can be intrepreted as a float, but is propably there due to error
		elif words[1].replace('.','').isdigit() != 1:
			ret = 0
	except:
		ret = 0
		
		
	return ret




#used to decide if line is valid or not, calls is_valid_total_line for the last actual line(Amount_Total: )

def is_valid_line(line):
	ret = 1
	k = 0

	words = line.split()
	if len(words) != 4 and is_valid_total_line(line):
		return 1

	if len(words) != 4 and is_valid_total_line(line) != 1:
		if ":" in words[1]:
	
			k = 1
		
		else:
			return 0


	try:

		quantity = float(words[1+k])
		itemPrice = float(words[2+k])
		totPrice = float(words[3+k])
		


		if totPrice != quantity*itemPrice:
			ret = 0
	except:
		ret = 0		

	return ret


#decide if line has the form of a valid separation line
def is_valid_separator(line):

	ret = 1 
	for i in range(0,len(line)-1):
		if line[i] != '-':
			ret = 0
	
	return ret		

#decide if line has the form of a valid line with actual context
def is_valid_afm(lineIndex,linesArr):
	ret = 1
	

	
	#split the line into words
	line = linesArr[lineIndex]
	words=line.split()
	
	
		
	try:
		if words[0].upper() != "ΑΦΜ:":
			ret = 0
		
		if len(words) == 2:
				
			if afm_validity_check(str(words[1])) != 1:
				
				ret = 0
		else:
			ret = 0	
	except:
		ret = 0	
	
	return ret





def line_check(someLine,line_num):

	#return success
	ret = 1
	
	
	if is_valid_line(someLine,line_num) != 1:
		
		ret = 0

	elif is_valid_separator(someLine) != 1:
		ret = 0
	
#lines as argument	
def check_context(initIndex, endIndex,lines):

	ret = 1 
	for i in range(initIndex, endIndex):
		if not is_valid_line(lines[i]):
			ret = 0

	return ret		


def block_check(linesArr,initIndex,finalIndex,totLines,record):

	el = 1

	i = 0
	separatorCount = 0	# flag the incident, where two separators are found
	startIndex = 0    	# mark the index of first occurence 
	endIndex = 0      	# mark the index of last occurence
	contextCount = 0  	# count the actual context lines, if requirements are met store them permanently
	while i < totLines:
		line = linesArr[i]
		
		if len(line.strip()) == 0:

			i+=1
			continue
			
		if is_valid_separator(line):
			
			
			
			if separatorCount == 0:
				separatorCount+=1
				startIndex = i
				
			else:
				endIndex = i #mark the end of possible useful block
				separatorCount == 0  #restore flag 
				if is_valid_afm(startIndex+1,linesArr)  and is_valid_total_line(linesArr[endIndex -1]):

					

				
					if check_context(startIndex+2,endIndex-1,linesArr):
						save_context(startIndex+1,endIndex-1,linesArr,record,el)
						el += 1
			

				startIndex = i  #mark the next possible start
				
				
		i+=1








ans = -1
records = {}

while ans != 4:
	#handle invalid format of input exception
	try:
		ans = int(input("Give your preference: (1: Read new input file, 2: Print statistics for a specific product, 3: Print statistics for a specific AFM, 4: Exit the program)")) #prompt input,convert to int
	except ValueError as exc:
		print()	
		
	#handle user's options	
	if ans == 1:

		#get input and trim any whitespaces,tabs or \n's 
		
		af=input("Insert a valid file name: ").strip()

		#used for statistics gathering, maybe remove if needed

		block_lines = 0
		block_count = 0
		try:
			#open file given,with an alternative way no try/cathc block or file.close() needed
			with open(af,"r",encoding = 'utf-8') as given_file:
				
					file_lines = given_file.readlines()  #cache for efficiency
					total_lines = len(file_lines)		#count the lines
					#print content of each line for debug phase
				
					block_check(file_lines,0,0,total_lines,records)
		except FileNotFoundError:
			pass
				
		for keys,recs in records.items():
			
			print(keys,recs)
				
		ans = -1
					

	elif ans == 2:

		print("\n")
		inp = input("Insert a product name: ").upper()
		print("\n")


		#sort based on master key - AFM
		r = dict(sorted(records.items(), key=operator.itemgetter(0)))
		

		for keys,recs in r.items():
			
				if recs.get(inp,-1) != -1 :
					
					print(keys+" "+str(recs.get(inp,-1)))

			

		print("\n")
		ans = -1


	elif ans == 3:
		inp = input("Insert a valid ΑΦΜ: ")
		l = records.get(inp,0)   #O(1) complexity for searching
		try:
			
			#sort based on subkeys, prod_names
			#use of itemgetter is recommended by docs instead of a lambda func, list of tuples is created
			prod_sorted = sorted(l.items(), key=operator.itemgetter(0))


			print("\n")
			for el in prod_sorted:
				print(el[0]+" "+str(el[1]))
			print("\n")
			

		
		except:
			print("ΑΦΜ was searched but not found(or process was interrupted)..Perhaps you should try again")

		ans = -1
		

	elif ans == 4:
		print("Program will now be terminated! Bye..")

	else:
		print("Insert a valid choice! Only choices (1-4) are valid..")

















	
		





			
	
