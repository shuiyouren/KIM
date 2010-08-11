<?php header ("content-type: text/xml");


require_once './sql_connect.php';
require_once './eserver.php';

$eserver = new eserver () ;
$eserver->getVariables( $_GET ) ;

$eserver->process() ;

?>
