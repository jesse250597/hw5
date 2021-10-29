#import files
import re
import sys

#command line arguments
files = sys.argv[1]
searchString = sys.argv[2]
outputFile = sys.argv[3]

#list to store the chapters/title of the book
titleStore=[]

#regex to search the dialogues
regex_dialog ="[\"“]([^\"”]*)[\"”]"

#regex to search chapter/title similar to the ones in "sh.txt"
regex_chapter_sh = "^(\s)*[(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?V|V?I{1,3}))]+\.[A-Z\-\’\s]+\n"

#regex to search chapter/title similar to the ones in "dracula.txt"
regex_chapter_dracula = "^(CHAPTER){0,1} (M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?V|V?I{1,3}))[\s]*[A-Z(\')(.)\s*]*[A-Z\"\s\,]*[0-9]*[\sA-Z]+"

r_sh = re.compile(regex_chapter_sh)
r_dracula = re.compile(regex_chapter_dracula)

#to be used in case regex_chapter_dracula return true
chapterNamesOnNewLine = 0

#opening the files and storing the titles
with open(files,encoding="utf8") as f:
    data = f.readlines()
f.close()

titleStore_1 = list(filter(r_sh.match,data))
titleStore_2 = list(filter(r_dracula.match,data))

if(len(titleStore_1)>len(titleStore_2)):
	titleStore = titleStore_1
else:
	titleStore = titleStore_2
	chapterNamesOnNewLine = 1

index = 0
#capturing the dialogues using regex
dialogues = []
fullText = ""
for line in data:        
	tempLine = ''.join([str(elem) for elem in line])
	if(index<len(titleStore) and titleStore[index] in tempLine):
		dialogues.append(fullText)
		fullText = ""
		index+=1
	else: 
		fullText += tempLine
dialogues.append(fullText)
dialogues = dialogues[1:]

if(chapterNamesOnNewLine==1):   
	#this loop will only execute where titles of chapters are on new lines. 
	#if they're on the same line, chapterNamesOnNewLine will be 0 and this will not execute.
	for i in range(0, len(dialogues[1:])):
		p = dialogues[1:][i].split("\n")
		#include extra words that accompany with the title/chapter name eg:"to be continued" 
		if((not p[1].isspace())):
			titleStore[i] = titleStore[i].replace("\n","") + " " + p[1]
		elif(p[2].startswith("_L")):
			titleStore[i] = titleStore[i].replace("\n","") + " " + p[2]



f = open(outputFile+".txt", "w")
foundOrNot = 0

#Search Function
for i in range(0,len(dialogues)):
	textDialogues = re.findall(regex_dialog, dialogues[i])
	print(len(textDialogues))
	textDialogues_1 = []
	for dialogue in textDialogues:
		textDialogues_1.append(dialogue.replace("\n", " "))
	
	for dialogSearch in textDialogues_1:
		if searchString in dialogSearch:
			print("Found in {}.".format(titleStore[i].strip()))
			f.write("Found in {}.\n".format(titleStore[i].strip()))
			foundOrNot = 1

if(foundOrNot==0):
	print("Not found in the specified document.")
	f.write("Not found in the specified document.")
	
f.close()