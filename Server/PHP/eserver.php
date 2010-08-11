<?php

require_once('rc4crypt/class.rc4crypt.php');
require_once('store.php');

class eserver
{
	function __construct () {
		echo'<?xml version="1.0" encoding="ISO-8859-1"?>
<eserver>
';

	}

	public function getVariables ( $get ) {

		$this->get = $get ;

		$this->user = $this->getVariable ( 'user' ) ;
		$this->password = $this->getVariable ( 'password' ) ;

		$this->request = $this->getVariable ( 'request' ) ;

		$this->req['passphrase_md5'] = $this->getVariable ( 'passphrase_md5' ) ;

		$this->info = $this->getVariable ( 'info' ) ;

	}

	public function addUser ( $user, $password, $password2, $country, $language, $timezone ) {

        if ( ($user!='') && ($password!='') && ($password2!='') ) {
            if ( $password == $password2 ) {

                $Store = new store ;
                $update = $Store->insert( 'users', array ( array ('user', $user), array ( 'password', $password), array ( 'country', $country),
                                           array ( 'language', $language), array ( 'timezone', $timezone ) ) ) ;
                return 'ok' ;
            } else {
                return 'unmatch' ;
            }
        } else {
            return 'missing' ;
        }
	}

	function getVariable ( $name ) {
		if ( isset($this->get [ $name ]) ) {
			return $this->get [ $name ] ;
		} else {
			return false ;
		}
	}

	function requests () {
		switch ($_GET['request']) {
			case 'login' :
				echo " <!-- login -->\n" ;
				echo $this->request_login () ;
				break;
			case 'suid' :
				echo " <!-- suid -->\n" ;
				echo $this->request_suid () ;
				break;
			default:
				echo " <!-- Unrecognized request -->\n" ;
		}
	}


	function request_login () {

        $this->passphrase = $this->new_passphrase () ;

        $fields[] = array ( 'passphrase_temp', $this->passphrase ) ;
        $where[] = array ( 'user', $this->user ) ;

        $Store = new store ;
        $update = $Store->update( 'users', $fields, $where, 1 ) ;

        unset ( $fields ) ;
        unset ( $where ) ;

        $fields[] = 'password' ;
        $fields[] = 'passphrase_temp' ;

        $where[] = array ( 'user', $this->user ) ;
        $data = $Store->select( 'users', $fields, $where, 1 ) ;

        $row = mysql_fetch_object($data) ;
		$this->password = $row->password ;

        if ($update) {
            echo " <!-- OK -->\n" ;
        } else {
            //$sql_err = mysql_error ( $update ) ;
            echo " <!-- ERROR: -->\n" ;
        }

        $this->epassphrase = rc4crypt::encrypt($this->password, $this->passphrase, 0) ;
        $hex = bin2hex( $this->epassphrase ) ;

        $html_pass = htmlentities  ( $this->passphrase ) ;

		echo " <!-- pass: $this->password passphrase: $html_pass  -->\n" ;
        $result = "<epassphrase>$hex</epassphrase>" ;
        return $result ;
    }

	function request_suid () {

        $Store = new store ;
        $data = $Store->select( 'users', array ( 'password', 'passphrase_temp' ), array ( array ( 'user', $this->user) ) , 1 ) ;

        $row = mysql_fetch_object($data) ;
		$this->passphrase = $row->passphrase_temp ;
		$this->password = $row->password ;

		echo " <!-- passphrase: $this->passphrase  -->\n" ;

		echo " <!-- password: $this->password  -->\n" ;

        $pass_md5 = md5 ( $this->passphrase ) ;

        if ($pass_md5 == $this->req['passphrase_md5'] ) {

            $Store = new store ;
            $update = $Store->update( 'users', array ( array ( 'suid', $this->suid ), array ( 'passphrase', $this->passphrase ) ),
                                      array ( array ( 'user', $this->user) ), 1 ) ;

            $this->esuid = rc4crypt::encrypt($this->passphrase, $this->suid, 0) ;
            $hex = bin2hex( $this->esuid ) ;

		    echo " <!-- suid: $this->suid  -->\n" ;
            $result = "<esuid>$hex</esuid>" ;

            //$test = rc4crypt::encrypt($this->password, $this->esuid, 0) ;
		    //echo " <!-- suid: $test  -->\n" ;
        } else {
            $this->error = 'error' ;
        }

        return $result ;
    }

