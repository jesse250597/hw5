#!/usr/bin/env python
# coding: utf-8

# In[31]:


#import files
import re
import sys

#command line arguments
inputFile = sys.argv[1]
outputFile = sys.argv[2]
fw = open(outputFile+".txt", "w")


#regex to search the dialogues
regex_dialog ="[\"“]([^\"”]*)[\"”]"
quoteMark = '"'
dialogues = []
dialogueStore = []
#opening the files and storing the titles
with open(inputFile,encoding="utf8") as f:
    data = f.readlines()
    data = ' '.join([str(elem) for elem in data])
    data = data.replace("\n","")
    dialogueStore.extend(re.findall(regex_dialog,data))
   
    for  d in dialogueStore:
        fw.write(quoteMark + d + quoteMark+"\n")
        print(quoteMark + d + quoteMark)


f.close()
fw.close()