<?php

class EServer
{

    private $clientAuth ;
    private $nodeAuth ;
    private $Process ;
    private $Listen ;
    private $DataBase ;
    private $Crypt ;

    public function __construct() {
        
    }

    //REGISTER
    public function registerClientAuth( &$clientAuth ){
        $this->clientAuth = &$clientAuth ;
    }

    public function registerNodeAuth( &$nodeAuth ){
        $this->nodeAuth = &$nodeAuth ;
    }

    public function registerProcess( &$Process ){
        $this->Process = &$Process ;
    }

    public function registerListen( &$Listen ){
        $this->Listen = &$Listen ;
    }

    public function registerDataBase( &$DataBase ){
        $this->DataBase = &$DataBase ;
    }

    public function registerCrypt( &$Crypt ){
        $this->Crypt = &$Crypt ;
    }


    //FUNCTIONS
    public function injectToListen ( $input ) {
        if ( $input != "" ) {
            //$input = $this->Crypt->Decrypt ( $input ) ;
            $return_ = $this->Listen->Inject ( $input ) ;
            //return $return_ ;
        }
    }

    //START
    public function onListen ( $listenData ) {
        $num = 0 ;

        //print_r ($listenData) ;
        //return ;

        foreach ( $listenData->Requests as $EncReq ) {

            //Redirect AuthRequest
            if ( $EncReq->Type == "auth_client" ) {
                $listenData->Requests[ $num ]->Responce = $this->clientAuth->Auth ( $EncReq ) ;
            } elseif ( $EncReq->Type == "auth_node" ) {
                $listenData->Requests[ $num ]->Responce = $this->nodeAuth->Auth ( $EncReq ) ;
            } else {
                $DecReq = $this->Crypt->Decrypt ( $EncReq ) ;
            }

            //print_r ( $DecReq ) ;

            //Other Requests
            if ( $DecReq->Type == $this->Process->Type ) {
                $listenData->Requests[ $num ]->Responce = $this->Process->doProcess ( $DecReq ) ;
            }
            $num++ ;
        }
    }

    public function  Output () {
        echo "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n<eresponses>" ;
		
		
		if ( is_array($this->Listen->listenData->Requests) ) {
		
		
			//echo "is array" ;
		
			foreach ( $this->Listen->listenData->Requests as $EncReq ) {
				//print_r ( $EncReq ) ;
				echo "\n<eresponse type=\"".$EncReq->Type."\">\n<body>" ;
				echo $EncReq->Responce ;
				echo "\n</body>\n</eresponse>" ; 
			}
			
		}
		
        echo "\n</eresponses>" ;
    }

    public function Start () {

        //$this->Process->registerClientAuth ( $this->clientAuth ) ;
        //$this->Process->registerNodeAuth ( $this->nodeAuth ) ;
        //echo "function: ".$this->onListen ;
        $this->Listen->registerOnListen ( $this, "onListen" ) ;
        $this->Process->registerDataBase ( $this->DataBase ) ;
        $this->nodeAuth->registerDataBase ( $this->DataBase ) ;

    }

}
