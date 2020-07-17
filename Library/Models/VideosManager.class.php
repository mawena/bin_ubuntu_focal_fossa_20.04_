<?php
namespace Library\Models;

use Library\Entities\Video;

abstract class VideosManager extends \Library\Manager{
    /**
    * Returns a list of videos
    *
    * @param integer $debut  La première videos à sélectionner
    * @param integer $limite Le nombre de videos à sélectionner
    * @return array La liste des videos. Chaque entrée est une instance de videos.
    */
    abstract public function getList($debut = -1, $limite = -1);
    
    /**
    * Return a Video
    *
    * @param integer $id L'identifiant de la videos à récupérer
    * @return Videos La videos demandée
    */
    abstract public function getUnique($id);

    /**
     * Returns the number of videos
     *
     * @param $regex string le mot clé
     * @return int
     */
    abstract function count($regex);

    /**
     * Add a video
     *
     * @param Video $video
     * @return void
     */
    abstract function add(Video $video);

    /**
     * Return All Artistes
     *
     * @return array
     */
    abstract function getAllArtistes();
}