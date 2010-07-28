<?php

class ERequest
{

    public $Type ;
    public $Body ;
    public $Responce ;

    function __construct( $Type_, $Body_) {
        $this->Type = $Type_ ;
        //$this->Subtype = $Name_ ;
        $this->Body = $Body_ ;
        
    }

}
