#!/bin/python3
import os
for i in range(1, 5):
	os.system("mkdir Partie0"+str(i))
	for j in range(1, 6):
		os.system("touch Partie0"+str(i)+"/"+str(j)+"-.txt")
		os.system('echo """'+"""Partie0"""+str(i)+""":
Chapitre0"""+str(j)+""":

						/1/-Notes importantes:
#

						/2/-Supléments et infos:
-

										#BY MAWENA

"""+'""" >> '+"Partie0"+str(i)+"/"+str(j)+"-.txt")

