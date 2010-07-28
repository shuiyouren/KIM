<?php header ("content-type: text/xml"); ?>
<?php

//Example Server

require_once ( "ENode/ENode.php" ) ;
require_once ( "ENode/DataBase/db_dummy.php" ) ;
require_once ( "ENode/DataBase/db_mysql.php" ) ;
require_once ( "ENode/AuthClient/authclient_plain.php" ) ;
require_once ( "ENode/AuthNode/authnode_plain.php" ) ;
require_once ( "ENode/AuthNode/authnode_rc4md5.php" ) ;
require_once ( "ENode/Listen/listen_http.php" ) ;
require_once ( "ENode/Input/input_random.php" ) ;
require_once ( "ENode/Crypt/crypt_none.php" ) ;
require_once ( "ENode/Crypt/crypt_reverse.php" ) ;
require_once ( "ENode/Process/process_messenger.php" ) ;

$FashionENode = new ENode () ;

//$dataBase = new DBDummy () ;
$dataBase = new DBMysql () ;
$dataBase->setTablePrefix ( "es_" ) ;
$FashionENode->registerDataBase ( $dataBase ) ;

$clientAuth = new AuthClientPlain () ;
$FashionENode->registerClientAuth ( $clientAuth ) ;

//$nodeAuth = new AuthNodePlain () ;
$nodeAuth = new AuthNodeRc4Md5 () ;
$FashionENode->registerNodeAuth ( $nodeAuth ) ;

$Crypt = new CryptNone () ;
//Crypt = new CryptReverse () ;
$FashionENode->registerCrypt ( $Crypt ) ;

$Process = new ProcessMessenger () ;
$FashionENode->registerClientAuth ( $Process ) ;

$Listen = new ListenHTTP () ;
$FashionENode->registerListen ( $Listen ) ;

$Input = new InputRandom () ;
$FashionENode->registerInput ( $Input ) ;

$Process = new ProcessMessenger () ;
$FashionENode->registerProcess ( $Process ) ;

$FashionENode->Start () ;

$FashionENode->injectToListen ( $_POST['erequest'] ) ;

$FashionENode->Output () ;

?>
