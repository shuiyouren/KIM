<?php

require_once('authnode_rc4md5/rc4crypt/class.rc4crypt.php');

class AuthNodeRc4Md5
{

    public $Type ;
    private $Database ;

    private $user ;

    public function __construct () {
        $this->Type = "rc4md5" ;
    }

    public function registerDataBase ( &$Database_ ) {
        $this->Database =& $Database_ ;
    }

    public function Auth( $req ){
        //print_r ( $req  ) ;

        $error_xml = false ;

        try {
			$xml_auth = new SimpleXMLElement( $req->Body );
		} catch (Exception $e) {
			$error_xml = true ;
            $result .= '<status type="error"><errorString>XML can not be parsed<errorString><status>' ;
			//DEBUG
			//echo "ERROR XML ( ".$url."): ".$e."<br />XML: ".$req->Body."<br />" ;
		}

        if ( $error_xml ) return $result ;

        $this->user = (string)$xml_auth->user ;
        //$password = (string)$req->password ;

        //print_r ( $this->user ) ;

        $result = "" ;
        //$DBase = new $this->Database () ;

        //Step1
        if ( $xml_auth->subtype == "step1" ) {
            $this->passphrase = $this->new_passphrase () ;

            $fields[] = array ( 'passphrase_temp', $this->passphrase ) ;
            $where[] = array ( 'id', $this->user ) ;

            
            $update = $this->Database->update( 'user', $fields, $where, 1 ) ;
            $update = true ;

            unset ( $fields ) ;
            unset ( $where ) ;

            $fields[] = 'password' ;
            $fields[] = 'passphrase_temp' ;

            $where[] = array ( 'id', $this->user ) ;
            $data = $this->Database->select( 'user', $fields, $where, 1 ) ;

			if ( !is_array($data) ) {
				$result = '<status type="error"><errorString>DBase error: '.$this->Database->error.'</errorString></status>' ;
				return $result ;
			}
			
            //$row = mysql_fetch_object($data) ;
		    $this->password = $data[0]['password'] ;
            //$this->password = "prueba" ;

            //echo "Data:";
            //print_r ( $data ) ;

            if ($update) {
                //$result .= " <!-- OK -->\n" ;
            } else {
                //$sql_err = mysql_error ( $update ) ;
                //$result .= " <!-- ERROR: -->\n" ;
            }

            //$this->passphrase = "2" ;

            $this->epassphrase = rc4crypt::encrypt($this->password, $this->passphrase, 0) ;
            $hex = bin2hex( $this->epassphrase ) ;

            $html_pass = htmlentities  ( $this->passphrase ) ;

		    //$result .=  " <!-- pass: $this->password passphrase: $html_pass  -->\n" ;
            $result .= "<epassphrase>$hex</epassphrase>" ;
            $result .= "\n<status type=\"ok\" />" ;

            return $result ;
        } elseif ( $xml_auth->subtype == "step2" ) {


            $this->user = (string)$xml_auth->user ;
            //$this->user = "prueba" ;

            unset ( $fields ) ;
            unset ( $where ) ;

            $fields = array ( 'password', 'passphrase_temp' ) ;
            $where[] = array ( 'id', $this->user ) ;
            $data = $this->Database->select( 'user', $fields, $where, 1 ) ;

            //$row = mysql_fetch_object($data) ;
		    $this->password = $data[0]['password'] ;
            $this->passphrase = $data[0]['passphrase_temp'] ;

            //echo "Data:";
            //print_r ( $data ) ;

            //$result .= " <!-- passphrase: $this->passphrase  -->\n" ;

		    //$result .= " <!-- password: $this->password  -->\n" ;

            $pass_md5 = md5 ( $this->passphrase ) ;

            if ($pass_md5 == (string)$xml_auth->passphrase_md5 ) {

                $this->suid = time();                                                                                                                                                 

                //$DBase = new $this->Database () ;
                $update = $this->Database->update( 'user', array ( array ( 'suid', $this->suid ), array ( 'passphrase', $this->passphrase ) ),
                                          array ( array ( 'id', $this->user) ), 1 ) ;

                $this->esuid = rc4crypt::encrypt($this->passphrase, (string)$this->suid, 0) ;
                $hex = bin2hex( $this->esuid ) ;

		        //$result .= " <!-- suid: $this->suid  -->\n" ;
                $result .= "<esuid>$hex</esuid>" ;
                $result .= "\n<status type=\"ok\" />" ;

                //$test = rc4crypt::encrypt($this->password, $this->esuid, 0) ;
		        //echo " <!-- suid: $test  -->\n" ;
            } else {
                $result .= '<status type="error"><errorString>Authorization error</errorString></status>' ;
            }
         } else {
            $result .= '<status type="error"><errorString>Unrecognized subtype</errorString></status>' ;
        }
        return $result ;
    }

    function new_passphrase () {
        $pass = '' ;
        for ($i=0;  $i<=127; $i++) $pass.= chr ( rand(97, 122) ) ;
        return $pass ;
    }

}
