<?php

class EData
{

    public $Requests ;
    public $Errors ;

    function __construct( $Requests_, $Errors_) {
        $this->Requests = $Requests_ ;
        $this->Errors = $Errors_ ;
        
    }

}
