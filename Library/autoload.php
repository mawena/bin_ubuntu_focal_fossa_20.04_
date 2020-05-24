<?php
function autoload($class){
    require '/home/mawena/bin/'.str_replace('\\', '/', $class).'.class.php';
}
spl_autoload_register('autoload');