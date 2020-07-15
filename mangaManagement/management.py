"""Se charge de la gestion des opérations sur les mangas"""

import os
from mangaManagement.management import *


def getMangaListLocal(scanPathList, floderName, formatName):
    mangaList = []
    print(getHeader("Liste(s) de(s) manga(s):\n"))
    for scanPath in scanPathList:
        for name in os.listdir(scanPath):
            if(os.path.exists(scanPath + name + "/" + floderName)):
                if (len(os.listdir(scanPath + name + "/" + floderName)) !=
                        0):  #Si le manga contient des images à convertir
                    mangaList.append([
                        name, "{0}{1}/{2}/".format(scanPath, name, floderName),
                        "{0}{1}/{2}/".format(scanPath, name,
                                             formatName), "{0}_".format(name)
                    ])
                    print(getBold(str(len(mangaList)) + "-" + mangaList[-1][0]))
    return mangaList


def getMangaNumList(mangaList):
    while (True):  #Boucle de vérification des données entrantes
        mangaNumList, errors = input(getOkBlue(
            "\nEntrez le(s) numéro(s) de manga(s) à convertir (séparé par des espaces), ou * pour tout:"
        )).split(" "), []

        if (len(mangaNumList) == 1
                and mangaNumList[0] == "*"):  #Pour compiler tous les dossiers
            mangaNumList = []
            for i in range(0, len(mangaList)):
                mangaNumList.append(i + 1)

        for manga_num in mangaNumList:  #Gestion des erreurs
            try:
                manga_num = int(manga_num) - 1
                if (manga_num < 0 or manga_num > len(mangaList) - 1):
                    errors.append(manga_num)
                    print(getFail("Veuillez entrer des nombres compris entre 1 et " + str(len(mangaList)) + "\n"))
            except TypeError:
                errors.append(manga_num)
                print(getFail("Veuillez entrer des entiers compris entre 1 et " +
                      str(len(mangaList)) + "\n"))
            except ValueError:
                errors.append(manga_num)
                print(getFail("Veuillez entrer des entiers compris entre 1 et " +
                      str(len(mangaList)) + "\n"))
        if (len(errors) == 0):
            break
    return mangaNumList


def rmMangasImages(mangaList, mangaNumList):
    if (len(mangaNumList) > 1):
        rep = input(getWarning("Voulez vous supprimer des images?(o/n):"))
    else:
        rep = "o"
    if (rep == "o"):
        for mangaNum in mangaNumList:  #Boucle de gestion des images après compression
            mangaNum = int(mangaNum) - 1
            name, imagePath, cbzPath, cbzName = mangaList[
                mangaNum]  #Definition des variables après lecture des informations
            chapitreList = os.listdir(imagePath)
            #Gestion des images après convertion #BYMawena
            rep = input(getWarning("Suprimer les images de {0} ?(o/n):".format(
                mangaList[mangaNum][0])))
            if rep == "o":
                os.system("rm -r {0}*".format(imagePath))
                print(getWarning("Images de {0} suprimées".format(mangaList[mangaNum][0])))


def rmItems(Path, extention):
    rep = input(getWarning(
        "Suprimer les fichiers de {0} ayant l'extention \"{1}\"?(o/n)".format(
            Path, extention)))
    if (rep == "o"):
        os.system("rm -r {0}*.pdf".format(Path, extention))
        print(getWarning("Les fichiers {1} du dossier {0} ont été suprimées".format(
                    Path, extention)))

def creatDir(dirPath):
    if(os.path.exists(dirPath) == False):
        print(getWarning("Creation du dossier: ["+dirPath+"]"))
        os.makedirs(dirPath)


def containsListWords(principal, wordList):
    principal = principal.upper()
    for word in wordList:
        if (principal.__contains__(word.upper())):
            return True
    return False

def getHeader(temp):
    return "\033[95m"+temp+"\033[0m"

def getOkBlue(temp):
    return "\033[94m"+temp+"\033[0m"

def getOkGreen(temp):
    return "\033[92m"+temp+"\033[0m"

def getWarning(temp):
    return "\033[93m"+temp+"\033[0m"

def getFail(temp):
    return "\033[91m"+temp+"\033[0m"

def getBold(temp):
    return "\033[1m"+temp+"\033[0m"    

def getUnderline(temp):
    return "\033[4m"+temp+"\033[0m"