	function process () {

        #$this->suid = dechex ( time() ) ;
        $this->suid = strval ( time() ) ;
        $this->error = 'ok' ;

		$this->requests () ;

         echo " <error>$this->error</error>" ;

	}

    function new_passphrase () {
        $pass = '' ;
        for ($i=0;  $i<=127; $i++) $pass.= chr ( rand(97, 122) ) ;
        return $pass ;
    }

	function __destruct() {
		echo'</eserver>';
	}


}

/*
class eserver
{
	function __construct () {
		echo'<?xml version="1.0" encoding="ISO-8859-1"?>
<eserver>
';

	}

	function getVariables ( $get ) {

		$this->get = $get ;

		$this->user = $this->getVariable ( 'user' ) ;
		$this->password = $this->getVariable ( 'password' ) ;

		$this->request = $this->getVariable ( 'request' ) ;

		$this->req['contact'] = $this->getVariable ( 'contact' ) ;
		$this->req['nick'] = $this->getVariable ( 'nick' ) ;
		$this->req['subnick'] = $this->getVariable ( 'subnick' ) ;
		$this->req['status'] = $this->getVariable ( 'status' ) ;
		$this->req['xml'] = $this->getVariable ( 'xml' ) ;
		$this->req['recipient'] = $this->getVariable ( 'recipient' ) ;
		$this->req['contact'] = $this->getVariable ( 'contact' ) ;
		$this->req['avatar'] = $this->getVariable ( 'avatar' ) ;

		$this->info = $this->getVariable ( 'info' ) ;

	}

	function process () {

        $this->stamp = time() ;
        $this->error = 'ok' ;

		if ( $this->authorize () ) {
			$this->updateIp () ;
			$this->updateStatus () ;

			$port = 1864 ;
			$timeout = 2 ;
			$errno = -1 ;

			echo " <clientip>$this->ip</clientip>\n" ;

			echo " <clientstamp>$this->stamp</clientstamp>\n" ;

			$this->requests () ;
			$this->info () ;
		 }
         echo " <error>$this->error</error>" ;

	}

	function authorize () {

		if ( isset( $this->authorized ) ) return $this->authorized ;

        if ( $this->user == 'test1' ) {
            $this->error = 'error' ;
			$this->authorized = false ;
			return false ;
        }

		$user = $this->user ;
		$password = $this->password ;

		if ( ($user!='') and ($password!='') ) {

			$total = mysql_query("SELECT COUNT(*) FROM es_users WHERE user='$user' and password='$password' ;");
			$total = mysql_fetch_row($total) or $this->error = 'error' ;
            if ( $this->error == 'error' ) {
                return false ;
            }
			$total = $total[0];

			if ( $total>0 ) {

                $consulta = "UPDATE es_users SET stamp = '".$this->stamp."' WHERE user ='".$user."' LIMIT 1 ;" ;
                $resultado = mysql_query($consulta) or $this->error = 'error' ;
                if ( $this->error == 'error' ) {
                    return false ;
                }

				$this->authorized = true ;
				return true ;
			} else {
                $this->error = 'error' ;
				$this->authorized = false ;
				return false ;
			}
		} else {
            $this->error = 'error' ;
			$this->authorized = false ;
			return false ;
		}

	}

	function getVariable ( $name ) {
		if ( isset($this->get [ $name ]) ) {
			return $this->get [ $name ] ;
		} else {
			return false ;
		}
	}

	function updateStatus () {
        if ( $this->req['status']!='' ) {
            $this->status = $this->req['status'] ;
		    $consulta = "UPDATE es_users SET status = '".$this->status."' WHERE user ='".$this->user."' LIMIT 1 ;" ;
		    $resultado = mysql_query($consulta) or $this->error = 'error' ;
        }
	}

	function updateIp () {
		$this->ip=$_SERVER['REMOTE_ADDR'] ;

		$consulta = "UPDATE es_users SET ip = '".$this->ip."' WHERE user ='".$this->user."' LIMIT 1 ;" ;
		$resultado = mysql_query($consulta) or $this->error = 'error' ;
	}

	function requests () {
		switch ($_GET['request']) {
			case 'contactlist' :
				echo $this->returnContactlist () ;
				break;
			case 'setnick' :
				echo " <!-- set nick -->\n" ;
				$this->setNick () ;
				break;
			case 'setsubnick' :
				echo " <!-- set subnick -->\n" ;
				$this->setSubnick () ;
				break;
			case 'setavatar' :
				echo " <!-- set avatar -->\n" ;
				$this->setAvatar () ;
				break;
			case 'addcontact' :
				echo " <!-- add contact -->\n" ;
				$this->addContact () ;
				break;
			case 'refresh' :
				echo " <!-- refresh -->\n" ;
				echo $this->refresh () ;
				break;
			case 'send' :
				echo " <!-- send -->\n" ;
				echo $this->send () ;
				break;
			default:
				echo " <!-- Unrecognized request -->\n" ;
		}
	}

	function returnContactlist () {

		$user = $this->user ;

		$consult = mysql_query("SELECT user, contact FROM es_contacts WHERE user='$user' ;") ;
		$result = "<contacts\n>" ;
		while ( $row = mysql_fetch_object($consult) ) {
			$contact = $row->contact ;
			$consult2 = mysql_query("SELECT nick,subnick,avatar,ip,status,stamp FROM es_users WHERE user='$contact' ;") ;
			while ( $row2 = mysql_fetch_object($consult2) ) {
                if ($contact == 'test1') {
                    $row2->status = '0' ;
                    $row2->stamp = $this->stamp ;
                }
				$result .= " <contact>\n" ;
				$result .= "  <user>".$contact."</user>\n";
				$result .= "  <nick>".$row2->nick."</nick>\n";
				$result .= "  <subnick>".$row2->subnick."</subnick>\n";
				$result .= "  <avatar>".$row2->avatar."</avatar>\n";
				$result .= "  <ip>".$row2->ip."</ip>\n";
				$result .= "  <status>".$row2->status."</status>\n";
				$result .= "  <stamp>".$row2->stamp."</stamp>\n";
				$result .= " </contact>\n" ;
			}
		}
		$result .= "</contacts>\n" ;

		return $result ;
	}

	function info () {

		if ($this->info == 'yes' ) {

			$user = $this->user ;

			$consult = mysql_query("SELECT nick,subnick,avatar,ip,status,stamp  FROM es_users WHERE user='$user' ;") ;
			$result = '' ;
			while ( $row = mysql_fetch_object($consult) ) {
				$result  = " <info>\n" ;
				$result .= "  <nick>".$row->nick."</nick>\n";
				$result .= "  <subnick>".$row->subnick."</subnick>\n";
				$result .= "  <avatar>".$row->avatar."</avatar>\n";
				$result .= "  <ip>".$row->ip."</ip>\n";
				$result .= "  <status>".$row2->status."</status>\n";
				$result .= "  <stamp>".$row2->stamp."</stamp>\n";
				$result .= " </info>\n" ;
			}

			echo $result ;
		}
	}

	function setNick () {
		$user = $this->user ;
		$nick = $this->req['nick'] ;

		$error = 0;
		if ($nick!= '') {
		    $consulta = "UPDATE es_users SET nick = '".$nick."' WHERE user ='".$user."' LIMIT 1 ;" ;
		    $resultado = mysql_query($consulta) or $error = 1;
		} else {
		    $error = 1 ;
		}
		if ($error) {
		    $this->error = 'error';
		}
	}

	function setSubnick () {
		$user = $this->user ;
		$subnick = $this->req['subnick'] ;

		$error = 0;
		if ($subnick!= '') {
		    $consulta = "UPDATE es_users SET subnick = '".$subnick."' WHERE user ='".$user."' LIMIT 1 ;" ;
		    $resultado = mysql_query($consulta) or $error = 1;
		    echo "<!-- New: ".$subnick." -->";
		} else {
		    $error = 1 ;
		}
		if ($error) {
		    $this->error = 'error';
		}
	}

	function setAvatar () {
		$user = $this->user ;
		$avatar = $this->req['avatar'] ;

		$error = 0;
		if ($avatar!= '') {
		    $consulta = "UPDATE es_users SET avatar = '".$avatar."' WHERE user ='".$user."' LIMIT 1 ;" ;
		    $resultado = mysql_query($consulta) or $error = 1;
		    echo "<!-- New: ".$avatar." -->";
		} else {
		    $error = 1 ;
		}
		if ($error) {
		    $this->error = 'error';
		}
	}

    function addContact () {
        $contact = $this->req['contact'] ;

        if ( $contact == '' ){
            $this->error='error' ;
            return ;
        }

		$user = $this->user ;
		$total = mysql_query("SELECT COUNT(*) FROM es_users WHERE user='$contact' ;");
		$total = mysql_fetch_row($total);
		$total = $total[0];
        if ($total>0) {
		    $consulta = "INSERT INTO es_contacts VALUES( '$user', '$contact', 0 ) ;" ;
		    $resultado = mysql_query($consulta) or $this->error='error' ;
        } else {
            $this->error='error' ;
        }
    }

    function removeContact () {
        $contact = $this->req['contact'] ;

        if ( $contact == '' ){
            $this->error='error' ;
            return ;
        }

		$user = $this->user ;
		$consulta = "DELETE FROM es_contacts WHERE `user` ='". $user ."' AND `contact` ='".$remove."' LIMIT 1 ;" ;
		$resultado = mysql_query($consulta) or $this->error='error' ;
    }

    function refresh () {

		$user = $this->user ;

		$consult = mysql_query("SELECT user, contact FROM es_contacts WHERE user='$user' ;") ;
		$result = "<contacts\n>" ;
		while ( $row = mysql_fetch_object($consult) ) {
			$contact = $row->contact ;
			$consult2 = mysql_query("SELECT nick,subnick,avatar,ip,status,stamp FROM es_users WHERE user='$contact' ;") ;
			while ( $row2 = mysql_fetch_object($consult2) ) {
                if ($contact == 'test1') {
                    $row2->status = '0' ;
                    $row2->stamp = $this->stamp ;
                }
				$result .= " <contact>\n" ;
				$result .= "  <user>".$contact."</user>\n";
				$result .= "  <nick>".$row2->nick."</nick>\n";
				$result .= "  <subnick>".$row2->subnick."</subnick>\n";
				$result .= "  <avatar>".$row2->avatar."</avatar>\n";
				$result .= "  <ip>".$row2->ip."</ip>\n";
				$result .= "  <status>".$row2->status."</status>\n";
				$result .= "  <stamp>".$row2->stamp."</stamp>\n";
				$result .= " </contact>\n" ;
			}
		}
		$result .= "</contacts>\n" ;

        $result .= "<datas>\n" ;
		$consult3 = mysql_query("SELECT sid,`from`,content FROM es_connections WHERE `to`='$user' ;") ;
		while ( $row3 = mysql_fetch_object($consult3) ) {
			$result .= " <data>\n" ;
			$result .= "  <sid>".$row3->sid."</sid>\n";
			$result .= "  <from>".$row3->from."</from>\n";
			$result .= "  <content>".htmlentities ( $row3->content ) ."</content>\n";
			$result .= " </data>\n" ;

            $consult4 = mysql_query("DELETE FROM es_connections WHERE `sid` ='". $row3->sid ."' AND `from` ='".$row3->from."' LIMIT 1 ;");
        }

        $result .= "</datas>\n" ;

		$this->error = 'ok';
		return $result ;
    }

    function send () {

		$xml = $this->req['xml'] ;
        $recipient = $this->req['recipient'] ;
        $sender = $this->user ;

        if ($recipient == 'test1') {
            $recipient = $this->user ;
            $sender = 'testi1' ;

            $xml = str_replace ( $this->user, 'UseR', $xml ) ;
            $xml = str_replace ( 'test1', $this->user, $xml ) ;
            $xml = str_replace ( 'UseR', 'test1', $xml ) ;

        }

        $stamp = time () ;

        $consulta = "INSERT INTO es_connections VALUES( '$stamp', '$sender', '$recipient', '$xml' ) ;" ;
		$resultado = mysql_query($consulta) or die ('La consulta fall&oacute;: ' . mysql_error());
    }

	function __destruct() {
		echo'</eserver>';
	}

}
*/
?>
