#import files
import re
import sys
from tkinter import *

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

# Python program for KMP Algorithm
def KMPSearch(pat, txt):
	M = len(pat)
	N = len(txt)

	# create lps[] that will hold the longest prefix suffix
	# values for pattern
	lps = [0]*M
	j = 0 # index for pat[]

	# Preprocess the pattern (calculate lps[] array)
	computeLPSArray(pat, M, lps)

	i = 0 # index for txt[]
	while i < N:
		if pat[j] == txt[i]:
			i += 1
			j += 1

		if j == M:
			print ("Found pattern at index " + str(i-j))
			j = lps[j-1]

		# mismatch after j matches
		elif i < N and pat[j] != txt[i]:
			# Do not match lps[0..lps[j-1]] characters,
			# they will match anyway
			if j != 0:
				j = lps[j-1]
			else:
				i += 1

titleStore_1 = list(filter(r_sh.match,data))
titleStore_2 = list(filter(r_dracula.match,data))

if(len(titleStore_1)>len(titleStore_2)):
	titleStore = titleStore_1
else:
	titleStore = titleStore_2
	chapterNamesOnNewLine = 1
	
def computeLPSArray(pat, M, lps):
	len = 0 # length of the previous longest prefix suffix

	lps[0] # lps[0] is always 0
	i = 1

	# the loop calculates lps[i] for i = 1 to M-1
	while i < M:
		if pat[i]== pat[len]:
			len += 1
			lps[i] = len
			i += 1
		else:
			# This is tricky. Consider the example.
			# AAACAAAA and i = 7. The idea is similar
			# to search step.
			if len != 0:
				len = lps[len-1]

				# Also, note that we do not increment i here
			else:
				lps[i] = 0
				i += 1
	
	
txt = "ABABDABACDABABCABAB"
pat = "ABABCABAB"
KMPSearch(pat, txt)

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

#Python Program to search string in text using Tkinter

#to create a window
root = Tk()

#root window is the parent window
fram = Frame(root)

#adding label to search box
Label(fram,text='Text to find:').pack(side=LEFT)

#adding of single line text box
edit = Entry(fram)

#positioning of text box
edit.pack(side=LEFT, fill=BOTH, expand=1)

#setting focus
edit.focus_set()

#adding of search button
butt = Button(fram, text='Find')
butt.pack(side=RIGHT)
fram.pack(side=TOP)

#text box in root window
text = Text(root)

#text input area at index 1 in text window
text.insert('1.0','''Type your text here''')
text.pack(side=BOTTOM)


#function to search string in text
def find():
	
	#remove tag 'found' from index 1 to END
	text.tag_remove('found', '1.0', END)
	
	#returns to widget currently in focus
	s = edit.get()
	if s:
		idx = '1.0'
		while 1:
			#searches for desired string from index 1
			idx = text.search(s, idx, nocase=1,
							stopindex=END)
			if not idx: break
			
			#last index sum of current index and
			#length of text
			lastidx = '%s+%dc' % (idx, len(s))
			
			#overwrite 'Found' at idx
			text.tag_add('found', idx, lastidx)
			idx = lastidx
		
		#mark located string as red
		text.tag_config('found', foreground='red')
	edit.focus_set()
butt.config(command=find)

#mainloop function calls the endless loop of the window,
#so the window will wait for any
#user interaction till we close it
root.mainloop()
