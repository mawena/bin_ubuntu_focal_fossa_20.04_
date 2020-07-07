"""Se charge de la gestion des opérations sur les mangas"""

import os
def getMangaListListLocal(scanPath, floderName):
	mangaListList = []
	print("Liste(s) de(s) manga(s):\n")
	for name in os.listdir(scanPath):
		if (len(os.listdir(scanPath+name+"/"+floderName)) != 0):  #Si le manga contient des images à convertir
			mangaListList.append([name, "{0}{1}/{2}/".format(scanPath, name, floderName), "{0}_".format(name)])
			print(str(len(mangaListList))+"-"+mangaListList[-1][0])
	return mangaListList

def getMangaNumList(mangaListList):
	while(True):	#Boucle de vérification des données entrantes
		mangaNumList, errors=input("\nEntrez le(s) numéro(s) de manga(s) à convertir (séparé par des espaces), ou * pour tout:").split(" "), []

		if (len(mangaNumList) == 1 and mangaNumList[0] == "*"): #Pour compiler tous les dossiers
			mangaNumList = []
			for i in range(0, len(mangaListList)):
				mangaNumList.append(i+1)

		for manga_num in mangaNumList:	#Gestion des erreurs
			try:
				manga_num = int(manga_num)-1
				if(manga_num<0 or manga_num> len(mangaListList)-1):
					errors.append(manga_num)
					print("Veuillez entrer des nombres compris entre 1 et "+str(len(mangaListList))+"\n")
			except TypeError:
				errors.append(manga_num)
				print("Veuillez entrer des entiers compris entre 1 et "+str(len(mangaListList))+"\n")
			except ValueError:
				errors.append(manga_num)
				print("Veuillez entrer des entiers compris entre 1 et "+str(len(mangaListList))+"\n")
		if(len(errors) == 0):
			break
	return mangaNumList

def rmMangasImages(mangaListList, mangaNumList):
	if(len(mangaNumList)>1):
		rep = input("Voulez vous supprimer des images?(o/n):")
	else:
		rep = "o"
	if(rep == "o"):
		for mangaNum in mangaNumList:	#Boucle de gestion des images après compression
			mangaNum = int(mangaNum)-1
			name,imagePath,cbzName = mangaListList[mangaNum]	#Definition des variables après lecture des informations
			chapitreList=os.listdir(imagePath)
			#Gestion des images après convertion #BYMawena
			rep=input("Suprimer les images de {0} ?(o/n):".format(mangaListList[mangaNum][0]))
			if rep == "o":
				os.system("rm -r {0}*".format(imagePath))
				print("Images de {0} suprimées".format(mangaListList[mangaNum][0]))

def rmItems(Path, extention):
	rep = input("Suprimer les fichiers de {0} ayant l'extention \"{1}\"?(o/n)".format(Path, extention))
	if(rep == "o"):
		os.system("rm -r {0}*.pdf".format(Path, extention))
		print("Les fichiers {1} du dossier {0} ont été suprimées".format(Path, extention))

def containsListWords(principal, wordList):
	for word in wordList:
		if(principal.__contains__(word)):
			return True
	return False