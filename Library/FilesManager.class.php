<?php

namespace Library;

use Library\Entities\Video;
use Library\Manager;
use Library\Models\VideosManager_PDO;

class FilesManager{
    /**
     * Function to convert to absoule path
     *
     * @param [string] $path
     * @return string
     */
    public function slasher($path){
        $path = (string)$path;
        $path = realpath($path);
        return ( $path[-1] == "/") ? $path: $path."/" ;
    }

    /**
     * Remove unwanted characters from a name
     *
     * @param string $name
     * @param array $undesirables
     * @return string
     */
    public function renameOne(string $name, array $undesirables){
        foreach ($undesirables as $undesirable => $remplacer){
            $name = str_replace($undesirable, $remplacer, $name);
        }
        return  $name;
    }

    /**
     * Remove unwanted characters from a name board
     *
     * @param array $names
     * @param array $undesirables
     * @return array
     */
    public function renameArray(array $names, array $undesirables){
        $renames=array();
        foreach($names as $name){
            foreach ($undesirables as $undesirable => $remplacer){
                $name = str_replace($undesirable, $remplacer, $name);
            }
            $renames[] = $name;
        }
        return $renames;
    }

    /**
     * File a file according to a certain classification
     *
     * @param string $path  chemin de travail
     * @param array $extensions listes des extensions
     * @param array $undesirables   lites des caractères indésirables
     * @param array $elements   listes des artistes
     * @return void
     */
    public function fileFame(string $path, array $extensions, array $undesirables, array $elements){
        $answer=strtolower(readline("Ce programme va modifier vos fichiers sans retour possible, êtes vous sur de vouloir continuer le rangement?(yes/no):"));
        if($answer[0] == "y"){
            echo "Renomage et rangement des fichiers\n";
            $path = $this->slasher($path);
            foreach ($extensions as $extension){
                foreach(glob($path."*".$extension) as $pathFind){
                    $goodName=$this->renameOne(substr($pathFind, strlen($path)), $undesirables);    //retourne un nom corect
                    if($pathFind != $path.$goodName){   //Si le nom doit être changé
                        rename($pathFind, $path.$goodName);
                        echo "'".$pathFind."' => '".$path.$goodName."'\n"  ;
                    }
                    foreach($elements as $element){     //On parcoure les élément pour déplacer les fichiers
                        if( strpos(strtolower($goodName), strtolower($element)) !== false ){
                            if(!is_dir($path.$element)){
                                mkdir($path.$element);
                                echo "Création du dossier : <".$path.$element.">\n";
                            }
                            rename($path.$goodName, $path.$element."/".$goodName);
                            echo $path.$goodName." => ".$path.$element."/".$goodName."\n";
                        break;
                        }
                    }
                }
            }
        }else{
            echo "Arret du programme\n";
        }
    }

    /**
     * Returns a certain classification of the path according to a list of extensions
     *
     * @param string $path
     * @param array $extensions
     * @return array
     */
    public function tree2(string $path, array $extensions){
        if(is_dir($path))
        {
            $files=array();
            $path=$this->slasher($path);
            if($pointeur = opendir($path))
            {
                while(($fichier = readdir($pointeur)) !== false)
                {
                    if($fichier != "." && $fichier != ".." && $fichier != "Thumbs.db")
                    {
                        if(is_dir($path.$fichier)){
                            foreach($extensions as $extension){
                                if(glob($this->slasher($path.$fichier)."*".$extension)){
                                    foreach ( glob($this->slasher($path.$fichier)."*".$extension) as $result ){
                                        $result = (substr($result, strlen($path.$fichier)+1));
                                        $files[$fichier][$extension][] = $result;
                                    }
                                }
                            }
                        }
                    }
                }
                closedir($pointeur);
            }
            return $files;
        }
    }
    
    /**
     * Upload elements
     *
     * @param array $artistes
     * @param Manager $manager
     * @param string $path
     * @param string $pathSave
     * @return void
     */
    public function upload(array $artistes, Manager $manager, string $path, string $pathSave){
        $pathSave = $this->slasher($pathSave);
        
        echo "Upload des fichiers\n";
        $answer=strtolower(readline("Ce programme va modifier vos fichiers sans retour possible, êtes vous sur de vouloir continuer l'upload?(yes/no):"));
        if($answer[0] == "y"){
            foreach($artistes as $artiste => $elements){
                (!is_dir($pathSave.$artiste)) ? mkdir($pathSave.$artiste) : null;
                foreach ($elements as $extension => $tab){
                    foreach($tab as $element){
                        $element = substr($element, 0, strlen($element)-strlen($extension)-1);
                        $test = new Video(array("nom" => $element, "extention" => $extension, "artiste" => $artiste));
                        ($manager->count($element))? null : $manager->add(new Video(array("nom" => $element, "extention" => $extension, "artiste" => $artiste)));   //Ajout à la bdd
                        rename($path.$artiste."/".$element.".".$extension, $pathSave.$artiste."/".$element.".".$extension);    //Déplacement
                        echo $path.$artiste."/".$element.".".$extension." => ".$pathSave.$artiste."/".$element.".".$extension."\n";
                        (glob($this->slasher($path.$artiste)."*")) ? null : rmdir($path.$artiste);
                    }
                }
            }
        }
    }
}

                                        #BY MAWENA