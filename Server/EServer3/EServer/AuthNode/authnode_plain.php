<?php

class AuthNodePlain
{

    public $Type ;

    public function __construct () {
        $this->Type = "plain" ;
    }

    public function Auth( $req ){
        //$user = (string)$req->user ;
        //$password = (string)$req->password ;


        $error_xml = false ;

        try {
			$xml_auth = new SimpleXMLElement( $req->Body );
		} catch (Exception $e) {
			$error_xml = true ;
			//DEBUG
			echo "ERROR XML ( ".$url."): ".$e."<br />XML: ".$req->Body."<br />" ;
		}

        //print_r ( $req ) ;

        if ( ( $xml_auth->user == "prueba") && ( $xml_auth->password == "prueba") ) {
            return time() ;
        } else {
            return "fail" ;
        }
    }

}
