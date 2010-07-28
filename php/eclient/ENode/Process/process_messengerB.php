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

    public function doProcess( $requ ){
        return $requ->Body ;
    }

}
