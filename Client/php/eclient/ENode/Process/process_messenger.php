<?php

class ProcessMessenger
{

    public $Type ;
    private $Database ;

    public function __construct () {
        $this->Type = "messenger" ;
    }

    public function registerDataBase ( $Database_ ) {
        $this->Database = $Database_ ;
    }

    public function doProcess( $req ){
        //return "hola" ;
        $error_xml = false ;

        try {
			$xml_auth = new SimpleXMLElement( $req->Body );
		} catch (Exception $e) {
			$error_xml = true ;
            $result .= '<status type="error"><errorString>XML can not be parsed</errorString></status>' ;
			//DEBUG
			//echo "ERROR XML ( ".$url."): ".$e."<br />XML: ".$req->Body."<br />" ;
		}

        if ( $error_xml ) return $result ;
		
		//$this->user = (string)$xml_auth->user ;

        $result = "" ;
        $DBase = new $this->Database () ;
		
		$this->subtype = (string)$xml_auth->subtype ;
		
		switch ($this->subtype) {
			case "get_category_list" :
				return $this->get_category_list () ;
			break ;
			case "get_cloth_list" :
				return $this->get_cloth_list () ;
			break ;
            case "message" :
				return $this->message () ;
			break ;
            case "listen" :
				return $this->listen () ;
			break ;
		}
		
    }
	
    private function message () {
        $result = '<status type="ok" />' ;
        return $result ;
    }

    private function message () {
        $result = '<status type="ok" />' ;
        return $result ;
    }

}
