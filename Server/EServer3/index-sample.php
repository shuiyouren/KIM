<?php header ("content-type: text/xml"); ?>
<?php

//Example Server

require_once ( "EServer/EServer.php" ) ;
require_once ( "EServer/DataBase/db_dummy.php" ) ;
require_once ( "EServer/DataBase/db_mysql.php" ) ;
require_once ( "EServer/AuthClient/authclient_plain.php" ) ;
require_once ( "EServer/AuthNode/authnode_plain.php" ) ;
require_once ( "EServer/AuthNode/authnode_rc4md5.php" ) ;
require_once ( "EServer/Listen/listen_http.php" ) ;
require_once ( "EServer/Crypt/crypt_none.php" ) ;
require_once ( "EServer/Crypt/crypt_reverse.php" ) ;
require_once ( "EServer/Process/process_messenger.php" ) ;

$FashionEServer = new EServer () ;

//$dataBase = new DBDummy () ;
$dataBase = new DBMysql () ;
$dataBase->setTablePrefix ( "es_" ) ;
$FashionEServer->registerDataBase ( $dataBase ) ;

$clientAuth = new AuthClientPlain () ;
$FashionEServer->registerClientAuth ( $clientAuth ) ;

//$nodeAuth = new AuthNodePlain () ;
$nodeAuth = new AuthNodeRc4Md5 () ;
$FashionEServer->registerNodeAuth ( $nodeAuth ) ;

$Crypt = new CryptNone () ;
//Crypt = new CryptReverse () ;
$FashionEServer->registerCrypt ( $Crypt ) ;

$Process = new ProcessMessenger () ;
$FashionEServer->registerClientAuth ( $Process ) ;

$Listen = new ListenHTTP () ;

$FashionEServer->registerListen ( $Listen ) ;

$Process = new ProcessMessenger () ;
$FashionEServer->registerProcess ( $Process ) ;

$FashionEServer->Start () ;

$FashionEServer->injectToListen ( $_POST['erequest'] ) ;

$FashionEServer->Output () ;

?>
