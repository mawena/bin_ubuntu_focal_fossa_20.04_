"""Se charge des téléchargements"""
import urllib3, os, re
connection_pool = urllib3.PoolManager()
from mangaManagement.management import *

def downloadImage(imageLink, imagePath):
    if os.path.exists(imagePath):  #Si le fichier existe déja
            print(getWarning("[" + imagePath + "] existe déja"))
    else:
        resp = connection_pool.request('GET', imageLink)
        if (resp.status == 200):
            f = open(imagePath, "wb")
            f.write(resp.data)
            f.close()
            resp.release_conn()
            print(getOkGreen("[" + imageLink + "] => [" + imagePath + "]"))
        elif (resp.status == 404):
            print(getFail("Le fichier {0} n'existe pas en ligne".format(imageLink)))
            return False
        elif(resp.status == 403):
            print(getFail("L'accès au fichier {0} est interdit".format(imageLink)))
            return False
        elif(resp.status == 503):
            print(getFail("Le serveur du fichier {0} est temporairement indisponible".format(imageLink)))
            return False
        else:
            print(getFail("Il y a eu une erreur inconue lors du téléchargement du fichier "+imageLink+" , Le code html est "+getUnderline(str(resp.status))))
            return False
    return True

def getHTMLPage(HTMLPageLink):
    resp = connection_pool.request('GET', HTMLPageLink)
    if (resp.status == 200):
        print(getOkGreen("Téléchargement de la page {0} ".format(HTMLPageLink)))
    return resp.data

def getImagesLinksMangakakalot(HTMLPage):
    regex = re.compile('<img.*?src=[\'"]https://s3.mkklcdnv3.com(.*?)[\'"]')
    imagesLinks = []
    for resultat in regex.findall(str(HTMLPage)):
        imagesLinks.append("https://bu.mkklcdnbuv1.com"+resultat)
    return imagesLinks

def getMangaList(mdFilePath, mangaSavingPath, imageType):
    os.system("clear")
    with open(mdFilePath, "r") as file:
        fileText=file.read()
    mangaList=[]
    print(getHeader(getBold(getUnderline("Liste des mangas:\n"))))
    for line in fileText.split("\n"):
        mangaList.append(line.split("] : ["))
        mangaList[-1][0],mangaList[-1][-1]=mangaList[-1][0][1:],mangaList[-1][-1][:-1]   #On éfface le premier caractère de la première chaîne de caractères et le dernier caractère de la dernière chaîne de caractères
        mangaList[-1].append(mangaSavingPath+mangaList[-1][0]+"/"+imageType+"/")
        print(getBold(str(len(mangaList))+"-"+mangaList[-1][0])) #On affiche le Name du scan
    return mangaList

def getDic(configFile):
    os.system("clear")
    with open(configFile, "r") as file:
        fileText = file.read()
    dic = {}
    for line in fileText.split("\n"):
        lineVars = line.split("\t\t")
        dic[(lineVars[0])] = lineVars[1]
    return dic
def getMangaNum(mangaList):
    while(True):
      try:
          mangaNum=int(input(getOkBlue("\nEntrez le numéro du manga à télécharger:")))-1
          if(mangaNum<0 or mangaNum> len(mangaList)-1):
              print(getFail("Veuillez entrer un Namebre compris entre 1 et "+str(len(mangaList))))
          else:
              break
      except TypeError:
          print(getFail("Veuillez entrer un entier compris entre 1 et "+str(len(mangaList))+"\n"))
      except ValueError:
          print(getFail("Veuillez entrer un entier compris entre 1 et "+str(len(mangaList))+"\n"))
    os.system("clear")
    return mangaNum

def getVersion(langs):
    print(getHeader("Versions:"))
    comp = 1
    for choice in langs:
        print(getBold(str(comp)+"-"+choice))
        comp+=1
    comp=1
    while(True):
        try:
            lang = langs[(int(input(getOkBlue("quel est le numéro de la version à télécharger?:"))))-1]
            if(langs.__contains__(lang)):
              break
            else:
                print(getFail("Veuillez entrer un Namebre compris entre 1 et "+str(len(langs))))
        except TypeError:
          print(getFail("Veuillez entrer un entier compris entre 1 et "+str(len(langs))+"\n"))
        except ValueError:
          print(getFail("Veuillez entrer un entier compris entre 1 et "+str(len(langs))+"\n"))
        except IndexError:
          print(getFail("Veuillez entrer un entier compris entre 1 et "+str(len(langs))+"\n"))
    os.system("clear")
    return lang

def getNbreImage(toPrint):
    while(True):
        try:
            nbreImage = (int(input(getOkBlue(toPrint))))
        except TypeError:
            print(getFail("Veuillez entrer un entier\n"))
        except ValueError:
            print(getFail("Veuillez entrer un entier\n"))
        break
    os.system("clear")
    return nbreImage

def getChapterVars(Name):
    vars, more = [], ""
    while(True):
        try:
            entre=input(getOkBlue("Entrez le(s) chapitre(s) de comencement (et de fin séparés par un espace):")).split(" ")
            if(len(entre) == 1):
                if(entre[0] == ""):
                    withoutChapter=True
                    start, end=0, 0
                else:
                    withoutChapter=False
                    start, end=int(entre[0]), int(entre[0])
            else:
                withoutChapter=False
                start, end= int(entre[0]), int(entre[1])

            if(start<0 or end<0):
                print(getFail("Les chapitres doivent êtres supérieures ou égal à 0\n"))
            elif(start>end):
                print(getFail("Le chapitre de début doit être inférieur à celui de fin\n"))
            else:
                break
        except TypeError:
            print(getFail("Les chapitres doivent être des entiers\n"))
    os.system("clear")
    for chapitre in range(start, end+1):
        if(withoutChapter):
            chapitre=input(getWarning("Entrez le(s) référence(s) de chapitre(s) (séparés par un espace):"))
        else:
            if(chapitre <= 9):
                more = "00"
            elif(chapitre <= 99):
                more = "0"
            else:
                more = ""
        chapitre=str(chapitre)
        for temp in chapitre.split(" "):
            vars.append([temp, more])
    return vars