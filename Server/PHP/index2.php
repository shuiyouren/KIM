<?php header ("content-type: text/xml");

echo'<?xml version="1.0" encoding="ISO-8859-1"?>
<eserver>
';

try {
	require_once './sql_connect.php';
	require_once './authorize.php';
} catch (Exception $e) {
	echo " <status>requiere_once_error</status>" ;
	echo "<eserver>" ;
	die();
}
$status = 'ok' ;

function returnContactlist ( $user ) {

	$consult = mysql_query("SELECT user, contact FROM es_contacts WHERE user='$user' ;") ;
	$result = "<contacts\n>" ;
	while ( $row = mysql_fetch_object($consult) ) {
		$contact = $row->contact ;
		$consult2 = mysql_query("SELECT nick,subnick,avatar,ip FROM es_users WHERE user='$contact' ;") ;
		while ( $row2 = mysql_fetch_object($consult2) ) {
			$result .= " <contact>\n" ;
			$result .= "  <user>".$contact."</user>\n";
			$result .= "  <nick>".$row2->nick."</nick>\n";
			$result .= "  <subnick>".$row2->subnick."</subnick>\n";
			$result .= "  <avatar>".$row2->avatar."</avatar>\n";
			$result .= "  <ip>".$row2->ip."</ip>\n";
			$result .= " </contact>\n" ;
		}
	}
	$result .= "</contacts>\n" ;

	return $result ;
}

function returnInfo ( $user ) {

	$consult = mysql_query("SELECT nick,subnick,avatar,ip  FROM es_users WHERE user='$user' ;") ;
	$result = '' ;
	while ( $row = mysql_fetch_object($consult) ) {
		$result  = " <info>\n" ;
		$result .= "  <nick>".$row->nick."</nick>\n";
		$result .= "  <subnick>".$row->subnick."</subnick>\n";
		$result .= "  <avatar>".$row->avatar."</avatar>\n";
		$result .= "  <ip>".$row->ip."</ip>\n";
		$result .= " </info>\n" ;
	}

	return $result ;
}
/*
    <alias>test1@live.com</alias>
    <alias>test1@yahoo.com</alias>
   </aliases>
*/

function setNick ( $user, $nick ) {
    $error = 0;
    if ($nick!= '') {
        $consulta = "UPDATE es_users SET nick = '".$nick."' WHERE user ='".$user."' LIMIT 1 ;" ;
        $resultado = mysql_query($consulta) or $error = 1;
    } else {
        $error = 1 ;
    }
    if ($error) {
        $status = 'error';
    } else {
        $status = 'ok';
    }
}

function setSubnick ( $user, $subnick ) {
    $error = 0;
    if ($subnick!= '') {
        $consulta = "UPDATE es_users SET subnick = '".$subnick."' WHERE user ='".$user."' LIMIT 1 ;" ;
        $resultado = mysql_query($consulta) or $error = 1;
        echo "<!-- New: ".$subnick." -->";
    } else {
        $error = 1 ;
    }
    if ($error) {
        $status = 'error';
    } else {
        $status = 'ok';
    }
}

function addContact ( $user, $contact ) {
}

if ( isset ($_GET['user']) and isset ($_GET['password']) and ( $_GET['user']!='' ) and ( $_GET['password']!='' ) ) {
	$authorize=Authorize ( $_GET['user'], $_GET['password'] ) ;
	if ( $authorize ) {

		$ip=$_SERVER['REMOTE_ADDR'] ;

		$consulta = "UPDATE es_users SET ip = '".$ip."' WHERE user ='".$_GET['user']."' LIMIT 1 ;" ;
		$resultado = mysql_query($consulta) or die ('La consulta fall&oacute;: ' . mysql_error());

		$port = 1864 ;
		$timeout = 2 ;
		$errno = -1 ;

		if ( isset ($_GET['port']) and ( $_GET['port']!='' ) ) {
			$port = $_GET['port'] ;
			echo " <port>$port</port>" ;
		}

		$portsopen = 1 ;

		echo " <clientip>$ip</clientip>\n" ;
		if (!$portsopen) {
			$portsopen_str = "no" ;
		}else{
			$portsopen_str = "yes" ;
		}
		echo " <portsopen>$portsopen_str</portsopen><!-- port = $port -->\n" ;

		if ( isset ($_GET['request']) ) {

			switch ($_GET['request']) {
				case 'contactlist' :
					echo returnContactlist ( $_GET['user'] ) ;
				    break;
				case 'setnick' :
                    echo " <!-- set nick -->\n" ;
					setNick ( $_GET['user'], $_GET['nick'] ) ;
				    break;
				case 'setsubnick' :
                    echo " <!-- set subnick -->\n" ;
					setSubnick ( $_GET['user'], $_GET['subnick'] ) ;
				    break;
				case 'addcontact' :
                    echo " <!-- add contact -->\n" ;
					addContact ( $_GET['user'], $_GET['contact'] ) ;
				    break;
                default:
                    echo " <!-- Unrecognized request -->\n" ;
			}
		}

		if ( isset ($_GET['info']) ) {
			switch ($_GET['info']) {
				case 'yes' :
					echo returnInfo ( $_GET['user'] ) ;
				break;
			}
		}
	} else {
		$status = 'authorization_error' ;
	}
} else {
	$status = 'authorization_error' ;
}


?>
 <status><?=$status?></status>
</eserver>
